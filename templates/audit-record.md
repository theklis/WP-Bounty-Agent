# Audit record: <target, version/commit, date>

Use only sections relevant to the scope. Fill this in ignored `research/`; do not copy target source or secrets into curated documentation. Put distinct vulnerability claims in [finding records](finding.md), not in this map.

## Preflight and security model

- Mode and research question: `<...>`
- Audit state, last reviewed, and next action: `<...>`
- Supplied input and source identity: `<original path/type, archive digest or repository ref/dirty state, extracted root, exact version/commit>`
- Source provenance, completeness, and conflicting metadata: `<...>`
- Target Hunter handoff/lead IDs and verified version match, if any: `<...>`
- Plugin/theme, dependencies and tested environment: `<...>`
- Authorization, scope, exclusions, workspace, knowledge consulted: `<...>`
- Unresolved setup assumptions: `<...>`
- Purpose and major security-relevant features: `<...>`
- Actors; objects; owns/manages/assigned-to/tenant relationships: `<...>`
- Legitimate state transitions and sensitive effects: `<...>`
- Deep-dive themes selected or deferred, with reasons: `<...>`

## Reachable surfaces and boundaries

| Entry / registration evidence | Actor and prerequisites | Input / object | Checks and downstream path | State / effect | Link or gap |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

| Boundary and allowed transition | Required authority or proof | Enforcement point / evidence | Attacker influence or uncertainty |
| --- | --- | --- | --- |
|  |  |  |  |

## Security-relevant state

| Value / object / token | Origin and who controls or learns it | Storage and transformations | Consumer and authority granted | Expiry / revocation / gap |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

## Security invariants

Record target-specific rules as expected secure behavior, not proof of enforcement. Unknown enforcement is an investigation question, not a finding by itself.

| ID | Rule / expected property | Actors, objects, or boundary | Apparent enforcement | Enforcement evidence/status or open question | Related path/finding |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

## Paths and coverage

Link cross-file or cross-request paths and finding IDs here. For each necessary transition, cite source and mark it supported, inferred, unknown, or contradicted per the [evidence model](../docs/evidence.md). Record relevant authentication, authorization, exact-object ownership/isolation, and request integrity separately. Do not substitute one check for another.

| From → relation → to | Actor / prerequisite | Evidence and premise status | Gap or counterevidence |
| --- | --- | --- | --- |
|  |  |  |  |

| Scoped actor / feature / surface / boundary / state / operation / chain | Mapped / reviewed / deep-reviewed / deferred / not applicable / unresolved | Source and reasoning completed | Gap, reason, or next action |
| --- | --- | --- | --- |
|  |  |  |  |

## Candidate and validation queue

Link distinct [finding records](finding.md); group routes with the same root issue. This table is a resume and testing queue, not a second evidence ledger.

| Finding ID / status | Confidence, priority, and reason | Weakest unresolved premise | Next human verification / plan |
| --- | --- | --- | --- |
|  |  |  |  |

## Second pass and final research summary

- New attacker and analytical perspectives; first-pass assumption challenged: `<...>`
- Paths revisited, new checks or surfaces, candidate and coverage changes: `<...>`
- Queue disposition and human validation needs: `<...>`
- Rejected paths and their specific counterevidence: `<...>`
- Important blind spots, deferred areas, and exclusions: `<...>`
- Conclusion limited to reviewed paths and conditions: `<...>`
