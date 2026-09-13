package dev.gustavopere.blackarcana.network;

import java.util.Objects;
import java.util.UUID;

/** Client intent to close one exact server-authored Astral Severance projection session. */
public record AstralReturnIntentPayload(
        int protocolVersion,
        UUID projectionId,
        long sequence
) {
    public AstralReturnIntentPayload {
        ArcanaProtocol.requireCompatible(protocolVersion);
        Objects.requireNonNull(projectionId, "projectionId");
        if (sequence <= 0L) throw new IllegalArgumentException("Astral return sequence must be positive");
    }
}
