# Phase 2AM checkpoint — Reliquified L_Ender's Cataclysm New Relics Fix 1.0.2

## State

`CATALOG CLOSURE CANDIDATE / PUBLISHER-SURFACE COMPATIBILITY BRIDGE / NOT CANONICAL UNTIL LATEST-MAIN RECONCILIATION + EXACT-HEAD CI GREEN + MERGE`

## Base

- initial canonical `main`: `433233164f61bbf6b6d5cb8aa9625cf286a79a23`
- predecessor: Phase 2AL / PR #145, component #40
- branch: `docs/magic-catalog-phase2am-reliquified-cataclysm-fix-1.0.2`
- canonical coverage at branch creation: `40/100 = 40%`
- proposed result after canonical merge: `41/100 = 41%`

No equivalent open PR or branch for `reliquified_lenders_cataclysm_new_relics_fix` was found before branch creation. Open stale Ars provider PRs remain separate concurrent work and are not modified here.

## Physical identity

- artifact: `reliquified-lenders-cataclysm-new-relics-fix-1.0.2.jar`
- mod id: `reliquified_lenders_cataclysm_new_relics_fix`
- runtime: `1.0.2`
- physical SHA-1: `9d4710e665ec74af917bb9f5f819154ca9f74ca0`
- physical NeoForge: `21.1.248`

## Exact publisher release

CurseForge:

- project `1665965`;
- file `8778365`;
- filename `reliquified-lenders-cataclysm-new-relics-fix-1.0.2.jar`;
- uploaded `2026-08-31`;
- Minecraft 1.21.1 / NeoForge;
- Client & Server;
- All Rights Reserved.

Exact 1.0.2 file changelog: bridge limited to the addon's base class, preventing global `RelicItem` modifications.

## Physical stack

Required publisher families are present:

- Relics `0.12.8`;
- Curios `9.5.1+1.21.1`;
- OctoLib `0.6.2`;
- L_Ender's Cataclysm `3.33`;
- Reliquified L_Ender's Cataclysm `0.1.1`.

## Closed public semantic surface

This phase closes the component at the exact publisher surface, not at a fabricated source-internal ceiling.

Publisher-declared compatibility responsibilities:

1. removed `IRelicItem` startup/API repair;
2. legacy definitions → `RelicTemplate`;
3. Curios integration and attribute modifiers;
4. stats/levels/ranks/cooldowns/experience;
5. legacy active abilities;
6. player-motion packet replacement;
7. ability order/progression values;
8. descriptions/tooltips.

Exactly five existing relics are named as fixed:

- Void Cloak;
- Scouring Eye;
- Void Vortex in Bottle;
- Vacuum Glove;
- Void Bubble.

Semantic result:

- 0 new relic identities attributed to the fix;
- 0 standalone spell identities published for the fix;
- one compatibility component closed for authority/deduplication.

## Source boundary

No exact public source for fix 1.0.2 was located from the publisher page or GitHub repository search.

The original addon's public `1.21.1` repository currently declares `mod_version=0.2`, while the physical original addon is `0.1.1`. That current tree is not used to invent exact physical-original or fix internals.

Consequently exact mixin classes/counts/targets, transform signatures, player-motion packet schema, RelicTemplate IDs and persistence keys remain `NÃO VERIFICADO`.

## Authority result

- Relics owns current relic framework/progression/cooldown infrastructure.
- Reliquified L_Ender's Cataclysm owns the five relic identities and intended content behavior.
- Curios owns equip-slot state/infrastructure.
- the 1.0.2 fix owns only translation/compatibility for the old addon against the new framework.
- Black Arcana owns its canonical magic runtime and does not duplicate this bridge.
- RPG Skill Tree receives no relic or magic runtime authority from this fix.

## Provenance / clean-room

The fix is All Rights Reserved. No source code, bytecode or assets were copied/decompiled/adapted. This audit uses physical metadata plus publisher-authored release/description evidence.

The original addon's current public repository was consulted only at metadata level to establish that its current `0.2` branch is not an exact `0.1.1` source authority.

## Remaining QA

Does not block semantic component closure:

- exact fix source/JAR identity unavailable;
- exact internal mixin/transform inventory unavailable;
- dedicated-server boot of the full physical relic stack not independently exercised in this catalog phase;
- Curios modifiers, rank/XP/cooldown persistence and active abilities require runtime QA;
- player-motion networking requires multiplayer QA;
- upstream native Relics 0.12 support in the original addon would require re-evaluating whether keeping this bridge causes double adaptation.

## Merge protocol

Before merge:

1. fetch latest `main`;
2. reconcile if advanced;
3. review exact diff;
4. run Black Arcana CI on the exact reconciled HEAD;
5. require repository unit/diff/build/JAR/GameTest/dedicated-server gates GREEN;
6. merge only with expected exact HEAD;
7. confirm final `main` SHA.
