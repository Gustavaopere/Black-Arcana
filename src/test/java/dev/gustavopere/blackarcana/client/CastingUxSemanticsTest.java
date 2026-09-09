package dev.gustavopere.blackarcana.client;

import dev.gustavopere.blackarcana.api.ArcanaCastResult;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDangerTier;
import dev.gustavopere.blackarcana.network.HazardResistanceForecastPayload;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotEquals;

class CastingUxSemanticsTest {
    @Test
    void selectedAndHoveredRemainIndependentIdentityFacts() {
        assertEquals(CastingUxSemantics.FocusState.NONE, CastingUxSemantics.focus(false, false));
        assertEquals(CastingUxSemantics.FocusState.SELECTED, CastingUxSemantics.focus(true, false));
        assertEquals(CastingUxSemantics.FocusState.HOVERED, CastingUxSemantics.focus(false, true));
        assertEquals(CastingUxSemantics.FocusState.SELECTED_HOVERED, CastingUxSemantics.focus(true, true));
    }

    @Test
    void keyboardFocusRemainsIndependentFromSelectionAndPointerHover() {
        assertEquals(CastingUxSemantics.FocusState.FOCUSED, CastingUxSemantics.focus(false, false, true));
        assertEquals(CastingUxSemantics.FocusState.SELECTED_FOCUSED, CastingUxSemantics.focus(true, false, true));
        assertEquals(CastingUxSemantics.FocusState.HOVERED_FOCUSED, CastingUxSemantics.focus(false, true, true));
        assertEquals(
                CastingUxSemantics.FocusState.SELECTED_HOVERED_FOCUSED,
                CastingUxSemantics.focus(true, true, true));
    }

    @Test
    void forecastClearNeverCollapsesIntoAuthoritativeCastSuccess() {
        var forecast = CastingUxSemantics.admissionForGate(HazardResistanceForecastPayload.GateStatus.CLEAR);
        var result = CastingUxSemantics.admissionForResult(ArcanaCastResult.Status.SUCCESS);

        assertEquals(CastingUxSemantics.AdmissionState.FORECAST_CLEAR, forecast);
        assertEquals(CastingUxSemantics.AdmissionState.CAST_SUCCEEDED, result);
        assertNotEquals(forecast, result);
    }

    @Test
    void predictableBlockedForecastRemainsDistinctFromAuthoritativeDenial() {
        assertEquals(
                CastingUxSemantics.AdmissionState.FORECAST_BLOCKED,
                CastingUxSemantics.admissionForGate(HazardResistanceForecastPayload.GateStatus.IDENTITY));
        assertEquals(
                CastingUxSemantics.AdmissionState.CAST_DENIED,
                CastingUxSemantics.admissionForResult(ArcanaCastResult.Status.DENIED_IDENTITY));
        assertEquals(
                CastingUxSemantics.AdmissionState.FORECAST_UNAVAILABLE,
                CastingUxSemantics.admissionForGate(HazardResistanceForecastPayload.GateStatus.UNAVAILABLE));
    }

    @Test
    void effectFailureIsNotPresentedAsACompletedSuccessOrPredictiveDenial() {
        assertEquals(
                CastingUxSemantics.AdmissionState.CAST_FAILED,
                CastingUxSemantics.admissionForResult(ArcanaCastResult.Status.EFFECT_FAILED));
    }

    @Test
    void normalDangerTierDoesNotCreateDangerStyling() {
        assertEquals(CastingUxSemantics.HazardState.NONE, CastingUxSemantics.hazardForTier(ArcaneDangerTier.NORMAL));
        assertEquals(CastingUxSemantics.HazardState.DANGER_PRESENT, CastingUxSemantics.hazardForTier(ArcaneDangerTier.UNSTABLE));
    }

    @Test
    void hazardForecastSeparatesHardMinimumWarningRecommendationAndUnknown() {
        assertEquals(
                CastingUxSemantics.HazardState.BELOW_MINIMUM,
                CastingUxSemantics.hazardForResistance(HazardResistanceForecastPayload.Status.BELOW_MINIMUM));
        assertEquals(
                CastingUxSemantics.HazardState.BELOW_RECOMMENDED,
                CastingUxSemantics.hazardForResistance(HazardResistanceForecastPayload.Status.BELOW_RECOMMENDED));
        assertEquals(
                CastingUxSemantics.HazardState.RECOMMENDATION_MET,
                CastingUxSemantics.hazardForResistance(HazardResistanceForecastPayload.Status.RECOMMENDED));
        assertEquals(
                CastingUxSemantics.HazardState.FORECAST_UNAVAILABLE,
                CastingUxSemantics.hazardForResistance(HazardResistanceForecastPayload.Status.UNAVAILABLE));
        assertEquals(
                CastingUxSemantics.HazardState.NONE,
                CastingUxSemantics.hazardForResistance(HazardResistanceForecastPayload.Status.NORMAL));
    }

    @Test
    void loadoutDraftMembershipNeverPretendsLocalEditsWereServerAccepted() {
        assertEquals(
                CastingUxSemantics.LoadoutMembership.NOT_INCLUDED,
                CastingUxSemantics.loadoutMembership(false, false));
        assertEquals(
                CastingUxSemantics.LoadoutMembership.ACCEPTED,
                CastingUxSemantics.loadoutMembership(true, true));
        assertEquals(
                CastingUxSemantics.LoadoutMembership.DRAFT_ADDED,
                CastingUxSemantics.loadoutMembership(false, true));
        assertEquals(
                CastingUxSemantics.LoadoutMembership.DRAFT_REMOVED,
                CastingUxSemantics.loadoutMembership(true, false));
    }
}
