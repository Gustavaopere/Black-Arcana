package dev.gustavopere.blackarcana.integration.neoforge;

import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class MinecraftNoeticRuntimeWiringTest {
    private static final Path RUNTIME_SOURCE = repositoryRoot()
            .resolve("src/main/java/dev/gustavopere/blackarcana/integration/neoforge/MinecraftNoeticRuntime.java");

    @Test
    void stillnessMovementUsesEntityPreAndPostHooksInsteadOfOnlyServerPostTick() throws IOException {
        String source = Files.readString(RUNTIME_SOURCE);
        assertTrue(source.contains("EntityTickEvent.Pre"),
                "Stillness must have a pre-entity-tick hook so packet/previous-tick drift is corrected before entity work");
        assertTrue(source.contains("EntityTickEvent.Post"),
                "Stillness must have a post-entity-tick hook so travel during the entity tick cannot accumulate");
        assertTrue(source.contains("enforceStillnessBeforeEntityTick"),
                "Pre hook must delegate to the gaze runtime movement lock");
        assertTrue(source.contains("enforceStillnessAfterEntityTick"),
                "Post hook must delegate to the gaze runtime movement lock");
    }

    @Test
    void deathCleanupIsDeferredUntilTheDeathOutcomeIsFinal() throws IOException {
        String source = Files.readString(RUNTIME_SOURCE);
        assertTrue(source.contains("pendingDeaths"),
                "LivingDeathEvent must only enqueue bounded pending cleanup until cancellation outcome is known");
        assertTrue(source.contains("settlePendingDeaths"),
                "Server tick must settle pending deaths after death-prevention listeners have completed");

        int handlerStart = source.indexOf("private static void onLivingDeath");
        assertTrue(handlerStart >= 0, "Noetic runtime must keep an explicit LivingDeathEvent handler");
        int nextMethod = source.indexOf("\n    private static void", handlerStart + 1);
        String handler = source.substring(handlerStart, nextMethod < 0 ? source.length() : nextMethod);
        assertFalse(handler.contains("clearLifecycleEntity("),
                "LivingDeathEvent must not clear Noetic state before Soul Anchor can cancel the death");
    }

    @Test
    void sanctuaryCanCancelTargetAcquisitionBeforeMobAiUsesIt() throws IOException {
        String source = Files.readString(RUNTIME_SOURCE);
        assertTrue(source.contains("LivingChangeTargetEvent"),
                "Pact Sanctuary must intercept target changes before mob attack goals consume the target");
        assertTrue(source.contains("onLivingChangeTarget"),
                "The composition root must register an explicit target-change handler");
        assertTrue(source.contains("blocksTargetChange"),
                "Target-change admission must delegate to the bounded Sanctuary runtime");
        assertTrue(source.contains("event.setCanceled(true)"),
                "A protected Sanctuary target acquisition must be cancelled before AI can attack");
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
