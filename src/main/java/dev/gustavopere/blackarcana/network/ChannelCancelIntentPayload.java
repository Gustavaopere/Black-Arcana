package dev.gustavopere.blackarcana.network;

import dev.gustavopere.blackarcana.api.ArcanaCastId;

import java.util.Objects;

/** Client request to cancel one exact server-owned channel session. */
public record ChannelCancelIntentPayload(int protocolVersion, String castId) {
    public ChannelCancelIntentPayload {
        ArcanaProtocol.requireCompatible(protocolVersion);
        Objects.requireNonNull(castId, "castId");
        if (castId.length() > ArcanaProtocol.MAX_CAST_ID_LENGTH) {
            throw new IllegalArgumentException("castId exceeds protocol bound");
        }
        ArcanaCastId.parse(castId);
    }

    public ArcanaCastId parsedCastId() {
        return ArcanaCastId.parse(castId);
    }
}
