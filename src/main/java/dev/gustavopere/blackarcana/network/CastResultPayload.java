package dev.gustavopere.blackarcana.network;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaCastResult;

import java.util.Objects;

public record CastResultPayload(
        int protocolVersion,
        String castId,
        String status,
        String code,
        String detail
) {
    public CastResultPayload {
        ArcanaProtocol.requireCompatible(protocolVersion);
        Objects.requireNonNull(castId, "castId");
        Objects.requireNonNull(status, "status");
        Objects.requireNonNull(code, "code");
        Objects.requireNonNull(detail, "detail");
        ArcanaCastId.parse(castId);
        ArcanaCastResult.Status.valueOf(status);
        if (code.length() > ArcanaProtocol.MAX_RESULT_CODE_LENGTH) throw new IllegalArgumentException("code exceeds protocol bound");
        if (detail.length() > ArcanaProtocol.MAX_RESULT_DETAIL_LENGTH) throw new IllegalArgumentException("detail exceeds protocol bound");
    }

    public static CastResultPayload from(ArcanaCastId castId, ArcanaCastResult result) {
        Objects.requireNonNull(castId, "castId");
        Objects.requireNonNull(result, "result");
        return new CastResultPayload(
                ArcanaProtocol.VERSION,
                castId.canonical(),
                result.status().name(),
                result.code(),
                result.detail());
    }
}
