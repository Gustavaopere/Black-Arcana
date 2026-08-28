package dev.gustavopere.blackarcana.network.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.network.ArcanaProtocol;
import dev.gustavopere.blackarcana.network.LoadoutSnapshotPayload;
import io.netty.buffer.ByteBuf;
import net.minecraft.network.codec.ByteBufCodecs;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.ResourceLocation;

import java.util.List;
import java.util.Objects;

public record LoadoutSnapshotPacket(int protocolVersion, List<String> spellIds) implements CustomPacketPayload {
    public static final Type<LoadoutSnapshotPacket> TYPE = new Type<>(
            ResourceLocation.fromNamespaceAndPath(BlackArcanaMod.MOD_ID, "loadout_snapshot"));
    public static final StreamCodec<ByteBuf, LoadoutSnapshotPacket> STREAM_CODEC = StreamCodec.composite(
            ByteBufCodecs.VAR_INT, LoadoutSnapshotPacket::protocolVersion,
            ByteBufCodecs.stringUtf8(ArcanaProtocol.MAX_RESOURCE_ID_LENGTH)
                    .apply(ByteBufCodecs.list(ArcanaProtocol.MAX_LOADOUT_SLOTS)), LoadoutSnapshotPacket::spellIds,
            LoadoutSnapshotPacket::new);

    public LoadoutSnapshotPacket {
        Objects.requireNonNull(spellIds, "spellIds");
        spellIds = List.copyOf(spellIds);
        new LoadoutSnapshotPayload(protocolVersion, spellIds);
    }

    public static LoadoutSnapshotPacket from(LoadoutSnapshotPayload payload) {
        return new LoadoutSnapshotPacket(payload.protocolVersion(), payload.spellIds());
    }

    public LoadoutSnapshotPayload toDomain() {
        return new LoadoutSnapshotPayload(protocolVersion, spellIds);
    }

    @Override
    public Type<? extends CustomPacketPayload> type() {
        return TYPE;
    }
}
