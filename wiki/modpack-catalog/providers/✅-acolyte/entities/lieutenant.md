# Lieutenant — entity and animated combat contract (1.0.3)

Identity: `acolyte:lieutenant`; class `net.raptorzizi.acolyte.entity.mobs.lieutenant.LieutenantEntity`, extending Iron's `AbstractSpellCastingMob`, implementing Enemy and host IAnimatedAttacker. This card also owns `LieutenantAnimatedWarlockAttackGoal`, `LieutenantEntity$AttackType`, local look/move controls, model and renderer. It is one entity and **no new spell identity**.

## Evidence and status

Source: exact publisher `acolyte-1.0.3.jar`, CurseForge file `8098233`, 621,837 bytes; SHA-1 `ad0abc821f3f8a6573ac19a50970fc1bc46b4275`, SHA-256 `73fe745bbb0016fbc00af9ba14c0ecfe0a1d8a7d72a7892557739182b3486256`. Installed JAR equality is unproved. Method descriptors and PCs below identify the local `javap -p -c -s -constants` evidence described in [binary contracts](../BINARY-CONTRACTS-1.0.3.md); entry coverage is in the [artifact manifest](../ARTIFACT-CATALOG-MANIFEST-1.0.3.json). Publisher-only factual interoperability summary; no implementation or assets reproduced. Embedded MIT / publisher All Rights Reserved conflict remains recorded at the provider boundary.

`mutating_hook: NOT_VERIFIED`; `physical: NOT_TESTED`; certified perk boundaries: **0**. Documentation changes no runtime. Referenced spells remain Iron's-owned; **+0 Acolyte semantic spells**.

## Registration, attributes and equipment

`ModEntityRegistry.lambda$static$7()Lnet/minecraft/world/entity/EntityType;`, PCs 0–41, registers MONSTER, size 0.85×2.3, eye height 2.3 and client tracking range 64. `LieutenantEntity.<init>(Lnet/minecraft/world/entity/EntityType;Lnet/minecraft/world/level/Level;)V`, PCs 6–65, initializes an empty summoned-UUID list, `lieutenant_animations` controller with transition 0, empty animation queue, XP reward 25 and custom look/move control.

`prepareAttributes()Lnet/minecraft/world/entity/ai/attributes/AttributeSupplier$Builder;`, PCs 0–71, starts with monster attributes and sets ATTACK_DAMAGE=0, MAX_HEALTH=180, FOLLOW_RANGE=25, KNOCKBACK_RESISTANCE=0.8, ATTACK_KNOCKBACK=2, STEP_HEIGHT=1, ENTITY_INTERACTION_RANGE=3.5 and MOVEMENT_SPEED=0.19. `populateDefaultEquipmentSlots(Lnet/minecraft/util/RandomSource;Lnet/minecraft/world/DifficultyInstance;)V`, PCs 0–17, equips host KEEPER_FLAMBERGE in main hand; the zero base attack attribute is not final sword damage. No independently fixed final damage is supplied here.

`finalizeSpawn(Lnet/minecraft/world/level/ServerLevelAccessor;Lnet/minecraft/world/DifficultyInstance;Lnet/minecraft/world/entity/MobSpawnType;Lnet/minecraft/world/entity/SpawnGroupData;)Lnet/minecraft/world/entity/SpawnGroupData;`, PCs 0–10, populates equipment using host Utils.random and returns the supplied group data. Unlike the human/demon family finalizers, this override does **not** call host finalizeSpawn, roll an archetype or apply profile stats.

## AI, targeting and defenses

`registerGoals()V`, PCs 0–134: float priority 0; local animated-warlock attack priority 4 with constructor operands speed 1 and intervals 10/30; water-avoiding random stroll priority 4/speed 1; random look priority 6. Target selector: hurt-by priority 1, nearest player priority 2 with sight check, nearest Mob priority 3 with sight check and predicate excluding DemonEntity. `lambda$registerGoals$0(Lnet/minecraft/world/entity/LivingEntity;)Z`, PCs 0–12, only tests that exclusion; other alliance handling is separate. Follow range 25 and tracking range 64 have distinct purposes.

