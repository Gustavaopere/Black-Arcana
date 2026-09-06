package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.core.world.ChunkRef;
import net.minecraft.core.BlockPos;
import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Set;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class MinecraftForbiddenDomainRuntimeContractTest {
    private static final Path SOURCE = repositoryRoot()
        .resolve("src/main/java/dev/gustavopere/blackarcana/integration/neoforge/MinecraftForbiddenDomainRuntime.java");

    @Test
    void coveredChunksUseFloorCoordinatesAndRemainBounded() {
        Set<ChunkRef> chunks = Set.copyOf(MinecraftForbiddenDomainRuntime.coveredChunks(
            "minecraft:overworld", new BlockPos(0, 64, 0), 8));

        assertEquals(4, chunks.size());
        assertTrue(chunks.contains(new ChunkRef("minecraft:overworld", -1, -1)));
        assertTrue(chunks.contains(new ChunkRef("minecraft:overworld", -1, 0)));
        assertTrue(chunks.contains(new ChunkRef("minecraft:overworld", 0, -1)));
        assertTrue(chunks.contains(new ChunkRef("minecraft:overworld", 0, 0)));

        assertTrue(MinecraftForbiddenDomainRuntime.coveredChunks(
            "minecraft:overworld", new BlockPos(15, 64, 15), 24).size() <= 16);
    }

    @Test
    void adapterReusesCanonicalWorldAuthoritiesAndNeverForceLoadsOrTeleports() throws IOException {
        String source = Files.readString(SOURCE);
        assertTrue(source.contains("runtime.protectedDestinationGuard()"));
        assertTrue(source.contains("runtime.worldEffectPolicy().authorizeCast"));
        assertTrue(source.contains("EntityInteractionType.DOMAIN_CAPTURE"));
        assertTrue(source.contains("ServerTickEvent.Post"));
        assertTrue(source.contains("PlayerEvent.PlayerLoggedOutEvent"));
        assertTrue(source.contains("state.domains.clearParticipant(playerId)"));
        assertTrue(source.contains("ServerStoppedEvent"));

        assertFalse(source.contains("addRegionTicket"));
        assertFalse(source.contains("setChunkForced"));
        assertFalse(source.contains("forceChunk"));
        assertFalse(source.contains("teleportTo("));
        assertFalse(source.contains("getChunk("));
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
