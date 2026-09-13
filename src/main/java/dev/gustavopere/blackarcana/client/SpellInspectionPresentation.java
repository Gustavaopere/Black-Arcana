package dev.gustavopere.blackarcana.client;

import net.minecraft.client.gui.Font;
import net.minecraft.network.chat.Component;
import net.minecraft.util.FormattedCharSequence;

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
    private static final int TOOLTIP_HORIZONTAL_RESERVE = 24;

    private SpellInspectionPresentation() {
    }

    static List<Component> lines(String canonicalSpellId, Component displayName, Component hazardLine) {
        Objects.requireNonNull(canonicalSpellId, "canonicalSpellId");
        Objects.requireNonNull(displayName, "displayName");

        Component id = Component.literal(canonicalSpellId)
                .append(" · ")
                .append(Component.translatable("screen.black_arcana.inspect.id"));
        return hazardLine == null
                ? List.of(displayName, id)
                : List.of(displayName, id, hazardLine);
    }

    static List<FormattedCharSequence> wrappedLines(
            Font font,
            int viewportWidth,
            String canonicalSpellId,
            Component displayName,
            Component hazardLine
    ) {
        Objects.requireNonNull(font, "font");
        int maxTextWidth = Math.max(1, viewportWidth - TOOLTIP_HORIZONTAL_RESERVE);
        return lines(canonicalSpellId, displayName, hazardLine).stream()
                .flatMap(line -> font.split(line, maxTextWidth).stream())
                .toList();
    }
}
