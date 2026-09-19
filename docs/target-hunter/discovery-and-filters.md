# Define, discover, and filter

## Stage 1 — Define the hunt

Establish the research date, broad or focused category, plugin/theme preference, explicit researcher tier if supplied, practical install-count constraints, licence/budget tolerance for premium functionality, WooCommerce interest, and local test constraints. Use the internal [mode preflight](../modes.md) for scope, workspace, loaded guidance, and unresolved assumptions. If a preference is absent, continue with a broad discovery and state the assumption; never infer tier from the researcher's history. An unknown tier remains an explicit variable in later scope assessments.

## Stage 2 — Discover from functionality

Build roughly **10–30 plausible candidates** from several functional classes or from the requested class. Search for software whose real workflows cross actor, object, authority, file, payment, identity, network, or deferred-work boundaries. Booking, membership, commerce, import/export, backup, registration, LMS, integration, and authentication are useful starting points, not a fixed favored list. Include novel project/tenant/member or other custom models when they offer consequential boundaries. Popularity and code size do not make a candidate by themselves.

For each initial candidate, record a short reason it entered the pool and the source/date for its identity and availability. Prefer the current [WordPress.org plugin directory](https://wordpress.org/plugins/), its official plugin API, and release/SVN history for repository plugins: slug, active installations, version, last update, compatibility requirements, author, description, changelog, and public download. Use the [WordPress.org theme directory](https://wordpress.org/themes/) for listed themes, noting when equivalent metadata is unavailable. Use an official project-linked repository for releases and change history; verify that a mirror actually belongs to the project. Use vendor documentation for workflows and licences. Use [Wordfence program intelligence](../../knowledge/bounty/wordfence/README.md) for current scope and its vulnerability database for history; official CVE records or NVD can clarify past versions and CWE. Secondary writeups may add context but cannot override primary facts. Record publication date separately from the release or vulnerability event date.

At this stage, use metadata and documentation. Do not download source for every candidate or query arbitrary production sites. If a page/API is inaccessible, mark the fact unknown and keep only candidates whose remaining evidence supports further work. Avoid turning an old directory listing or remembered install count into a current fact.

## Stage 3 — Apply hard filters carefully

Screen **the locally reviewable component and the relevant vulnerability families**, not one universal active-install threshold. Recheck current Wordfence scope, exclusions, tier effects, product availability, and any verified temporary event using the [dated intelligence](../../knowledge/bounty/wordfence/README.md). A low-install product may still be worth considering for a class with broader scope; a tier-dependent outcome remains tier-dependent. Bounty fit and technical security value are separate judgments.

Usually remove candidates when current evidence establishes that: meaningful source cannot be legitimately obtained; the interesting component is solely a remote vendor service; the only valuable feature is paid code or a licence unavailable for local study; relevant software is closed with no supported exception; or the architecture offers little meaningful attacker-to-authority boundary. A simple plugin is not automatically disqualified. Previous CVEs alone never disqualify it.

Mark each filter **passes**, **fails**, **conditional**, or **unknown**, with the decisive source and date. Distinguish a verified disqualifier from a missing fact. If a product could be in scope only for certain classes, tiers, repository conditions, or a documented closure exception, retain it conditionally or request a current check rather than asserting eligibility. Keep a brief reason for eliminations; spend deeper effort only on survivors.
