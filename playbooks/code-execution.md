# Command and code execution

## Identify the execution boundary

Load this when a plugin builds OS commands, dynamic PHP, include/require paths, callable names, templates/expressions, install/update actions, or writes a file that may later execute. Derive the rule for who may choose executable behavior and under what configuration. A sensitive execution API is not itself a vulnerability: the stated attacker must reach it and influence a part interpreted as code, command grammar, callable, or executable file content. Separate server-side code execution from browser script execution, which belongs in [rendering/XSS](rendering-and-xss.md).

## Reconstruct the full path

Trace **entry and actor → controlled value or stored state → allowlists/escaping/normalization → exact command/callable/include/template → execution context → observable effect**. For commands, distinguish data arguments from shell interpretation, including whether a shell is invoked. For callables and dynamic templates, determine which names the attacker may select and which functions/classes are actually loadable. For include paths, resolve the final path and file ownership. For file-write chains, prove that the destination is interpreted as executable in the target server configuration and that a reachable request or worker triggers it. Plugin/theme installation and update functions have their own privilege and deployment prerequisites; do not infer guest reachability from their presence.

Cross-request paths matter: an import or low-privilege option write may set a template name, callback, or command argument later used by a privileged job. Trace that bridge and reauthorization. [Filesystem/archives](filesystem-and-archives.md), [serialization](sql-and-serialization.md), [privilege/configuration](privilege-and-configuration.md), and [deferred-work knowledge](../knowledge/wordpress/background-and-rendering.md) are companions when the path reaches them.

## Disproof and validation

Seek fixed command templates with constrained arguments, trusted-only writers, callable allowlists, canonical include paths, non-executable upload locations, and disabled or unreachable features. A callback chosen from a fixed safe map is different from arbitrary function control. A file upload or PHP object creation does not establish RCE without an execution step. Before calling a path strong, cite evidence for attacker control *after* checks, executable interpretation, and a consequential effect under the recorded environment.

In an authorized local test, use a benign marker or controlled test function/file to distinguish data handling from execution; document configuration and cleanup. Do not claim code execution from a failed include, a file on disk, or an unverified server assumption. [WordPress filesystem knowledge](../knowledge/wordpress/files-and-network.md) helps resolve write behavior, not authority.
