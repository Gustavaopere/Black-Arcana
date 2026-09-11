package dev.gustavopere.blackarcana.network.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.network.ArcanaProtocol;
import dev.gustavopere.blackarcana.network.AstralProjectionViewPayload;
import io.netty.buffer.ByteBuf;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.ResourceLocation;

import java.util.Objects;
import java.util.UUID;

/** Server-authored BEGIN/END presentation for one exact Astral projection. */
public record AstralProjectionViewPacket(
        int protocolVersion,
        String action,
        UUID projectionId,
        int projectionEntityId
) implements CustomPacketPayload {
    public static final Type<AstralProjectionViewPacket> TYPE = new Type<>(
            ResourceLocation.fromNamespaceAndPath(BlackArcanaMod.MOD_ID, "astral_projection_view"));
    public static final StreamCodec<ByteBuf, AstralProjectionViewPacket> STREAM_CODEC = StreamCodec.of(
            AstralProjectionViewPacket::encode,
            AstralProjectionViewPacket::decode);

    public AstralProjectionViewPacket {
        Objects.requireNonNull(action, "action");
        Objects.requireNonNull(projectionId, "projectionId");
        toDomain(protocolVersion, action, projectionId, projectionEntityId);
    }

    public static AstralProjectionViewPacket from(AstralProjectionViewPayload payload) {
        Objects.requireNonNull(payload, "payload");
        return new AstralProjectionViewPacket(
                payload.protocolVersion(),
                payload.action().name(),
                payload.projectionId(),
                payload.projectionEntityId());
    }

    public AstralProjectionViewPayload toDomain() {
        return toDomain(protocolVersion, action, projectionId, projectionEntityId);
    }

    private static AstralProjectionViewPayload toDomain(
            int protocolVersion,
            String action,
            UUID projectionId,
            int projectionEntityId
    ) {
        return new AstralProjectionViewPayload(
                protocolVersion,
                AstralProjectionViewPayload.Action.valueOf(action),
                projectionId,
                projectionEntityId);
    }

    private static void encode(ByteBuf buffer, AstralProjectionViewPacket packet) {
        buffer.writeInt(packet.protocolVersion);
        buffer.writeByte(packet.toDomain().action() == AstralProjectionViewPayload.Action.BEGIN ? 0 : 1);
        AstralProjectionMovePacket.writeUuid(buffer, packet.projectionId);
        buffer.writeInt(packet.projectionEntityId);
    }

    private static AstralProjectionViewPacket decode(ByteBuf buffer) {
        int protocolVersion = buffer.readInt();
        int actionCode = buffer.readUnsignedByte();
        String action = switch (actionCode) {
            case 0 -> AstralProjectionViewPayload.Action.BEGIN.name();
            case 1 -> AstralProjectionViewPayload.Action.END.name();
            default -> throw new IllegalArgumentException("Unknown Astral projection view action: " + actionCode);
        };
        return new AstralProjectionViewPacket(
                protocolVersion,
                action,
                AstralProjectionMovePacket.readUuid(buffer),
                buffer.readInt());
    }

    @Override
    public Type<? extends CustomPacketPayload> type() {
        return TYPE;
    }
}
