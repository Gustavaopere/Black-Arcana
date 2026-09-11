package dev.gustavopere.blackarcana.network.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.content.noetic.AstralProjectionMovementIntent;
import dev.gustavopere.blackarcana.network.ArcanaProtocol;
import io.netty.buffer.ByteBuf;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.ResourceLocation;

import java.util.UUID;

/** Bounded client movement/look intent for one exact server-authored Astral session. */
public record AstralProjectionMovePacket(
        int protocolVersion,
        UUID projectionId,
        long sequence,
        float strafe,
        float forward,
        float vertical,
        float yaw,
        float pitch
) implements CustomPacketPayload {
    public static final Type<AstralProjectionMovePacket> TYPE = new Type<>(
            ResourceLocation.fromNamespaceAndPath(BlackArcanaMod.MOD_ID, "astral_projection_move"));
    public static final StreamCodec<ByteBuf, AstralProjectionMovePacket> STREAM_CODEC = StreamCodec.of(
            AstralProjectionMovePacket::encode,
            AstralProjectionMovePacket::decode);

    public AstralProjectionMovePacket {
        ArcanaProtocol.requireCompatible(protocolVersion);
        AstralProjectionMovementIntent intent = new AstralProjectionMovementIntent(
                projectionId, sequence, strafe, forward, vertical, yaw, pitch);
        if (!intent.axesWithinUnitBounds()) {
            throw new IllegalArgumentException("Astral projection movement axes exceed the bounded wire contract");
        }
    }

    public static AstralProjectionMovePacket from(AstralProjectionMovementIntent intent) {
        return new AstralProjectionMovePacket(
                ArcanaProtocol.VERSION,
                intent.projectionId(),
                intent.sequence(),
                intent.strafe(),
                intent.forward(),
                intent.vertical(),
                intent.yaw(),
                intent.pitch());
    }

    public AstralProjectionMovementIntent toIntent() {
        return new AstralProjectionMovementIntent(
                projectionId, sequence, strafe, forward, vertical, yaw, pitch);
    }

    private static void encode(ByteBuf buffer, AstralProjectionMovePacket packet) {
        buffer.writeInt(packet.protocolVersion);
        writeUuid(buffer, packet.projectionId);
        buffer.writeLong(packet.sequence);
        buffer.writeFloat(packet.strafe);
        buffer.writeFloat(packet.forward);
        buffer.writeFloat(packet.vertical);
        buffer.writeFloat(packet.yaw);
        buffer.writeFloat(packet.pitch);
    }

    private static AstralProjectionMovePacket decode(ByteBuf buffer) {
        return new AstralProjectionMovePacket(
                buffer.readInt(),
                readUuid(buffer),
                buffer.readLong(),
                buffer.readFloat(),
                buffer.readFloat(),
                buffer.readFloat(),
                buffer.readFloat(),
                buffer.readFloat());
    }

    static void writeUuid(ByteBuf buffer, UUID value) {
        buffer.writeLong(value.getMostSignificantBits());
        buffer.writeLong(value.getLeastSignificantBits());
    }

    static UUID readUuid(ByteBuf buffer) {
        return new UUID(buffer.readLong(), buffer.readLong());
    }

    @Override
    public Type<? extends CustomPacketPayload> type() {
        return TYPE;
    }
}
