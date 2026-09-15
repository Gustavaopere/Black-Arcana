# Black Arcana — Status

Last updated: 2026-09-15

## Authoritative execution rule

D034 supersedes D031 for numbered-stage promotion. The mandatory order is:

`05 -> 05A -> 06 -> 07 -> 07A -> 08 -> 09`

For each stage:

`AUDIT -> IDENTIFY GAPS -> IMPLEMENT -> TEST -> VALIDATE -> MARK ✅ -> AUDIT AGAIN -> ONLY THEN ADVANCE`

A stage is not complete while any requirement defined by its plans remains pending, deferred, partially implemented or unproven. Required manual, physical, real-client, real-modpack and provider-native validation is part of completion when a plan requires it. Automated CI, GameTests, a frozen runtime contract or an exact-SHA artifact cannot be converted into manual evidence.

Existing downstream implementation created under the former D031 policy remains repository history and may be reused later. It does not authorize current work to skip the earliest incomplete stage.

## Current active stage

**Stage 05 — Casting & UX is the only active numbered stage.**

Current Stage 05 state: `ACTIVE / IMPLEMENTATION PRESENT / REQUIRED PHYSICAL VALIDATION PENDING`.

The current plan ledger is in `plans/05-casting-ux/00-execution-status.md`. At this checkpoint:

- 05.01–05.06 remain 🟡 because required physical/runtime-input/client/provider acceptance is not fully proven;
- 05.07 Presentation Data Contracts is ✅;
- `docs/qa/casting-ux-manual-matrix.md` remains the real-client evidence matrix;
- `docs/qa/casting-ux-real-client-runbook.md` defines how PASS/FAIL/BLOCKED evidence must be recorded;
- no remaining manual row may be inferred from CI or code inspection.

### Latest canonical Stage 05.01 authority hardening

PR #271 closed a deterministic server-authority gap in the immediate-cast ingress path. A client could previously submit a registered/executable spell for a loadout slot containing a different server-owned spell and reach the engine.

Canonical runtime checkpoint before this documentation reconciliation:

- merge SHA: `1d0e221440506005fd4cd16220436f3573c0adec`;
- branch workflow `35035822174`: GREEN;
- PR-head workflow `35036140396`: GREEN;
- post-merge workflow `35036436151`: GREEN for unit tests, diff sanity, NeoForge build, built-JAR verification, Foundation GameTests, dedicated-server smoke and artifact publication;
- QA artifact: `black-arcana-1d0e221440506005fd4cd16220436f3573c0adec`;
- artifact ID: `10423705741`;
- artifact SHA-256: `f61d7f3f533e220e1f81e72ee75e98dacd7358367e5def88ce6a6df173a73629`.

This closes that deterministic implementation gap only. It does not complete 05.01 and does not mark any real-client matrix row PASS.

## Stage table

| Stage | State | Promotion meaning |
|---|---|---|
| 00 Foundation | ✅ COMPLETE | historical completed predecessor |
| 01 Reference Catalog | ✅ COMPLETE | historical completed predecessor |
| 02 Arcana Core | ✅ COMPLETE | historical completed predecessor |
| 03 Integration Layer | ✅ COMPLETE | historical completed predecessor |
| 04 World Safety | ✅ COMPLETE | historical completed predecessor |
| 05 Casting & UX | 🟡 ACTIVE / BLOCKING | finish every 05 plan and required physical acceptance before 05A |
| 05A Arcane Danger | ⛔ BLOCKED BY 05 | implementation exists in `main`, but full audit/promotion is deferred until Stage 05 is complete |
| 06 Rituals | ⛔ BLOCKED BY 05 -> 05A | historical implementation exists; do not treat it as stage-complete until predecessors close and Stage 06 is fully reaudited |
| 07 Spell Domains | ⛔ BLOCKED BY 05 -> 05A -> 06 | historical 07.01–07.07 work remains reusable, but Stage 07 is not the active work target |
| 07A Arcane Polarity, Fusion & Metamagic | ⛔ BLOCKED BY 07 | do not start until all Stage 07 plans are fully complete |
| 08 Progression & Balance | ⛔ BLOCKED BY 07A | RPG Skill Tree remains progression/attributes/Mastery/perks/gates authority; Black Arcana remains magic-runtime authority |
| 09 Hardening & Release | ⛔ BLOCKED BY 08 | final integrated hardening only after all prior stages are complete |

## Authority boundaries

Black Arcana owns the authoritative magic runtime: casting, rituals, magical domains, Arcane Danger, persistence, world safety and provider-native magic integration.

RPG Skill Tree owns progression, attributes, Mastery, perks and progression gates. Later work must not duplicate that authority inside Black Arcana.

Client UI remains presentational/predictive only. External providers remain behind verified adapters and optional integrations fail closed where compatibility or causal identity is not proven.

## Stage 05 completion gate

Stage 05 cannot be promoted while any applicable 05.01–05.06 acceptance item remains unresolved. In particular, current required evidence includes real-client/runtime observation of input rebinding and GUI-focus suppression, server-owned loadout apply/clear/reconnect behavior, supported 16-slot reachability, radial toggle/hold and cast separation, stale-state lifecycle behavior, client-config authority isolation, and required real-modpack/provider coexistence.

The exact applicable rows and evidence requirements are canonical in the Stage 05 plan files plus `docs/qa/casting-ux-manual-matrix.md`. If a row cannot be exercised, record `BLOCKED` with the concrete reason; do not manufacture PASS.

Only after Stage 05 is completely proven may Stage 05A be audited for promotion. The same rule then applies sequentially through 09.

## Historical downstream implementation

Code and evidence already merged for 05A, 06 and 07 are preserved. Their previous labels such as `IMPLEMENTED`, `FINAL VALIDATION DEFERRED`, `CANONICAL RUNTIME` or partial-domain canonical checkpoints describe historical implementation state only. Under D034 they are not stage-completion claims and do not change the active-stage order.

Do not delete or reimplement correct historical code merely because promotion was reset. When its stage becomes active, audit it against the current plans and latest `main`, reuse correct canonical implementation, and implement only what is actually missing.
