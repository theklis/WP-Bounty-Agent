"""Synthetic, local-only safety and navigation tests."""

from __future__ import annotations

import stat
import sys
import tempfile
import unittest
import contextlib
import io
import warnings
import zipfile
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from source_nav import entrypoints, identify, inventory
from zip_intake import Limits, ZipSafetyError, extract_zip, inspect_zip
from wp_audit_helper import main
import source_nav


class ZipTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.archive = self.root / "target.zip"
        self.workspace = self.root / "audit"
        self.workspace.mkdir()

    def make_zip(self, names):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            with zipfile.ZipFile(self.archive, "w") as archive:
                for name, content in names:
                    archive.writestr(name, content)

    def test_ordinary_plugin_and_wrapper(self):
        self.make_zip([("wrapper/plugin/main.php", "<?php\n/* Plugin Name: Example\nVersion: 1.0 */\n")])
        report = inspect_zip(self.archive)
        self.assertEqual(report["status"], "safe")
        result = extract_zip(self.archive, self.workspace)
        self.assertEqual(result["product_roots"]["status"], "single")
        self.assertEqual(result["product_roots"]["candidates"][0]["root"], "wrapper/plugin")
        self.assertTrue((self.workspace / "source/wrapper/plugin/main.php").is_file())
        self.assertEqual(report["sha256"], inspect_zip(self.archive)["sha256"])

    def test_multiple_roots_ambiguous(self):
        self.make_zip([("a/main.php", "<?php\n/*\nPlugin Name: A\n*/"), ("b/main.php", "<?php\n/*\nPlugin Name: B\n*/")])
        result = extract_zip(self.archive, self.workspace)
        self.assertEqual(result["product_roots"]["status"], "ambiguous")

    def test_rejected_names_and_no_escape(self):
        for name in ("../escape.php", "..\\escape.php", "/absolute.php", "C:\\temp\\x.php",
                     "\\\\server\\share\\x.php", "CON.txt", "data:stream", "trailing. ", "a//b.php", "a/./b.php"):
            with self.subTest(name=name):
                self.make_zip([(name, "x")])
                self.assertEqual(inspect_zip(self.archive)["status"], "rejected")
                with self.assertRaises(ZipSafetyError): extract_zip(self.archive, self.workspace)
                self.assertFalse((self.workspace / "source").exists())
                self.assertFalse((self.root / "escape.php").exists())

    def test_collisions(self):
        for names in (("a/b.php", "a\\b.php"), ("Plugin/Main.php", "plugin/main.php"),
                      ("a", "a/b.php")):
            with self.subTest(names=names):
                self.make_zip([(names[0], "a"), (names[1], "b")])
                self.assertEqual(inspect_zip(self.archive)["status"], "rejected")

    def test_symlink_special_and_budget(self):
        link = zipfile.ZipInfo("link")
        link.create_system = 3
        link.external_attr = (stat.S_IFLNK | 0o777) << 16
        with zipfile.ZipFile(self.archive, "w") as archive: archive.writestr(link, "../outside")
        self.assertEqual(inspect_zip(self.archive)["status"], "rejected")
        self.make_zip([("big.php", "x" * 1024)])
        self.assertEqual(inspect_zip(self.archive, Limits(10, 100, 100))["status"], "rejected")
        with self.assertRaises(ZipSafetyError): extract_zip(self.archive, self.workspace, Limits(10, 100, 100))
        self.assertEqual(inspect_zip(self.archive, Limits(0x1, 2048, 2048))["status"], "safe")
        self.make_zip([("a", "x"), ("b", "x")])
        self.assertEqual(inspect_zip(self.archive, Limits(1, 2048, 2048))["status"], "rejected")

    def test_no_overwrite(self):
        self.make_zip([("main.php", "original")])
        dest = self.workspace / "source"
        dest.mkdir()
        (dest / "main.php").write_text("existing")
        with self.assertRaises(ZipSafetyError): extract_zip(self.archive, self.workspace)
        self.assertEqual((dest / "main.php").read_text(), "existing")

    def test_nul_name_rejected(self):
        self.make_zip([("name.php", "x")])
        data = self.archive.read_bytes().replace(b"name.php", b"na\x00e.php")
        self.archive.write_bytes(data)
        self.assertEqual(inspect_zip(self.archive)["status"], "rejected")

    def test_cli_json_deterministic(self):
        self.make_zip([("main.php", "x")])
        def call():
            buffer = io.StringIO()
            with contextlib.redirect_stdout(buffer):
                code = main(["--format", "json", "inspect-zip", str(self.archive)])
            self.assertEqual(code, 0)
            return buffer.getvalue()
        self.assertEqual(call(), call())

    def test_corrupt_data_cleans_staging(self):
        self.make_zip([("main.php", "UNIQUE_PAYLOAD_FOR_CRC")])
        self.archive.write_bytes(self.archive.read_bytes().replace(b"UNIQUE_PAYLOAD_FOR_CRC", b"BROKEN_PAYLOAD_FOR_CRC"))
        self.assertEqual(inspect_zip(self.archive)["status"], "safe")
        with self.assertRaises(ZipSafetyError): extract_zip(self.archive, self.workspace)
        self.assertFalse((self.workspace / "source").exists())
        self.assertFalse(any(self.workspace.iterdir()))

    def test_cli_rejects_nonresearch_workspace(self):
        self.make_zip([("main.php", "x")])
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(main(["extract-zip", str(self.archive), str(self.workspace)]), 2)
        self.assertFalse((self.workspace / "source").exists())


class SourceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "plugin"
        self.root.mkdir()

    def test_identity_conflict_and_theme(self):
        (self.root / "main.php").write_text("<?php\n/*\nPlugin Name: Example\nVersion: 1.0\nRequires PHP: 8.0\n*/\n", encoding="utf-8")
        (self.root / "readme.txt").write_text("Stable tag: 2.0\n", encoding="utf-8")
        result = identify(self.root)
        self.assertTrue(result["version_conflict"])
        self.assertEqual(result["status"], "ambiguous")
        self.assertEqual(result["candidates"][0]["fields"]["Plugin Name"]["value"], "Example")
        (self.root / "main.php").unlink()
        (self.root / "style.css").write_text("/*\nTheme Name: Example Theme\nVersion: 3.0\n*/\n", encoding="utf-8")
        self.assertEqual(identify(self.root)["candidates"][0]["kind"], "theme")

    def test_entry_categories_and_dynamic_limit(self):
        source = """<?php
add_action('wp_ajax_save', 'save_item');
add_action('wp_ajax_nopriv_search', 'search_item');
register_rest_route('sample/v1', '/thing', ['methods' => 'GET', 'callback' => 'get_thing', 'permission_callback' => 'can_get']);
register_rest_route('sample/v1', '/other', ['methods' => 'POST', 'callback' => [$this, 'other'], 'permission_callback' => [$this, 'can_other']]);
add_action('admin_post_export', 'export_item');
add_action('admin_post_nopriv_submit', 'submit_item');
add_shortcode('sample', 'render_sample');
wp_schedule_event(time(), 'hourly', 'sample_cron');
add_action('sample_cron', 'run_cron');
add_action('woocommerce_order_status_changed', 'sync_order');
add_action('wp_ajax_' . $suffix, 'dynamic');
eval($code); $wpdb->query($sql); unserialize($data);
// add_action('wp_ajax_nopriv_fake', 'fake');
$example = "add_action('wp_ajax_nopriv_fake2', 'fake2')";
"""
        (self.root / "main.php").write_text(source, encoding="utf-8")
        records = entrypoints(self.root)["entries"]
        expected = {"AJAX_AUTH", "AJAX_UNAUTH", "REST_ROUTE", "ADMIN_POST_AUTH", "ADMIN_POST_UNAUTH",
                    "SHORTCODE", "CRON_SCHEDULE", "WOOCOMMERCE_HOOK", "DYNAMIC_REGISTRATION"}
        self.assertTrue(expected.issubset({record["category"] for record in records}))
        ajax = next(item for item in records if item["category"] == "AJAX_AUTH")
        self.assertEqual((ajax["file"], ajax["line"], ajax["callback"]), ("main.php", 2, "save_item"))
        rest = next(item for item in records if item["category"] == "REST_ROUTE")
        self.assertEqual((rest["namespace"], rest["route"], rest["permission_callback"]), ("sample/v1", "/thing", "can_get"))
        dynamic = next(item for item in records if item["category"] == "DYNAMIC_REGISTRATION")
        self.assertIsNone(dynamic["hook_or_route"])
        self.assertEqual(dynamic["line"], 12)
        other = next(item for item in records if item.get("route") == "/other")
        self.assertEqual(other["permission_callback"], "$this::can_other")
        self.assertNotIn("vulnerability", str(records).lower())
        self.assertFalse(any(term in str(records) for term in ("eval", "$wpdb", "unserialize")))
        self.assertFalse(any("fake" in str(item) for item in records))

    def test_action_scheduler_hook_positions(self):
        source = """<?php
as_enqueue_async_action('async_hook', []);
as_schedule_single_action(time(), 'single_hook', []);
as_schedule_recurring_action(time(), 3600, 'recurring_hook', []);
as_schedule_cron_action(time(), '0 * * * *', 'cron_hook', []);
"""
        (self.root / "main.php").write_text(source, encoding="utf-8")
        records = entrypoints(self.root)["entries"]
        self.assertEqual(len(records), 4)
        self.assertEqual(
            {item["registration"]: item["hook_or_route"] for item in records},
            {
                "as_enqueue_async_action": "async_hook",
                "as_schedule_single_action": "single_hook",
                "as_schedule_recurring_action": "recurring_hook",
                "as_schedule_cron_action": "cron_hook",
            },
        )
        self.assertTrue(all(item["category"] == "ACTION_SCHEDULER" for item in records))

    def test_git_inspection_disables_optional_writes(self):
        outputs = [str(self.root.resolve()) + "\n", "a" * 40 + "\n", "main\n", " M main.php\n"]
        with patch("source_nav.subprocess.run", side_effect=[SimpleNamespace(stdout=value) for value in outputs]) as run:
            result = source_nav._git(self.root.resolve())
        self.assertEqual(result, {"commit": "a" * 40, "branch": "main", "dirty": True})
        self.assertEqual(
            [call.args[0][6:] for call in run.call_args_list],
            [
                ["rev-parse", "--show-toplevel"],
                ["rev-parse", "HEAD"],
                ["branch", "--show-current"],
                ["status", "--porcelain", "--untracked-files=normal"],
            ],
        )
        for call in run.call_args_list:
            self.assertEqual(
                call.args[0][:6],
                ["git", "--no-optional-locks", "-c", "core.fsmonitor=false", "-C", str(self.root.resolve())],
            )
            self.assertTrue(call.kwargs["check"])

    def test_digest_change_and_symlink_skip(self):
        path = self.root / "main.php"
        path.write_text("<?php add_action('x', 'y');", encoding="utf-8")
        before = inventory(self.root)
        self.assertEqual(before["source_digest"], entrypoints(self.root)["source_digest"])
        path.write_text("<?php add_action('y', 'z');", encoding="utf-8")
        self.assertNotEqual(before["source_digest"], inventory(self.root)["source_digest"])

    def test_symlink_outside_root_skipped(self):
        outside = Path(self.temp.name) / "outside.php"
        outside.write_text("<?php add_action('wp_ajax_nopriv_outside', 'x');", encoding="utf-8")
        try: (self.root / "outside.php").symlink_to(outside)
        except (OSError, NotImplementedError): self.skipTest("symlinks unavailable on this host")
        result = entrypoints(self.root)
        self.assertFalse(any(item["file"] == "outside.php" for item in result["entries"]))
        self.assertTrue(any("outside.php" in issue for issue in result["skipped"]))
        self.assertFalse(result["digest_complete"])

    def test_link_guard_path_is_not_read(self):
        (self.root / "outside.php").write_text("<?php add_action('wp_ajax_nopriv_outside', 'x');", encoding="utf-8")
        original = source_nav._linkish
        with patch("source_nav._linkish", side_effect=lambda path: path.name == "outside.php" or original(path)):
            result = entrypoints(self.root)
        self.assertFalse(result["entries"])
        self.assertTrue(any("outside.php: symlink/reparse" in issue for issue in result["skipped"]))

    def test_digest_budget_marks_incomplete(self):
        (self.root / "large.php").write_text("<?php add_action('x', 'y');", encoding="utf-8")
        with patch("source_nav.MAX_HASH_FILE", 1):
            result = inventory(self.root)
        self.assertFalse(result["digest_complete"])
        self.assertTrue(any("digest budget exceeded" in issue for issue in result["skipped"]))

    def test_inventory_stays_concise_for_many_directories(self):
        for number in range(50):
            directory = self.root / f"part-{number:02d}"
            directory.mkdir()
            (directory / "module.php").write_text("<?php\n", encoding="utf-8")
        result = inventory(self.root)
        self.assertEqual(result["total_files"], 50)
        self.assertEqual(len(result["top_level"]), 20)
        self.assertEqual(result["other_top_level_count"], 30)


if __name__ == "__main__": unittest.main()
