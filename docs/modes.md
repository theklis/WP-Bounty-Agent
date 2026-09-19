# Operating modes

These are specifications for later milestones, not implemented commands. Each mode must respect [research principles](research-principles.md), [the evidence model](evidence.md), and human validation.

Before a substantial mode task, establish its working state internally: mode; target/plugin and version or commit where applicable; authorized scope; local research workspace; relevant documentation/playbooks loaded; and important unresolved assumptions. Keep this in session context or a local journal as useful. It does not require a verbose user-facing preflight or automation.

| Mode | Input and intended output |
| --- | --- |
| **TARGET HUNT** | Public plugin/theme and current program information → sourced shortlist with a functionality-based attack-surface thesis, eligibility caveats, and duplicate-risk uncertainty. Recheck time-sensitive rules. |
| **AUDIT** | Locally supplied permitted source tree or ZIP → architecture and actor/object model, attack surfaces, traced candidate paths, coverage gaps, and manual validation guidance. |
| **DEEP DIVE** | One component, surface, family, or path → detailed trace, assumptions, counterexamples, and focused tests. |
| **CHAIN REVIEW** | Existing findings and functionality map → potential multi-stage paths across requests, handlers, and stored state, with each transition evidenced. |
| **SECOND PASS** | Prior audit plus changed attacker assumptions → explicit search for missed surfaces and documented coverage deltas. |
| **BENCHMARK** | Historical target and withheld answer → blind audit record, then comparison with ground truth and a documented miss or false-positive analysis. |
| **LEARN FROM RESULT** | Researcher-confirmed outcome or correction → provenance-bearing proposed lesson, reviewed before curation. |

Modes may share records and specialist playbooks. They must not silently change a finding to **CONFIRMED**, treat benchmark ground truth as audit input, or treat program eligibility as permanently known.
