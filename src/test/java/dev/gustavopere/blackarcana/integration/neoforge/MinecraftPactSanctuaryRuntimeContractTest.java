package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.content.noetic.FamiliarOwnershipRegistry;
import dev.gustavopere.blackarcana.content.noetic.PactSanctuarySpec;
import net.minecraft.server.MinecraftServer;
import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Set;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

class MinecraftPactSanctuaryRuntimeContractTest {
    private static final Path RUNTIME_SOURCE = repositoryRoot()
            .resolve("src/main/java/dev/gustavopere/blackarcana/integration/neoforge/MinecraftPactSanctuaryRuntime.java");
    private static final Path CEILINGS_SOURCE = repositoryRoot()
            .resolve("src/main/java/dev/gustavopere/blackarcana/content/noetic/NoeticSafetyCeilings.java");

    @Test
    void sanctuaryRuntimeExposesBoundedServerAuthoritativeSurface() throws Exception {
        MinecraftPactSanctuaryRuntime runtime = new MinecraftPactSanctuaryRuntime(new FamiliarOwnershipRegistry(4));
        assertNotNull(runtime);

        assertEquals(ArcanaDecision.class,
                MinecraftPactSanctuaryRuntime.class.getMethod(
                        "activate",
                        MinecraftServer.class,
                        UUID.class,
                        UUID.class,
                        PactSanctuarySpec.class,
                        Set.class).getReturnType());
        assertEquals(int.class,
                MinecraftPactSanctuaryRuntime.class.getMethod("tick", MinecraftServer.class).getReturnType());
        assertEquals(int.class,
                MinecraftPactSanctuaryRuntime.class.getMethod("activeSanctuaries", MinecraftServer.class).getReturnType());
        assertEquals(int.class,
                MinecraftPactSanctuaryRuntime.class.getMethod(
                        "clearEntity", MinecraftServer.class, UUID.class).getReturnType());
        assertEquals(int.class,
                MinecraftPactSanctuaryRuntime.class.getMethod(
                        "clearForServerStop", MinecraftServer.class).getReturnType());
    }

    @Test
    void sanctuarySpatialQueriesRespectCanonicalRefreshThrottle() throws IOException {
        String runtimeSource = Files.readString(RUNTIME_SOURCE);
        String ceilingsSource = Files.readString(CEILINGS_SOURCE);
        assertTrue(runtimeSource.contains("nextRefreshAtTick"),
                "Active Sanctuary state must track the next permitted spatial refresh");
        assertTrue(runtimeSource.contains("SANCTUARY_REFRESH_INTERVAL_TICKS"),
                "Sanctuary tick must throttle entity queries to the canonical refresh interval");
        assertTrue(ceilingsSource.contains("SANCTUARY_REFRESH_INTERVAL_TICKS = 20"),
                "Stage 07.07 should use the canonical 20-tick default Sanctuary refresh");
        assertTrue(ceilingsSource.contains("MIN_SANCTUARY_REFRESH_INTERVAL_TICKS = 5"),
                "The hard five-tick Sanctuary refresh floor must remain explicit");
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
