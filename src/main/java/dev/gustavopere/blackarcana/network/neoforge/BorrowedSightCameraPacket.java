package dev.gustavopere.blackarcana.network.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.network.ArcanaProtocol;
import dev.gustavopere.blackarcana.network.BorrowedSightCameraPayload;
import io.netty.buffer.ByteBuf;
import net.minecraft.network.codec.ByteBufCodecs;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.ResourceLocation;

import java.util.Objects;
import java.util.UUID;

/** Wire-only S2C camera presentation command for Borrowed Sight. */
public record BorrowedSightCameraPacket(
        int protocolVersion,
        boolean active,
        int entityId,
        String targetId
) implements CustomPacketPayload {
    public static final Type<BorrowedSightCameraPacket> TYPE = new Type<>(
        ResourceLocation.fromNamespaceAndPath(BlackArcanaMod.MOD_ID, "borrowed_sight_camera"));

    public static final StreamCodec<ByteBuf, BorrowedSightCameraPacket> STREAM_CODEC = StreamCodec.composite(
        ByteBufCodecs.VAR_INT, BorrowedSightCameraPacket::protocolVersion,
        ByteBufCodecs.BOOL, BorrowedSightCameraPacket::active,
        ByteBufCodecs.VAR_INT, BorrowedSightCameraPacket::entityId,
        ByteBufCodecs.stringUtf8(36), BorrowedSightCameraPacket::targetId,
        BorrowedSightCameraPacket::new);

    public BorrowedSightCameraPacket {
        Objects.requireNonNull(targetId, "targetId");
        toDomain(protocolVersion, active, entityId, targetId);
    }

    public static BorrowedSightCameraPacket from(BorrowedSightCameraPayload payload) {
        Objects.requireNonNull(payload, "payload");
        return new BorrowedSightCameraPacket(
            ArcanaProtocol.VERSION,
            payload.active(),
            payload.entityId(),
            payload.targetId().toString());
    }

    public BorrowedSightCameraPayload toDomain() {
        return toDomain(protocolVersion, active, entityId, targetId);
    }

    private static BorrowedSightCameraPayload toDomain(
            int protocolVersion,
            boolean active,
            int entityId,
            String targetId
    ) {
        ArcanaProtocol.requireCompatible(protocolVersion);
        UUID parsed;
        try {
            parsed = UUID.fromString(targetId);
        } catch (IllegalArgumentException invalid) {
            throw new IllegalArgumentException("invalid Borrowed Sight camera target UUID", invalid);
        }
        return new BorrowedSightCameraPayload(active, entityId, parsed);
    }

    @Override
    public Type<? extends CustomPacketPayload> type() {
        return TYPE;
    }
}
