# Demon Archer — entity contract (1.0.3)

Identity: `acolyte:demon_archer`; implementation `net.raptorzizi.acolyte.entity.mobs.wizards.demon.DemonArcherEntity`. This is one registered entity type. [Shared demon behavior](demon-family.md) owns alliances, profile lifecycle, cast-animation callbacks, persistence and common client rendering. [Packaged demon/archer profiles](../profiles/demon-archer.md) own weighted loadouts and effective stat overrides.

## Evidence and status

Source: exact publisher `acolyte-1.0.3.jar`, CurseForge file `8098233`, 621,837 bytes; SHA-1 `ad0abc821f3f8a6573ac19a50970fc1bc46b4275`, SHA-256 `73fe745bbb0016fbc00af9ba14c0ecfe0a1d8a7d72a7892557739182b3486256`. Installed JAR equality is unproved. Method descriptors and PCs below identify the local `javap -p -c -s -constants` evidence described in [binary contracts](../BINARY-CONTRACTS-1.0.3.md); entry coverage is in the [artifact manifest](../ARTIFACT-CATALOG-MANIFEST-1.0.3.json). Publisher-only factual interoperability summary; no implementation or assets reproduced. Embedded MIT / publisher All Rights Reserved conflict remains recorded at the provider boundary.

`mutating_hook: NOT_VERIFIED`; `physical: NOT_TESTED`; certified perk boundaries: **0**. Documentation changes no runtime. Referenced spells remain Iron's-owned; **+0 Acolyte semantic spells**.

## Attributes and identity

`DemonArcherEntity.getArchetypeName()Ljava/lang/String;`, PCs 0–2, returns `demon/archer`. `prepareAttributes()Lnet/minecraft/world/entity/ai/attributes/AttributeSupplier$Builder;`, PCs 0–37, starts with living attributes and explicitly sets ATTACK_DAMAGE=0, MAX_HEALTH=40, FOLLOW_RANGE=32, MOVEMENT_SPEED=0.25. These are registration baselines; profile stat application and equipment can change effective attributes. Zero base attack damage does not mean zero final weapon or spell damage.

`ModEntityRegistry.lambda$static$2()Lnet/minecraft/world/entity/EntityType;`, PCs 0–36, registers MONSTER category, dimensions 0.6×1.8 and client tracking range 64. Tracking range is not spell range. `shouldDespawnInPeaceful()Z`, PCs 0–1, returns true. Spawn/distribution resources do not create extra biome entity IDs.

## Combat composition

All PCs in this section are `DemonArcherEntity.registerArchetypeGoals()V`. A null selected profile returns at PCs 0–7. If `barrageSpell` is non-null (8–62), priority-1 Iron's `SpellBarrageGoal` receives the spell, integer arguments 1/1, interval `[barrageAttackInterval,barrageAttackInterval+20]` and profile projectile count. Its constructor descriptor is `(Lio/redspace/ironsspellbooks/api/entity/IMagicEntity;Lio/redspace/ironsspellbooks/api/spells/AbstractSpell;IIIII)V`. The supplied 1/1 cast-level bounds and configured count belong to this composition; projectile effects are host-owned.

PCs 65–112 install [SingleUseSpellGoal](../goals/single-use-spell.md) at priority 2 when the profile has a spell. Constructor `(Lio/redspace/ironsspellbooks/api/entity/IMagicEntity;Lio/redspace/ironsspellbooks/api/spells/AbstractSpell;IIII)V` receives level bounds 1/1 and delay bounds `[singleUseSpellDelay,singleUseSpellDelay+20]`. This is a local goal, separate from the mage's host wizard single-use policy.

PCs 115–140 install [UniversalRangedGoal](../goals/universal-ranged.md) at priority 3 with speed 1, profile `attackInterval` and navigation range argument 15. Constructor is `(Lnet/minecraft/world/entity/PathfinderMob;DIF)V`. The 15-block value gates movement, not every shot; the goal card specifies charge, visibility and release behavior.

PCs 143–157 additionally install water-avoiding random stroll at priority 5/speed 1.

## Arrow projection and animation

`performRangedAttack(Lnet/minecraft/world/entity/LivingEntity;F)V`, PCs 0–40, creates an ordinary ARROW stack and delegates arrow construction to `ProjectileUtil.getMobArrow`, passing the callback's float and null weapon-stack argument. It sets arrow **base damage** to `selectedProfile.getStatOverride("attack_damage",6)/2`; this is not final damage after speed, armor, enchantments or damage events. The method assumes a non-null selected profile and consumes no inventory arrows locally.

