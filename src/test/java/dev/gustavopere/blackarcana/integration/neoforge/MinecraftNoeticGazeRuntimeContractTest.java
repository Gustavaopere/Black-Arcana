package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.content.noetic.NoeticGazePolicy;
import dev.gustavopere.blackarcana.content.noetic.NoeticSafetyCeilings;
import dev.gustavopere.blackarcana.content.noetic.NullificationRegistry;
import net.minecraft.server.MinecraftServer;
import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

class MinecraftNoeticGazeRuntimeContractTest {
    private static final Path RUNTIME_SOURCE = repositoryRoot()
            .resolve("src/main/java/dev/gustavopere/blackarcana/integration/neoforge/MinecraftNoeticGazeRuntime.java");
    private static final Path CEILINGS_SOURCE = repositoryRoot()
            .resolve("src/main/java/dev/gustavopere/blackarcana/content/noetic/NoeticSafetyCeilings.java");

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
        int hardCeiling = NoeticSafetyCeilings.MAX_GAZE_DURATION_TICKS;
        assertEquals(160, hardCeiling);
        assertEquals(160, NoeticGazePolicy.effectiveControlTicks(hardCeiling, hardCeiling, 0));
        assertEquals(80, NoeticGazePolicy.effectiveControlTicks(hardCeiling, hardCeiling, 1));
        assertEquals(40, NoeticGazePolicy.effectiveControlTicks(hardCeiling, hardCeiling, 2));
        assertEquals(0, NoeticGazePolicy.effectiveControlTicks(
                hardCeiling,
                hardCeiling,
                NoeticSafetyCeilings.MAX_GAZE_DR_STACKS));
        assertEquals(40, NoeticGazePolicy.effectiveControlTicks(hardCeiling, 40, 0));
    }

    @Test
    void playerTargetsReceiveExplicitReapplicationImmunity() throws IOException {
        String runtimeSource = Files.readString(RUNTIME_SOURCE);
        String ceilingsSource = Files.readString(CEILINGS_SOURCE);
        assertTrue(runtimeSource.contains("playerImmunityUntil"),
                "Player Stillness targets need an explicit cooldown independent of generic DR stacks");
        assertTrue(runtimeSource.contains("gaze_player_reapplication_immunity"),
                "A recast during the PvP immunity window must fail closed with an explicit denial");
        assertTrue(ceilingsSource.contains("GAZE_PLAYER_REAPPLICATION_IMMUNITY_TICKS = 80"),
                "Stage 07.07 should use the canonical 80-tick default player immunity");
        assertTrue(ceilingsSource.contains("MIN_GAZE_PLAYER_REAPPLICATION_IMMUNITY_TICKS = 40"),
                "The repository hard floor for player reapplication immunity must stay explicit");
    }

    private static Path repositoryRoot() {
        String workspace = System.getenv("GITHUB_WORKSPACE");
        if (workspace != null && !workspace.isBlank()) return Path.of(workspace);
        Path candidate = Path.of("").toAbsolutePath();
        while (candidate != null) {
            if (Files.exists(candidate.resolve("settings.gradle")) && Files.isDirectory(candidate.resolve(".github"))) {
                return candidate;
            }
            candidate = candidate.getParent();
        }
        throw new IllegalStateException("Unable to locate repository root from test working directory");
    }
}
