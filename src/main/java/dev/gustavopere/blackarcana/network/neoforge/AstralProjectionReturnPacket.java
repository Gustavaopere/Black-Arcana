package dev.gustavopere.blackarcana.network.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.network.ArcanaProtocol;
import io.netty.buffer.ByteBuf;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.ResourceLocation;

import java.util.Objects;
import java.util.UUID;

/** Exact-session client request to return from an already-active Astral projection. */
public record AstralProjectionReturnPacket(
        int protocolVersion,
        UUID projectionId
) implements CustomPacketPayload {
    public static final Type<AstralProjectionReturnPacket> TYPE = new Type<>(
            ResourceLocation.fromNamespaceAndPath(BlackArcanaMod.MOD_ID, "astral_projection_return"));
    public static final StreamCodec<ByteBuf, AstralProjectionReturnPacket> STREAM_CODEC = StreamCodec.of(
            AstralProjectionReturnPacket::encode,
            AstralProjectionReturnPacket::decode);

    public AstralProjectionReturnPacket {
        ArcanaProtocol.requireCompatible(protocolVersion);
        Objects.requireNonNull(projectionId, "projectionId");
    }

    public static AstralProjectionReturnPacket from(UUID projectionId) {
        return new AstralProjectionReturnPacket(ArcanaProtocol.VERSION, projectionId);
    }

    private static void encode(ByteBuf buffer, AstralProjectionReturnPacket packet) {
        buffer.writeInt(packet.protocolVersion);
        AstralProjectionMovePacket.writeUuid(buffer, packet.projectionId);
    }

    private static AstralProjectionReturnPacket decode(ByteBuf buffer) {
        return new AstralProjectionReturnPacket(
                buffer.readInt(),
                AstralProjectionMovePacket.readUuid(buffer));
    }

    @Override
    public Type<? extends CustomPacketPayload> type() {
        return TYPE;
    }
}
