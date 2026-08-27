package dev.gustavopere.blackarcana.network.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.network.ArcanaProtocol;
import dev.gustavopere.blackarcana.network.CastIntentPayload;
import io.netty.buffer.ByteBuf;
import net.minecraft.network.codec.ByteBufCodecs;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.ResourceLocation;

import java.util.Objects;

/** Wire-only NeoForge representation of a minimal client cast intent. */
public record CastIntentPacket(
        int protocolVersion,
        String castId,
        String spellId,
        int loadoutSlot,
        String targetHint
) implements CustomPacketPayload {
    private static final int MAX_CAST_ID_LENGTH = 36;
    private static final int MAX_SPELL_ID_LENGTH = 192;

    public static final Type<CastIntentPacket> TYPE = new Type<>(
            ResourceLocation.fromNamespaceAndPath(BlackArcanaMod.MOD_ID, "cast_intent"));

    public static final StreamCodec<ByteBuf, CastIntentPacket> STREAM_CODEC = StreamCodec.composite(
            ByteBufCodecs.VAR_INT, CastIntentPacket::protocolVersion,
            ByteBufCodecs.stringUtf8(MAX_CAST_ID_LENGTH), CastIntentPacket::castId,
            ByteBufCodecs.stringUtf8(MAX_SPELL_ID_LENGTH), CastIntentPacket::spellId,
            ByteBufCodecs.VAR_INT, CastIntentPacket::loadoutSlot,
            ByteBufCodecs.stringUtf8(ArcanaProtocol.MAX_TARGET_HINT_LENGTH), CastIntentPacket::targetHint,
            CastIntentPacket::new);

    public CastIntentPacket {
        Objects.requireNonNull(castId, "castId");
        Objects.requireNonNull(spellId, "spellId");
        Objects.requireNonNull(targetHint, "targetHint");
        // Reuse the domain contract so wire and non-wire validation cannot drift.
        new CastIntentPayload(protocolVersion, castId, spellId, loadoutSlot, targetHint);
    }

    public static CastIntentPacket from(CastIntentPayload payload) {
        Objects.requireNonNull(payload, "payload");
        return new CastIntentPacket(
                payload.protocolVersion(), payload.castId(), payload.spellId(),
                payload.loadoutSlot(), payload.targetHint());
    }

    public CastIntentPayload toDomain() {
        return new CastIntentPayload(protocolVersion, castId, spellId, loadoutSlot, targetHint);
    }

    @Override
    public Type<? extends CustomPacketPayload> type() {
        return TYPE;
    }
}
