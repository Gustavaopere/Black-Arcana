package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import net.minecraft.core.BlockPos;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

import java.util.List;
import java.util.UUID;

@SuppressWarnings("removal")
@GameTestHolder(BlackArcanaMod.MOD_ID)
@PrefixGameTestTemplate(false)
public final class InnerDominionLifecycleDiagnosticGameTests {
    private InnerDominionLifecycleDiagnosticGameTests() { }

    @GameTest(template = "foundation_empty", timeoutTicks = 100)
    public static void directServerPlayerRecoveryUsesCapturedOrigin(GameTestHelper helper) {
        var owner = helper.makeMockServerPlayerInLevel();
        BlockPos origin = helper.absolutePos(new BlockPos(1, 2, 1));
        owner.setPos(origin.getX() + 0.5D, origin.getY(), origin.getZ() + 0.5D);
        double originX = owner.getX();
        double originY = owner.getY();
        double originZ = owner.getZ();
        var server = helper.getLevel().getServer();
        UUID sessionId = UUID.randomUUID();

        var opened = MinecraftInnerDominionRuntime.openLocalizedSession(
            server,
            sessionId,
            owner.getUUID(),
            List.of(owner.getUUID()),
            8.0D,
            200L);
        helper.assertTrue(opened.decision().allowed(), "direct recovery fixture must open");

        BlockPos displaced = helper.absolutePos(new BlockPos(5, 2, 1));
        owner.setPos(displaced.getX() + 0.5D, displaced.getY(), displaced.getZ() + 0.5D);

        var originSafety = MinecraftSafeDestinationResolver.evaluate(
            server,
            owner,
            helper.getLevel(),
            originX,
            originY,
            originZ);
        helper.assertTrue(originSafety.allowed(),
            "captured origin unexpectedly rejected before recovery; code=" + originSafety.code()
                + " facts=" + originSafety.facts());

        var recovery = MinecraftInnerDominionRuntime.recoverParticipant(server, owner);

        double distance = distanceSquared(owner.getX(), owner.getY(), owner.getZ(), originX, originY, originZ);
        helper.assertTrue(recovery.decision().allowed() && recovery.recovered(),
            "direct ServerPlayer recovery must settle; code=" + recovery.decision().code());
        helper.assertTrue(!recovery.usedFallback(),
            "direct ServerPlayer recovery should prefer the still-valid origin over fallback");
        helper.assertTrue(distance < 0.01D,
            "direct ServerPlayer recovery must move the exact provided player to origin; distance=" + distance
                + " actual=" + owner.getX() + "," + owner.getY() + "," + owner.getZ()
                + " origin=" + originX + "," + originY + "," + originZ);
        helper.succeed();
    }

    private static double distanceSquared(double ax, double ay, double az, double bx, double by, double bz) {
        double dx = ax - bx;
        double dy = ay - by;
        double dz = az - bz;
        return dx * dx + dy * dy + dz * dz;
    }
}
