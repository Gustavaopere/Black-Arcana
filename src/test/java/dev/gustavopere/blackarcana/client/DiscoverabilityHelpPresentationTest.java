package dev.gustavopere.blackarcana.client;

import net.minecraft.network.chat.Component;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

class DiscoverabilityHelpPresentationTest {
    @Test
    void boundValueUsesTheCurrentBindingLabelVerbatim() {
        var binding = DiscoverabilityModel.BindingPresentation.bound(
                "key.black_arcana.open_radial",
                "Mouse 5");

        Component value = DiscoverabilityHelpPresentation.bindingValue(binding);

        assertEquals("Mouse 5", value.getString());
    }

    @Test
    void unboundValueUsesExplicitLocalizedUnboundStateInsteadOfADefaultKey() {
        var binding = DiscoverabilityModel.BindingPresentation.unbound(
                "key.black_arcana.edit_loadout");

        Component value = DiscoverabilityHelpPresentation.bindingValue(binding);

        assertEquals("help.black_arcana.binding.unbound", value.getString());
    }
}
