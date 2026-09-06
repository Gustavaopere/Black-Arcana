package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.api.ArcanaCastContext;
import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaCost;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaServices;
import dev.gustavopere.blackarcana.api.ArcanaSpellDefinition;
import dev.gustavopere.blackarcana.content.cinder.BlackPyreDomainSpecifications;
import dev.gustavopere.blackarcana.content.cinder.BlackPyreSafetyCeilings;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntimeManager;
import dev.gustavopere.blackarcana.core.world.ChunkRef;
import dev.gustavopere.blackarcana.core.world.EntityInteractionType;
import dev.gustavopere.blackarcana.core.world.TemporaryMutationKey;
import dev.gustavopere.blackarcana.core.world.WorldEffectMode;
import dev.gustavopere.blackarcana.core.world.WorldEffectPolicyConfig;
import dev.gustavopere.blackarcana.core.world.WorldMutationClass;
import dev.gustavopere.blackarcana.core.world.WorldMutationType;
import net.minecraft.core.BlockPos;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.server.MinecraftServer;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.atomic.AtomicInteger;

@GameTestHolder(BlackArcanaMod.MOD_ID)
@PrefixGameTestTemplate(false)
public final class BlackPyreAuthorityHardeningGameTests {
    private BlackPyreAuthorityHardeningGameTests() { }

