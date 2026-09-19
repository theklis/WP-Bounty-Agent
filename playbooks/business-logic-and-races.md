# Business logic, state machines, and races

## Derive the target's rules

Load this for workflows with meaningful order, status, ownership, price, quota, approval, invitation, booking, subscription, refund, or one-time actions. Model actors, objects, relationships, and legal transitions before proposing a weakness. Write target-specific invariants in the [audit record](../templates/audit-record.md): which fields must come from the server, which event must precede another, what becomes immutable after a transition, which action is one-time, and which actor/object binding must survive each step. An unfamiliar workflow is not insecure merely because it differs from a generic pattern.

## Follow the whole workflow

Trace each handler that creates, updates, consumes, or reverses the relevant state. Compare client-supplied status/price/quantity/owner with server-derived values; inspect cancellation and rescheduling after payment, repeated activation, approval or invitation acceptance, refunds, coupons, inventory reservations, and background completion where the target supports them. Ask whether a valid step can occur out of order, be repeated, target someone else's object, or feed a privileged later step. Record the actual state before and after each request, plus who can cause the transition. [Authorization](authorization-and-isolation.md), [tokens](tokens-and-state.md), and [commerce](commerce.md) deepen specific boundaries without replacing the target's rule.

## Concurrency is a separate premise

Consider a race only when an invariant depends on atomicity: check-then-mutate, one-time token consumption, quota/inventory decrement, ownership or role changes, or duplicate payment/refund processing. Identify two operations that can overlap, the shared state each reads/writes, the expected interleaving, and the effect of violating it. Ordinary sequential statements are not evidence of a race. Look for locks, transactions, unique constraints, conditional updates, idempotency keys, and queue serialization as counterevidence; verify that they cover the same state and workers in the target environment. [Storage](../knowledge/wordpress/data-and-storage.md) and [deferred-work](../knowledge/wordpress/background-and-rendering.md) references help resolve implementation behavior.

## Falsification and validation

Seek server-side recomputation, transition guards, object binding, idempotent handlers, immutable fields, and business rules that intentionally permit the alleged alternate path. A strong candidate requires a violated target-specific invariant, reachable attacker steps, all necessary states, and a consequential outcome; a race claim additionally needs a plausible overlap and non-atomic effect.

For local verification, construct the smallest valid baseline workflow, then vary one transition, binding, or repeat action. For concurrency, use only a controlled local environment and record the two request schedules and final state; a failed single attempt does not prove atomic safety. Preserve negative controls and cleanup. Use [chaining](chaining.md) when a minor state deviation enables a different sensitive handler.
