package dev.gustavopere.blackarcana.client;

import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class DiscoverabilityBindingPresentationTest {
    @Test
    void reboundBindingCarriesOnlyTheCurrentLabelAndNeverInventsTheDefault() {
        var binding = DiscoverabilityModel.BindingPresentation.bound(
                "key.black_arcana.open_radial",
                "G");

        assertEquals("key.black_arcana.open_radial", binding.actionTranslationKey());
        assertEquals("G", binding.currentLabel().orElseThrow());
        assertFalse(binding.unbound());
        assertFalse(binding.currentLabel().orElseThrow().equals("R"));
    }

    @Test
    void unboundBindingIsExplicitAndContainsNoFallbackKey() {
        var binding = DiscoverabilityModel.BindingPresentation.unbound(
                "key.black_arcana.edit_loadout");

        assertTrue(binding.unbound());
        assertTrue(binding.currentLabel().isEmpty());
    }

    @Test
    void quickCastBindingsRemainEightIndependentPresentationFacts() {
        var quickCasts = List.of(
                DiscoverabilityModel.BindingPresentation.bound("key.black_arcana.quick_cast_1", "1"),
                DiscoverabilityModel.BindingPresentation.bound("key.black_arcana.quick_cast_2", "2"),
                DiscoverabilityModel.BindingPresentation.unbound("key.black_arcana.quick_cast_3"),
                DiscoverabilityModel.BindingPresentation.unbound("key.black_arcana.quick_cast_4"),
                DiscoverabilityModel.BindingPresentation.unbound("key.black_arcana.quick_cast_5"),
                DiscoverabilityModel.BindingPresentation.unbound("key.black_arcana.quick_cast_6"),
                DiscoverabilityModel.BindingPresentation.unbound("key.black_arcana.quick_cast_7"),
                DiscoverabilityModel.BindingPresentation.bound("key.black_arcana.quick_cast_8", "Mouse 4"));

        var snapshot = new DiscoverabilityModel.BindingSnapshot(
                DiscoverabilityModel.BindingPresentation.bound("key.black_arcana.open_radial", "G"),
                DiscoverabilityModel.BindingPresentation.bound("key.black_arcana.cast_selected", "C"),
                DiscoverabilityModel.BindingPresentation.unbound("key.black_arcana.edit_loadout"),
                quickCasts);

        assertEquals(8, snapshot.quickCasts().size());
        assertEquals("1", snapshot.quickCasts().get(0).currentLabel().orElseThrow());
        assertTrue(snapshot.quickCasts().get(2).unbound());
        assertEquals("Mouse 4", snapshot.quickCasts().get(7).currentLabel().orElseThrow());
    }

    @Test
    void snapshotRejectsAnythingOtherThanEightQuickCastMappings() {
        assertThrows(IllegalArgumentException.class, () -> new DiscoverabilityModel.BindingSnapshot(
                DiscoverabilityModel.BindingPresentation.bound("key.black_arcana.open_radial", "G"),
                DiscoverabilityModel.BindingPresentation.bound("key.black_arcana.cast_selected", "C"),
                DiscoverabilityModel.BindingPresentation.unbound("key.black_arcana.edit_loadout"),
                List.of(DiscoverabilityModel.BindingPresentation.unbound("key.black_arcana.quick_cast_1"))));
    }
}
