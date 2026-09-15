package dev.gustavopere.blackarcana.network;

import dev.gustavopere.blackarcana.api.ArcanaCastId;

import java.util.Objects;

/** Client request to release one exact server-owned channel session. */
public record ChannelReleaseIntentPayload(
        int protocolVersion,
        String castId,
        String targetHint
) {
    public ChannelReleaseIntentPayload {
        ArcanaProtocol.requireCompatible(protocolVersion);
        Objects.requireNonNull(castId, "castId");
        Objects.requireNonNull(targetHint, "targetHint");
        if (castId.length() > ArcanaProtocol.MAX_CAST_ID_LENGTH) {
            throw new IllegalArgumentException("castId exceeds protocol bound");
        }
        ArcanaCastId.parse(castId);
        if (targetHint.length() > ArcanaProtocol.MAX_TARGET_HINT_LENGTH) {
            throw new IllegalArgumentException("targetHint exceeds protocol bound");
        }
    }

    public ArcanaCastId parsedCastId() {
        return ArcanaCastId.parse(castId);
    }
}
