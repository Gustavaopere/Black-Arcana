package dev.gustavopere.blackarcana.network.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.network.ArcanaProtocol;
import dev.gustavopere.blackarcana.network.HazardResistanceForecastPayload;
import io.netty.buffer.ByteBuf;
import net.minecraft.network.codec.ByteBufCodecs;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.ResourceLocation;

import java.util.Objects;

public record HazardResistanceForecastPacket(
    int protocolVersion,
    long requestId,
    String spellId,
    boolean available,
    String status,
    String dangerTier,
    double effectiveArcaneResistance,
    double minimumArcaneResistance,
    double recommendedArcaneResistance,
    boolean gateForecastAvailable,
    String gateStatus
) implements CustomPacketPayload {
    public static final Type<HazardResistanceForecastPacket> TYPE = new Type<>(
        ResourceLocation.fromNamespaceAndPath(BlackArcanaMod.MOD_ID, "hazard_resistance_forecast"));

    /** Explicit codec because vanilla StreamCodec.composite is bounded to six fields in 1.21.1. */
    public static final StreamCodec<ByteBuf, HazardResistanceForecastPacket> STREAM_CODEC = StreamCodec.of(
        (buffer, value) -> {
            ByteBufCodecs.VAR_INT.encode(buffer, value.protocolVersion());
            ByteBufCodecs.VAR_LONG.encode(buffer, value.requestId());
            ByteBufCodecs.stringUtf8(ArcanaProtocol.MAX_RESOURCE_ID_LENGTH).encode(buffer, value.spellId());
            ByteBufCodecs.BOOL.encode(buffer, value.available());
            ByteBufCodecs.stringUtf8(ArcanaProtocol.MAX_RESULT_STATUS_LENGTH).encode(buffer, value.status());
            ByteBufCodecs.stringUtf8(ArcanaProtocol.MAX_DANGER_TIER_LENGTH).encode(buffer, value.dangerTier());
            ByteBufCodecs.DOUBLE.encode(buffer, value.effectiveArcaneResistance());
            ByteBufCodecs.DOUBLE.encode(buffer, value.minimumArcaneResistance());
            ByteBufCodecs.DOUBLE.encode(buffer, value.recommendedArcaneResistance());
            ByteBufCodecs.BOOL.encode(buffer, value.gateForecastAvailable());
            ByteBufCodecs.stringUtf8(ArcanaProtocol.MAX_RESULT_STATUS_LENGTH).encode(buffer, value.gateStatus());
        },
        buffer -> new HazardResistanceForecastPacket(
            ByteBufCodecs.VAR_INT.decode(buffer),
            ByteBufCodecs.VAR_LONG.decode(buffer),
            ByteBufCodecs.stringUtf8(ArcanaProtocol.MAX_RESOURCE_ID_LENGTH).decode(buffer),
            ByteBufCodecs.BOOL.decode(buffer),
            ByteBufCodecs.stringUtf8(ArcanaProtocol.MAX_RESULT_STATUS_LENGTH).decode(buffer),
            ByteBufCodecs.stringUtf8(ArcanaProtocol.MAX_DANGER_TIER_LENGTH).decode(buffer),
            ByteBufCodecs.DOUBLE.decode(buffer),
            ByteBufCodecs.DOUBLE.decode(buffer),
            ByteBufCodecs.DOUBLE.decode(buffer),
            ByteBufCodecs.BOOL.decode(buffer),
            ByteBufCodecs.stringUtf8(ArcanaProtocol.MAX_RESULT_STATUS_LENGTH).decode(buffer)));

    public HazardResistanceForecastPacket {
        toDomain(protocolVersion, requestId, spellId, available, status, dangerTier,
            effectiveArcaneResistance, minimumArcaneResistance, recommendedArcaneResistance,
            gateForecastAvailable, gateStatus);
    }

    public static HazardResistanceForecastPacket from(HazardResistanceForecastPayload payload) {
        Objects.requireNonNull(payload, "payload");
        return new HazardResistanceForecastPacket(
            payload.protocolVersion(), payload.requestId(), payload.spellId(), payload.available(),
            payload.status(), payload.dangerTier(), payload.effectiveArcaneResistance(),
            payload.minimumArcaneResistance(), payload.recommendedArcaneResistance(),
            payload.gateForecastAvailable(), payload.gateStatus());
    }

    public HazardResistanceForecastPayload toDomain() {
        return toDomain(protocolVersion, requestId, spellId, available, status, dangerTier,
            effectiveArcaneResistance, minimumArcaneResistance, recommendedArcaneResistance,
            gateForecastAvailable, gateStatus);
    }

    private static HazardResistanceForecastPayload toDomain(
        int version,
        long requestId,
        String spellId,
        boolean available,
        String status,
        String dangerTier,
        double effective,
        double minimum,
        double recommended,
        boolean gateForecastAvailable,
        String gateStatus
    ) {
        return new HazardResistanceForecastPayload(
            version, requestId, spellId, available, status, dangerTier, effective, minimum, recommended,
            gateForecastAvailable, gateStatus);
    }

    @Override
    public Type<? extends CustomPacketPayload> type() {
        return TYPE;
    }
}
