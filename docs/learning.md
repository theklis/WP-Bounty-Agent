# Learning model

The repository can accumulate reviewed knowledge; the underlying model is not retrained by writing files. Local research feedback belongs in `research/lessons/` until it is sanitized and accepted. Curated general lessons belong under [`knowledge/lessons/`](../knowledge/lessons/README.md); specific historical analyses can go under [`knowledge/cases/`](../knowledge/cases/README.md).

Record the source outcome first: confirmed vulnerability, rejected hypothesis, partially correct reasoning, researcher correction, or missed path. Preserve the target/version and evidence locally, including relevant [journal](../templates/journal.md) decisions. A proposed lesson then states a general pattern, its scope, counterexamples, provenance, and confidence class. Use the [lesson template](../templates/lesson.md).

Every curated lesson declares one basis: **verified fact**, **researcher-provided feedback**, **inferred pattern**, or **experimental technique**. The first two still need provenance; the latter two must not masquerade as established rules. One plugin example does not prove a universal WordPress rule. Benchmark lessons should distinguish blind audit output from later ground-truth comparison.

A rejected hypothesis shows only that its specific tested path failed under recorded conditions; it does not establish that similar patterns, components, APIs, or attack paths are safe elsewhere. Likewise, one confirmed vulnerability does not make a universal vulnerability rule. Generalize only to the scope supported by the evidence, and record that scope explicitly.

Review before promotion: remove sensitive target data, verify cited public sources or approved summaries, check that the claimed generality matches the evidence, and link to the originating research record if appropriate. Commit meaningful revisions so Git history exposes methodology changes. No automatic lesson promotion exists in Milestone 1.
