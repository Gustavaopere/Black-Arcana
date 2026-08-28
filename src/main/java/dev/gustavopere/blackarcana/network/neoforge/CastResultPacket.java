package dev.gustavopere.blackarcana.network.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.network.ArcanaProtocol;
import dev.gustavopere.blackarcana.network.CastResultPayload;
import io.netty.buffer.ByteBuf;
import net.minecraft.network.codec.ByteBufCodecs;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.ResourceLocation;

import java.util.Objects;

/** Wire-only server result for one cast id. */
public record CastResultPacket(
        int protocolVersion,
        String castId,
        String status,
        String code,
        String detail
) implements CustomPacketPayload {
    public static final Type<CastResultPacket> TYPE = new Type<>(
            ResourceLocation.fromNamespaceAndPath(BlackArcanaMod.MOD_ID, "cast_result"));

    public static final StreamCodec<ByteBuf, CastResultPacket> STREAM_CODEC = StreamCodec.composite(
            ByteBufCodecs.VAR_INT, CastResultPacket::protocolVersion,
            ByteBufCodecs.stringUtf8(ArcanaProtocol.MAX_CAST_ID_LENGTH), CastResultPacket::castId,
            ByteBufCodecs.stringUtf8(ArcanaProtocol.MAX_RESULT_STATUS_LENGTH), CastResultPacket::status,
            ByteBufCodecs.stringUtf8(ArcanaProtocol.MAX_RESULT_CODE_LENGTH), CastResultPacket::code,
            ByteBufCodecs.stringUtf8(ArcanaProtocol.MAX_RESULT_DETAIL_LENGTH), CastResultPacket::detail,
            CastResultPacket::new);

    public CastResultPacket {
        Objects.requireNonNull(castId, "castId");
        Objects.requireNonNull(status, "status");
        Objects.requireNonNull(code, "code");
        Objects.requireNonNull(detail, "detail");
        new CastResultPayload(protocolVersion, castId, status, code, detail);
    }

    public static CastResultPacket from(CastResultPayload payload) {
        Objects.requireNonNull(payload, "payload");
        return new CastResultPacket(
                payload.protocolVersion(), payload.castId(), payload.status(),
                payload.code(), payload.detail());
    }

    public CastResultPayload toDomain() {
        return new CastResultPayload(protocolVersion, castId, status, code, detail);
    }

    @Override
    public Type<? extends CustomPacketPayload> type() {
        return TYPE;
    }
}
