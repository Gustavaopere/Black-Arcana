package dev.gustavopere.blackarcana.client;

import net.minecraft.client.KeyMapping;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

/** Resolves presentation-only binding facts from Minecraft's current KeyMapping state. */
final class DiscoverabilityBindings {
    private DiscoverabilityBindings() { }

    static DiscoverabilityModel.BindingSnapshot snapshot() {
        List<DiscoverabilityModel.BindingPresentation> quickCasts = new ArrayList<>(
                BlackArcanaKeyMappings.QUICK_CAST.length);
        for (int index = 0; index < BlackArcanaKeyMappings.QUICK_CAST.length; index++) {
            quickCasts.add(presentation(
                    "key.black_arcana.quick_cast_" + (index + 1),
                    BlackArcanaKeyMappings.QUICK_CAST[index]));
        }
        return new DiscoverabilityModel.BindingSnapshot(
                presentation("key.black_arcana.open_radial", BlackArcanaKeyMappings.OPEN_RADIAL),
                presentation("key.black_arcana.cast_selected", BlackArcanaKeyMappings.CAST_SELECTED),
                presentation("key.black_arcana.edit_loadout", BlackArcanaKeyMappings.EDIT_LOADOUT),
                quickCasts);
    }

    static DiscoverabilityModel.BindingPresentation presentation(
            String actionTranslationKey,
            KeyMapping mapping
    ) {
        Objects.requireNonNull(actionTranslationKey, "actionTranslationKey");
        Objects.requireNonNull(mapping, "mapping");
        if (mapping.isUnbound()) {
            return DiscoverabilityModel.BindingPresentation.unbound(actionTranslationKey);
        }
        return DiscoverabilityModel.BindingPresentation.bound(
                actionTranslationKey,
                mapping.getTranslatedKeyMessage().getString());
    }
}
