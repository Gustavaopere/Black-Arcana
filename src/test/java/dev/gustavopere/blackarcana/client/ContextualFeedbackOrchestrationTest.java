package dev.gustavopere.blackarcana.client;

import org.junit.jupiter.api.Test;

import java.lang.reflect.Method;
import java.nio.file.Files;
import java.nio.file.Path;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assertions.fail;

class ContextualFeedbackOrchestrationTest {
    private static final Path HUD = repositoryRoot().resolve(
            "src/main/java/dev/gustavopere/blackarcana/client/BlackArcanaHudLayer.java");

    @Test
    void phaseAArbitrationKeepsSelectionAndAuthoritativeResultAsIndependentChannels() throws Exception {
        assertDecision(
                BlackArcanaClientConfig.FeedbackLevel.STANDARD,
                true,
                false,
                null,
                true,
                false);
        assertDecision(
                BlackArcanaClientConfig.FeedbackLevel.STANDARD,
                false,
                true,
                CastingUxSemantics.AdmissionState.CAST_DENIED,
                false,
                true);
        assertDecision(
                BlackArcanaClientConfig.FeedbackLevel.STANDARD,
                false,
                true,
                CastingUxSemantics.AdmissionState.CAST_SUCCEEDED,
                false,
                false);
        assertDecision(
                BlackArcanaClientConfig.FeedbackLevel.VERBOSE,
                false,
                true,
                CastingUxSemantics.AdmissionState.CAST_SUCCEEDED,
                false,
                true);
        assertDecision(
                BlackArcanaClientConfig.FeedbackLevel.MINIMAL,
                true,
                true,
                CastingUxSemantics.AdmissionState.CAST_FAILED,
                false,
                true);
        assertDecision(
                BlackArcanaClientConfig.FeedbackLevel.MINIMAL,
                true,
                true,
                CastingUxSemantics.AdmissionState.CAST_SUCCEEDED,
                false,
                false);
        assertDecision(
                BlackArcanaClientConfig.FeedbackLevel.VERBOSE,
                false,
                false,
                CastingUxSemantics.AdmissionState.CAST_SUCCEEDED,
                false,
                false);
    }

    @Test
    void hudDoesNotForceCurrentSelectionIdentityMerelyBecauseAResultIsRecent() throws Exception {
        String source = Files.readString(HUD);
        int decision = source.indexOf("ContextualFeedbackOrchestration.decide(");
        int selectionGuard = source.indexOf("if (decision.showSelectionContext())");
        int selectedLine = source.indexOf("selectedSpellLine().ifPresent(lines::add);");
        int hazardLine = source.indexOf("selectedHazardLine().ifPresent(lines::add);");
        int gateLine = source.indexOf("selectedGateLine().ifPresent(lines::add);");
        int resultGuard = source.indexOf("if (decision.showAuthoritativeResult())");

        assertTrue(decision >= 0, "HUD must delegate cross-channel visibility to a deterministic orchestrator");
        assertTrue(selectionGuard >= 0 && selectionGuard < selectedLine,
                "selected spell identity must be owned by the independent selection channel");
        assertTrue(selectionGuard < hazardLine && selectionGuard < gateLine,
                "hazard/gate context must remain scoped to the selection channel");
        assertTrue(resultGuard > gateLine,
                "authoritative result visibility must be evaluated as its own channel");

        int legacyBroadSelectionGuard = source.indexOf(
                "if (level != BlackArcanaClientConfig.FeedbackLevel.MINIMAL) {");
        assertFalse(legacyBroadSelectionGuard >= 0 && legacyBroadSelectionGuard < selectedLine,
                "result recency must not keep the current selected-spell line alive");
    }

    private static void assertDecision(
            BlackArcanaClientConfig.FeedbackLevel level,
            boolean selectionRecent,
            boolean resultRecent,
            CastingUxSemantics.AdmissionState resultState,
            boolean expectedSelection,
            boolean expectedResult
    ) throws Exception {
        Class<?> orchestrator;
        try {
            orchestrator = Class.forName(
                    "dev.gustavopere.blackarcana.client.ContextualFeedbackOrchestration");
        } catch (ClassNotFoundException exception) {
            orchestrator = fail("ContextualFeedbackOrchestration production boundary is not implemented yet", exception);
        }

        Method decide;
        try {
            decide = orchestrator.getDeclaredMethod(
                    "decide",
                    BlackArcanaClientConfig.FeedbackLevel.class,
                    boolean.class,
                    boolean.class,
                    CastingUxSemantics.AdmissionState.class);
        } catch (NoSuchMethodException exception) {
            decide = fail("ContextualFeedbackOrchestration.decide(...) is missing", exception);
        }
        decide.setAccessible(true);
        Object decision = decide.invoke(null, level, selectionRecent, resultRecent, resultState);

        Method showSelection = decision.getClass().getDeclaredMethod("showSelectionContext");
        Method showResult = decision.getClass().getDeclaredMethod("showAuthoritativeResult");
        showSelection.setAccessible(true);
        showResult.setAccessible(true);

        boolean actualSelection = (boolean) showSelection.invoke(decision);
        boolean actualResult = (boolean) showResult.invoke(decision);
        if (expectedSelection) assertTrue(actualSelection); else assertFalse(actualSelection);
        if (expectedResult) assertTrue(actualResult); else assertFalse(actualResult);
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
        return fail("Unable to locate repository root from test working directory");
    }
}
