package dev.gustavopere.blackarcana.api;

import java.util.Objects;

public record ArcanaCastRequest(ArcanaSpellDefinition spell, ArcanaCastContext context) {
    public ArcanaCastRequest {
        Objects.requireNonNull(spell, "spell");
        Objects.requireNonNull(context, "context");
    }
}
