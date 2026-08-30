package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.content.space.LiminalSafetyCeilings;
import net.minecraft.core.BlockPos;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.server.MinecraftServer;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.phys.Vec3;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

@GameTestHolder(BlackArcanaMod.MOD_ID)
@PrefixGameTestTemplate(false)
public final class VeilstepReflexGameTests {
    private static final String RUNTIME =
        "dev.gustavopere.blackarcana.integration.neoforge.MinecraftVeilstepReflexRuntime";

    private VeilstepReflexGameTests() { }

    @SuppressWarnings("removal")
    @GameTest(template = "foundation_empty", timeoutTicks = 80)
    public static void firstSafeCandidateConsumesOneChargeAndCooldownStopsRetriggerLoop(GameTestHelper helper) throws Exception {
        var caster = helper.makeMockServerPlayerInLevel();
        var level = helper.getLevel();
        MinecraftServer server = level.getServer();
        long now = server.getTickCount();

        Vec3 blocked = new Vec3(caster.getX() + 2.5D, caster.getY(), caster.getZ() + 0.5D);
        Vec3 safe = new Vec3(caster.getX() + 4.5D, caster.getY(), caster.getZ() + 0.5D);
        BlockPos blockedPos = BlockPos.containing(blocked);
        BlockPos safePos = BlockPos.containing(safe);
        level.setBlockAndUpdate(blockedPos, Blocks.STONE.defaultBlockState());
        level.setBlockAndUpdate(blockedPos.above(), Blocks.AIR.defaultBlockState());
        level.setBlockAndUpdate(safePos, Blocks.AIR.defaultBlockState());
        level.setBlockAndUpdate(safePos.above(), Blocks.AIR.defaultBlockState());

        ArcanaDecision charged = setCharges(server, caster.getUUID(), 2, 2);
        helper.assertTrue(charged.allowed(), "host-granted bounded Veilstep charges must be accepted");
        double beforeX = caster.getX();

        Object triggered = trigger(
            server,
            caster.getUUID(),
            List.of(blocked, safe),
            now,
            20L,
            false);
        helper.assertTrue(decision(triggered).allowed(), "eligible threat with one safe candidate must trigger Veilstep");
        helper.assertTrue(teleported(triggered), "successful Veilstep must settle a teleport");
        helper.assertTrue(remainingCharges(triggered) == 1 && charges(server, caster.getUUID()) == 1,
            "successful Veilstep must consume exactly one host-granted charge");
        helper.assertTrue(caster.getX() > beforeX + 3.0D,
            "Veilstep must skip the blocked candidate and select the first safe candidate");

        Object loop = trigger(
            server,
            caster.getUUID(),
            List.of(safe),
            now + 1L,
            20L,
            false);
        helper.assertTrue(!decision(loop).allowed() && "veilstep_cooldown".equals(decision(loop).code()),
            "internal cooldown must stop repeated threat-trigger loops");
        helper.assertTrue(charges(server, caster.getUUID()) == 1,
            "cooldown denial must not consume another charge");
        helper.succeed();
    }

    @SuppressWarnings("removal")
    @GameTest(template = "foundation_empty", timeoutTicks = 80)
    public static void protectedThreatAndFailedBoundedSearchConsumeNothing(GameTestHelper helper) throws Exception {
        var caster = helper.makeMockServerPlayerInLevel();
        var level = helper.getLevel();
        MinecraftServer server = level.getServer();
        long now = server.getTickCount();

        Vec3 safe = new Vec3(caster.getX() + 3.5D, caster.getY(), caster.getZ() + 0.5D);
        BlockPos safePos = BlockPos.containing(safe);
        level.setBlockAndUpdate(safePos, Blocks.AIR.defaultBlockState());
        level.setBlockAndUpdate(safePos.above(), Blocks.AIR.defaultBlockState());
        helper.assertTrue(setCharges(server, caster.getUUID(), 1, 1).allowed(),
            "protected-threat fixture must begin with one charge");
        double beforeX = caster.getX();
        double beforeY = caster.getY();
        double beforeZ = caster.getZ();

        Object protectedThreat = trigger(
            server,
            caster.getUUID(),
            List.of(safe),
            now,
            20L,
            true);
        helper.assertTrue(!decision(protectedThreat).allowed()
                && "veilstep_protected_threat".equals(decision(protectedThreat).code()),
            "damage classified by the host as protected/unavoidable must never trigger Veilstep");
        helper.assertTrue(charges(server, caster.getUUID()) == 1,
            "protected threat denial must not consume charge");
        helper.assertTrue(unchanged(caster, beforeX, beforeY, beforeZ),
            "protected threat denial must not move caster");

        Vec3 blocked = new Vec3(caster.getX() + 2.5D, caster.getY(), caster.getZ() + 0.5D);
        BlockPos blockedPos = BlockPos.containing(blocked);
        level.setBlockAndUpdate(blockedPos, Blocks.STONE.defaultBlockState());
        level.setBlockAndUpdate(blockedPos.above(), Blocks.AIR.defaultBlockState());
        Object noSafe = trigger(
            server,
            caster.getUUID(),
            List.of(blocked),
            now + 1L,
            20L,
            false);
        helper.assertTrue(!decision(noSafe).allowed()
                && "veilstep_no_safe_destination".equals(decision(noSafe).code()),
            "failed safe-position search must fail closed");
        helper.assertTrue(charges(server, caster.getUUID()) == 1,
            "failed safe-position search must not consume charge");
        helper.assertTrue(unchanged(caster, beforeX, beforeY, beforeZ),
            "failed safe-position search must leave caster unchanged");
        helper.succeed();
    }

