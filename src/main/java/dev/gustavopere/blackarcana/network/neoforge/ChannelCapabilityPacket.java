package dev.gustavopere.blackarcana.network.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.network.ArcanaProtocol;
import dev.gustavopere.blackarcana.network.ChannelCapabilityPayload;
import io.netty.buffer.ByteBuf;
import net.minecraft.network.codec.ByteBufCodecs;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.ResourceLocation;

import java.util.List;
import java.util.Objects;

/** Wire-only S2C snapshot of spells that support server-authoritative channel invocation. */
public record ChannelCapabilityPacket(
        int protocolVersion,
        List<Entry> entries
) implements CustomPacketPayload {
    public static final Type<ChannelCapabilityPacket> TYPE = new Type<>(
            ResourceLocation.fromNamespaceAndPath(BlackArcanaMod.MOD_ID, "channel_capability"));

    private static final StreamCodec<ByteBuf, Entry> ENTRY_CODEC = StreamCodec.composite(
            ByteBufCodecs.stringUtf8(ArcanaProtocol.MAX_RESOURCE_ID_LENGTH), Entry::spellId,
            ByteBufCodecs.VAR_LONG, Entry::minimumTicks,
            ByteBufCodecs.VAR_LONG, Entry::maximumTicks,
            Entry::new);

    public static final StreamCodec<ByteBuf, ChannelCapabilityPacket> STREAM_CODEC = StreamCodec.composite(
            ByteBufCodecs.VAR_INT, ChannelCapabilityPacket::protocolVersion,
            ENTRY_CODEC.apply(ByteBufCodecs.list(ChannelCapabilityPayload.MAX_ENTRIES)), ChannelCapabilityPacket::entries,
            ChannelCapabilityPacket::new);

    public ChannelCapabilityPacket {
        Objects.requireNonNull(entries, "entries");
        entries = List.copyOf(entries);
        toDomain(protocolVersion, entries);
    }

    public static ChannelCapabilityPacket from(ChannelCapabilityPayload payload) {
        Objects.requireNonNull(payload, "payload");
        return new ChannelCapabilityPacket(
                payload.protocolVersion(),
                payload.entries().stream()
                        .map(entry -> new Entry(entry.spellId(), entry.minimumTicks(), entry.maximumTicks()))
                        .toList());
    }

    public ChannelCapabilityPayload toDomain() {
        return toDomain(protocolVersion, entries);
    }

    private static ChannelCapabilityPayload toDomain(int version, List<Entry> entries) {
        return new ChannelCapabilityPayload(
                version,
                entries.stream()
                        .map(entry -> new ChannelCapabilityPayload.Entry(
                                entry.spellId(), entry.minimumTicks(), entry.maximumTicks()))
                        .toList());
    }

    @Override
    public Type<? extends CustomPacketPayload> type() {
        return TYPE;
    }

    public record Entry(String spellId, long minimumTicks, long maximumTicks) {
        public Entry {
            new ChannelCapabilityPayload.Entry(spellId, minimumTicks, maximumTicks);
        }
    }
}
