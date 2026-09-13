package dev.gustavopere.blackarcana.network.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.network.AstralMoveIntentPayload;
import io.netty.buffer.ByteBuf;
import net.minecraft.core.UUIDUtil;
import net.minecraft.network.codec.ByteBufCodecs;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.ResourceLocation;

import java.util.Objects;
import java.util.UUID;

/** Wire-only C2S representation of bounded Astral Severance movement/look intent. */
public record AstralMoveIntentPacket(
        int protocolVersion,
        UUID projectionId,
        long sequence,
        MovementAxes movement,
        LookDeltas look
) implements CustomPacketPayload {
    public static final Type<AstralMoveIntentPacket> TYPE = new Type<>(
            ResourceLocation.fromNamespaceAndPath(BlackArcanaMod.MOD_ID, "astral_move_intent"));

    public static final StreamCodec<ByteBuf, AstralMoveIntentPacket> STREAM_CODEC = StreamCodec.composite(
            ByteBufCodecs.VAR_INT, AstralMoveIntentPacket::protocolVersion,
            UUIDUtil.STREAM_CODEC, AstralMoveIntentPacket::projectionId,
            ByteBufCodecs.VAR_LONG, AstralMoveIntentPacket::sequence,
            MovementAxes.STREAM_CODEC, AstralMoveIntentPacket::movement,
            LookDeltas.STREAM_CODEC, AstralMoveIntentPacket::look,
            AstralMoveIntentPacket::new);

    public AstralMoveIntentPacket {
        Objects.requireNonNull(projectionId, "projectionId");
        Objects.requireNonNull(movement, "movement");
        Objects.requireNonNull(look, "look");
        new AstralMoveIntentPayload(
                protocolVersion,
                projectionId,
                sequence,
                movement.strafeAxis(),
                movement.verticalAxis(),
                movement.forwardAxis(),
                look.yawDeltaDegrees(),
                look.pitchDeltaDegrees());
    }

    public static AstralMoveIntentPacket from(AstralMoveIntentPayload payload) {
        Objects.requireNonNull(payload, "payload");
        return new AstralMoveIntentPacket(
                payload.protocolVersion(),
                payload.projectionId(),
                payload.sequence(),
                new MovementAxes(payload.strafeAxis(), payload.verticalAxis(), payload.forwardAxis()),
                new LookDeltas(payload.yawDeltaDegrees(), payload.pitchDeltaDegrees()));
    }

    public AstralMoveIntentPayload toDomain() {
        return new AstralMoveIntentPayload(
                protocolVersion,
                projectionId,
                sequence,
                movement.strafeAxis(),
                movement.verticalAxis(),
                movement.forwardAxis(),
                look.yawDeltaDegrees(),
                look.pitchDeltaDegrees());
    }

    @Override
    public Type<? extends CustomPacketPayload> type() {
        return TYPE;
    }

    public record MovementAxes(double strafeAxis, double verticalAxis, double forwardAxis) {
        private static final StreamCodec<ByteBuf, MovementAxes> STREAM_CODEC = StreamCodec.composite(
                ByteBufCodecs.DOUBLE, MovementAxes::strafeAxis,
                ByteBufCodecs.DOUBLE, MovementAxes::verticalAxis,
                ByteBufCodecs.DOUBLE, MovementAxes::forwardAxis,
                MovementAxes::new);
    }

    public record LookDeltas(float yawDeltaDegrees, float pitchDeltaDegrees) {
        private static final StreamCodec<ByteBuf, LookDeltas> STREAM_CODEC = StreamCodec.composite(
                ByteBufCodecs.FLOAT, LookDeltas::yawDeltaDegrees,
                ByteBufCodecs.FLOAT, LookDeltas::pitchDeltaDegrees,
                LookDeltas::new);
    }
}
