package dev.gustavopere.blackarcana.network;

import dev.gustavopere.blackarcana.api.ArcanaSpellId;

import java.util.HashSet;
import java.util.List;
import java.util.Objects;
import java.util.Set;

public record SpellPresentationPayload(int protocolVersion, List<Entry> entries) {
    public SpellPresentationPayload {
        ArcanaProtocol.requireCompatible(protocolVersion);
        Objects.requireNonNull(entries, "entries");
        entries = List.copyOf(entries);
        if (entries.size() > ArcanaProtocol.MAX_PRESENTATION_ENTRIES) {
            throw new IllegalArgumentException("too many presentation entries");
        }

        Set<String> spellIds = new HashSet<>(entries.size());
        for (Entry entry : entries) {
            Objects.requireNonNull(entry, "presentation entry");
            if (!spellIds.add(entry.spellId())) {
                throw new IllegalArgumentException("duplicate presentation spell id: " + entry.spellId());
            }
        }
    }

    public record Entry(String spellId, String translationKey, String iconId) {
        public Entry {
            Objects.requireNonNull(spellId, "spellId");
            Objects.requireNonNull(translationKey, "translationKey");
            Objects.requireNonNull(iconId, "iconId");
            if (spellId.length() > ArcanaProtocol.MAX_RESOURCE_ID_LENGTH) {
                throw new IllegalArgumentException("spellId exceeds protocol bound");
            }
            ArcanaSpellId.parse(spellId);
            if (translationKey.isBlank()) throw new IllegalArgumentException("translationKey cannot be blank");
            if (iconId.isBlank()) throw new IllegalArgumentException("iconId cannot be blank");
            if (translationKey.length() > ArcanaProtocol.MAX_TRANSLATION_KEY_LENGTH) {
                throw new IllegalArgumentException("translationKey exceeds protocol bound");
            }
            if (iconId.length() > ArcanaProtocol.MAX_ICON_ID_LENGTH) {
                throw new IllegalArgumentException("iconId exceeds protocol bound");
            }
        }
    }
}
