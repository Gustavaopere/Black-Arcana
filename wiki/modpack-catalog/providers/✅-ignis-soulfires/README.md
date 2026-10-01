# Cataclysm: Ignis Soulfires — 1.8.0

Status: `✅ CATALOGED / EXACT PHYSICAL=PUBLISHER ARTIFACT / 8 DISCRETE SUPERNATURAL PLAYER ACTIONS / COUNTED_EXACT / TOOL MODES + PASSIVE GEAR EXCLUDED / RUNTIME QA SEPARATE`

## Current physical identity

- sibling authority: `neoforge-rpg-skilltree@682a62c13c38215691be24361ffd303abb32dc01`;
- certified dossier: `PROJECT-INSTRUCTIONS/modlist/Addons + Armor, Tools, and Weapons + Cosmetic + Ores and Resources/✅-cataclysm-ignis-soulfires v1.8.0.md`;
- JAR: `ignissoulfires-1.8.0.jar`;
- mod id: `ignissoulfires`;
- runtime: `1.8.0`;
- Minecraft 1.21.1 / NeoForge;
- physical SHA-1: `a6f1c8cfe673aaff17f081ee9546e3600b4c72f1`.

## Exact publisher-artifact closure

NON-MERGE evidence PR **#491** audited the official 1.8.0 artifact and hard-gated equality against the physical pack fingerprint.

- audit HEAD: `24e0b5b63e816d96314acc610b7abdb39dec0792`;
- audit run: `36832733575` — SUCCESS;
- evidence artifact: `11148470931`;
- artifact digest: `sha256:c7c8f7116590df736eaecb02521658b47d8f27ada402facdfde2215a4401f60a`;
- publisher SHA-1: `a6f1c8cfe673aaff17f081ee9546e3600b4c72f1`;
- publisher SHA-256: `a2368227b6cab37988334b4b6b8b6936fdf939aaa3518494a3921b45a426989d`;
- bytes: `489267`.

The publisher SHA-1 exactly equals the current physical sibling SHA-1. This catalog therefore describes the exact installed artifact.

Bounded archive inventory: **454 entries / 181 classes / 273 non-class resources / 378 provider-associated paths**. No Iron's/Ars-style spell, glyph or ritual registry surface was found; the relevant supernatural gameplay is exposed through item-owned active actions.

See [`EXACT-1.8.0-ARTIFACT-AUDIT.md`](EXACT-1.8.0-ARTIFACT-AUDIT.md).

## Semantic action inventory

| Owner | Action | Exact action seam | State |
|---|---|---|---|
| `bulwark_of_the_soul_flame` | Bulwark Deployment | `deployBulwark(...)` | `COUNTED_EXACT` |
| `bulwark_of_the_soul_flame` | Bulwark Charge | `releaseUsing(...)`, `chargeCooldown`, Cataclysm `ChargeAttachment` | `COUNTED_EXACT` |
| `souled_gauntlet_of_bulwark` | Soul-Fire Chain | shift channel + distinct chain cooldown/range/pull/hit seams | `COUNTED_EXACT` |
| `souled_gauntlet_of_bulwark` | Gauntlet Charge | non-shift release + distinct `chargeCooldown` + `ChargeAttachment` | `COUNTED_EXACT` |
| `the_souled_immolator` | Soul-Fire Stun Area | shift release + area cooldown/radius/stun-damage seams | `COUNTED_EXACT` |
| `the_souled_immolator` | Flame Strike | non-shift release + `spawnFlameStrike(...)` + `strikeCooldown` | `COUNTED_EXACT` |
| `the_souled_incinerator` | Incinerator Dash | shift release + dash cooldown/damage/knockback seams | `COUNTED_EXACT` |
| `the_souled_incinerator` | Incinerator Slam | non-shift release + `useIncineratorSlam(...)` + `slamCooldown` | `COUNTED_EXACT` |

Detailed cards: [`actions/README.md`](actions/README.md).

These are eight identities because each is a distinct player-invoked action branch with a distinct provider settlement seam/cooldown or spawned outcome. Stun, Blazing Brand, knockback, particles, damage, wall effects and individual spawned strikes are downstream consequences and are not counted again.

## Exact acquisition routes

The exact installed artifact packages provider-owned routes for every action-hosting item:

- Bulwark — shaped crafting and smithing transform;
- Souled Gauntlet — `cataclysm:weapon_fusion` from Cataclysm Gauntlet of Guard + provider Bulwark;
- Immolator of Souls — `cataclysm:weapon_fusion` from Cataclysm The Immolator + Souled Ignitium Ingot;
- Incinerator of Souls — smithing transform from Cataclysm The Incinerator + Souled Ignitium materials/template.

This closes catalog-level acquisition provenance. Live recipe availability and assembled-pack execution remain runtime QA.

## Cataloged but excluded from the semantic numerator

The exact artifact also exposes thrown-tool operation, tool return, distance breaking/actions, Souled 3×3 tool behavior, prospecting, Tree Cap, tool-mode cycling, passive Souled Blazing Grips behavior, armor/horse-armor effects, materials, attributes, recipes, advancements and client presentation.

Those surfaces remain relevant provider gameplay, but the global semantic ledger explicitly does not mint extra spell-equivalent identities from ordinary tool modes, gear/passives, effects/statuses or downstream consequences.

## Authority boundary

Ignis Soulfires owns its item/action definitions, active weapon branches/cooldowns, Bulwark wall, Souled Ignitium progression, tool modes/prospecting/Tree Cap, armor/horse-armor effects and provider config/state. L_Ender's Cataclysm remains authority for Cataclysm-owned base items/effects/entities and shared machinery such as `ChargeAttachment` and weapon-fusion recipes.

Black Arcana must not duplicate these eight settlements, add a second cooldown/resource ledger or convert their downstream effects into extra casts. RPG Skill Tree does not become runtime owner of these actions.

## Runtime QA remains fail-closed

Catalog closure does not prove dedicated-server/full-pack behavior, deployed numeric config, Cataclysm 3.33 ABI behavior for every path, multiplayer/interruption, protected-region Bulwark behavior, datapack-overridden acquisition, death/relog/restart lifecycle, combat-bridge exactly-once behavior, tool/prospecting compatibility or any Black Arcana adapter.

## Result

**✅ Cataloged.** Ignis Soulfires 1.8.0 contributes **8 `COUNTED_EXACT` discrete supernatural player actions** to the strict semantic-magic minimum. Tool modes and passive gear effects are documented but add **+0** under the semantic metric.