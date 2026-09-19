# Vulnerability chaining across authority changes

## Revisit primitives without inventing links

Load this when an audit has observations or modest primitives that may compose across requests, handlers, actors, objects, stored state, or integrations. Ask of each primitive: **what new authority, information, or state control does it actually grant?** Then identify the next reachable surface that accepts that exact capability. Candidate primitives include identifier control, limited disclosure, token leakage, partial write, option/meta update, stored content, file placement, restricted SSRF, role change, or a public endpoint. Their presence is not a chain by itself.

## Build a minimal attack graph

Record nodes for actor, entry, object, token/state, trust decision, and effect. Label edges *can invoke*, *controls*, *writes*, *reads*, *leaks*, *authorizes*, *triggers*, or *transforms*, with target-version source evidence. Trace **first primitive → changed capability/state → second entry or worker → new trust decision → final effect**. Recheck identity, action authorization, exact-object relationship, and request integrity at each relevant transition. A value written under low privilege may be consumed by a privileged worker; a token issued in one handler may leak in another and be accepted by a third; an authorization decision for object A may be reused after substituting B. Each edge must be independently reachable in the necessary order and environment.

Separate findings for independent claims, then link them in the local [finding record](../templates/finding.md) if composition produces a stronger impact. Record prerequisites, timing, expiry, and what the attacker retains between requests. Prefer the shortest path that explains the effect; extra speculative edges weaken clarity. The [core attack-graph phase](../docs/audit-methodology/trace-security-paths.md) governs graph evidence, and [deferred-work knowledge](../knowledge/wordpress/background-and-rendering.md) helps with worker transitions.

## Break the chain before promoting it

Try to falsify each bridge: is the leaked token bound to someone else; is the stored value sanitized on retrieval; does the worker reauthorize; is the second endpoint unreachable; has the object changed state; does a nonce or session context differ? Mark each material premise **supported**, **inferred**, **unknown**, or **contradicted** under the [evidence model](../docs/evidence.md). Do not combine two hypothetical primitives into an imaginary exploit. A strong candidate needs a complete plausible path with no known blocking check; human validation still determines **CONFIRMED**.

For local validation, establish the baseline for each step with separate actors and objects, then run the ordered sequence and capture the authority gained at every transition. Test negative controls for wrong token/object, reversed order, or missing first primitive. If a later step fails, record the specific failed premise rather than generalizing that the entire vulnerability family is safe.