    @SuppressWarnings("removal")
    @GameTest(template = "foundation_empty", timeoutTicks = 80)
    public static void candidateAndChargeBoundsFailClosedBeforeMutation(GameTestHelper helper) throws Exception {
        var caster = helper.makeMockServerPlayerInLevel();
        MinecraftServer server = helper.getLevel().getServer();
        long now = server.getTickCount();

        helper.assertTrue(setCharges(server, caster.getUUID(), 0, 1).allowed(),
            "zero available charges within a positive host cap is a valid armed state");
        Object emptyCharge = trigger(
            server,
            caster.getUUID(),
            List.of(new Vec3(caster.getX() + 1.0D, caster.getY(), caster.getZ())),
            now,
            20L,
            false);
        helper.assertTrue(!decision(emptyCharge).allowed() && "veilstep_no_charge".equals(decision(emptyCharge).code()),
            "Veilstep without an available charge must fail closed");

        helper.assertTrue(setCharges(server, caster.getUUID(), 1, 1).allowed(),
            "candidate-cap fixture must restore one charge");
        List<Vec3> tooMany = new ArrayList<>();
        for (int i = 0; i <= LiminalSafetyCeilings.MAX_SAFE_SEARCH_CANDIDATES; i++) {
            tooMany.add(new Vec3(caster.getX(), caster.getY(), caster.getZ()));
        }
        Object candidateCap = trigger(server, caster.getUUID(), tooMany, now + 1L, 20L, false);
        helper.assertTrue(!decision(candidateCap).allowed()
                && "veilstep_candidate_cap".equals(decision(candidateCap).code()),
            "safe-position search above the hard candidate ceiling must fail closed");
        helper.assertTrue(charges(server, caster.getUUID()) == 1,
            "candidate-cap denial must not consume charge");
        helper.succeed();
    }

    private static ArcanaDecision setCharges(MinecraftServer server, UUID casterId, int charges, int maxCharges)
            throws Exception {
        Class<?> runtime = Class.forName(RUNTIME);
        Method method = runtime.getMethod(
            "setCharges", MinecraftServer.class, UUID.class, int.class, int.class);
        return (ArcanaDecision) method.invoke(null, server, casterId, charges, maxCharges);
    }

    private static Object trigger(
            MinecraftServer server,
            UUID casterId,
            List<Vec3> candidates,
            long nowTick,
            long cooldownTicks,
            boolean protectedThreat
    ) throws Exception {
        Class<?> runtime = Class.forName(RUNTIME);
        Method method = runtime.getMethod(
            "trigger",
            MinecraftServer.class,
            UUID.class,
            List.class,
            long.class,
            long.class,
            boolean.class);
        return method.invoke(null, server, casterId, candidates, nowTick, cooldownTicks, protectedThreat);
    }

    private static int charges(MinecraftServer server, UUID casterId) throws Exception {
        Class<?> runtime = Class.forName(RUNTIME);
        return (int) runtime.getMethod("charges", MinecraftServer.class, UUID.class)
            .invoke(null, server, casterId);
    }

    private static ArcanaDecision decision(Object result) throws Exception {
        return (ArcanaDecision) result.getClass().getMethod("decision").invoke(result);
    }

    private static boolean teleported(Object result) throws Exception {
        return (boolean) result.getClass().getMethod("teleported").invoke(result);
    }

    private static int remainingCharges(Object result) throws Exception {
        return (int) result.getClass().getMethod("remainingCharges").invoke(result);
    }

    private static boolean unchanged(net.minecraft.world.entity.Entity entity, double x, double y, double z) {
        return Math.abs(entity.getX() - x) < 0.01D
            && Math.abs(entity.getY() - y) < 0.01D
            && Math.abs(entity.getZ() - z) < 0.01D;
    }
}
