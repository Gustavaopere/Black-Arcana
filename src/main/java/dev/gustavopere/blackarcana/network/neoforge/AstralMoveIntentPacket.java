package dev.gustavopere.blackarcana.network.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.network.AstralMoveIntentPayload;
import io.netty.buffer.ByteBuf;
import net.minecraft.network.codec.ByteBufCodecs;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.ResourceLocation;

import java.util.Objects;
import java.util.UUID;

/** Wire-only C2S representation of bounded Astral Severance movement/look intent. */
public record AstralMoveIntentPacket(
        int protocolVersion,
        long projectionMostSignificantBits,
        long projectionLeastSignificantBits,
        long sequence,
        double strafeAxis,
        double verticalAxis,
        double forwardAxis,
        float yawDeltaDegrees,
        float pitchDeltaDegrees
) implements CustomPacketPayload {
    public static final Type<AstralMoveIntentPacket> TYPE = new Type<>(
            ResourceLocation.fromNamespaceAndPath(BlackArcanaMod.MOD_ID, "astral_move_intent"));

    public static final StreamCodec<ByteBuf, AstralMoveIntentPacket> STREAM_CODEC = StreamCodec.composite(
            ByteBufCodecs.VAR_INT, AstralMoveIntentPacket::protocolVersion,
            ByteBufCodecs.LONG, AstralMoveIntentPacket::projectionMostSignificantBits,
            ByteBufCodecs.LONG, AstralMoveIntentPacket::projectionLeastSignificantBits,
            ByteBufCodecs.LONG, AstralMoveIntentPacket::sequence,
            ByteBufCodecs.DOUBLE, AstralMoveIntentPacket::strafeAxis,
            ByteBufCodecs.DOUBLE, AstralMoveIntentPacket::verticalAxis,
            ByteBufCodecs.DOUBLE, AstralMoveIntentPacket::forwardAxis,
            ByteBufCodecs.FLOAT, AstralMoveIntentPacket::yawDeltaDegrees,
            ByteBufCodecs.FLOAT, AstralMoveIntentPacket::pitchDeltaDegrees,
            AstralMoveIntentPacket::new);

    public AstralMoveIntentPacket {
        new AstralMoveIntentPayload(
                protocolVersion,
                new UUID(projectionMostSignificantBits, projectionLeastSignificantBits),
                sequence,
                strafeAxis,
                verticalAxis,
                forwardAxis,
                yawDeltaDegrees,
                pitchDeltaDegrees);
    }

    public static AstralMoveIntentPacket from(AstralMoveIntentPayload payload) {
        Objects.requireNonNull(payload, "payload");
        return new AstralMoveIntentPacket(
                payload.protocolVersion(),
                payload.projectionId().getMostSignificantBits(),
                payload.projectionId().getLeastSignificantBits(),
                payload.sequence(),
                payload.strafeAxis(),
                payload.verticalAxis(),
                payload.forwardAxis(),
                payload.yawDeltaDegrees(),
                payload.pitchDeltaDegrees());
    }

    public AstralMoveIntentPayload toDomain() {
        return new AstralMoveIntentPayload(
                protocolVersion,
                new UUID(projectionMostSignificantBits, projectionLeastSignificantBits),
                sequence,
                strafeAxis,
                verticalAxis,
                forwardAxis,
                yawDeltaDegrees,
                pitchDeltaDegrees);
    }

    @Override
    public Type<? extends CustomPacketPayload> type() {
        return TYPE;
    }
}
