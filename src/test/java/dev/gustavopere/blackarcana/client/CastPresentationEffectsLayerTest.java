package dev.gustavopere.blackarcana.client;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import org.junit.jupiter.api.Test;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class CastPresentationEffectsLayerTest {
    private static final Path ROOT = repositoryRoot();

    @Test
    void authoritativeOutcomeReplacesAnticipationAndCannotBeHiddenByLowerPriorityIntent() {
        CastPresentationPulseState state = new CastPresentationPulseState(4L, 8L);
        var anticipation = directive(
                CastAudiovisualOrchestration.Kind.ANTICIPATION,
                CastPresentationLifecycle.Authority.LOCAL_INTENT_PRESENTATION,
                true,
                true);
        var denied = directive(
                CastAudiovisualOrchestration.Kind.RESULT_DENIED,
                CastPresentationLifecycle.Authority.AUTHORITATIVE_CAST_RESULT,
                true,
                true);

        state.accept(anticipation, 10L);
        assertEquals(CastAudiovisualOrchestration.Kind.ANTICIPATION, state.current(10L).orElseThrow().kind());
        assertEquals(14L, state.current(10L).orElseThrow().expiresAtTick());

        state.accept(denied, 11L);
        assertEquals(CastAudiovisualOrchestration.Kind.RESULT_DENIED, state.current(11L).orElseThrow().kind());
        assertEquals(19L, state.current(11L).orElseThrow().expiresAtTick());

        state.accept(anticipation, 12L);
        assertEquals(CastAudiovisualOrchestration.Kind.RESULT_DENIED, state.current(12L).orElseThrow().kind(),
                "a fresh local intent must not visually erase an active authoritative outcome");
        assertTrue(state.current(18L).isPresent());
        assertTrue(state.current(19L).isEmpty());
    }

    @Test
    void newerAuthoritativeOutcomeReplacesOlderAuthoritativeOutcomeAcrossCasts() {
        CastPresentationPulseState state = new CastPresentationPulseState(4L, 8L);
        var denied = directive(
                CastAudiovisualOrchestration.Kind.RESULT_DENIED,
                CastPresentationLifecycle.Authority.AUTHORITATIVE_CAST_RESULT,
                true,
                true);
        var success = directive(
                CastAudiovisualOrchestration.Kind.RESULT_SUCCESS,
                CastPresentationLifecycle.Authority.AUTHORITATIVE_CAST_RESULT,
                true,
                true);

        state.accept(denied, 20L);
        state.accept(success, 21L);

        assertEquals(CastAudiovisualOrchestration.Kind.RESULT_SUCCESS, state.current(21L).orElseThrow().kind(),
                "latest authoritative result must replace an older authoritative pulse regardless of severity");
        assertEquals(29L, state.current(21L).orElseThrow().expiresAtTick());
    }

    @Test
    void reducedMotionAndReducedFlashesStillRetainAVisibleAuthoritativeOutcomeShape() {
        CastPresentationPulseState state = new CastPresentationPulseState(4L, 8L);
        state.accept(directive(
                CastAudiovisualOrchestration.Kind.RESULT_FAILED,
                CastPresentationLifecycle.Authority.AUTHORITATIVE_CAST_RESULT,
                false,
                false), 30L);

        CastPresentationPulseState.Pulse pulse = state.current(30L).orElseThrow();
        assertFalse(pulse.optionalMotionAllowed());
        assertFalse(pulse.flashHeavyEffectsAllowed());
        assertTrue(pulse.authoritativeOutcome());
        assertTrue(pulse.visualShapeRequired(),
                "critical result presentation must not disappear when motion/flashes/audio are reduced");
    }

    @Test
    void transientStateIsSingleEntryBoundedAndClearable() {
        CastPresentationPulseState state = new CastPresentationPulseState(4L, 8L);
        state.accept(directive(
                CastAudiovisualOrchestration.Kind.RESULT_SUCCESS,
                CastPresentationLifecycle.Authority.AUTHORITATIVE_CAST_RESULT,
                true,
                false), 1L);
        state.accept(directive(
                CastAudiovisualOrchestration.Kind.RESULT_FAILED,
                CastPresentationLifecycle.Authority.AUTHORITATIVE_CAST_RESULT,
                true,
                false), 2L);

        assertEquals(1, state.activeCount());
        assertEquals(CastAudiovisualOrchestration.Kind.RESULT_FAILED, state.current(2L).orElseThrow().kind());
        state.clear();
        assertEquals(0, state.activeCount());
        assertTrue(state.current(2L).isEmpty());
    }

    @Test
    void physicalClientWiresReloadSinkVisualLayerAndSessionTeardown() throws Exception {
        Path client = ROOT.resolve("src/main/java/dev/gustavopere/blackarcana/client/BlackArcanaClient.java");
        Path input = ROOT.resolve("src/main/java/dev/gustavopere/blackarcana/client/ClientInputController.java");
        Path effects = ROOT.resolve("src/main/java/dev/gustavopere/blackarcana/client/CastPresentationEffectsLayer.java");
        Path resources = ROOT.resolve("src/main/java/dev/gustavopere/blackarcana/client/CastPresentationResources.java");

        String clientSource = Files.readString(client);
        String inputSource = Files.readString(input);
        String resourcesSource = Files.readString(resources);
        assertTrue(Files.isRegularFile(effects), "physical audiovisual sink is not implemented yet");
        String effectsSource = Files.readString(effects);

        assertTrue(clientSource.contains("modEventBus.addListener(CastPresentationResources::registerReloadListener);"));
        assertTrue(clientSource.contains("modEventBus.addListener(CastPresentationEffectsLayer::register);"));
        assertTrue(clientSource.contains("CastPresentationClientRuntime.installSink(CastPresentationEffectsLayer::accept);"));
        assertTrue(inputSource.contains("CastPresentationEffectsLayer.clear();"),
                "disconnect/session loss must also clear transient visual state");
        assertTrue(resourcesSource.contains("RegisterClientReloadListenersEvent"));
        assertTrue(resourcesSource.contains("invalidate();"));

        assertTrue(effectsSource.contains("CastPresentationResources.resolveSoundEvent("));
        assertTrue(effectsSource.contains("SoundEvent.createVariableRangeEvent("));
        assertTrue(effectsSource.contains("SimpleSoundInstance.forUI("));
        assertTrue(effectsSource.contains("graphics.fill("),
                "generic result/denial must retain a non-audio shape carrier");
        assertFalse(effectsSource.contains("hitResult"),
                "generic result presentation must not infer a target/impact position");
    }

    private static CastAudiovisualOrchestration.Directive directive(
            CastAudiovisualOrchestration.Kind kind,
            CastPresentationLifecycle.Authority authority,
            boolean motion,
            boolean flashes
    ) {
        return new CastAudiovisualOrchestration.Directive(
                ArcanaCastId.random(),
                Optional.empty(),
                authority,
                kind,
                0.0D,
                motion,
                flashes);
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
        throw new IllegalStateException("Unable to locate repository root");
    }
}
