package dev.gustavopere.blackarcana.network.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.network.ArcanaProtocol;
import dev.gustavopere.blackarcana.network.HazardPreflightPayload;
import io.netty.buffer.ByteBuf;
import net.minecraft.network.codec.ByteBufCodecs;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.ResourceLocation;

import java.util.List;
import java.util.Objects;

public record HazardPreflightPacket(int protocolVersion, List<Entry> entries) implements CustomPacketPayload {
    public static final Type<HazardPreflightPacket> TYPE = new Type<>(
            ResourceLocation.fromNamespaceAndPath(BlackArcanaMod.MOD_ID, "hazard_preflight"));

    private static final StreamCodec<ByteBuf, Entry> ENTRY_CODEC = StreamCodec.composite(
            ByteBufCodecs.stringUtf8(ArcanaProtocol.MAX_RESOURCE_ID_LENGTH), Entry::spellId,
            ByteBufCodecs.stringUtf8(ArcanaProtocol.MAX_DANGER_TIER_LENGTH), Entry::dangerTier,
            ByteBufCodecs.DOUBLE, Entry::minimumArcaneResistance,
            ByteBufCodecs.DOUBLE, Entry::recommendedArcaneResistance,
            Entry::new);

    public static final StreamCodec<ByteBuf, HazardPreflightPacket> STREAM_CODEC = StreamCodec.composite(
            ByteBufCodecs.VAR_INT, HazardPreflightPacket::protocolVersion,
            ENTRY_CODEC.apply(ByteBufCodecs.list(ArcanaProtocol.MAX_HAZARD_PREFLIGHT_ENTRIES)), HazardPreflightPacket::entries,
            HazardPreflightPacket::new);

    public HazardPreflightPacket {
        Objects.requireNonNull(entries, "entries");
        entries = List.copyOf(entries);
        toDomain(protocolVersion, entries);
    }

    public static HazardPreflightPacket from(HazardPreflightPayload payload) {
        Objects.requireNonNull(payload, "payload");
        return new HazardPreflightPacket(
                payload.protocolVersion(),
                payload.entries().stream()
                        .map(entry -> new Entry(
                                entry.spellId(),
                                entry.dangerTier(),
                                entry.minimumArcaneResistance(),
                                entry.recommendedArcaneResistance()))
                        .toList());
    }

    public HazardPreflightPayload toDomain() {
        return toDomain(protocolVersion, entries);
    }

    private static HazardPreflightPayload toDomain(int version, List<Entry> entries) {
        return new HazardPreflightPayload(
                version,
                entries.stream()
                        .map(entry -> new HazardPreflightPayload.Entry(
                                entry.spellId(),
                                entry.dangerTier(),
                                entry.minimumArcaneResistance(),
                                entry.recommendedArcaneResistance()))
                        .toList());
    }

    @Override
    public Type<? extends CustomPacketPayload> type() {
        return TYPE;
    }

    public record Entry(
            String spellId,
            String dangerTier,
            double minimumArcaneResistance,
            double recommendedArcaneResistance
    ) {
        public Entry {
            new HazardPreflightPayload.Entry(
                    spellId, dangerTier, minimumArcaneResistance, recommendedArcaneResistance);
        }
    }
}
