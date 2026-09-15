package dev.gustavopere.blackarcana.network;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;

import java.util.Objects;

/** Client request to begin a server-owned channel session. */
public record ChannelBeginIntentPayload(
        int protocolVersion,
        String castId,
        String spellId,
        int loadoutSlot
) {
    public ChannelBeginIntentPayload {
        ArcanaProtocol.requireCompatible(protocolVersion);
        Objects.requireNonNull(castId, "castId");
        Objects.requireNonNull(spellId, "spellId");
        new CastIntentPayload(protocolVersion, castId, spellId, loadoutSlot, "");
    }

    public ArcanaCastId parsedCastId() {
        return ArcanaCastId.parse(castId);
    }

    public ArcanaSpellId parsedSpellId() {
        return ArcanaSpellId.parse(spellId);
    }

    public CastIntentPayload toCastIntent() {
        return new CastIntentPayload(protocolVersion, castId, spellId, loadoutSlot, "");
    }
}
