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
    double recommendedArcaneResistance
) implements CustomPacketPayload {
    public static final Type<HazardResistanceForecastPacket> TYPE = new Type<>(
        ResourceLocation.fromNamespaceAndPath(BlackArcanaMod.MOD_ID, "hazard_resistance_forecast"));

    public static final StreamCodec<ByteBuf, HazardResistanceForecastPacket> STREAM_CODEC = StreamCodec.composite(
        ByteBufCodecs.VAR_INT, HazardResistanceForecastPacket::protocolVersion,
        ByteBufCodecs.VAR_LONG, HazardResistanceForecastPacket::requestId,
        ByteBufCodecs.stringUtf8(ArcanaProtocol.MAX_RESOURCE_ID_LENGTH), HazardResistanceForecastPacket::spellId,
        ByteBufCodecs.BOOL, HazardResistanceForecastPacket::available,
        ByteBufCodecs.stringUtf8(ArcanaProtocol.MAX_RESULT_STATUS_LENGTH), HazardResistanceForecastPacket::status,
        ByteBufCodecs.stringUtf8(ArcanaProtocol.MAX_DANGER_TIER_LENGTH), HazardResistanceForecastPacket::dangerTier,
        ByteBufCodecs.DOUBLE, HazardResistanceForecastPacket::effectiveArcaneResistance,
        ByteBufCodecs.DOUBLE, HazardResistanceForecastPacket::minimumArcaneResistance,
        ByteBufCodecs.DOUBLE, HazardResistanceForecastPacket::recommendedArcaneResistance,
        HazardResistanceForecastPacket::new);

    public HazardResistanceForecastPacket {
        toDomain(protocolVersion, requestId, spellId, available, status, dangerTier,
            effectiveArcaneResistance, minimumArcaneResistance, recommendedArcaneResistance);
    }

    public static HazardResistanceForecastPacket from(HazardResistanceForecastPayload payload) {
        Objects.requireNonNull(payload, "payload");
        return new HazardResistanceForecastPacket(
            payload.protocolVersion(), payload.requestId(), payload.spellId(), payload.available(),
            payload.status(), payload.dangerTier(), payload.effectiveArcaneResistance(),
            payload.minimumArcaneResistance(), payload.recommendedArcaneResistance());
    }

    public HazardResistanceForecastPayload toDomain() {
        return toDomain(protocolVersion, requestId, spellId, available, status, dangerTier,
            effectiveArcaneResistance, minimumArcaneResistance, recommendedArcaneResistance);
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
        double recommended
    ) {
        return new HazardResistanceForecastPayload(
            version, requestId, spellId, available, status, dangerTier, effective, minimum, recommended);
    }

    @Override
    public Type<? extends CustomPacketPayload> type() {
        return TYPE;
    }
}
