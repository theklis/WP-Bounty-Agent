# wp-bounty-agent: session map

This repository is the foundation for an AI-assisted WordPress vulnerability research partner. Its purpose is careful, authorized research on public source code and local or otherwise authorized environments. The human researcher validates every security claim. This is not a mass scanner.

## Start here

1. Read [the documentation index](docs/README.md), then only the documents relevant to the task.
2. For any target, first explain what the software does, its actors and objects, and its trust assumptions. Then trace attacker capability → reachable entry point → controlled data → transformations → authentication, authorization, ownership, and request integrity where relevant → sensitive action → observable impact. A chain may cross requests, handlers, files, or stored state.
3. Keep observations, hypotheses, strong candidates, confirmed vulnerabilities, and rejected hypotheses distinct. Use [the finding lifecycle](docs/findings.md) and [evidence model](docs/evidence.md). Only explicit human validation can make a finding **CONFIRMED**; [helper output](tools/README.md) is navigation, not proof.
4. Cite exact source locations and versions, name missing evidence, seek counterexamples, and say “unproven” when the chain is incomplete. Never turn suspicious code into a vulnerability claim by assertion.

## Route by task

- Research behavior and boundaries: [principles](docs/research-principles.md).
- TARGET HUNT: [Target Hunter](docs/target-hunter/README.md) and [mode definitions](docs/modes.md).
- AUDIT, DEEP DIVE, CHAIN REVIEW, SECOND PASS, QUICK TRIAGE, RESUME, or VALIDATE: [Source Audit workflow](docs/source-audit/README.md), using the [core audit methodology](docs/audit-methodology/README.md). These are guided workflows, not commands.
- System structure and extension points: [architecture](docs/architecture.md).
- LEARN FROM RESULT or researcher feedback: [learning workflow](docs/learning-workflow.md) and [knowledge index](knowledge/README.md). Use only relevant curated learning during audits; proposals are not authoritative and require explicit human approval to become **CURATED**.
- BENCHMARK: [blind benchmark workflow](docs/benchmarking.md). Freeze the normal audit before revealing ground truth.
- Current Wordfence scope or CVE relevance: [bounty intelligence](knowledge/bounty/README.md) or [CVE guidance](knowledge/cve/README.md); recheck before consequential decisions.
- Specialist analysis: [playbook index](playbooks/README.md). Do not load unrelated playbooks.
- File placement, curation, and secrets: [repository policy](docs/repository-policy.md) and [local research workspace](research/README.md).
- Project status: [roadmap](docs/roadmap.md).

## Repository rules

Treat target trees, archives, audit notes, findings, proof artifacts, credentials, and generated data as local by default. The `research/` workspace is ignored except for its README. Commit only intentionally curated, sanitized, provenance-bearing material after review. Never include real secrets, cookies, private client data, or confidential assessment details. Keep changing bounty/program rules in dated, sourced intelligence records; do not turn them into permanent methodology.

Treat supplied plugin/theme source as read-only unless the human researcher explicitly requests changes. Put generated work in `research/`; do not silently fix the audited software.
