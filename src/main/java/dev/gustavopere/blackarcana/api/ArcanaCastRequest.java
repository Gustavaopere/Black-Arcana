package dev.gustavopere.blackarcana.api;

import java.util.Objects;

public record ArcanaCastRequest(ArcanaCastId castId, ArcanaSpellDefinition spell, ArcanaCastContext context) {
    public ArcanaCastRequest {
        Objects.requireNonNull(castId, "castId");
        Objects.requireNonNull(spell, "spell");
        Objects.requireNonNull(context, "context");
    }

    public ArcanaCastRequest(ArcanaSpellDefinition spell, ArcanaCastContext context) {
        this(ArcanaCastId.random(), spell, context);
    }
}
