package dev.gustavopere.blackarcana.network.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.network.AstralViewPayload;
import io.netty.buffer.ByteBuf;
import net.minecraft.core.UUIDUtil;
import net.minecraft.network.codec.ByteBufCodecs;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.ResourceLocation;

import java.util.Objects;
import java.util.UUID;

/** Wire-only S2C representation of an exact-session Astral Severance camera instruction. */
public record AstralViewPacket(
        int protocolVersion,
        String action,
        UUID projectionId,
        int entityId
) implements CustomPacketPayload {
    private static final int MAX_ACTION_LENGTH = 8;

    public static final Type<AstralViewPacket> TYPE = new Type<>(
            ResourceLocation.fromNamespaceAndPath(BlackArcanaMod.MOD_ID, "astral_view"));
    public static final StreamCodec<ByteBuf, AstralViewPacket> STREAM_CODEC = StreamCodec.composite(
            ByteBufCodecs.VAR_INT, AstralViewPacket::protocolVersion,
            ByteBufCodecs.stringUtf8(MAX_ACTION_LENGTH), AstralViewPacket::action,
            UUIDUtil.STREAM_CODEC, AstralViewPacket::projectionId,
            ByteBufCodecs.VAR_INT, AstralViewPacket::entityId,
            AstralViewPacket::new);

    public AstralViewPacket {
        Objects.requireNonNull(action, "action");
        Objects.requireNonNull(projectionId, "projectionId");
        toDomain(protocolVersion, action, projectionId, entityId);
    }

    public static AstralViewPacket from(AstralViewPayload payload) {
        Objects.requireNonNull(payload, "payload");
        return new AstralViewPacket(
                payload.protocolVersion(),
                payload.action().name(),
                payload.projectionId(),
                payload.entityId());
    }

    public AstralViewPayload toDomain() {
        return toDomain(protocolVersion, action, projectionId, entityId);
    }

    private static AstralViewPayload toDomain(
            int protocolVersion,
            String action,
            UUID projectionId,
            int entityId
    ) {
        return new AstralViewPayload(
                protocolVersion,
                AstralViewPayload.Action.valueOf(action),
                projectionId,
                entityId);
    }

    @Override
    public Type<? extends CustomPacketPayload> type() {
        return TYPE;
    }
}
