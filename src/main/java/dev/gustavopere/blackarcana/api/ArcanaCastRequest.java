package dev.gustavopere.blackarcana.api;

import java.util.Objects;

public record ArcanaCastRequest(ArcanaCastId castId, ArcanaSpellDefinition spell, ArcanaCastContext context, int loadoutSlot) {
    public static final int MAX_LOADOUT_SLOTS = 16;

    public ArcanaCastRequest {
        Objects.requireNonNull(castId, "castId");
        Objects.requireNonNull(spell, "spell");
        Objects.requireNonNull(context, "context");
        if (loadoutSlot < 0 || loadoutSlot >= MAX_LOADOUT_SLOTS) {
            throw new IllegalArgumentException("loadoutSlot must be between 0 and " + (MAX_LOADOUT_SLOTS - 1));
        }
    }

    public ArcanaCastRequest(ArcanaCastId castId, ArcanaSpellDefinition spell, ArcanaCastContext context) {
        this(castId, spell, context, 0);
    }

    public ArcanaCastRequest(ArcanaSpellDefinition spell, ArcanaCastContext context) {
        this(ArcanaCastId.random(), spell, context, 0);
    }
}
