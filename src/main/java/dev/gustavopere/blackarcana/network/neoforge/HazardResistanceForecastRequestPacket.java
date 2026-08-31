package dev.gustavopere.blackarcana.network.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.network.ArcanaProtocol;
import dev.gustavopere.blackarcana.network.HazardResistanceForecastRequestPayload;
import io.netty.buffer.ByteBuf;
import net.minecraft.network.codec.ByteBufCodecs;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.ResourceLocation;

import java.util.Objects;

public record HazardResistanceForecastRequestPacket(
    int protocolVersion,
    long requestId,
    String spellId
) implements CustomPacketPayload {
    public static final Type<HazardResistanceForecastRequestPacket> TYPE = new Type<>(
        ResourceLocation.fromNamespaceAndPath(BlackArcanaMod.MOD_ID, "hazard_resistance_forecast_request"));

    public static final StreamCodec<ByteBuf, HazardResistanceForecastRequestPacket> STREAM_CODEC = StreamCodec.composite(
        ByteBufCodecs.VAR_INT, HazardResistanceForecastRequestPacket::protocolVersion,
        ByteBufCodecs.VAR_LONG, HazardResistanceForecastRequestPacket::requestId,
        ByteBufCodecs.stringUtf8(ArcanaProtocol.MAX_RESOURCE_ID_LENGTH), HazardResistanceForecastRequestPacket::spellId,
        HazardResistanceForecastRequestPacket::new);

    public HazardResistanceForecastRequestPacket {
        toDomain(protocolVersion, requestId, spellId);
    }

    public static HazardResistanceForecastRequestPacket from(HazardResistanceForecastRequestPayload payload) {
        Objects.requireNonNull(payload, "payload");
        return new HazardResistanceForecastRequestPacket(
            payload.protocolVersion(), payload.requestId(), payload.spellId());
    }

    public HazardResistanceForecastRequestPayload toDomain() {
        return toDomain(protocolVersion, requestId, spellId);
    }

    private static HazardResistanceForecastRequestPayload toDomain(int version, long requestId, String spellId) {
        return new HazardResistanceForecastRequestPayload(version, requestId, spellId);
    }

    @Override
    public Type<? extends CustomPacketPayload> type() {
        return TYPE;
    }
}
