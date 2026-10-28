# Demon family — shared entity contract (1.0.3)

This support card covers abstract `net.raptorzizi.acolyte.entity.mobs.wizards.demon.DemonEntity`, `DemonModel` and `DemonRenderer`. There is **no registered `acolyte:demon` base type**. Actual types are [Demon Mage](demon-mage.md), [Demon Warrior](demon-warrior.md) and [Demon Archer](demon-archer.md), each inheriting Iron's `AbstractSpellCastingMob` and this Enemy family.

## Evidence and status

Source: exact publisher `acolyte-1.0.3.jar`, CurseForge file `8098233`, 621,837 bytes; SHA-1 `ad0abc821f3f8a6573ac19a50970fc1bc46b4275`, SHA-256 `73fe745bbb0016fbc00af9ba14c0ecfe0a1d8a7d72a7892557739182b3486256`. Installed JAR equality is unproved. Method descriptors and PCs below identify the local `javap -p -c -s -constants` evidence described in [binary contracts](../BINARY-CONTRACTS-1.0.3.md); entry coverage is in the [artifact manifest](../ARTIFACT-CATALOG-MANIFEST-1.0.3.json). Publisher-only factual interoperability summary; no implementation or assets reproduced. Embedded MIT / publisher All Rights Reserved conflict remains recorded at the provider boundary.

`mutating_hook: NOT_VERIFIED`; `physical: NOT_TESTED`; certified perk boundaries: **0**. Documentation changes no runtime. Referenced spells remain Iron's-owned; **+0 Acolyte semantic spells**.

## Goal composition, allegiance and damage

`DemonEntity.registerGoals()V`, PCs 0–91, installs float priority 0, selected role goals, host patrol priority 8 with radius 30/speed 0.75, player look priority 9/range 8, recovery priority 10, then target goals. `registerTargetGoals()V`, PCs 0–117, uses nearest-attackable targets with sight checking: HumanEntity priority 1, player 2, host `NeutralWizard` 4, hurt-by retaliation 5, golem 6, Villager 7. No explicit new target radius is supplied; each role's FOLLOW_RANGE attribute feeds host/vanilla selection. `isLeftHanded()Z`, PCs 0–1, returns false.

`isAlliedTo(Lnet/minecraft/world/entity/Entity;)Z`, PCs 0–27, accepts inherited allies, every DemonEntity and LieutenantEntity. `hurt(Lnet/minecraft/world/damagesource/DamageSource;F)Z`, PCs 0–27, rejects a **causing entity** of either demon family or lieutenant, then delegates unchanged damage to the host. Unlike the human override, there is no independent direct-projectile-entity check and no broad call to `isAlliedTo` in this local hurt filter. `getHurtSound(Lnet/minecraft/world/damagesource/DamageSource;)Lnet/minecraft/sounds/SoundEvent;`, PCs 0–3, uses vanilla VILLAGER_HURT unless a role overrides it.

## Spawn and persistent lifecycle

`finalizeSpawn(Lnet/minecraft/world/level/ServerLevelAccessor;Lnet/minecraft/world/DifficultyInstance;Lnet/minecraft/world/entity/MobSpawnType;Lnet/minecraft/world/entity/SpawnGroupData;)Lnet/minecraft/world/entity/SpawnGroupData;`, PCs 0–203: capture base attributes; random skin 0–2; weighted profile roll; apply profile stats; XP from profile or 15; sync; clear/rebuild both goal selectors; equip; set/clear visible profile custom name; resolve biome folder; then host finalize. `captureBaseAttributes()V` and `applyProfileStats()V` delegate to ArchetypeUtils (PCs 0–8 / 0–12). See [archetype pipeline](../systems/archetype-loadout-pipeline.md) for stat/spell lookup and [profiles](../profiles/demon-mage.md) for the actual packaged loadouts.

`populateDefaultEquipmentSlots(Lnet/minecraft/util/RandomSource;Lnet/minecraft/world/DifficultyInstance;)V`, PCs 0–146, does nothing for null profile. Missing profile head chooses one of four `ModItemsRegistry.DEMON_HORNS` entries uniformly; explicit head is applied otherwise. Chest/legs/feet are applied; main hand is only populated when empty. `applySlot(Lnet/minecraft/world/entity/EquipmentSlot;Lnet/minecraft/world/item/Item;)V`, PCs 0–6, delegates to ArchetypeUtils; no offhand population here.

