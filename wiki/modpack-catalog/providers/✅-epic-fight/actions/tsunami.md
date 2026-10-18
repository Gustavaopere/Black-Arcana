# Tsunami

- Provider: **Epic Fight** (`epicfight`)
- Version: `21.17.3.1`
- Exact physical/publisher SHA-1: `fb199b7bbea2fc402da28ab586e73f47e32f8fc0`
- Skill id: `epicfight:tsunami`
- Owner/reachability: `minecraft:trident` with vanilla **Riptide**
- Semantic type: deliberate supernatural tide/mobility attack
- State: `COUNTED_EXACT`

## Technical parameters for perks — exact JAR vs adjacent source

✅ **Exact publisher JAR 21.17.3.1:** packaged `data/epicfight/skill_parameters/tsunami.json` declares **`consumption=50.0`**, unit/charge settlement unverified. The [bounded Java21 proof #39093719405](../EXACT-TRIDENT-CAUSAL-REFERENCES-21.17.3.1.md) confirms `isInWaterOrRain` with two compiled results in `EpicFightSkills` and both animations `TSUNAMI` / `TSUNAMI_REINFORCED`. `ConditionalWeaponInnateSkill` selects an animation and invokes `playAnimationSynchronized`. This establishes an environmental selection seam, not measured dash distance/damage.

⚠️ **Source-adjacent 21.17.3 only:** `ARMOR_NEGATION_MODIFIER adder(100)`, `STUN_TYPE KNOCKDOWN`, and tag `WEAPON_INNATE` in its configured attack phase. [Source L352–360](https://github.com/Antikythera-Studios/epicfight/blob/a78aa24b72e90a9d09f5fd61925e4369d117abaf/src/main/java/yesman/epicfight/registry/entries/EpicFightSkills.java#L352-L360). The constant 100 is not proof of a 100% HP-damage bonus or full armor bypass.

**Perk axes:** target, range, dash length, AOE radius, hitbox, projectile velocity/scale, real damage type, cast duration, cooldown and settled cost remain **NÃO VERIFICADO**. A perk may not permanently apply the rain variant or duplicate water particles as casts; both animations belong to one Tsunami root. ⛔ External retarget/range manipulation without safe provider hook.

## Identity and selector

The exact `EpicFightMovesets.TRIDENT` innate selector resolves Tsunami when the trident has Riptide.

Because Riptide is the first selector branch, this path takes precedence over the Channeling and Loyalty branches in the same exact selector.

## Exact provider behavior

The exact artifact packages dedicated Tsunami animation resources and provider Tsunami particle paths. Exact control flow also chooses a strengthened action variant when the server player is in water or rain.

Water/rain state modifies this same Tsunami identity. It does not create a second semantic root.

## Deduplication boundary

Dash/movement, particles, animation, hits, damage and the strengthened environmental variant are parameters or consequences of the one provider-owned action.

## Authority boundary

Epic Fight remains authority for movement, resource state, animation, target/hit processing and all settlement. Black Arcana catalogs the action but must not duplicate it.

Sources: `../EXACT-21.17.3.1-ARTIFACT-SKILL-AUDIT.md`, `../skills/SKILL-DISPOSITION-21.17.3.1.md`.
