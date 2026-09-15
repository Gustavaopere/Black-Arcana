package dev.gustavopere.blackarcana.network.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.network.ArcanaProtocol;
import dev.gustavopere.blackarcana.network.ChannelReleaseIntentPayload;
import io.netty.buffer.ByteBuf;
import net.minecraft.network.codec.ByteBufCodecs;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.ResourceLocation;

import java.util.Objects;

/** Wire-only C2S representation of a channel RELEASE intent. */
public record ChannelReleaseIntentPacket(
        int protocolVersion,
        String castId,
        String targetHint
) implements CustomPacketPayload {
    public static final Type<ChannelReleaseIntentPacket> TYPE = new Type<>(
            ResourceLocation.fromNamespaceAndPath(BlackArcanaMod.MOD_ID, "channel_release_intent"));

    public static final StreamCodec<ByteBuf, ChannelReleaseIntentPacket> STREAM_CODEC = StreamCodec.composite(
            ByteBufCodecs.VAR_INT, ChannelReleaseIntentPacket::protocolVersion,
            ByteBufCodecs.stringUtf8(ArcanaProtocol.MAX_CAST_ID_LENGTH), ChannelReleaseIntentPacket::castId,
            ByteBufCodecs.stringUtf8(ArcanaProtocol.MAX_TARGET_HINT_LENGTH), ChannelReleaseIntentPacket::targetHint,
            ChannelReleaseIntentPacket::new);

    public ChannelReleaseIntentPacket {
        new ChannelReleaseIntentPayload(protocolVersion, castId, targetHint);
    }

    public static ChannelReleaseIntentPacket from(ChannelReleaseIntentPayload payload) {
        Objects.requireNonNull(payload, "payload");
        return new ChannelReleaseIntentPacket(
                payload.protocolVersion(),
                payload.castId(),
                payload.targetHint());
    }

    public ChannelReleaseIntentPayload toDomain() {
        return new ChannelReleaseIntentPayload(protocolVersion, castId, targetHint);
    }

    @Override
    public Type<? extends CustomPacketPayload> type() {
        return TYPE;
    }
}
