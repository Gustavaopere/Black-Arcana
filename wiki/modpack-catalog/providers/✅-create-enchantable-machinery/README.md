# Create: Enchantable Machinery — 3.6.0

Status: `✅ CATALOGED / EXACT PHYSICAL=PUBLISHER ARTIFACT / ZERO_SEMANTIC_MACHINE_ENCHANTMENT_APPLICATION / +0 STRICT / RUNTIME QA SEPARATE`

## Current physical identity

- sibling physical row: **#183**;
- JAR: `createenchantablemachinery-3.6.0+mc1.21.1-neoforge.jar`;
- mod id: `createenchantablemachinery`;
- runtime: `3.6.0`;
- physical SHA-1: `ed9a5cf654235f54a3c5aced27ac654d5258e393`.

The addon makes selected Create machines enchantable and persists/uses existing Minecraft or external enchantments on those machines. It does not own a new spell, ritual, glyph, ability or enchantment identity roster.

## Exact publisher-artifact closure

NON-MERGE evidence PR **#556** audits Modrinth version `Cw5k6c0a` (same 3.6.0 NeoForge 1.21.1 line as CurseForge File `7766920`) and hard-gates the artifact against the physical pack fingerprint.

- audit HEAD: `dd9ae99608f7561961ca909ce1f5cf2c2987e0ea`;
- exact-artifact run: `37159216158` — **SUCCESS**;
- evidence artifact: `11286842169`;
- evidence digest: `sha256:fc321c53755dfd7220744b5a40ebc6a749b50d2fa6a5020254c8ac99742a55d0`;
- publisher SHA-1: `ed9a5cf654235f54a3c5aced27ac654d5258e393`;
- publisher SHA-256: `933ad37b064d8c6005f1f6eb09b3274fe9f5961a6841fb9e7bb65a7bff66f653`;
- bytes: `575,739`.

The publisher SHA-1 exactly equals the current physical pack SHA-1.

See [`EXACT-3.6.0-ARTIFACT-AUDIT.md`](EXACT-3.6.0-ARTIFACT-AUDIT.md).

## Exact semantic inventory

The exact artifact contains **282 entries / 142 classes / 140 resources / 17 provider-data paths / 12 provider JSON files**.

Provider-owned semantic path counts are zero for spell, magic, ritual, ability, mana, arcane, glyph, summon, soul, teleport, portal and curse. `enchant` is intentionally non-zero because the entire addon is enchantment application/state infrastructure.

Critically, the exact JAR contains **zero datapack enchantment definitions** and no provider-owned enchantment registry. All observed enchantment lookups resolve Minecraft/external enchantment holders such as Efficiency/Silk Touch or generic item enchantment data.

## Exact enchantable machine set — 11

The exact provider tag `createenchantablemachinery:enchantable_blocks` contains:

1. `create:mechanical_drill`
2. `create:mechanical_saw`
3. `create:mechanical_harvester`
4. `create:encased_fan`
5. `create:millstone`
6. `create:crushing_wheel`
7. `create:mechanical_plough`
8. `create:mechanical_mixer`
9. `create:mechanical_press`
10. `create:mechanical_roller`
11. `create:spout`

The provider maps each Create machine to an enchantable variant and copies/persists the standard `minecraft:enchantments` component through placement, block state and loot/drop paths.

## Player interaction boundary

Exhaustive activation-signature inspection finds no cast/use action roster. The only player-facing `use` mixins on Drill, Roller and Saw detect an already-enchanted matching block item and delegate to the enchantable block variant. The other relevant overrides are placement/removal/state lifecycle.

Applying an existing enchantment through an Enchanting Table/anvil or placing an enchanted machine is enchantment economy/state manipulation, not a new semantic spell/ritual/action identity.

Detailed disposition: [`SEMANTIC-SURFACE-DISPOSITION.md`](SEMANTIC-SURFACE-DISPOSITION.md).

## Authority boundary

Minecraft and external enchantment providers remain authority for enchantment identities and effects. Create remains authority for the underlying machine/process state machine. Enchantable Machinery owns the machine↔enchantment mapping, persistence, display and machine-specific adaptation of those existing enchantments.

Black Arcana must not duplicate enchantment effects, re-own vanilla/modded enchantments, or count each machine/enchantment combination as a spell.

## Result

**✅ Cataloged — `ZERO_SEMANTIC_MACHINE_ENCHANTMENT_APPLICATION`.**

Strict semantic delta: **+0**.
