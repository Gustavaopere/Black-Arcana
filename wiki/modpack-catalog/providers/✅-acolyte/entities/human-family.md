# Human family — shared entity contract (1.0.3)

This support card covers abstract `net.raptorzizi.acolyte.entity.mobs.wizards.human.HumanEntity`, `HumanModel` and `HumanRenderer`. It is **not** a registered `acolyte:human` entity. The actual types are [Human Mage](human-mage.md), [Human Warrior](human-warrior.md) and [Human Archer](human-archer.md). All derive from Iron's `AbstractSpellCastingMob`; HumanEntity also implements companion and neutral-mob contracts.

## Evidence and status

Source: exact publisher `acolyte-1.0.3.jar`, CurseForge file `8098233`, 621,837 bytes; SHA-1 `ad0abc821f3f8a6573ac19a50970fc1bc46b4275`, SHA-256 `73fe745bbb0016fbc00af9ba14c0ecfe0a1d8a7d72a7892557739182b3486256`. Installed JAR equality is unproved. Method descriptors and PCs below identify the local `javap -p -c -s -constants` evidence described in [binary contracts](../BINARY-CONTRACTS-1.0.3.md); entry coverage is in the [artifact manifest](../ARTIFACT-CATALOG-MANIFEST-1.0.3.json). Publisher-only factual interoperability summary; no implementation or assets reproduced. Embedded MIT / publisher All Rights Reserved conflict remains recorded at the provider boundary.

`mutating_hook: NOT_VERIFIED`; `physical: NOT_TESTED`; certified perk boundaries: **0**. Documentation changes no runtime. Referenced spells remain Iron's-owned; **+0 Acolyte semantic spells**.

## Goal composition and targets

`HumanEntity.registerGoals()V` installs float and open-door goals at priority 0 (PCs 0–30), [stay order](../goals/stay-order.md) at 2 (33–50), then the selected role goals (53–61). Follow-owner priority 6 receives speed 1.399999976158142, distance arguments 10 and 3, boolean false, and final distance 20 (64–94). Patrol priority 7 receives radius 30 and speed 0.75 (97–116); host recovery is priority 8 (119–133), water-avoiding stroll priority 9 at speed 1 (136–151), look-at-player at priority 10/range 8 and random look at 10 (154–189).

The target selector uses host owner-hurt-by, owner-hurt-target and copy-owner-target goals at priorities 1/2/3; host hurt-by at 4 with its alliance predicate and empty alert-exclusion array; protect-owner at 5; and a vanilla nearest `Mob` target goal at 4 with interval 5 and booleans false/false (PCs 192–325). `lambda$registerGoals$2(Lnet/minecraft/world/entity/LivingEntity;)Z`, PCs 0–26, admits `Enemy` except `Creeper` only while unrecruited. `lambda$registerGoals$1` with the same descriptor, PCs 0–5, returns `isAlliedTo` for the host hurt-by goal. Role follow range is an attribute, not a newly fixed spell radius.

`createNavigation(Lnet/minecraft/world/level/Level;)Lnet/minecraft/world/entity/ai/navigation/PathNavigation;`, PCs 0–16, constructs Iron's `NotIdioticNavigation` and enables opening doors. `isLeftHanded()Z` returns false. Anger time is synced; `startPersistentAngerTimer()V`, PCs 0–22, samples `200 + nextInt(200)`, i.e. 200–399 ticks. Getter/setter UUID anger target state and inherited neutral-mob serialization are present; the local `tick()V` does not explicitly invoke an anger-update routine.

## Alliances and incoming damage

`isAlliedTo(Lnet/minecraft/world/entity/Entity;)Z`, PCs 0–119: inherited allies, any `AbstractVillager` and `IronGolem` are allies. While recruited, the exact owner player and recruited HumanEntity companions with the same non-null owner UUID are also allies. An unrecruited human is not automatically allied to every other human by this method.

`setTarget(Lnet/minecraft/world/entity/LivingEntity;)V`, PCs 0–50, refuses HumanEntity, host `PriestEntity`, villagers, golems and other non-null allies; null and other accepted targets delegate to the host setter. `hurt(Lnet/minecraft/world/damagesource/DamageSource;F)Z`, PCs 0–129, rejects damage when either causing entity or direct entity is HumanEntity, PriestEntity, IronGolem or AbstractVillager. It then rejects an allied causing entity, or a distinct allied direct entity, before passing the unchanged damage amount to the host. These direct-source checks are broader than owner alliance alone.

## Spawn, profiles and persistent state

`finalizeSpawn(Lnet/minecraft/world/level/ServerLevelAccessor;Lnet/minecraft/world/DifficultyInstance;Lnet/minecraft/world/entity/MobSpawnType;Lnet/minecraft/world/entity/SpawnGroupData;)Lnet/minecraft/world/entity/SpawnGroupData;`, PCs 0–203: capture base attributes, sample one of three skin variants, roll the role profile using a `java.util.Random` seeded from host random, apply profile stats, set profile XP or fallback 15, sync profile, clear both goal selectors and register them again, equip, set/clear visible custom name, resolve biome folder, then call host finalization. Exact weighting, stat overrides, spell pools and reload behavior belong to the [archetype pipeline](../systems/archetype-loadout-pipeline.md). Equipment applies profile head/chest/legs/feet; main hand is applied only when empty; no offhand population here.

