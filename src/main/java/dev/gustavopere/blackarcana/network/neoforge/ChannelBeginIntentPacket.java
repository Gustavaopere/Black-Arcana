package dev.gustavopere.blackarcana.network.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.network.ArcanaProtocol;
import dev.gustavopere.blackarcana.network.ChannelBeginIntentPayload;
import io.netty.buffer.ByteBuf;
import net.minecraft.network.codec.ByteBufCodecs;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.ResourceLocation;

import java.util.Objects;

/** Wire-only C2S representation of a channel BEGIN intent. */
public record ChannelBeginIntentPacket(
        int protocolVersion,
        String castId,
        String spellId,
        int sourceSlot
) implements CustomPacketPayload {
    public static final Type<ChannelBeginIntentPacket> TYPE = new Type<>(
            ResourceLocation.fromNamespaceAndPath(BlackArcanaMod.MOD_ID, "channel_begin_intent"));

    public static final StreamCodec<ByteBuf, ChannelBeginIntentPacket> STREAM_CODEC = StreamCodec.composite(
            ByteBufCodecs.VAR_INT, ChannelBeginIntentPacket::protocolVersion,
            ByteBufCodecs.stringUtf8(ArcanaProtocol.MAX_CAST_ID_LENGTH), ChannelBeginIntentPacket::castId,
            ByteBufCodecs.stringUtf8(ArcanaProtocol.MAX_RESOURCE_ID_LENGTH), ChannelBeginIntentPacket::spellId,
            ByteBufCodecs.VAR_INT, ChannelBeginIntentPacket::sourceSlot,
            ChannelBeginIntentPacket::new);

    public ChannelBeginIntentPacket {
        new ChannelBeginIntentPayload(protocolVersion, castId, spellId, sourceSlot);
    }

    public static ChannelBeginIntentPacket from(ChannelBeginIntentPayload payload) {
        Objects.requireNonNull(payload, "payload");
        return new ChannelBeginIntentPacket(
                payload.protocolVersion(),
                payload.castId(),
                payload.spellId(),
                payload.sourceSlot());
    }

    public ChannelBeginIntentPayload toDomain() {
        return new ChannelBeginIntentPayload(protocolVersion, castId, spellId, sourceSlot);
    }

    @Override
    public Type<? extends CustomPacketPayload> type() {
        return TYPE;
    }
}
