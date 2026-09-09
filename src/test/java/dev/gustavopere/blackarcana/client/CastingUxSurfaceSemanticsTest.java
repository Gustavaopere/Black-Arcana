package dev.gustavopere.blackarcana.client;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

class CastingUxSurfaceSemanticsTest {
    @Test
    void radialFocusUsesNonColorMarkersWithoutConflatingSelectedAndHovered() {
        assertEquals("", BlackArcanaRadialScreen.focusPrefix(CastingUxSemantics.FocusState.NONE));
        assertEquals("[S] ", BlackArcanaRadialScreen.focusPrefix(CastingUxSemantics.FocusState.SELECTED));
        assertEquals("> ", BlackArcanaRadialScreen.focusPrefix(CastingUxSemantics.FocusState.HOVERED));
        assertEquals(">[S] ", BlackArcanaRadialScreen.focusPrefix(CastingUxSemantics.FocusState.SELECTED_HOVERED));
    }

    @Test
    void loadoutRowsDistinguishAcceptedStateFromUnsentDraftDeltas() {
        assertEquals("[ ] ", BlackArcanaLoadoutScreen.membershipPrefix(CastingUxSemantics.LoadoutMembership.NOT_INCLUDED));
        assertEquals("[x] ", BlackArcanaLoadoutScreen.membershipPrefix(CastingUxSemantics.LoadoutMembership.ACCEPTED));
        assertEquals("[+] ", BlackArcanaLoadoutScreen.membershipPrefix(CastingUxSemantics.LoadoutMembership.DRAFT_ADDED));
        assertEquals("[-] ", BlackArcanaLoadoutScreen.membershipPrefix(CastingUxSemantics.LoadoutMembership.DRAFT_REMOVED));
    }

    @Test
    void hudUsesDistinctPlayerFacingKeysForDenialFailureAndSuccess() {
        assertEquals(
                "hud.black_arcana.denied",
                BlackArcanaHudLayer.resultTranslationKey(CastingUxSemantics.AdmissionState.CAST_DENIED));
        assertEquals(
                "hud.black_arcana.cast_failed",
                BlackArcanaHudLayer.resultTranslationKey(CastingUxSemantics.AdmissionState.CAST_FAILED));
        assertEquals(
                "hud.black_arcana.cast_success",
                BlackArcanaHudLayer.resultTranslationKey(CastingUxSemantics.AdmissionState.CAST_SUCCEEDED));
        assertThrows(
                IllegalArgumentException.class,
                () -> BlackArcanaHudLayer.resultTranslationKey(CastingUxSemantics.AdmissionState.FORECAST_CLEAR));
    }
}
