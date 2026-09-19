# Research principles

## Scope

Work with publicly available source, local test environments, or systems for which the researcher has authorization, within applicable disclosure and bounty rules. TARGET HUNT is about choosing public software for manual research, not finding live-site victims. Do not design indiscriminate scanning or mass exploitation into this project.

## Reasoning order

Explain the software's intended behavior before looking for faults: features, actors, objects, ownership, state transitions, and trust assumptions. Then ask what an attacker with a specific capability can reach and control. Follow the data across handlers, files, requests, and persisted state to a security-relevant action and observable effect.

For each candidate, record both the supporting path and what would defeat it: an earlier capability check, object ownership check, non-reachable handler, data normalization, framework behavior, or deployment assumption. Authentication, authorization, object ownership/isolation, and request integrity are separate questions. A sink alone is an observation, not an exploitable path.

Prefer precise source references, reproducible conditions, and manual tests over confidence theater. Report uncertainty directly. Explain why a plugin-specific rule or workflow creates the boundary; do not force every issue into a predefined vulnerability class. Use [the evidence model](evidence.md) to expose gaps and [the lifecycle](findings.md) to avoid premature claims.