    @GameTest(template = "foundation_empty", timeoutTicks = 100)
    public static void protectedEntityTargetIsNeverDamaged(GameTestHelper helper) {
        MinecraftServer server = helper.getLevel().getServer();
        ArcanaServerRuntime runtime = requireRuntime(server);
        var caster = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(1, 2, 1));
        var target = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(3, 2, 1));
        float before = target.getHealth();
        String targetId = target.getUUID().toString();
        String adapterId = "gt_black_pyre_entity_" + UUID.randomUUID().toString().substring(0, 8);
        runtime.protectionAdapters().register(adapterId, query ->
            query.interactionType() == EntityInteractionType.DAMAGE && query.targetId().equals(targetId)
                ? ArcanaDecision.deny("entity_protected_test", "GameTest protected Black Pyre entity")
                : ArcanaDecision.allow());

        var result = MinecraftBlackPyreRuntime.igniteDefault(
            server,
            caster.getUUID(),
            List.of(target.getUUID()),
            4.0D,
            false,
            caster.blockPosition().getX(),
            caster.blockPosition().getY(),
            caster.blockPosition().getZ());

        helper.assertTrue(result.damagedTargets() == 0, "protected target must not settle Black Pyre damage");
        helper.assertTrue(target.getHealth() == before, "protected target health must remain unchanged");
        helper.assertTrue(!result.decision().allowed(), "entity-only cast with no authorized target must fail closed");
        helper.succeed();
    }

    @GameTest(template = "foundation_empty", timeoutTicks = 100)
    public static void permanentRequestIsDeniedBelowFullMode(GameTestHelper helper) {
        MinecraftServer server = helper.getLevel().getServer();
        ArcanaServerRuntime runtime = requireRuntime(server);
        WorldEffectPolicyConfig previous = runtime.worldEffectPolicy().config();
        var caster = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(1, 2, 1));
        BlockPos pos = caster.blockPosition().offset(2, -1, 0);
        helper.getLevel().setBlock(pos, Blocks.STONE.defaultBlockState(), Block.UPDATE_ALL);
        ArcanaCastId castId = ArcanaCastId.random();
        try {
            runtime.configureWorldEffects(new WorldEffectPolicyConfig(WorldEffectMode.LIMITED, 4096, true, Map.of()));
            ArcanaDecision decision = runtime.permanentBlockGateway().orElseThrow().replace(
                worldRequest(caster.getUUID(), castId, helper.getLevel().getGameTime(), pos),
                ArcanaServices.TargetResolution.resolved(blockTargetId(helper, pos)),
                chunkRef(helper, pos),
                mutationKey(helper, pos),
                MinecraftTemporaryBlockBackend.encodeState(Blocks.BLACKSTONE.defaultBlockState()),
                WorldMutationType.FIRE_SPREAD,
                WorldMutationClass.PERMANENT);

            helper.assertTrue(!decision.allowed(), "PERMANENT Black Pyre terrain must be denied below FULL mode");
            helper.assertTrue("world_effect_mode".equals(decision.code()), "mode denial must retain the canonical machine-readable code");
            helper.assertTrue(runtime.worldEffectBudgets().usedUnits(castId) == 0, "mode denial must not burn world budget");
            helper.assertTrue(helper.getLevel().getBlockState(pos).is(Blocks.STONE), "denied permanent request must not mutate the block");
        } finally {
            runtime.configureWorldEffects(previous);
        }
        helper.succeed();
    }

    @GameTest(template = "foundation_empty", timeoutTicks = 100)
    public static void stalePermanentSettlementCannotOverwriteInterveningEdit(GameTestHelper helper) {
        MinecraftServer server = helper.getLevel().getServer();
        ArcanaServerRuntime runtime = requireRuntime(server);
        WorldEffectPolicyConfig previous = runtime.worldEffectPolicy().config();
        var caster = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(1, 2, 1));
        BlockPos pos = caster.blockPosition().offset(2, -1, 1);
        helper.getLevel().setBlock(pos, Blocks.STONE.defaultBlockState(), Block.UPDATE_ALL);
        ArcanaCastId castId = ArcanaCastId.random();
        TemporaryMutationKey key = mutationKey(helper, pos);
        AtomicInteger checks = new AtomicInteger();
        String adapterId = "gt_black_pyre_stale_" + UUID.randomUUID().toString().substring(0, 8);
        runtime.worldMutationProtectionAdapters().register(adapterId, query -> {
            if (query.castId().equals(castId) && query.key().equals(key) && checks.incrementAndGet() == 2) {
                helper.getLevel().setBlock(pos, Blocks.DIAMOND_BLOCK.defaultBlockState(), Block.UPDATE_ALL);
            }
            return ArcanaDecision.allow();
        });

        try {
            runtime.configureWorldEffects(new WorldEffectPolicyConfig(WorldEffectMode.FULL, 4096, true, Map.of()));
            ArcanaDecision decision = runtime.permanentBlockGateway().orElseThrow().replace(
                worldRequest(caster.getUUID(), castId, helper.getLevel().getGameTime(), pos),
                ArcanaServices.TargetResolution.resolved(blockTargetId(helper, pos)),
                chunkRef(helper, pos),
                key,
                MinecraftTemporaryBlockBackend.encodeState(Blocks.BLACKSTONE.defaultBlockState()),
                WorldMutationType.FIRE_SPREAD,
                WorldMutationClass.PERMANENT);

            helper.assertTrue(!decision.allowed(), "stale permanent Black Pyre CAS must fail closed");
            helper.assertTrue("world_state_changed".equals(decision.code()), "stale settlement must expose world_state_changed");
            helper.assertTrue(checks.get() >= 2, "protection must be rechecked immediately before permanent settlement");
            helper.assertTrue(runtime.worldEffectBudgets().usedUnits(castId) == 1, "one admitted stale CAS attempt consumes world budget exactly once");
            helper.assertTrue(helper.getLevel().getBlockState(pos).is(Blocks.DIAMOND_BLOCK), "intervening world/player edit must survive stale CAS rejection");
        } finally {
            runtime.configureWorldEffects(previous);
        }
        helper.succeed();
    }

    @GameTest(template = "foundation_empty", timeoutTicks = 100)
    public static void runtimeFrontierStressNeverExceedsHardConcurrentCeiling(GameTestHelper helper) {
        MinecraftServer server = helper.getLevel().getServer();
        ArcanaServerRuntime runtime = requireRuntime(server);
        WorldEffectPolicyConfig previous = runtime.worldEffectPolicy().config();
        var caster = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(1, 2, 1));
        List<ArcanaCastId> admitted = new ArrayList<>();
        try {
            runtime.configureWorldEffects(new WorldEffectPolicyConfig(WorldEffectMode.TEMPORARY, 4096, true, Map.of()));
            for (int i = 0; i < BlackPyreSafetyCeilings.MAX_CONCURRENT_FRONTIERS + 1; i++) {
                BlockPos seed = caster.blockPosition().offset(1 + i, -1, 3);
                helper.getLevel().setBlock(seed, Blocks.STONE.defaultBlockState(), Block.UPDATE_ALL);
                helper.getLevel().setBlock(seed.north(), Blocks.STONE.defaultBlockState(), Block.UPDATE_ALL);
                var result = MinecraftBlackPyreRuntime.igniteDefault(
                    server,
                    caster.getUUID(),
                    List.of(),
                    1.0D,
                    true,
                    seed.getX(),
                    seed.getY(),
                    seed.getZ());
                if (result.terrainApplied()) admitted.add(result.castId());
                helper.assertTrue(
                    MinecraftBlackPyreRuntime.activeFrontiers(server) <= BlackPyreSafetyCeilings.MAX_CONCURRENT_FRONTIERS,
                    "runtime must never exceed the hard concurrent frontier ceiling");
            }
            long ownActive = admitted.stream().filter(id -> MinecraftBlackPyreRuntime.isFrontierActive(server, id)).count();
            helper.assertTrue(ownActive <= BlackPyreSafetyCeilings.MAX_CONCURRENT_FRONTIERS,
                "stress cast set must remain bounded by the same hard frontier ceiling");
        } finally {
            runtime.configureWorldEffects(previous);
        }
        helper.succeed();
    }

    private static ArcanaServerRuntime requireRuntime(MinecraftServer server) {
        return ArcanaServerRuntimeManager.get(server)
            .orElseThrow(() -> new IllegalStateException("Black Arcana runtime unavailable"));
    }

    private static ArcanaCastRequest worldRequest(
        UUID casterId,
        ArcanaCastId castId,
        long serverTick,
        BlockPos pos
    ) {
        return new ArcanaCastRequest(
            castId,
            new ArcanaSpellDefinition(
                BlackPyreDomainSpecifications.BLACK_PYRE,
                "spell.black_arcana.black_pyre",
                "black_arcana:textures/spell/black_pyre.png",
                ArcanaCost.none(),
                true),
            new ArcanaCastContext(casterId, serverTick, "minecraft:overworld"),
            0,
            "block:" + pos.getX() + "," + pos.getY() + "," + pos.getZ());
    }

    private static String blockTargetId(GameTestHelper helper, BlockPos pos) {
        return helper.getLevel().dimension().location() + ":" + pos.getX() + "," + pos.getY() + "," + pos.getZ();
    }

    private static ChunkRef chunkRef(GameTestHelper helper, BlockPos pos) {
        return new ChunkRef(
            helper.getLevel().dimension().location().toString(),
            pos.getX() >> 4,
            pos.getZ() >> 4);
    }

    private static TemporaryMutationKey mutationKey(GameTestHelper helper, BlockPos pos) {
        return new TemporaryMutationKey(helper.getLevel().dimension().location().toString(), pos.asLong());
    }
}