PCs 41–138 aim from shooter x/z toward target x/z, at target `getY(0.3333)` relative to arrow y, adding vertical compensation `min(horizontalDistance×0.2,targetHeight×0.6)`. Arrow `shoot(DDDFF)V` receives speed 2 and inaccuracy `3−profile.tier`, with no local clamp (shipped tiers 1/2/3 supply 2/1/0). PCs 139–171 add the arrow to the world (the boolean result is ignored) and play ARROW_SHOOT, volume 1 and pitch `1/(randomFloat×0.4+0.8)`. No local raycast, block/protection check or successful-hit callback appears in this projection method; targeting policy comes from the family/goal and final collision/damage from vanilla.

PCs 174–205 set synced release=true, charge=false and `attackAnimationTick=15`. `tick()V`, PCs 0–117, calls family tick, then server-side decrements that timer; at zero it clears release and stops item use. A timer positive at entry bypasses the target-dependent charge branch for that tick, even if a target disappears. Only when the timer is nonpositive at entry does a non-null target set charge=true; absent target then clears charge/release and stops item use. `defineSynchedData(Lnet/minecraft/network/syncher/SynchedEntityData$Builder;)V`, PCs 0–29, initializes both booleans false. These booleans and timer have no role-local NBT persistence method.

`bowPredicate(Lsoftware/bernie/geckolib/animation/AnimationState;)Lsoftware/bernie/geckolib/animation/PlayState;`, PCs 0–83, prioritizes release using host ANIMATION_INSTANT_CAST, otherwise charge using BOW_CHARGE_ANIMATION, otherwise STOP. `registerControllers(Lsoftware/bernie/geckolib/animation/AnimatableManager$ControllerRegistrar;)V`, PCs 0–14, adds `bow_controller` then inherited controllers; constructor `(Lnet/minecraft/world/entity/EntityType;Lnet/minecraft/world/level/Level;)V`, PCs 11–29, uses transition length 2. `canFireProjectileWeapon(Lnet/minecraft/world/item/ProjectileWeaponItem;)Z`, PCs 0–19, accepts BowItem and CrossbowItem, although the callback above still constructs an ordinary arrow.

The local ambient/hurt/death getters use EVOKER_AMBIENT / EVOKER_HURT / EVOKER_DEATH (`getAmbientSound()Lnet/minecraft/sounds/SoundEvent;`, `getHurtSound(Lnet/minecraft/world/damagesource/DamageSource;)Lnet/minecraft/sounds/SoundEvent;`, `getDeathSound()Lnet/minecraft/sounds/SoundEvent;`, PCs 0–3 each).

## Acquisition surface

`data/acolyte/loot_table/entities/demon_archer.json` has two pools with one roll each and zero bonus rolls. Pool 1 supplies host arcane essence with uniform count input 0–4 plus vanilla looting increase input 0–1. Pool 2 chooses among eligible scroll/horn entries: the host scroll has randomized-spell quality input 0–0.3 and requires killed-by-player plus looting-aware random-chance condition (unenchanted 0.25; enchanted linear base 0.1, +0.05 per level above first). The demon-horn alternative has uniform set-count input 0–0.5. These are **alternative entries in one pool**, not guaranteed independent scroll and horn drops; fractional count inputs are resolved by vanilla loot-number semantics. No fixed scroll spell identity is implied.

## Integration axes and validation

| Axis | Boundary / limitation |
|---|---|
| Projection / delivery | Arrow construction/spawn callback above; actual entity addition is not verified at runtime. |
| Effects | Spell effects remain Iron's-owned; arrow collision/effects use vanilla projectile behavior. |
| Mana / costs | No local mana debit in this role. No recruitment currency contract for this entity. |
| Cooldown / duration | Local role delay operands are explicit above; host spell cooldown and cast duration delegated. The 15-tick timer is bow presentation. |
| Damage / healing | Arrow base-damage input is local; final damage/healing delegated. |
| Targeting / teams | Family target goals/alliance filter plus goal-specific range/visibility; follow/tracking ranges are distinct. |
| Rituals | N/A: no ritual registration, ritual object or ritual callback. |
| Progression / perks | No verified Black Arcana/RPG Skill Tree mutator or successful-effect observer. |

Physical QA must cover profile reload, host cast ordering, projectile/melee damage events, friendly fire, multiplayer ownership, protection and animation compatibility. Static call-site evidence does not certify those runtime interactions.
