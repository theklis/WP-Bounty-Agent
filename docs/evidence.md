# Evidence and confidence

For each finding, describe these dimensions in plain language. The [finding template](../templates/finding.md) gives them a consistent home.

| Dimension | Question to answer |
| --- | --- |
| Source evidence | Which exact file/function/line or local behavior supports the claim, in which version or commit? What does it actually show? |
| Reachability | Can the stated actor invoke every necessary entry point, including prerequisite states and requests? |
| Attacker control | Which bytes, fields, objects, or state transitions can that actor choose or influence? |
| Transformations and validation | How does controlled input change, and which checks constrain it before use? |
| Authentication | Who is the caller, and how is that identity established? |
| Authorization | Is that caller permitted to perform this action? Which capability or permission check establishes it? |
| Object ownership / isolation | May this caller act on this specific object, user, tenant, site, order, booking, or other resource? |
| Request integrity / anti-CSRF | Is a nonce or equivalent mechanism used, and what does it actually establish about the request? |
| Exploit assumptions | What configuration, role, timing, integration, or framework behavior is required but unverified? |
| Impact | What security effect follows, for which actor/object, and what evidence shows it is observable? |
| Missing or contrary evidence | What could disprove the path, and what has not yet been tested? |

Mark each material premise **supported**, **inferred**, **unknown**, or **contradicted** and point to its evidence. “Supported” means the cited source or human test establishes that premise under stated conditions; it does not mean the overall vulnerability is confirmed. A contradictory premise should lower the claim's status or lead to rejection.

Assess the four access and request checks separately where relevant. A valid WordPress nonce supports an anti-CSRF check; it does not itself establish authorization or object ownership.

Use qualitative overall confidence: **low** (key premises unknown), **moderate** (coherent path with material untested assumptions), or **high** (source-backed complete path with narrow remaining validation). Explain the rating in one sentence. Confidence is about the current hypothesis, not a probability, severity score, or lifecycle state. Even high confidence never upgrades a record to **CONFIRMED**. If a necessary link is missing, write “this remains unproven.”
