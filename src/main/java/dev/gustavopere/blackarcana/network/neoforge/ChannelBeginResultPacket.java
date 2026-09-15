package dev.gustavopere.blackarcana.network.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.network.ArcanaProtocol;
import dev.gustavopere.blackarcana.network.ChannelBeginResultPayload;
import io.netty.buffer.ByteBuf;
import net.minecraft.network.codec.ByteBufCodecs;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.ResourceLocation;

import java.util.Objects;

/** Wire-only S2C acknowledgement for a channel BEGIN. */
public record ChannelBeginResultPacket(
        int protocolVersion,
        String castId,
        boolean accepted,
        String code,
        String detail
) implements CustomPacketPayload {
    public static final Type<ChannelBeginResultPacket> TYPE = new Type<>(
            ResourceLocation.fromNamespaceAndPath(BlackArcanaMod.MOD_ID, "channel_begin_result"));

    public static final StreamCodec<ByteBuf, ChannelBeginResultPacket> STREAM_CODEC = StreamCodec.composite(
            ByteBufCodecs.VAR_INT, ChannelBeginResultPacket::protocolVersion,
            ByteBufCodecs.stringUtf8(ArcanaProtocol.MAX_CAST_ID_LENGTH), ChannelBeginResultPacket::castId,
            ByteBufCodecs.BOOL, ChannelBeginResultPacket::accepted,
            ByteBufCodecs.stringUtf8(ArcanaProtocol.MAX_RESULT_CODE_LENGTH), ChannelBeginResultPacket::code,
            ByteBufCodecs.stringUtf8(ArcanaProtocol.MAX_RESULT_DETAIL_LENGTH), ChannelBeginResultPacket::detail,
            ChannelBeginResultPacket::new);

    public ChannelBeginResultPacket {
        new ChannelBeginResultPayload(protocolVersion, castId, accepted, code, detail);
    }

    public static ChannelBeginResultPacket from(ChannelBeginResultPayload payload) {
        Objects.requireNonNull(payload, "payload");
        return new ChannelBeginResultPacket(
                payload.protocolVersion(),
                payload.castId(),
                payload.accepted(),
                payload.code(),
                payload.detail());
    }

    public ChannelBeginResultPayload toDomain() {
        return new ChannelBeginResultPayload(protocolVersion, castId, accepted, code, detail);
    }

    @Override
    public Type<? extends CustomPacketPayload> type() {
        return TYPE;
    }
}
