package dev.gustavopere.blackarcana;

import dev.gustavopere.blackarcana.content.noetic.AstralProjectionEntity;
import dev.gustavopere.blackarcana.content.noetic.AstralSeveranceRuntime;
import dev.gustavopere.blackarcana.integration.neoforge.MinecraftNoeticRuntime;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

@GameTestHolder(BlackArcanaMod.MOD_ID)
@PrefixGameTestTemplate(false)
public final class AstralSeveranceMovementGameTests {
    private AstralSeveranceMovementGameTests() { }

    @SuppressWarnings("removal")
    @GameTest(template = "foundation_empty", timeoutTicks = 80)
    public static void exactSessionControlMovesOnlyTheServerOwnedProjection(GameTestHelper helper) {
        var server = helper.getLevel().getServer();
        var caster = helper.makeMockServerPlayerInLevel();

        try {
            var start = MinecraftNoeticRuntime.activateAuthorizedAstralProjection(
                    server,
                    caster.getUUID(),
                    40,
                    8.0D);
            helper.assertTrue(start.decision().allowed(),
                    "movement fixture requires an authorized loaded Astral projection");
            var projection = start.projection().orElseThrow();
            var entity = caster.serverLevel().getEntity(projection.projectionId());
            helper.assertTrue(entity instanceof AstralProjectionEntity,
                    "movement fixture requires the server-owned Astral representation");

            double bodyX = caster.getX();
            double bodyY = caster.getY();
            double bodyZ = caster.getZ();
            var result = MinecraftNoeticRuntime.applyAuthorizedAstralControl(
                    server,
                    caster.getUUID(),
                    new AstralSeveranceRuntime.ControlIntent(
                            projection.projectionId(),
                            1L,
                            0.0D,
                            0.0D,
                            1.0D,
                            15.0F,
                            -5.0F),
                    new AstralSeveranceRuntime.ControlLimits(1.0D, 30.0F));
            helper.assertTrue(result == AstralSeveranceRuntime.ControlResult.APPLIED,
                    "exact-session bounded control must be applied by the server: " + result);

            var moved = MinecraftNoeticRuntime.astralProjection(server, caster.getUUID()).orElseThrow();
            helper.assertTrue(moved.lastProcessedControlSequence() == 1L,
                    "server-owned sequence must advance exactly once");
            helper.assertTrue(entity != null
                            && closeEnough(entity.getX(), moved.pose().x())
                            && closeEnough(entity.getY(), moved.pose().y())
                            && closeEnough(entity.getZ(), moved.pose().z())
                            && closeEnough(entity.getYRot(), moved.pose().yawDegrees())
                            && closeEnough(entity.getXRot(), moved.pose().pitchDegrees()),
                    "world representation must mirror the accepted logical pose");
            helper.assertTrue(closeEnough(caster.getX(), bodyX)
                            && closeEnough(caster.getY(), bodyY)
                            && closeEnough(caster.getZ(), bodyZ),
                    "Astral control must never move the physical player body");

            var stale = MinecraftNoeticRuntime.applyAuthorizedAstralControl(
                    server,
                    caster.getUUID(),
                    new AstralSeveranceRuntime.ControlIntent(
                            projection.projectionId(),
                            1L,
                            0.0D,
                            0.0D,
                            1.0D,
                            0.0F,
                            0.0F),
                    new AstralSeveranceRuntime.ControlLimits(1.0D, 30.0F));
            helper.assertTrue(stale == AstralSeveranceRuntime.ControlResult.STALE_SEQUENCE,
                    "replayed control sequence must fail closed");
            helper.assertTrue(closeEnough(entity.getX(), moved.pose().x())
                            && closeEnough(entity.getY(), moved.pose().y())
                            && closeEnough(entity.getZ(), moved.pose().z()),
                    "replayed control must not mutate the projection entity");
        } finally {
            MinecraftNoeticRuntime.clearEntity(server, caster.getUUID());
        }

        helper.assertTrue(MinecraftNoeticRuntime.activeStateCount(server) == 0,
                "movement GameTest cleanup must leave no Stage 07.07 state");
        helper.succeed();
    }

    @SuppressWarnings("removal")
    @GameTest(template = "foundation_empty", timeoutTicks = 80)
    public static void missingProjectionRepresentationClosesServerSession(GameTestHelper helper) {
        var server = helper.getLevel().getServer();
        var caster = helper.makeMockServerPlayerInLevel();
        var start = MinecraftNoeticRuntime.activateAuthorizedAstralProjection(
                server,
                caster.getUUID(),
                40,
                8.0D);
        helper.assertTrue(start.decision().allowed(),
                "representation-loss fixture requires an authorized loaded Astral projection");
        var projection = start.projection().orElseThrow();
        var entity = caster.serverLevel().getEntity(projection.projectionId());
        helper.assertTrue(entity instanceof AstralProjectionEntity,
                "representation-loss fixture requires the server-owned Astral representation");

        entity.discard();
        helper.runAfterDelay(2L, () -> {
            try {
                helper.assertTrue(
                        MinecraftNoeticRuntime.astralProjection(server, caster.getUUID()).isEmpty(),
                        "missing Astral representation must terminate the server-owned projection without MOVE input");
                helper.assertTrue(MinecraftNoeticRuntime.activeStateCount(server) == 0,
                        "representation-loss cleanup must leave no Stage 07.07 state");
                helper.succeed();
            } finally {
                MinecraftNoeticRuntime.clearEntity(server, caster.getUUID());
            }
        });
    }

    private static boolean closeEnough(double left, double right) {
        return Math.abs(left - right) <= 1.0E-6D;
    }
}
