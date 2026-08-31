package dev.gustavopere.blackarcana.network;

import dev.gustavopere.blackarcana.api.ArcanaSpellId;

import java.util.Objects;

/** Bounded client intent requesting a read-only resistance projection for one selected spell. */
public record HazardResistanceForecastRequestPayload(
    int protocolVersion,
    long requestId,
    String spellId
) {
    public HazardResistanceForecastRequestPayload {
        ArcanaProtocol.requireCompatible(protocolVersion);
        if (requestId < 0L) throw new IllegalArgumentException("requestId cannot be negative");
        Objects.requireNonNull(spellId, "spellId");
        if (spellId.isBlank() || spellId.length() > ArcanaProtocol.MAX_RESOURCE_ID_LENGTH) {
            throw new IllegalArgumentException("spellId must be non-blank and bounded");
        }
        ArcanaSpellId.parse(spellId);
    }

    public ArcanaSpellId parsedSpellId() {
        return ArcanaSpellId.parse(spellId);
    }
}
