package dev.gustavopere.blackarcana.network;

import dev.gustavopere.blackarcana.api.ArcanaSpellId;

import java.util.List;
import java.util.Objects;

public record SpellPresentationPayload(int protocolVersion, List<Entry> entries) {
    public SpellPresentationPayload {
        ArcanaProtocol.requireCompatible(protocolVersion);
        Objects.requireNonNull(entries, "entries");
        entries = List.copyOf(entries);
        if (entries.size() > ArcanaProtocol.MAX_PRESENTATION_ENTRIES) {
            throw new IllegalArgumentException("too many presentation entries");
        }
    }

    public record Entry(String spellId, String translationKey, String iconId) {
        public Entry {
            Objects.requireNonNull(spellId, "spellId");
            Objects.requireNonNull(translationKey, "translationKey");
            Objects.requireNonNull(iconId, "iconId");
            ArcanaSpellId.parse(spellId);
            if (translationKey.isBlank()) throw new IllegalArgumentException("translationKey cannot be blank");
            if (iconId.isBlank()) throw new IllegalArgumentException("iconId cannot be blank");
            if (translationKey.length() > 160) throw new IllegalArgumentException("translationKey exceeds protocol bound");
            if (iconId.length() > 192) throw new IllegalArgumentException("iconId exceeds protocol bound");
        }
    }
}
