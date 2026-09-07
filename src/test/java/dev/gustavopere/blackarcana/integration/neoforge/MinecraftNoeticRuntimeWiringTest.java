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

    @Test
    void observationCameraPresentationIsDerivedAfterCanonicalRevalidation() throws IOException {
        String source = Files.readString(RUNTIME_SOURCE);
        assertTrue(source.contains("import dev.gustavopere.blackarcana.network.NoeticViewTransitionTracker;"),
                "Noetic presentation sync must use the bounded transition tracker rather than a second observation registry");
        assertTrue(source.contains("import dev.gustavopere.blackarcana.network.neoforge.NoeticViewNetworkBridge;"),
                "Noetic presentation sync must use the canonical clientbound transport bridge");
        assertTrue(source.contains("new NoeticViewTransitionTracker(NoeticSafetyCeilings.MAX_ACTIVE_SESSIONS)"),
                "Presentation tracking must share the canonical active-session ceiling");

        int revalidation = source.indexOf("state.observation.tick(server);");
        int sync = source.indexOf("syncObservationViews(server, state);");
        assertTrue(revalidation >= 0 && sync > revalidation,
                "Client camera presentation must be derived only after canonical observation policy revalidation");

        assertTrue(source.contains("state.observations.session(player.getUUID())"),
                "Presentation must derive from the canonical server-owned observation session");
        assertTrue(source.contains("findLoadedLivingEntity(server, session.targetId())"),
                "Presentation target resolution must remain loaded-only and never acquire chunks");
        assertTrue(source.contains("NoeticObservationKind.BORROWED_SIGHT")
                        && source.contains("NoeticObservationKind.ASTRAL_SEVERANCE"),
                "Only the two camera-capable observation kinds may request remote camera presentation");
        assertTrue(source.contains("target.getId()"),
                "Clientbound camera presentation must use the already-loaded target runtime entity id");
        assertTrue(source.contains("state.viewTransitions.reconcile(player.getUUID(), desired)"),
                "BEGIN/END emission must be deduplicated through the bounded transition tracker");
        assertTrue(source.contains("NoeticViewNetworkBridge.send(player, payload)"),
                "Deduplicated presentation transitions must use the registered clientbound transport");
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