`isAlliedTo(Lnet/minecraft/world/entity/Entity;)Z`, PCs 0–40, accepts inherited allies, DemonEntity, LieutenantEntity and types tagged host `ModTags.INFERNAL_ALLIES`. `hurt(Lnet/minecraft/world/damagesource/DamageSource;F)Z`, PCs 0–65, rejects a causing entity of demon family or lieutenant. A direct entity which is any Projectile multiplies incoming damage by 0.75 before host hurt. During the first 10 entity ticks, IN_WALL damage also invokes host `Utils.doMobBreakSuffocatingBlocks`; the accepted damage then still delegates to the host. This is a real block-mutation boundary, without a local Black Arcana protection-policy veto.

`fireImmune()Z`, PCs 0–1, returns true. `isInvulnerableTo(Lnet/minecraft/world/damagesource/DamageSource;)Z`, PCs 0–23, accepts inherited invulnerability or damage tagged IS_FALL. These do not imply immunity to every host magic school.

`createBodyControl()Lnet/minecraft/world/entity/ai/control/BodyRotationControl;` returns vanilla BodyRotationControl (PCs 0–8). Local look `$1.rotateTowards(FFF)F`, PCs 0–10, scales the vanilla rotation bound by 2.5. Local movement `$2.rotlerp(FFF)F`, PCs 0–58, leaves rotation unchanged below squared horizontal wanted-distance 0.5; otherwise scales bound by 0.25. `createNavigation(Lnet/minecraft/world/level/Level;)Lnet/minecraft/world/entity/ai/navigation/PathNavigation;`, PCs 0–9, returns host NotIdioticNavigation.

## Attack-goal state and cast policy

`LieutenantAnimatedWarlockAttackGoal.<init>(Lnet/raptorzizi/acolyte/entity/mobs/lieutenant/LieutenantEntity;DII)V`, PCs 0–44, delegates mob/speed/intervals to host WarlockAttackGoal; initializes stomp/blood-step cooldowns 0, melee timer −1, chooses initial attack with distance operand 0 and sets wantsToMelee=true. `isActing()Z` and `canContinueToUse()Z`, PCs 0–19 each, accept inherited result **or meleeAnimTimer>0**. `stop()V`, PCs 0–14, calls host stop then timer=−1 and clears queued combo; it does not reset the two spell cooldown counters locally.

All next PCs are in `handleAttackLogic(D)V` unless stated. The incoming double is treated as squared distance, converted by sqrt for comparisons (0–10), while `meleeRange()F` is inherited. Do not substitute the attribute 3.5 for a proven host reach formula. `lieutenant.isMeleeing` is assigned from timer>0 before further state changes (12–28). Positive stomp/blood-step counters decrement once per **call of this method** (31–62), not by an independent always-running world timer.

At PCs 79–141, if timer<0, the mob is not casting, blood-step counter<=0, and distance>8, initiate host BLOOD_STEP_SPELL at **level 1**, set counter 180 and return. No local LOS test guards this branch. At PCs 640–736, when idle and distance is below meleeRange (or 3×meleeRange for next Lunge), inherited hasLineOfSight is true and decrementing meleeAttackDelay reaches exactly zero, available stomp counter plus not-casting requests host STOMP_SPELL at **level 1**, sets counter 120 and resets melee interval. Otherwise start the melee action (739–743). Far/no-LOS expired melee delays reset through the host; distance may reroll the next attack (746–787). These are **Acolyte AI counters**, separate from any spell-owned cooldown or mana policy. Requested spells remain Iron's semantic owner.

## Melee actions, hit settlement and combos

