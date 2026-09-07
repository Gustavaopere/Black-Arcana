package dev.gustavopere.blackarcana.network.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.content.noetic.NoeticObservationKind;
import dev.gustavopere.blackarcana.network.NoeticViewPayload;
import io.netty.buffer.ByteBuf;
import net.minecraft.network.codec.ByteBufCodecs;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.ResourceLocation;

import java.util.Objects;

public record NoeticViewPacket(
        int protocolVersion,
        String action,
        String kind,
        int targetEntityId
) implements CustomPacketPayload {
    private static final int MAX_ACTION_LENGTH = 8;
    private static final int MAX_KIND_LENGTH = 32;

    public static final Type<NoeticViewPacket> TYPE = new Type<>(
            ResourceLocation.fromNamespaceAndPath(BlackArcanaMod.MOD_ID, "noetic_view"));

    public static final StreamCodec<ByteBuf, NoeticViewPacket> STREAM_CODEC = StreamCodec.composite(
            ByteBufCodecs.VAR_INT, NoeticViewPacket::protocolVersion,
            ByteBufCodecs.stringUtf8(MAX_ACTION_LENGTH), NoeticViewPacket::action,
            ByteBufCodecs.stringUtf8(MAX_KIND_LENGTH), NoeticViewPacket::kind,
            ByteBufCodecs.VAR_INT, NoeticViewPacket::targetEntityId,
            NoeticViewPacket::new);

    public NoeticViewPacket {
        Objects.requireNonNull(action, "action");
        Objects.requireNonNull(kind, "kind");
        toDomain(protocolVersion, action, kind, targetEntityId);
    }

    public static NoeticViewPacket from(NoeticViewPayload payload) {
        Objects.requireNonNull(payload, "payload");
        return new NoeticViewPacket(
                payload.protocolVersion(),
                payload.action().name(),
                payload.kind().name(),
                payload.targetEntityId());
    }

    public NoeticViewPayload toDomain() {
        return toDomain(protocolVersion, action, kind, targetEntityId);
    }

    private static NoeticViewPayload toDomain(
            int protocolVersion,
            String action,
            String kind,
            int targetEntityId
    ) {
        return new NoeticViewPayload(
                protocolVersion,
                NoeticViewPayload.Action.valueOf(action),
                NoeticObservationKind.valueOf(kind),
                targetEntityId);
    }

    @Override
    public Type<? extends CustomPacketPayload> type() {
        return TYPE;
    }
}
