package dev.gustavopere.blackarcana.config;

import dev.gustavopere.blackarcana.api.ArcanaSpellId;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

public record SpellDataDefinition(int schemaVersion, String id, String translationKey, String iconId) {
    public static final int CURRENT_SCHEMA_VERSION = 1;

    public SpellDataDefinition {
        Objects.requireNonNull(id, "id");
        Objects.requireNonNull(translationKey, "translationKey");
        Objects.requireNonNull(iconId, "iconId");
    }

    public List<String> validate() {
        List<String> errors = new ArrayList<>();
        if (schemaVersion != CURRENT_SCHEMA_VERSION) {
            errors.add("unsupported schemaVersion: " + schemaVersion);
        }
        try {
            ArcanaSpellId.parse(id);
        } catch (IllegalArgumentException ex) {
            errors.add(ex.getMessage());
        }
        if (translationKey.isBlank()) errors.add("translationKey cannot be blank");
        if (iconId.isBlank()) errors.add("iconId cannot be blank");
        return List.copyOf(errors);
    }
}