`doMeleeAction()V`, PCs 0–78, makes next attack current, swings main hand, loads `AttackAnimationData.lengthInTicks` into the melee timer, clears lunge flags, and sends host `SyncAnimationPacket(String,Entity)` to players tracking the lieutenant. The string is **currentAttack.toString()** (the enum name), not a newly owned spell ID. Local `playAnimation(Ljava/lang/String;)V`, PCs 0–39, resolves that string using AttackType.valueOf, takes its data.animationId, queues RawAnimation.thenPlay, and logs caught exceptions. This maps the enum packet identity to the data animation identity shown below. Its controller predicate resets/applies/clears the queue then returns CONTINUE. `isAnimating()Z`, PCs 0–25, combines controller state and host state.

During timer>0, PCs 142–213 force facing before lunge, decrement timer, and test host AttackAnimationData.isHitFrame on timer−4 first: a true timer−4 test skips the later timer hit test for **both** attack kinds; only non-Lunge also plays swing sound. Only a false timer−4 result reaches the direct timer hit-frame test and then selects normal or lunge logic. These are countdown inputs to the host frame API, not a claim that listed frame markers directly equal accepted hits.

For a non-lunge hit frame (226–385), push toward target by normalized target-minus-mob vector×0.550000011920929. At distance<=inherited meleeRange and host `Utils.hasLineOfSight(level,mob,target,true)`, call `doHurtTarget(Entity)Z`, then reset target.invulnerableTime to **0 even when the returned hit flag is false**. A successful hit plays impact sound; if attack data isSingleHit, queue a `randomizeNextAttack(0)` combo when randomFloat<0.75 **or target is blocking**. This goal supplies no independent final sword damage multiplier; weapon, attributes, host and damage events settle it.

For Lunge (388–563), the first eligible hit frame pushes once by normalized target-minus-mob multiplied componentwise by (2.4,0.5,2.4) plus (0,0.15,0), saves old position, stops navigation and plays swing. Until hasHitLunge, distance<=0.45×meleeRange calls doHurtTarget, plays impact on success, then knocks target back with strength 1 using oldLungePos−targetPosition and sets hasHitLunge=true **regardless of returned hit success**. This branch has no local LOS check. The flag limits the local lunge hit attempt, not all external damage events.

When animation ends, a queued combo with non-null, non-dead target immediately runs doMeleeAction (566–607). Otherwise timer==0 rerolls next attack, calls host resetMeleeAttackInterval with the incoming squared-distance argument, then timer=−1 (610–634). `randomizeNextAttack(F)Lnet/raptorzizi/acolyte/entity/mobs/lieutenant/LieutenantEntity$AttackType;`, PCs 0–80, excludes the last enum entry Lunge when distance<1.5×meleeRange. At larger distance a random<0.25 and distance>2.5×meleeRange selects Lunge outright; otherwise uniformly choose among all six. Thus beyond 2.5×range the overall lunge probability is 0.25+0.75/6=0.375; between 1.5× and 2.5× it is 1/6. The constructor/queued-combo call uses distance 0; under positive inherited melee range the first branch excludes Lunge.

`doMovement(D)V`, PCs 0–60, stops navigation for dead/dying target; above meleeRange² asks navigation.moveTo(target,speedModifier×1.2999999523162842). At/inside range it performs no local stop call in that branch. `forceFaceTarget()V`, PCs 0–83, returns after hasLunged; otherwise synchronizes body/head/entity yaw from target horizontal direction.

## Attack-data identities

`LieutenantEntity$AttackType.<clinit>()V`, PCs 0–205, constructs the following host `AttackAnimationData(ILjava/lang/String;[I)V` inputs; enum constructor descriptor including synthetic name/ordinal is `(Ljava/lang/String;IILjava/lang/String;[I)V`. Data interpretation is delegated to Iron's.

