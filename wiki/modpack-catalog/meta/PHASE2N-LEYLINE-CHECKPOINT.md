# Phase 2N — Leyline Spellbooks checkpoint

## Base

Work began from `main@1586260b06a94c3c11c164b7c58d5c130798a891` after a fresh reconciliation of the physical modlist, Notion, provider queue and concurrent branches/PRs.

Ars Nouveau was intentionally excluded because another active branch/PR already owned that catalog area. Phase 2N selected Leyline Spellbooks because it remained high-value, incomplete and unclaimed.

## Scope completed

- confirmed installed `leylines-1.0.3.jar`, mod id `leylines`, runtime `1.0.3`;
- reconciled CurseForge Project `1636676` / File `8565076` / NeoForge 1.21.1 release identity;
- corrected installed-artifact provenance to the current physical modlist hash `dfa6908731f432905caaaa1e53b4aedeaa26ed59`;
- independently corroborated that same SHA-1 against a public manifest for CurseForge File ID `8565076`;
- rejected the stale SHA-1 `5307a4edc885ab949eed4438d9d7f9cb6176421d` for Leylines; independent public manifests associate it with `letsdo-wildernature-neoforge-1.1.5.jar` / File ID `8543233`;
- consolidated duplicate provider trees into canonical `providers/leyline-spellbooks/`;
- preserved the nine existing public spell pages and verified their fail-closed wording;
- normalized the nine public signature names as a **lower bound**, because the publisher explicitly says `and more`;
- cataloged publisher-confirmed progression and 1.0.3 rift encounter semantics;
- added provider-wide semantic deduplication for portal pairs, recall anchors, temporal control, rupture/knock-up, charge state and bounded rift encounters;
- updated clean-room provenance under ARR.

## What Phase 2N does not claim

Phase 2N does **not** claim:

- complete spell count or registry inventory;
- `9/9 COMPLETE`;
- exact spell IDs/classes/values;
- exact charge implementation;
- exact item/block/entity/effect/attribute registries;
- exact API/hooks/networking/persistence;
- runtime/config/client validation of Leyline-specific internals;
- JAR bytecode inspection or decompilation.

## Evidence ceiling

No exact publisher source repository was located. The official CurseForge download flow was reached, but the permitted browser/runtime did not provide inspectable JAR bytes and the local shell had no external DNS route to the published Maven/CDN endpoints.

**PENDÊNCIA — REQUER ARTEFATO EXATO INSPECIONÁVEL / NAVEGAÇÃO EXTERNA CAPAZ DE ENTREGAR O BINÁRIO**

Until then, provider-specific internal integration remains fail-closed and unknown Leyline content is reserved as unknown provider space rather than treated as a confirmed Black Arcana gap.
