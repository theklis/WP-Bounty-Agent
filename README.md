# wp-bounty-agent

**v1.1.0.** The project version is in [VERSION](VERSION).

This repository guides an AI-assisted WordPress vulnerability researcher through public target selection, deep review of locally supplied plugin/theme source, attack-path reasoning, manual validation planning, learning from human outcomes, and blind evaluation of audit quality. It is oriented toward Wordfence bug bounty research, while keeping technical validity separate from current program scope and CVE decisions. The human researcher confirms security claims.

It is not a mass scanner, autonomous exploitation framework, submission bot, or substitute for manual testing. A suspicious API, missing local check, or helper match is not proof of a vulnerability. Research only public source and authorized local environments; do not scan third-party installations.

## Start here

Open this repository in a fresh Codex session. [AGENTS.md](AGENTS.md) routes the task and sets the evidence and safety rules. State the intended workflow in ordinary language and provide any available scope, source path, target version, and research question. Codex follows the relevant documents through the [documentation map](docs/README.md); the mode names below are guided requests, not commands parsed by the helper CLI.

For a source audit, supply a legitimate local ZIP or source-tree path. The [Source Audit workflow](docs/source-audit/README.md) identifies the exact source and creates ignored local records before analysis. Target source stays read-only. A full audit can be paused and resumed; a QUICK TRIAGE must disclose its narrower coverage. A strong candidate enters a human-validation queue, and only explicit human reproduction makes it **CONFIRMED**.

```text
understand software → model actors, objects, and trust → map reachable surfaces
→ derive security invariants → trace data and authority across requests and state
→ form falsifiable paths → challenge them → queue manual tests
→ learn from human outcomes → evaluate the method with blind benchmarks
```

An audit may honestly finish with no vulnerability identified in its reviewed scope. A hunt may find no strong target, a result may support no reusable lesson, and a benchmark may be contaminated or invalid.

## Supported workflows

| Request | What it produces | Where to start |
| --- | --- | --- |
| **TARGET HUNT** | Sourced, qualitative shortlist and exact-version audit handoff; never a vulnerability verdict | [Target Hunter](docs/target-hunter/README.md) |
| **AUDIT** | Software/security model, meaningful surface coverage, traced candidates, counterevidence, and manual test queue | [Source Audit](docs/source-audit/README.md) |
| **QUICK TRIAGE** | Explicitly partial source review and next audit questions | [Source Audit modes](docs/source-audit/resume-and-output.md) |
| **DEEP DIVE** | Focused analysis of one feature, boundary, or path | [Source Audit modes](docs/source-audit/resume-and-output.md) |
| **CHAIN REVIEW** | Evidence for each transition between existing primitives | [Source Audit modes](docs/source-audit/resume-and-output.md) |
| **SECOND PASS** | Changed attacker perspective and analytical direction, with coverage deltas | [Source Audit modes](docs/source-audit/resume-and-output.md) |
| **RESUME** | Continuation after source identity and prior record checks | [Source Audit modes](docs/source-audit/resume-and-output.md) |
| **VALIDATE** | Plain-English, checkpointed manual walkthrough for an existing candidate; the researcher supplies observed results | [Manual validation](docs/source-audit/manual-validation.md) |
| **LEARN FROM RESULT** | Bounded local proposal from a human result or correction; curation needs separate explicit approval | [Learning workflow](docs/learning-workflow.md) |
| **BENCHMARK** | Normal blind Source Audit, frozen output, then separate ground-truth comparison | [Benchmark workflow](docs/benchmarking.md) |

The [core audit methodology](docs/audit-methodology/README.md) drives source reasoning. Load [WordPress knowledge](knowledge/wordpress/README.md) and [specialist playbooks](playbooks/README.md) selectively for the target's architecture. [Current Wordfence and CVE intelligence](docs/current-intelligence.md) is dated and must be rechecked before consequential decisions.

## Example requests

These are natural-language examples, not CLI syntax:

```text
TARGET HUNT: Find strong current public/free WordPress plugin targets for Wordfence research. Explain why the first deserves audit time.

AUDIT research/audits/example/source/plugin. Focus on low-privilege and unauthenticated attack paths; record deferred coverage.

QUICK TRIAGE this local plugin ZIP for its architecture and most consequential entry families; tell me what a full audit would still need.

DEEP DIVE candidate F03. Trace every consumer of its token and look for object re-binding.

CHAIN REVIEW the existing primitives. Test each required authority and state bridge.

SECOND PASS this audit from privileged consumer back to attacker-controlled writer.

RESUME research/audits/example/ after verifying that its source has not changed.

VALIDATE F03. Explain the plugin feature, then walk me through the first local test checkpoint.

LEARN FROM RESULT F03 was rejected: the final object is re-bound to the authenticated customer. Propose any bounded lesson for review.

BENCHMARK this prepared local target in a separate blind context; freeze the ordinary audit before revealing ground truth.
```

## Records, tools, and limits

Use [record templates](templates/README.md) in the ignored [research workspace](research/README.md) for audit maps, findings, validation plans, learning proposals, and benchmark runs. Keep private data, target source, generated indexes, and proof artifacts local. [Repository policy](docs/repository-policy.md) governs deliberate curation into tracked knowledge.

The optional [Python helper](tools/README.md) performs conservative ZIP intake and lightweight identity, inventory, and static entry-point navigation. It neither executes target code nor makes security judgments. It may miss dynamic or wrapped registrations; it is not a PHP parser. Runtime behavior may require authorized local testing, source review cannot guarantee discovery, historical advisories may be incomplete, and prior model knowledge can contaminate a purportedly blind benchmark. Program and CVE rules can change.

See the [release QA checklist](docs/release-checklist.md) and [roadmap](docs/roadmap.md) for release status.
