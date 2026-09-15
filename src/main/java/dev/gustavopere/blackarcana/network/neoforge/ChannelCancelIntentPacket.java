package dev.gustavopere.blackarcana.network.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.network.ArcanaProtocol;
import dev.gustavopere.blackarcana.network.ChannelCancelIntentPayload;
import io.netty.buffer.ByteBuf;
import net.minecraft.network.codec.ByteBufCodecs;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.ResourceLocation;

import java.util.Objects;

/** Wire-only C2S representation of a channel CANCEL intent. */
public record ChannelCancelIntentPacket(
        int protocolVersion,
        String castId
) implements CustomPacketPayload {
    public static final Type<ChannelCancelIntentPacket> TYPE = new Type<>(
            ResourceLocation.fromNamespaceAndPath(BlackArcanaMod.MOD_ID, "channel_cancel_intent"));

    public static final StreamCodec<ByteBuf, ChannelCancelIntentPacket> STREAM_CODEC = StreamCodec.composite(
            ByteBufCodecs.VAR_INT, ChannelCancelIntentPacket::protocolVersion,
            ByteBufCodecs.stringUtf8(ArcanaProtocol.MAX_CAST_ID_LENGTH), ChannelCancelIntentPacket::castId,
            ChannelCancelIntentPacket::new);

    public ChannelCancelIntentPacket {
        new ChannelCancelIntentPayload(protocolVersion, castId);
    }

    public static ChannelCancelIntentPacket from(ChannelCancelIntentPayload payload) {
        Objects.requireNonNull(payload, "payload");
        return new ChannelCancelIntentPacket(payload.protocolVersion(), payload.castId());
    }

    public ChannelCancelIntentPayload toDomain() {
        return new ChannelCancelIntentPayload(protocolVersion, castId);
    }

    @Override
    public Type<? extends CustomPacketPayload> type() {
        return TYPE;
    }
}
