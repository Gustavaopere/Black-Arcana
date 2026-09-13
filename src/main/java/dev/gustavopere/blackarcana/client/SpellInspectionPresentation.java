package dev.gustavopere.blackarcana.client;

import net.minecraft.network.chat.Component;

import java.util.List;
import java.util.Objects;

/**
 * Builds the bounded Stage 05.14 inspection lines from already-authorized client presentation data.
 *
 * This helper intentionally exposes only static presentation identity plus an optional pre-existing
 * hazard presentation line. It does not infer cost, cooldown, targeting, provider, domain or cast
 * admission state.
 */
final class SpellInspectionPresentation {
    private SpellInspectionPresentation() {
    }

    static List<Component> lines(String canonicalSpellId, Component displayName, Component hazardLine) {
        Objects.requireNonNull(canonicalSpellId, "canonicalSpellId");
        Objects.requireNonNull(displayName, "displayName");

        Component id = Component.translatable("screen.black_arcana.inspect.id")
                .append(": ")
                .append(Component.literal(canonicalSpellId));
        return hazardLine == null
                ? List.of(displayName, id)
                : List.of(displayName, id, hazardLine);
    }
}
