# Galena Gauntlet — targeting and mining engine (1.0.10 / NeoForge 21.1.248)

## Evidence

Publisher 1.0.10 SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c32e9f2e95bffae0e7c`, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, 75,279,314 bytes. Minecraft 1.21.1 / Java 21. Official NeoForge 21.1.248 installer `68eeab77059ba53df1812f1afa5bf530ab2566a3cdcd5f924aa6e71be42e410c`, server overlay `1808fab692dc44b2d474295d1cdd9f1fe8a7dceab4f594210873646fafdf1359`, SRG `26ca9c40d7e1681190b428583c38816852218e78df3f8bdb60a59a78503aec71`, universal `90a56f70425711b4e1a4b94ff0c2904ae9f6d74ca6478b3b2152ac794a07b8e5`.

[Discovery run 45461280041](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45461280041), job 138684193655, artifact 14951699632. Report **687,147 bytes**, SHA-256 `5ecefad9c5a2994c6977a11d4bf11335d09993b299b8906c12356e32c726e3dc`, 18 owners. [Probe](../../../../docs/qa/alexscaves_1010_galena_targeting_mining_engine_probe.py), [workflow](../../../../.github/workflows/alexscaves-1010-galena-targeting-mining-engine.yml). Distributed classfile observation, not transformed runtime or physical QA; final-head replay required.

## Targeting

Reuses [publisher player targeting](EXACT-GALENA-GAUNTLET-PLAYER-TARGETING-1.0.10.md): 30+5×FIELD_EXTENSION requested distance, distinct from 64 AABB lookup. Entity.canBeHitByProjectile Code `bae99d779a063f502285e64e4366db0afe69c601b63b2a43529e1a3d3424bfa0` requires isAlive @1 and isPickable @8. Both virtual calls; no direct team/PvP check in this predicate.

ProjectileUtil class `47c5e685f77f34709e3c8bc883962d326185b6dac67578572a86c268a3801bda`:

- getHitResultOnViewVector(Entity,Predicate,D) Code `adef922982a467b6ae5c562190f7d226473e57e493be9d3b00ed19b87234728f`: view vector with 0F @2, scale by distance @6, level @12, eye position @18, 0F @31 and COLLIDER @32, getHitResult @35.
- getHitResult Code `2cc7c9aec892ea906224389223919cddde437560032779d2cdc64a7224bff43b`: start+vector, block clip (COLLIDER/NONE for above caller), non-MISS replaces endpoint @43, shooter AABB expandTowards(vector) @59, inflate(1D) @63, getEntityHitResult @69; non-null entity result takes priority.
- Level/Entity/Vec3/Vec3/AABB/Predicate/F overload Code `8736ca0f2a85862907755435928f16926b060877c495345975255d1a6143d30b`: Level.getEntities @14, candidate box inflate supplied float @54, clip segment @63, distance squared @85, strict nearest comparison @95, EntityHitResult @124. The view-vector caller supplies 0F, not the default 0.3F of the alternative overload. The different overload with Entity and double threshold has pick radius/root vehicle logic; do not transpose those gates to this path.

Neither requested ray length nor broad-phase box establishes damage range or permission. Weapon contact and cooldown remain native predicates.

## Mining and settlement

Reuses [native mining order and progress](EXACT-GALENA-GAUNTLET-MINING-WORLD-EFFECT-1.0.10.md): S>1, local progress increments (S/H)/(Ferrous Haste?8:10), P>=1 and server-side before destruction. No explicit local positive-hardness guard.

EventHooks.getBreakSpeed Code `c420275d6286557b9fc4de6bb3bd2d82c90e869c3f4e37a66485c3b1fb9385b3` posts event @18; canceled gives -1F @32, otherwise getNewSpeed @39. Native S>1 gate rejects -1. Event speed is not authorization for destruction. onPlayerDestroyItem Code `2ec07159eee598bdf5d7a7fd1bd98511d52fae9b684b5e47436954f1ea59d63d` posts @13 without own item-break guard.

ItemStack.getDestroySpeed delegates Item; base Item Code `a1a5ed76990431d7b4d7ddd98a5e35884f606b0efb29a2b57448b0029ad64534` uses TOOL.getMiningSpeed or 1F. ItemStack.mineBlock Code `d340f229881d8992d8ffaf32a7cf7ce561d3c83b0c42cb805c357237e831b3c5` calls Item.mineBlock @14 and on true awards ITEM_USED @30. Base Item.mineBlock Code `75b6070bd61a640a2b4d74755c1307cb5c2b1144f21ac4bbacae5fa01a34a394` returns false without TOOL; otherwise nonclient, nonzero block destroy speed and damagePerBlock>0 gate hurtAndBreak MAINHAND @57; returns true @60 even when no debit. Subclass overrides and effective components can differ. Native weapon requests damageItem(1) before mineBlock; no fixed combined durability cost.

Level.destroyBlock(BlockPos,Z,Entity,I) Code `836ad2882a9182e07105ee97351b93d1eb3ef6578e4171ad3d5115481d77a887`: state @2, air false, fluid state @19; level event @45 on applicable branch; drops flag can call Block.dropResources @81 with EMPTY stack before setBlock @94 (legacy fluid state, flags 3). Game event only if replacement reports true. No direct player claim check or BreakEvent identified in this selected body. Two-argument inherited overload forwarding still requires targeted proof.

Block.playerDestroy Code `797663dff5d9f03011a740782aedee5331e3f6c5a643a475cc275a66f2d5ddcb`: BLOCK_MINED stat @8, exhaustion 0.005F @15, dropResources @27, no local branch. Six-argument dropResources Code `0da85ad4d076651361b5b95492b5ff5ca5152924dfa3c7c3ea24b4bacad959c1`: server gate, beginCapturingDrops @7, getDrops @21, iteration @31, stopCapturingDrops @36, CommonHooks.handleBlockDrops @54. Its actual listener/settlement body not covered here. Block.popExperience Code `a0416aa8c0cf244b076b0c67711a0b6e4863e0f05d2063fb961597c93367584d` requires RULE_DOBLOCKDROPS and not restoringBlockSnapshots, then ExperienceOrb.award @26. IBlockStateExtension.getExpDrop delegates virtual Block.getExpDrop; IBlockExtension default returns 0; actual block overrides and loot tables are not universal constants.

Distinct player ingress: ServerPlayerGameMode.destroyBlock Code `6be0b6e7b1c76e7efc137cc22527de8814781acdfacfc264bf793bf40550d040` calls fireBlockBreak @23; canceled event @28/31 returns false; GameMaster restrictions, blockActionRestricted @96, playerWillDestroy @116, creative route and noncreative harvest eligibility @166, mineBlock @184, removeBlock @193, playerDestroy @225 guarded by success/harvest. This does not establish that the Gauntlet uses that ingress.

Native Gauntlet calls destroyBlock and then unguarded awardStat on Shulker route or playerDestroy on other route; only XP branch separately checks destruction success. These findings identify causal ordering, **not actual bypass, duplicated drops, item loss, accepted mining or a safe perk hook**.

## Limits

Inherited two-argument destroyBlock dispatch, downstream handleBlockDrops, actual block/tool overrides, effective tags, claim listeners, transformed runtime and QA remain open. D006 server authority, D007 world policy. `static_contract=NOT_CERTIFIED`, `NO_MUTATION`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, provider OPEN; no root or ledger/index change.
