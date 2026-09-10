# Provider audit queue — Phase 2N delta

This narrow overlay prevails only for mod id `leylines` until the integral 103-provider queue is regenerated. Every other row remains governed by `PROVIDER-AUDIT-QUEUE.md` plus the previously declared narrow overlays.

## `leylines` — Leyline Spellbooks

- Installed JAR: `leylines-1.0.3.jar`
- Runtime: `1.0.3`
- Minecraft/loader: `1.21.1` / NeoForge
- CurseForge Project ID: `1636676`
- CurseForge File ID: `8565076`
- Physical modlist hash: `dfa6908731f432905caaaa1e53b4aedeaa26ed59`
- License: `All Rights Reserved`
- Current state: `EXACT INSTALLED IDENTITY 1.0.3 / PHYSICAL HASH CORRECTED / 9 PUBLIC SIGNATURE NAMES LOWER BOUND / PUBLISHER RIFT + PROGRESSION SURFACE CATALOGED / COMPLETE REGISTRY + BYTECODE/API QA PENDING / FAIL-CLOSED`

## Evidence advanced in Phase 2N

The publisher-facing surface is now normalized under the single canonical provider tree `providers/leyline-spellbooks/`:

- nine named signature spells are cataloged individually;
- the publisher says `and more`, so nine is a lower bound rather than a complete registry count;
- Blink Step, Rift Gate, Chrono Tether, Temporal Stutter, Fissure and Anchor Recall have individually attributable public semantics;
- Beam, Ley Blast and Eclipse are name-confirmed, but their individual mechanics remain unverified;
- pillar/rift progression and 1.0.3 rift reliability/arena behavior are recorded;
- provider-native authority/deduplication boundaries are recorded for portals, recall anchors, temporal control, world rupture, charges and wave encounters.

## Provenance correction

The current physical modlist row for `leylines-1.0.3.jar` records SHA-1 `dfa6908731f432905caaaa1e53b4aedeaa26ed59`. An independent public manifest for CurseForge File ID `8565076` corroborates the same artifact/hash pair. A previous catalog revision incorrectly assigned SHA-1 `5307a4edc885ab949eed4438d9d7f9cb6176421d` to Leylines; independent public manifests instead associate that value with `letsdo-wildernature-neoforge-1.1.5.jar` / CurseForge File ID `8543233`. The stale value is rejected for Leylines.

## Structural correction

The duplicate provider directory `providers/leylines/` was consolidated into `providers/leyline-spellbooks/`. The richer progression/rift/spell material was preserved and the duplicate tree removed. This is documentation normalization only.

## Remaining gate

No publisher-controlled exact 1.0.3 source repository was located. The official CurseForge download flow was reached, but the permitted environment did not obtain inspectable JAR bytes. No bytecode/resource extraction or decompilation was performed.

Still pending:

- complete spell count and registry IDs;
- spell values/formulas/targeting;
- exact charge/state implementation;
- item/block/entity/effect/attribute registries;
- recipes/loot probabilities;
- networking/persistence/API hooks;
- multiplayer rift ownership/cleanup details;
- runtime/config/client QA against the full pack.

**PENDÊNCIA — REQUER ARTEFATO EXATO INSPECIONÁVEL / NAVEGAÇÃO EXTERNA CAPAZ DE ENTREGAR O BINÁRIO**

Phase 2N therefore advances Leyline Spellbooks substantially but does **not** mark it `DONE`, `9/9 COMPLETE`, registry-complete or runtime-validated.
