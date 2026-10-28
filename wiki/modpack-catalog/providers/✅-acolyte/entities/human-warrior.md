# Human Warrior — entity contract (1.0.3)

Identity: `acolyte:human_warrior`; implementation `net.raptorzizi.acolyte.entity.mobs.wizards.human.HumanWarriorEntity`. This is one registered entity type. [Shared human behavior](human-family.md) owns alliances, profile lifecycle, cast-animation callbacks, persistence and common client rendering. [Packaged human/warrior profiles](../profiles/human-warrior.md) own weighted loadouts and effective stat overrides.

## Evidence and status

Source: exact publisher `acolyte-1.0.3.jar`, CurseForge file `8098233`, 621,837 bytes; SHA-1 `ad0abc821f3f8a6573ac19a50970fc1bc46b4275`, SHA-256 `73fe745bbb0016fbc00af9ba14c0ecfe0a1d8a7d72a7892557739182b3486256`. Installed JAR equality is unproved. Method descriptors and PCs below identify the local `javap -p -c -s -constants` evidence described in [binary contracts](../BINARY-CONTRACTS-1.0.3.md); entry coverage is in the [artifact manifest](../ARTIFACT-CATALOG-MANIFEST-1.0.3.json). Publisher-only factual interoperability summary; no implementation or assets reproduced. Embedded MIT / publisher All Rights Reserved conflict remains recorded at the provider boundary.

`mutating_hook: NOT_VERIFIED`; `physical: NOT_TESTED`; certified perk boundaries: **0**. Documentation changes no runtime. Referenced spells remain Iron's-owned; **+0 Acolyte semantic spells**.

## Attributes and identity

`HumanWarriorEntity.getArchetypeName()Ljava/lang/String;`, PCs 0–2, returns `human/warrior`. `prepareAttributes()Lnet/minecraft/world/entity/ai/attributes/AttributeSupplier$Builder;`, PCs 0–53, starts with living attributes and explicitly sets ATTACK_DAMAGE=0, MAX_HEALTH=60, FOLLOW_RANGE=24, MOVEMENT_SPEED=0.25, ATTACK_KNOCKBACK=0 and ENTITY_INTERACTION_RANGE=3.5. These are registration baselines; profile stat application and equipment can change effective attributes. Zero base attack damage does not mean zero final weapon or spell damage.

`ModEntityRegistry.lambda$static$4()Lnet/minecraft/world/entity/EntityType;`, PCs 0–36, registers MONSTER category, dimensions 0.6×1.8 and client tracking range 64. Tracking range is not spell range. `shouldDespawnInPeaceful()Z`, PCs 0–1, returns true. Spawn/distribution resources do not create extra biome entity IDs.

## Combat composition

All PCs in this section are `HumanWarriorEntity.registerArchetypeGoals()V`. A null selected profile returns at PCs 0–7. If `barrageSpell` is non-null (8–62), priority-1 Iron's `SpellBarrageGoal` receives the spell, integer arguments 1/1, interval `[barrageAttackInterval,barrageAttackInterval+20]` and profile projectile count. Its constructor descriptor is `(Lio/redspace/ironsspellbooks/api/entity/IMagicEntity;Lio/redspace/ironsspellbooks/api/spells/AbstractSpell;IIIII)V`. The supplied 1/1 cast-level bounds and configured count belong to this composition; projectile effects are host-owned.

PCs 65–112 install [SingleUseSpellGoal](../goals/single-use-spell.md) at priority 2 when the profile has a spell. Constructor `(Lio/redspace/ironsspellbooks/api/entity/IMagicEntity;Lio/redspace/ironsspellbooks/api/spells/AbstractSpell;IIII)V` receives level bounds 1/1 and delay bounds `[singleUseSpellDelay,singleUseSpellDelay+20]`. This is a local goal, separate from the mage's host wizard single-use policy.

PCs 115–169 compute integer-divided interval `m=attackInterval/2` (Java integer division) and `m+10`; construct [WarriorMeleeGoal](../goals/warrior-melee.md) with speed 1, set combo chance 0.3, set melee interval `[m,m+10]`, set melee movement modifier 1.3, then install priority 3. Constructor is `(Lio/redspace/ironsspellbooks/entity/mobs/abstract_spell_casting_mob/AbstractSpellCastingMob;FII)V`. Reach, animation hit frames and actual `doHurtTarget` settlement are delegated to that goal and its Iron's animated-warlock superclass. The 3.5 interaction-range attribute is not independently substituted for the host's reach formula here.

## Melee presentation and locomotion

Constructor `(Lnet/minecraft/world/entity/EntityType;Lnet/minecraft/world/level/Level;)V`, PCs 6–45, initializes an empty queued animation and `keeper_animations` controller (transition 0), then installs local look/move controls. `playAnimation(Ljava/lang/String;)V`, PCs 0–27, queues a named RawAnimation and logs caught exceptions. `predicate(Lsoftware/bernie/geckolib/animation/AnimationState;)Lsoftware/bernie/geckolib/animation/PlayState;`, PCs 0–32, resets the controller, applies/clears a queued animation, then returns CONTINUE. `registerControllers(Lsoftware/bernie/geckolib/animation/AnimatableManager$ControllerRegistrar;)V`, PCs 0–14, adds melee then inherited controllers; `isAnimating()Z`, PCs 0–25, combines non-STOPPED melee-controller state with inherited animation state.

Anonymous look control `$1.rotateTowards(FFF)F`, PCs 0–10, multiplies the supplied rotation limit by 2.5; `resetXRotOnTick()Z`, PCs 0–15, resets pitch only without a target. Move control `$2.strafe(FF)V`, PCs 0–6, passes the forward value but forces lateral strafe zero. `$2.rotlerp(FFF)F`, PCs 0–60, preserves current rotation while squared horizontal wanted-position distance is below 0.5, otherwise passes rotation limit×0.25 to vanilla. `createNavigation(Lnet/minecraft/world/level/Level;)Lnet/minecraft/world/entity/ai/navigation/PathNavigation;` returns host NotIdioticNavigation with doors enabled (PCs 0–16).

The local ambient/hurt/death getters use EVOKER_AMBIENT / EVOKER_HURT / EVOKER_DEATH (`getAmbientSound()Lnet/minecraft/sounds/SoundEvent;`, `getHurtSound(Lnet/minecraft/world/damagesource/DamageSource;)Lnet/minecraft/sounds/SoundEvent;`, `getDeathSound()Lnet/minecraft/sounds/SoundEvent;`, PCs 0–3 each).

## Integration axes and validation

| Axis | Boundary / limitation |
|---|---|
| Projection / delivery | Host spell barrage and local melee-goal composition; host melee hit settlement. |
| Effects | Spell effects remain Iron's-owned; role class adds no spell effect implementation. |
| Mana / costs | No local mana debit in this role. Temporary recruitment uses the [emerald contract](../systems/recruitment-contract.md). |
| Cooldown / duration | Local role delay operands are explicit above; host spell cooldown and cast duration delegated.  |
| Damage / healing | Base attributes/profile/equipment and host spells/goals determine results; no independent final damage/healing formula here. |
| Targeting / teams | Family target goals/alliance filter plus goal-specific range/visibility; follow/tracking ranges are distinct. |
| Rituals | N/A: no ritual registration, ritual object or ritual callback. |
| Progression / perks | No verified Black Arcana/RPG Skill Tree mutator or successful-effect observer. |

Physical QA must cover profile reload, host cast ordering, projectile/melee damage events, friendly fire, multiplayer ownership, protection and animation compatibility. Static call-site evidence does not certify those runtime interactions.
