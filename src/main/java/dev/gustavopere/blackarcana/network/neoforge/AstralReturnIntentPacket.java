package dev.gustavopere.blackarcana.network.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.network.AstralReturnIntentPayload;
import io.netty.buffer.ByteBuf;
import net.minecraft.network.codec.ByteBufCodecs;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.ResourceLocation;

import java.util.Objects;
import java.util.UUID;

/** Wire-only C2S representation of an exact-session Astral Severance return intent. */
public record AstralReturnIntentPacket(
        int protocolVersion,
        long projectionMostSignificantBits,
        long projectionLeastSignificantBits,
        long sequence
) implements CustomPacketPayload {
    public static final Type<AstralReturnIntentPacket> TYPE = new Type<>(
            ResourceLocation.fromNamespaceAndPath(BlackArcanaMod.MOD_ID, "astral_return_intent"));

    public static final StreamCodec<ByteBuf, AstralReturnIntentPacket> STREAM_CODEC = StreamCodec.composite(
            ByteBufCodecs.VAR_INT, AstralReturnIntentPacket::protocolVersion,
            ByteBufCodecs.LONG, AstralReturnIntentPacket::projectionMostSignificantBits,
            ByteBufCodecs.LONG, AstralReturnIntentPacket::projectionLeastSignificantBits,
            ByteBufCodecs.LONG, AstralReturnIntentPacket::sequence,
            AstralReturnIntentPacket::new);

    public AstralReturnIntentPacket {
        new AstralReturnIntentPayload(
                protocolVersion,
                new UUID(projectionMostSignificantBits, projectionLeastSignificantBits),
                sequence);
    }

    public static AstralReturnIntentPacket from(AstralReturnIntentPayload payload) {
        Objects.requireNonNull(payload, "payload");
        return new AstralReturnIntentPacket(
                payload.protocolVersion(),
                payload.projectionId().getMostSignificantBits(),
                payload.projectionId().getLeastSignificantBits(),
                payload.sequence());
    }

    public AstralReturnIntentPayload toDomain() {
        return new AstralReturnIntentPayload(
                protocolVersion,
                new UUID(projectionMostSignificantBits, projectionLeastSignificantBits),
                sequence);
    }

    @Override
    public Type<? extends CustomPacketPayload> type() {
        return TYPE;
    }
}
