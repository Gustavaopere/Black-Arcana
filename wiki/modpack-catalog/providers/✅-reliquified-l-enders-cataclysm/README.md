# Reliquified L_Ender's Cataclysm — 0.1.1

Status: `✅ CATALOGED / CURRENT PHYSICAL 0.1.1 / COUNTED_EXACT / 5 RELIC OWNERS / 7 OWNER-SCOPED ABILITY ROOTS / +7 STRICT / RUNTIME QA SEPARATE`

## Current physical identity

Current sibling physical authority records:

- sibling checkpoint: `neoforge-rpg-skilltree@f5508b496e4a607e1b0b53dde7e9242cf6d98d20`;
- physical row: **#479**;
- JAR: `reliquified_lenders_cataclysm-1.21.1-0.1.1.jar`;
- mod id: `reliquified_lenders_cataclysm`;
- runtime: `0.1.1`;
- Minecraft / loader: 1.21.1 / NeoForge;
- physical SHA-1: `be89d697455f04a1531ed81b45bcc038354430c8`;
- current host stack: L_Ender's Cataclysm `3.33`, Relics `0.12.8`, OctoLib `0.6.2`;
- compatibility companion: `reliquified-lenders-cataclysm-new-relics-fix-1.0.2.jar`.

The compatibility companion adapts the legacy Relics integration to the current Relics 0.12.x stack. It does not mint a second semantic identity for a Reliquified ability.

## Exact 0.1.1 artifact closure

Publisher version `ZHAIRSeF` supplies the exact NeoForge 1.21.1 file `reliquified_lenders_cataclysm-1.21.1-0.1.1.jar`.

Isolated NON-MERGE audit PR **#441** materialized that publisher artifact and hard-gated its SHA-1 against the current physical digest. Final exact-artifact audit:

- audit HEAD: `096c74db131ecffa95e4f2c22162b311c1c62db5`;
- workflow run: `36416011761`;
- result: **GREEN**;
- publisher SHA-1: `be89d697455f04a1531ed81b45bcc038354430c8`;
- physical SHA-1: `be89d697455f04a1531ed81b45bcc038354430c8`;
- exact artifact metadata version: `0.1.1`;
- exact artifact mod id: `reliquified_lenders_cataclysm`.

The audit is clean-room and bounded. It retains factual archive/metadata/localization/signature facts plus a narrow bytecode scan only for `AbilityData.builder(String)` declarations and `ItemRegistry.register(String, Supplier)` identities. It does not preserve full disassembly, implementation bodies, localization values or assets.

See [EXACT-0.1.1-ARTIFACT-AUDIT.md](EXACT-0.1.1-ARTIFACT-AUDIT.md).

## Exact registry and semantic inventory

The exact hash-matched 0.1.1 artifact contains exactly **five** provider relic item classes and exactly **five** corresponding registered item identities:

1. `scouring_eye`;
2. `void_vortex_in_bottle`;
3. `void_cloak`;
4. `vacuum_glove`;
5. `void_bubble`.

The exact artifact contains exactly **seven** `AbilityData.builder(String)` declarations across those five owners. The independently extracted exact localization root set also contains exactly the same seven owner/ability pairs, and the audit asserts the two sets are equal.

| # | Relic owner | Ability ID | Localized ability name |
|---:|---|---|---|
| 1 | Scouring Eye | `glowing_scour` | Pursuit |
| 2 | Void Vortex in Bottle | `spawn_vortex` | Void Tornado |
| 3 | Void Cloak | `void_invulnerability` | Invulnerability |
| 4 | Void Cloak | `void_rune` | Call of the Void |
| 5 | Void Cloak | `seismic_zone` | Final Cry |
| 6 | Vacuum Glove | `vacuum_slowdown` | The Edge |
| 7 | Void Bubble | `protective_bubble` | Protective Bubble |

The exact artifact exposes no provider data resource under `data/reliquified_lenders_cataclysm/` that would constitute an additional data-defined ability registry.

Result: the complete current 0.1.1 owner-scoped ability denominator is **7**.

## Release-line source corroboration

Official repository: `Octo-Studios/reliquified-lenders-cataclysm`.

Release-day source checkpoint `291f066c0471e44f50fe78ea8e7d786f6775446e` on branch `1.21.1` declares version `0.1` and independently exposes the same five registered relic owners and the same seven ability roots. Later development added additional relics before a subsequent 0.2 version bump; those moving-branch additions are not projected backward into 0.1.1.

The source is All Rights Reserved. It is used only for factual interoperability/catalog corroboration, not code/assets/text reuse.

## Exact-current acquisition evidence

The final hash-matched 0.1.1 audit closes the same Relics loot routes directly from the exact artifact:

- Scouring Eye — `CURSED_PYRAMID` / `THE_END`;
- Void Vortex in Bottle — `FROSTED_PRISON` / `THE_END`;
- Void Cloak — `CURSED_PYRAMID` / `FROSTED_PRISON` / `THE_END`;
- Vacuum Glove — `CURSED_PYRAMID` / `THE_END`;
- Void Bubble — `THE_END`.

The exact artifact also exposes exactly two provider-specific `LootEntry` fields, `CURSED_PYRAMID` and `FROSTED_PRISON`, with the Cataclysm Cursed Pyramid and Frosted Prison table identifiers. These exact-current routes reconcile all five registered relic owners and close provider-level survival reachability for all seven ability roots. Final assembled-world loot mutation and observed drop generation remain runtime QA rather than semantic-inventory evidence.

## Semantic disposition

Black Arcana already treats Reliquified provider ability roots as provider-owned semantic magic identities while excluding the relic item container, rank/stat modifiers, XP sources, spawned entities/projectiles and downstream consequences as additional objects.

The seven exact current roots are therefore:

**`COUNTED_EXACT 7 / +7 STRICT`.**

Runtime/config compatibility is not inferred from this catalog closure.

## Ownership boundary

- L_Ender's Cataclysm owns bosses, structures, drops and source mechanics.
- Relics owns generic relic progression, levels/ranks, ability framework state and cooldown/XP machinery.
- Reliquified L_Ender's Cataclysm owns its seven provider relic/ability identities.
- New Relics Fix 1.0.2 owns compatibility adaptation to the current Relics stack and does not mint duplicate identities.
- Black Arcana must not duplicate relic progression, cooldowns, provider ability execution or Cataclysm causal ownership.
- RPG Skill Tree remains sibling authority only for progression/attributes/Mastery/perks/gates exposed through real contracts.

## Runtime and compatibility QA remains separate

Catalog closure does not assert assembled-pack PASS. Remaining runtime gates include:

- dedicated-server startup with physical 0.1.1 + fix 1.0.2 + Relics 0.12.8 + Cataclysm 3.33 + OctoLib 0.6.2;
- Curios equip/unequip and stale-modifier behavior;
- XP/rank/level persistence across relog/restart;
- cooldown persistence and exactly-once expiry;
- active/proc abilities in remote multiplayer;
- motion/network behavior restored by the compatibility fix;
- boss kill/loot causal deduplication;
- live assembled loot injection and survival acquisition.

## Result

**✅ Cataloged — `COUNTED_EXACT`.**

Current semantic inventory: **7 owner-scoped Reliquified L_Ender's Cataclysm ability roots across 5 relic owners**.

Strict semantic delta: **+7**.