`addAdditionalSaveData(Lnet/minecraft/nbt/CompoundTag;)V`, PCs 0–88, calls host save, companion serialization, writes `SkinVariant`, `BiomeFolder`, inherited persistent-anger state, `OrderedToStay` and a non-null `ArchetypeProfile` id. `readAdditionalSaveData` with the same descriptor, PCs 0–147, restores companion/skin/anger/biome/stay state, resolves saved profile id within the role, applies/syncs it, and rebuilds both goal selectors. It does not call equipment population or restore profile XP/custom name in this local load method. Owner/contract expiration/death callbacks are detailed in [recruitment contract](../systems/recruitment-contract.md); the menu provider `HumanEntity$1` is covered by [confirmation protocol](../systems/recruit-confirmation-protocol.md).

## Casting and client presentation

`initiateCastSpell(Lio/redspace/ironsspellbooks/api/spells/AbstractSpell;I)V`, PCs 0–22, chooses `currentAnimFile` from the spell's cast-start animation through `ModUtils.resolveAnimFile`, retains the spell reference, then passes the **unchanged requested level** to the host method at PC 19. `castComplete()V`, PCs 0–53, optionally resolves the finish animation for a LONG spell whose finish holder is not pass-through, sets `animResetDelay=20`, then calls host completion. `tick()V`, PCs 0–40, calls host tick and companion contract tick, decrements the animation delay, and returns to host `animationInstantCast` when it reaches zero. Neither callback proves a successful hit, resource debit or once-only effect.

`HumanModel.getTextureResource(Lio/redspace/ironsspellbooks/entity/mobs/abstract_spell_casting_mob/AbstractSpellCastingMob;)Lnet/minecraft/resources/ResourceLocation;`, PCs 0–20, returns HumanEntity's texture selector or fallback. `getAnimationResource` with the same descriptor returns `currentAnimFile` or host instant-cast animation. HumanRenderer's constructor `(Lnet/minecraft/client/renderer/entity/EntityRendererProvider$Context;)V`, PCs 0–12, supplies HumanModel to the host renderer. Generic model geometry/animation are inherited from Iron's; no human-specific geometry is packaged.

Local texture payload is 21 PNG identities: `assets/acolyte/textures/entity/generic_skin/{desert,jungle,plains,savanna,snowy,swamp,taiga}/human{0,1,2}.png`. `HumanEntity.<clinit>()V`, PCs 0–9, fallback is `acolyte:textures/entity/generic_skin/plains/human0.png`. `getTextureLocation()Lnet/minecraft/resources/ResourceLocation;`, PCs 0–22, delegates custom skin/biome/index selection to ArchetypeUtils. Variants do not create additional entity IDs or spell loadouts.

## Shared utility contracts

`ModUtils.checkHumanSpawnRules(Lnet/minecraft/world/entity/EntityType;Lnet/minecraft/world/level/ServerLevelAccessor;Lnet/minecraft/world/entity/MobSpawnType;Lnet/minecraft/core/BlockPos;Lnet/minecraft/util/RandomSource;)Z`, PCs 0–111, rejects a disabled human-spawn gamerule when the accessor is ServerLevel, `NO_DEFAULT_MONSTERS` biomes, Peaceful, and failed vanilla `Mob.checkMobSpawnRules`. It finally requires **no HumanEntity in a block AABB inflated by 300 on each axis**; this is a box query, not a spherical 300-block combat radius. No local darkness test is made for humans.

`ModUtils.resolveAnimFile(Lio/redspace/ironsspellbooks/api/util/AnimationHolder;)Lnet/minecraft/resources/ResourceLocation;`, PCs 0–29, reads the player's optional animation, filters out namespace `irons_spellbooks` (`lambda$resolveAnimFile$0(Lnet/minecraft/resources/ResourceLocation;)Z`, PCs 0–17), maps accepted `namespace:path` to `namespace:animations/path.json` (`lambda$resolveAnimFile$1(Lnet/minecraft/resources/ResourceLocation;)Lnet/minecraft/resources/ResourceLocation;`, PCs 0–16; verbose BootstrapMethods concat recipe `animations/{path}.json`), and otherwise falls back to host instant-cast animation. Thus arbitrary host animation holders are not copied as local animation files. `resolveBiomeFolder(Lnet/minecraft/world/level/ServerLevelAccessor;Lnet/minecraft/core/BlockPos;)Ljava/lang/String;`, PCs 0–135, inspects biome **path** substrings in order: taiga, desert, jungle, savanna, snowy/frozen→snowy, swamp, badlands→desert, else plains; missing biome key also gives plains. This shared cosmetic helper is cross-owned with the archetype pipeline.

## Integration axes

| Axis | Exact local boundary / practical limit |
|---|---|
| Projection / delivery | Entity AI and host cast initiation are observable; no player spell projection API is supplied. Host spell delivery stays with Iron's. |
| Effects | Host spell effects and vanilla damage settlement are delegated; animation state is presentation, not successful effect settlement. |
| Mana / resources | No local mana price or debit in these cast overrides; host mob casting owns resource behavior. Recruitment has its separate emerald contract. |
| Cooldown / duration | The 20-tick animation reset is local presentation timing; goal delays are documented on role/goal cards. Generic host spell cooldown is delegated. |
| Damage / healing | Local friendly-fire rejection is explicit; accepted damage goes to `AbstractSpellCastingMob.hurt`. No independent healing formula. |
| Targeting / teams | Local alliance and target rules below precede host/vanilla behavior; these are integration-sensitive server decisions. |
| Rituals | N/A: no ritual identity, altar, ritual cost or ritual callback in this family. |
| Progression / perks | No verified Black Arcana or RPG Skill Tree callback. A read-only observer must distinguish cast request, animation and final host effect. |

Persistence, unload/reload, dedicated server/client class loading, same-owner multiplayer, protected regions and exactly-once host damage/cast observation remain physical QA cases; binary facts do not certify a mutation hook.
