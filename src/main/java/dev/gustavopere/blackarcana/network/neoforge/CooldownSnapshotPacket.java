package dev.gustavopere.blackarcana.network.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.network.ArcanaProtocol;
import dev.gustavopere.blackarcana.network.CooldownSnapshotPayload;
import io.netty.buffer.ByteBuf;
import net.minecraft.network.codec.ByteBufCodecs;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.ResourceLocation;

import java.util.List;
import java.util.Objects;

public record CooldownSnapshotPacket(int protocolVersion, List<Entry> entries) implements CustomPacketPayload {
    private static final int MAX_GROUP_ID_LENGTH = 192;

    public static final Type<CooldownSnapshotPacket> TYPE = new Type<>(
            ResourceLocation.fromNamespaceAndPath(BlackArcanaMod.MOD_ID, "cooldown_snapshot"));

    private static final StreamCodec<ByteBuf, Entry> ENTRY_CODEC = StreamCodec.composite(
            ByteBufCodecs.stringUtf8(MAX_GROUP_ID_LENGTH), Entry::groupId,
            ByteBufCodecs.VAR_LONG, Entry::remainingTicks,
            Entry::new);

    public static final StreamCodec<ByteBuf, CooldownSnapshotPacket> STREAM_CODEC = StreamCodec.composite(
            ByteBufCodecs.VAR_INT, CooldownSnapshotPacket::protocolVersion,
            ENTRY_CODEC.apply(ByteBufCodecs.list(ArcanaProtocol.MAX_COOLDOWN_ENTRIES)), CooldownSnapshotPacket::entries,
            CooldownSnapshotPacket::new);

    public CooldownSnapshotPacket {
        Objects.requireNonNull(entries, "entries");
        entries = List.copyOf(entries);
        toDomain(protocolVersion, entries);
    }

    public static CooldownSnapshotPacket from(CooldownSnapshotPayload payload) {
        Objects.requireNonNull(payload, "payload");
        return new CooldownSnapshotPacket(
                payload.protocolVersion(),
                payload.entries().stream().map(entry -> new Entry(entry.groupId(), entry.remainingTicks())).toList());
    }

    public CooldownSnapshotPayload toDomain() {
        return toDomain(protocolVersion, entries);
    }

    private static CooldownSnapshotPayload toDomain(int version, List<Entry> entries) {
        return new CooldownSnapshotPayload(
                version,
                entries.stream().map(entry -> new CooldownSnapshotPayload.Entry(entry.groupId(), entry.remainingTicks())).toList());
    }

    @Override
    public Type<? extends CustomPacketPayload> type() {
        return TYPE;
    }

    public record Entry(String groupId, long remainingTicks) {
        public Entry {
            Objects.requireNonNull(groupId, "groupId");
            new CooldownSnapshotPayload.Entry(groupId, remainingTicks);
        }
    }
}
