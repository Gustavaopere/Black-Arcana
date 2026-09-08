# Phase 2R — Ars Controle 1.6.15 checkpoint

Status: `SOURCE CATALOG COMPLETE / FINAL DIFF+SYNC+CI+MERGE PENDING / RUNTIME+PACK QA PENDING`

Execution branch: `docs/magic-catalog-phase2r-ars-controle`
PR: `#99`
Provider source pin: `Vonr/Ars-Controle@ecbb83ba512bc9ca7a025556fb9c62dbd32b6430`
Physical JAR: `ars_controle-1.21.1-1.6.15.jar`
Physical SHA-1: `fdf381d5733698abe336354c7541299ab495ecae`

## Exact source coverage

- registry surface: 4 blocks / 6 items / 3 BlockEntityTypes / 2 data components / 4 attachments / 1 creative tab / 9 spell parts;
- glyphs: 9/9 individually cataloged;
- glyph default acquisition: 9/9 resolved;
- systems: 6/6 individually cataloged;
- system default acquisition: 6/6 resolved;
- networking: 5 payloads classified;
- server/startup config: classified;
- empty/unregistered client config surface: recorded;
- Scryer's Linkage generic capability delegation: classified;
- provider mixins/validators: classified;
- ComputerCraft optional peripherals: classified, provider absent in current physical pack;
- LGPLv3 source/license pin: verified for read-only factual cataloging;
- Phase 2R queue/capability/provenance overlays: written.

## Corrections against older editorial inventory

1. Exact release has 3 BlockEntityTypes, not 4; Temporal Stability Sensor has no BE registration.
2. Exact release has 9 registered spell parts, not 31 glyph/components. The prior 31-component Notion count is historical/editorial rather than current registry authority.
3. No current physical ComputerCraft/CC:Tweaked top-level JAR was found.

## High-value safety findings

- Warping Spell Prism owns a configurable provider region-ticket path; no Black Arcana force-load authority follows from it.
- Warping Spell Prism entity-target Source settlement has a source-path divergence and remains runtime-QA gated.
- Scryer's Linkage `load_time` config is declared but its audited runtime path does not prove the corresponding ticket behavior.
- Remote multi-selection has no explicit volume/range cap visible in its audited box iteration.
- Portable Brazier Relay is one original Ars ritual object recontextualized to the carrier while normal brazier ticking is suppressed.

## Shared provenance policy

`SOURCES.md`, `THIRD_PARTY_NOTICES.md` and `docs/provenance/REFERENCE_LEDGER.md` are high-churn shared surfaces. The narrow Phase 2R provenance overlay is authoritative for Ars Controle until a safe shared-index regeneration/reconciliation; no unrelated entry is overwritten by this phase.

## Remaining before Phase 2R merge

1. Review exact PR diff; no runtime/Stage files may be introduced.
2. Verify diff sanity/trailing whitespace.
3. Refetch `main` and reconcile if advanced.
4. Run full CI on the final reconciled PR HEAD.
5. Resolve blocking review findings if any.
6. Merge only if exact-head gates are green.

Runtime/config/client/full-modpack acceptance is not part of the source-catalog merge claim and remains pending.
