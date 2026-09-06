package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.content.noetic.NoeticGazePolicy;
import dev.gustavopere.blackarcana.content.noetic.NoeticSafetyCeilings;
import dev.gustavopere.blackarcana.content.noetic.NullificationRegistry;
import net.minecraft.server.MinecraftServer;
import org.junit.jupiter.api.Test;

import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;

class MinecraftNoeticGazeRuntimeContractTest {
    @Test
    void gazeRuntimeExposesBoundedServerAuthoritativeSurface() throws Exception {
        MinecraftNoeticGazeRuntime runtime = new MinecraftNoeticGazeRuntime(new NullificationRegistry(8));
        assertNotNull(runtime);

        assertEquals(ArcanaDecision.class,
                MinecraftNoeticGazeRuntime.class.getMethod(
                        "startStillness",
                        MinecraftServer.class,
                        UUID.class,
                        UUID.class,
                        int.class).getReturnType());
        assertEquals(MinecraftNoeticGazeRuntime.NullificationResult.class,
                MinecraftNoeticGazeRuntime.class.getMethod(
                        "nullify",
                        MinecraftServer.class,
                        UUID.class,
                        UUID.class).getReturnType());
        assertEquals(void.class,
                MinecraftNoeticGazeRuntime.class.getMethod(
                        "tick", MinecraftServer.class).getReturnType());
        assertEquals(int.class,
                MinecraftNoeticGazeRuntime.class.getMethod(
                        "activeGazes", MinecraftServer.class).getReturnType());
        assertEquals(int.class,
                MinecraftNoeticGazeRuntime.class.getMethod(
                        "clearEntity", MinecraftServer.class, UUID.class).getReturnType());
        assertEquals(int.class,
                MinecraftNoeticGazeRuntime.class.getMethod(
                        "clearForServerStop", MinecraftServer.class).getReturnType());
    }

    @Test
    void stillnessDiminishingReturnsBoundDurationAndEventuallyGrantImmunity() {
        assertEquals(200, NoeticGazePolicy.effectiveControlTicks(200, 200, 0));
        assertEquals(100, NoeticGazePolicy.effectiveControlTicks(200, 200, 1));
        assertEquals(50, NoeticGazePolicy.effectiveControlTicks(200, 200, 2));
        assertEquals(0, NoeticGazePolicy.effectiveControlTicks(200, 200, NoeticSafetyCeilings.MAX_GAZE_DR_STACKS));
        assertEquals(40, NoeticGazePolicy.effectiveControlTicks(200, 40, 0));
    }
}
