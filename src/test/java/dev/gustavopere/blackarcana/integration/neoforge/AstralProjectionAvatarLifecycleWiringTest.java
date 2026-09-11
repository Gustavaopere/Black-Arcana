package dev.gustavopere.blackarcana.integration.neoforge;

import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

import static org.junit.jupiter.api.Assertions.assertTrue;

class AstralProjectionAvatarLifecycleWiringTest {
    private static final Path RUNTIME_SOURCE = repositoryRoot().resolve(
            "src/main/java/dev/gustavopere/blackarcana/integration/neoforge/MinecraftNoeticRuntime.java");

    @Test
    void astralAvatarRepresentationFollowsTheCanonicalProjectionLifecycle() throws IOException {
        String source = Files.readString(RUNTIME_SOURCE);

        assertTrue(source.contains("BlackArcanaNoeticEntities.ASTRAL_PROJECTION.get().create(caster.serverLevel())"),
                "Authorized Astral activation must materialize the dedicated avatar in the caster's already-loaded server level");
        assertTrue(source.contains("caster.serverLevel().addFreshEntity(avatar)"),
                "Astral avatar must be added by the server after the canonical lifecycle authorizes the projection");
        assertTrue(source.contains("astralAvatars"),
                "Composition root must keep a bounded exact-session avatar handle instead of scanning the world");

        assertTrue(source.contains("moveAstralProjection("),
                "Minecraft composition root needs one server-side movement adapter for accepted client intent");
        assertTrue(source.contains("state.astral.move(casterId, intent)"),
                "Movement adapter must delegate authority to AstralSeveranceRuntime rather than moving from client coordinates");
        assertTrue(source.contains("syncAstralAvatarPose("),
                "Only the server-owned accepted projection pose may be copied to the avatar entity");

        assertTrue(source.contains("removeAstralAvatar("),
                "Every terminal lifecycle path must be able to remove the ephemeral avatar representation");
        assertTrue(source.contains("closeAstralProjection("),
                "Terminal handlers must share one close+avatar-cleanup seam rather than duplicating lifecycle authority");
        assertTrue(source.contains("reconcileAstralAvatars("),
                "Unexpected avatar loss must fail closed by reconciling the bounded active projection set");
    }

    private static Path repositoryRoot() {
        String workspace = System.getenv("GITHUB_WORKSPACE");
        if (workspace != null && !workspace.isBlank()) {
            return Path.of(workspace);
        }

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
