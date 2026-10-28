# Demon Mage — entity contract (1.0.3)

Identity: `acolyte:demon_mage`; implementation `net.raptorzizi.acolyte.entity.mobs.wizards.demon.DemonMageEntity`. This is one registered entity type. [Shared demon behavior](demon-family.md) owns alliances, profile lifecycle, cast-animation callbacks, persistence and common client rendering. [Packaged demon/mage profiles](../profiles/demon-mage.md) own weighted loadouts and effective stat overrides.

## Evidence and status

Source: exact publisher `acolyte-1.0.3.jar`, CurseForge file `8098233`, 621,837 bytes; SHA-1 `ad0abc821f3f8a6573ac19a50970fc1bc46b4275`, SHA-256 `73fe745bbb0016fbc00af9ba14c0ecfe0a1d8a7d72a7892557739182b3486256`. Installed JAR equality is unproved. Method descriptors and PCs below identify the local `javap -p -c -s -constants` evidence described in [binary contracts](../BINARY-CONTRACTS-1.0.3.md); entry coverage is in the [artifact manifest](../ARTIFACT-CATALOG-MANIFEST-1.0.3.json). Publisher-only factual interoperability summary; no implementation or assets reproduced. Embedded MIT / publisher All Rights Reserved conflict remains recorded at the provider boundary.

`mutating_hook: NOT_VERIFIED`; `physical: NOT_TESTED`; certified perk boundaries: **0**. Documentation changes no runtime. Referenced spells remain Iron's-owned; **+0 Acolyte semantic spells**.

## Attributes and identity

`DemonMageEntity.getArchetypeName()Ljava/lang/String;`, PCs 0–2, returns `demon/mage`. `prepareAttributes()Lnet/minecraft/world/entity/ai/attributes/AttributeSupplier$Builder;`, PCs 0–37, starts with living attributes and explicitly sets ATTACK_DAMAGE=0, MAX_HEALTH=30, FOLLOW_RANGE=24, MOVEMENT_SPEED=0.25. These are registration baselines; profile stat application and equipment can change effective attributes. Zero base attack damage does not mean zero final weapon or spell damage.

`ModEntityRegistry.lambda$static$0()Lnet/minecraft/world/entity/EntityType;`, PCs 0–36, registers MONSTER category, dimensions 0.6×1.8 and client tracking range 64. Tracking range is not spell range. `shouldDespawnInPeaceful()Z`, PCs 0–1, returns true. Spawn/distribution resources do not create extra biome entity IDs.

## Combat composition

All PCs in this section are `DemonMageEntity.registerArchetypeGoals()V`. A null selected profile returns at PCs 0–7. If `barrageSpell` is non-null (8–62), priority-1 Iron's `SpellBarrageGoal` receives the spell, integer arguments 1/1, interval `[barrageAttackInterval,barrageAttackInterval+20]` and profile projectile count. Its constructor descriptor is `(Lio/redspace/ironsspellbooks/api/entity/IMagicEntity;Lio/redspace/ironsspellbooks/api/spells/AbstractSpell;IIIII)V`. The supplied 1/1 cast-level bounds and configured count belong to this composition; projectile effects are host-owned.

PCs 65–142 create Iron's `WizardAttackGoal` with speed 1.25 and interval `[attackInterval,attackInterval+20]`; `setSpellQuality(FF)` receives `[spellsQuality,spellsQuality+0.1]`; `setSpells(Ljava/util/List;Ljava/util/List;Ljava/util/List;Ljava/util/List;)Lio/redspace/ironsspellbooks/entity/mobs/goals/WizardAttackGoal;` receives attack, defense, mobility and utility lists in that order. The wizard constructor is `(Lio/redspace/ironsspellbooks/api/entity/IMagicEntity;DII)V`. A non-null single-use spell at PCs 143–186 is configured on **the host wizard goal** using delay bounds `[singleUseSpellDelay,singleUseSpellDelay+20]` and 1/1 integer level bounds. The configured wizard goal is installed at priority 2 at PCs 187–193. This role does not instantiate Acolyte's standalone SingleUseSpellGoal.

Target selection and follow range come from the shared family and attributes. Exact cast level selection from quality, visibility/distance checks, spell duration, spell damage/healing, mana behavior and generic spell cooldown reside in Iron's WizardAttackGoal/spell implementation; this Acolyte class supplies no independent formula for them.

No role-local ambient/death/hurt override is declared; shared demon hurt sound is VILLAGER_HURT, with other sounds inherited.

## Acquisition surface

`data/acolyte/loot_table/entities/demon_mage.json` has two pools with one roll each and zero bonus rolls. Pool 1 supplies host arcane essence with uniform count input 0–4 plus vanilla looting increase input 0–1. Pool 2 chooses among eligible scroll/horn entries: the host scroll has randomized-spell quality input 0–0.3 and requires killed-by-player plus looting-aware random-chance condition (unenchanted 0.25; enchanted linear base 0.1, +0.05 per level above first). The demon-horn alternative has uniform set-count input 0–0.5. These are **alternative entries in one pool**, not guaranteed independent scroll and horn drops; fractional count inputs are resolved by vanilla loot-number semantics. No fixed scroll spell identity is implied.

## Integration axes and validation

| Axis | Boundary / limitation |
|---|---|
| Projection / delivery | Host spell barrage and WizardAttackGoal cast requests. |
| Effects | Spell effects remain Iron's-owned; role class adds no spell effect implementation. |
| Mana / costs | No local mana debit in this role. No recruitment currency contract for this entity. |
| Cooldown / duration | Local role delay operands are explicit above; host spell cooldown and cast duration delegated.  |
| Damage / healing | Base attributes/profile/equipment and host spells/goals determine results; no independent final damage/healing formula here. |
| Targeting / teams | Family target goals/alliance filter plus goal-specific range/visibility; follow/tracking ranges are distinct. |
| Rituals | N/A: no ritual registration, ritual object or ritual callback. |
| Progression / perks | No verified Black Arcana/RPG Skill Tree mutator or successful-effect observer. |

Physical QA must cover profile reload, host cast ordering, projectile/melee damage events, friendly fire, multiplayer ownership, protection and animation compatibility. Static call-site evidence does not certify those runtime interactions.