| Enum / packet string | Data animation string | Length input | Frame-marker input | Static PC |
|---|---|---:|---|---|
| Double_Slash | sword_double_slash | 43 | 13,29 | 0–27 |
| Single_Upward | sword_single_upward | 26 | 13 | 30–52 |
| Single_Horizontal | sword_single_horizontal | 28 | 12 | 55–77 |
| Single_Horizontal_Fast | sword_single_horizontal_fast | 24 | 12 | 80–102 |
| Single_Stab | sword_stab | 21 | 11 | 105–127 |
| Lunge | sword_lunge | 76 | 56,57,58,59,60,61,62,63,64 | 130–196 |

No assets or animation implementation are reproduced; packet delivery and visual compatibility still need physical testing.

## Summoning and persistence

`customServerAiStep()V`, PCs 0–86, first calls host AI. Only while aggressive, at **tickCount%240==0**, in ServerLevel, it counts saved UUIDs resolving in that same ServerLevel to an alive DemonWarriorEntity. If fewer than **2**, spawn one warrior with random left/right boolean. It does not prune dead/missing UUIDs, fill both slots in one invocation, scan other dimensions, or enforce the cap inside the public spawning method.

`spawnDemonWarrior(Z)V`, PCs 0–179, requires ServerLevel, directly constructs registered DemonWarriorEntity, chooses ±90° from boolean, computes a sideways offset from forward vector×(3,0,3), raycasts from eyes with Fluid.NONE, resolves ground within argument 4, moves spawn point y+0.1, copies yaw, calls warrior finalizeSpawn with MOB_SUMMONED, adds entity, then appends its UUID **without testing addFreshEntity's boolean**. Normal demon profile/equipment finalization therefore applies to these summons. No explicit copied target/owner assignment is in this method.

`addAdditionalSaveData(Lnet/minecraft/nbt/CompoundTag;)V`, PCs 0–65, calls host and writes `summonedDemons` as a list of NbtUtils.createUUID int arrays. `readAdditionalSaveData` with the same descriptor, PCs 0–58, calls host, clears list and reloads tag list with element type 11. Local spell counters, animation timer, attack selection and lunge flags are goal state with no local NBT writer. `die(Lnet/minecraft/world/damagesource/DamageSource;)V`, PCs 0–46, calls host then, on ServerLevel, visits saved UUIDs and clears the list; `lambda$die$2(Lnet/minecraft/server/level/ServerLevel;Ljava/util/UUID;)V`, PCs 0–22, calls kill only when the UUID currently resolves to a DemonWarriorEntity in that level. Unloaded/cross-dimension entities are not resolved by this local loop.

## Client and sounds

LieutenantModel has no local animation-resource override. `getTextureResource` and `getModelResource`, both `(Lio/redspace/ironsspellbooks/entity/mobs/abstract_spell_casting_mob/AbstractSpellCastingMob;)Lnet/minecraft/resources/ResourceLocation;`, PCs 0–3 each, return constants set in `<clinit>()V`, PCs 0–20: `acolyte:textures/entity/lieutenant.png` and `acolyte:geo/entity/lieutenant.geo.json`. These two payloads are recorded by path only.

LieutenantRenderer constructor `(Lnet/minecraft/client/renderer/entity/EntityRendererProvider$Context;)V`, PCs 0–18, uses LieutenantModel and shadow radius 0.65. `preRender(Lcom/mojang/blaze3d/vertex/PoseStack;Lio/redspace/ironsspellbooks/entity/mobs/abstract_spell_casting_mob/AbstractSpellCastingMob;Lsoftware/bernie/geckolib/cache/object/BakedGeoModel;Lnet/minecraft/client/renderer/MultiBufferSource;Lcom/mojang/blaze3d/vertex/VertexConsumer;ZFIII)V`, PCs 0–31, scales pose 1.3 on all axes before host rendering; this visual scale is distinct from registered collision dimensions. `getRenderType(Lio/redspace/ironsspellbooks/entity/mobs/abstract_spell_casting_mob/AbstractSpellCastingMob;Lnet/minecraft/resources/ResourceLocation;Lnet/minecraft/client/renderer/MultiBufferSource;F)Lnet/minecraft/client/renderer/RenderType;`, PCs 0–4, returns entityTranslucent. `getPackedOverlay(Lio/redspace/ironsspellbooks/entity/mobs/abstract_spell_casting_mob/AbstractSpellCastingMob;FF)I`, PCs 0–22, packs OverlayTexture.u(first float) with v(deathTime>0); it does not use hurtTime in its local vertical-overlay test.

