package dev.gustavopere.blackarcana.content.souls;

import java.util.Objects;

/** Explicit whitelist for occult perception; it never turns into a generic hidden-entity reveal. */
public final class SpiritSightPolicy {
    public boolean visible(Trace trace) {
        Objects.requireNonNull(trace, "trace");
        if (!trace.providerAvailable()) return false;
        return switch (trace.kind()) {
            case MALUM_SPIRIT, EIDOLON_OCCULT, BLACK_ARCANA_WARD, BLACK_ARCANA_DOMAIN -> true;
            case HIDDEN_PLAYER, PRIVATE_CONTAINER, OTHER -> false;
        };
    }

    public record Trace(TraceKind kind, boolean providerAvailable) {
        public Trace { Objects.requireNonNull(kind, "kind"); }
    }

    public enum TraceKind {
        MALUM_SPIRIT,
        EIDOLON_OCCULT,
        BLACK_ARCANA_WARD,
        BLACK_ARCANA_DOMAIN,
        HIDDEN_PLAYER,
        PRIVATE_CONTAINER,
        OTHER
    }
}
