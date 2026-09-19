# v1 release QA checklist

Use this short gate before approving a project release. Record failures and corrective work; completion requires human review. The [roadmap](roadmap.md) holds the release status.

## Repository and navigation

- [ ] `python -m unittest discover -s tests -v` passes; retain documented platform skips.
- [ ] Relative Markdown links resolve from the repository root, and README → AGENTS/docs index → mode → method → templates/workspace is usable.
- [ ] `git diff --check` is clean; staged/tracked files contain no secrets, private data, target source, benchmark truth, filled findings, or generated output.
- [ ] `research/` workspaces and local artifacts remain ignored. Review the working tree before the eventual release commit.

## Research and intelligence

- [ ] Source/version identity, scope, coverage, deferred work, and missing evidence are explicit. Suspicious code and helper leads are not vulnerability verdicts.
- [ ] **CONFIRMED** has explicit human reproduction; rejection defeats a necessary premise under recorded conditions. Target source is read-only.
- [ ] Consequential Wordfence/CVE decisions recheck dated official intelligence; program scope and CVE assignment remain separate from technical validity.

## Learning, benchmark, and helper boundaries

- [ ] A **PROPOSED** lesson has a human-grounded basis; **CURATED** requires explicit human approval and sanitized provenance. Method/playbook edits have separate approval.
- [ ] Benchmark truth is withheld until the ordinary Source Audit output is frozen and verified. Contaminated, known-answer, and invalid runs are distinguished from clean discovery.
- [ ] ZIP intake and output containment remain conservative; helper indexes are navigation-only and do not execute target code.

After approval, update the milestone state, review the exact release diff, then create the approved commit/tag. This checklist does not authorize those actions.