Ambient/hurt/death use host KEEPER_IDLE / KEEPER_HURT / KEEPER_DEATH. `playAmbientSound()V`, PCs 0–23, uses volume 1 and pitch random integer 5–10×0.1. `playStepSound(Lnet/minecraft/core/BlockPos;Lnet/minecraft/world/level/block/state/BlockState;)V`, PCs 0–17, uses KEEPER_STEP volume 0.25/pitch 1; `nextStep()F`, PCs 0–8, is moveDist+0.8. Goal `playSwingSound()V` and `playImpactSound()V`, PCs 0–36 each, use KEEPER_SWING / KEEPER_SWORD_IMPACT, volume 1, pitch integer 9–13×0.1.

## Acquisition

`data/acolyte/loot_table/entities/lieutenant.json`: first pool has one roll, zero bonus rolls, host arcane essence uniform set-count input 0–8 plus vanilla looting-count-increase input 0–1. Second pool has one roll, zero bonus rolls and alternative entries: host scroll randomize-spell quality 0.25–0.85, conditioned on killed-by-player plus looting-aware random chance (unenchanted 0.25; enchanted linear base 0.1/+0.05 above level one), or `acolyte:dark_horn` set-count uniform input 1–1.2. These are alternatives in one pool, not guaranteed independent drops. Third pool uses roll-range input 1–3 and delegates to host loot table `irons_spellbooks:magic_items/good_ink`. Vanilla resolves fractional number-provider inputs and conditions; host resolves scroll spell identity and ink output. No new Acolyte spell is minted by these rewards.

## Integration axes and physical QA

| Axis | Exact boundary and limit |
|---|---|
| Projection / delivery | BLOOD_STEP and STOMP requested at level 1 through IMagicEntity; host spell delivery remains Iron's. Summon projection is direct entity creation/raycast/ground placement. |
| Effects / blocks | Local push/knockback, invulnerability-time reset, summon/death cleanup and early suffocation block break are explicit; host magic effects delegated. No proved WorldEffectPolicy or claim veto. |
| Mana / costs | No local mana debit or currency consumption in the attack/summon methods; host casting owns its resource semantics. |
| Cooldown / duration | 120/180 per-attack-logic-call counters; 240 entity-tick modulo summon checks; host melee interval reset and spell cooldown/cast duration are separate. |
| Damage / healing | Incoming projectile factor 0.75 and fall/fire defenses local; melee calls host/vanilla doHurtTarget with equipped sword. No independent healing formula. |
| Targeting / teams | Family/tag alliance, nearest-target selection, conditional LOS and inherited reach must all be preserved. Lunge lacks local LOS gating. |
| Rituals | N/A: minion summoning is an entity-AI method, with no ritual registry, altar or ritual resource contract. |
| Progression / perks | No verified Black Arcana/RPG Skill Tree callback. Do not treat packet, animation, cast request or target invulnerability reset as a successful damage settlement. |
| Persistence / network | Saved summon UUIDs, host animation packet to tracking players, inherited host state; cooldowns and attack state are not locally serialized. |

Pending physical cases: exact installed host/JAR, held-sword final damage, enum packet→visual animation resolution, melee countdown/hit-frame interpretation, repeated invulnerability resets, lunge through obstructed LOS, host cast acceptance versus counters, two-summon cap under unload/restart, rejected entity addition, cross-dimension death cleanup, protection/block mutation and multiplayer/Epic Fight coexistence. **No runtime hook or certification is promoted.**
