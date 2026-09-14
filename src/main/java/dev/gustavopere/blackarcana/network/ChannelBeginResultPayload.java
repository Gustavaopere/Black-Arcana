package dev.gustavopere.blackarcana.network;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaDecision;

import java.util.Objects;

/** Server acknowledgement for starting a channel without implying that the spell effect executed. */
public record ChannelBeginResultPayload(
        int protocolVersion,
        String castId,
        boolean accepted,
        String code,
        String detail
) {
    public ChannelBeginResultPayload {
        ArcanaProtocol.requireCompatible(protocolVersion);
        Objects.requireNonNull(castId, "castId");
        Objects.requireNonNull(code, "code");
        Objects.requireNonNull(detail, "detail");
        if (castId.length() > ArcanaProtocol.MAX_CAST_ID_LENGTH) {
            throw new IllegalArgumentException("castId exceeds protocol bound");
        }
        if (code.length() > ArcanaProtocol.MAX_RESULT_CODE_LENGTH) {
            throw new IllegalArgumentException("code exceeds protocol bound");
        }
        if (detail.length() > ArcanaProtocol.MAX_RESULT_DETAIL_LENGTH) {
            throw new IllegalArgumentException("detail exceeds protocol bound");
        }
        ArcanaCastId.parse(castId);
    }

    public static ChannelBeginResultPayload from(ArcanaCastId castId, ArcanaDecision decision) {
        Objects.requireNonNull(castId, "castId");
        Objects.requireNonNull(decision, "decision");
        return new ChannelBeginResultPayload(
                ArcanaProtocol.VERSION,
                castId.canonical(),
                decision.allowed(),
                decision.code(),
                decision.detail());
    }

    public ArcanaCastId parsedCastId() {
        return ArcanaCastId.parse(castId);
    }
}