`addAdditionalSaveData(Lnet/minecraft/nbt/CompoundTag;)V`, PCs 0–67: host save plus `SkinVariant`, `BiomeFolder` and non-null `ArchetypeProfile`. `readAdditionalSaveData` with the same descriptor, PCs 0–112, restores skin/optional biome, resolves saved profile id by role, applies/syncs stats, and clears/rebuilds both goal selectors. Local reload does not explicitly restore profile XP, custom name or populate equipment. No recruitment ownership/contract protocol exists in this family.

## Cast callbacks and presentation

`initiateCastSpell(Lio/redspace/ironsspellbooks/api/spells/AbstractSpell;I)V`, PCs 0–22, resolves cast-start animation through ModUtils, remembers the spell and delegates the unchanged level to the host. `castComplete()V`, PCs 0–53, uses a non-pass LONG finish animation when available, starts the 20-tick reset, then host completion. `tick()V`, PCs 0–32, calls host tick and restores the host instant-cast animation when that delay reaches zero. Spell costs, effects, actual cast eligibility and completion semantics remain host contracts.

DemonModel's `getTextureResource(Lio/redspace/ironsspellbooks/entity/mobs/abstract_spell_casting_mob/AbstractSpellCastingMob;)Lnet/minecraft/resources/ResourceLocation;` and `getAnimationResource` with the same descriptor, PCs 0–20 each, select DemonEntity texture/current animation, with fallback otherwise. DemonRenderer `(Lnet/minecraft/client/renderer/entity/EntityRendererProvider$Context;)V`, PCs 0–12, uses DemonModel and the host renderer. Geometry is inherited; 21 local textures are `assets/acolyte/textures/entity/generic_skin/{desert,jungle,plains,savanna,snowy,swamp,taiga}/demon{0,1,2}.png`.

**Exact fallback discrepancy:** `DemonEntity.<clinit>()V`, PCs 0–9, names `acolyte:textures/entity/generic_skin/plains/human0.png`. The family selector passes species `demon` to ArchetypeUtils in `getTextureLocation()Lnet/minecraft/resources/ResourceLocation;`, PCs 0–22, but its fallback constant is the human texture. The card records the binary instead of assuming a demon fallback. Shared biome-path and non-Iron's-animation mapping are described in [human-family utility contracts](human-family.md#shared-utility-contracts).

## Natural spawn utility

`ModUtils.checkDemonSpawnRules(Lnet/minecraft/world/entity/EntityType;Lnet/minecraft/world/level/ServerLevelAccessor;Lnet/minecraft/world/entity/MobSpawnType;Lnet/minecraft/core/BlockPos;Lnet/minecraft/util/RandomSource;)Z`, PCs 0–86: if the accessor is ServerLevel, disabled demon-natural-spawn gamerule rejects; then reject `NO_DEFAULT_MONSTERS`, Peaceful, failed `Monster.isDarkEnoughToSpawn`, or failed `Monster.checkMobSpawnRules`. Unlike humans, no 300-block family-exclusion box is tested. This predicate does not itself spawn an entity or guarantee profile/biome results.

## Integration axes

| Axis | Exact local boundary / practical limit |
|---|---|
| Projection / delivery | Entity AI and host cast initiation are observable; no player spell projection API is supplied. Host spell delivery stays with Iron's. |
| Effects | Host spell effects and vanilla damage settlement are delegated; animation state is presentation, not successful effect settlement. |
| Mana / resources | No local mana price or debit in these cast overrides; host mob casting owns resource behavior. No recruitment contract is declared for demons. |
| Cooldown / duration | The 20-tick animation reset is local presentation timing; goal delays are documented on role/goal cards. Generic host spell cooldown is delegated. |
| Damage / healing | Local friendly-fire rejection is explicit; accepted damage goes to `AbstractSpellCastingMob.hurt`. No independent healing formula. |
| Targeting / teams | Local alliance and target rules below precede host/vanilla behavior; these are integration-sensitive server decisions. |
| Rituals | N/A: no ritual identity, altar, ritual cost or ritual callback in this family. |
| Progression / perks | No verified Black Arcana or RPG Skill Tree callback. A read-only observer must distinguish cast request, animation and final host effect. |

Persistence, unload/reload, dedicated server/client class loading, same-owner multiplayer, protected regions and exactly-once host damage/cast observation remain physical QA cases; binary facts do not certify a mutation hook.
