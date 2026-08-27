package dev.gustavopere.blackarcana.network;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;

import java.util.Objects;

public record CastIntentPayload(
        int protocolVersion,
        String castId,
        String spellId,
        int loadoutSlot,
        String targetHint
) {
    public CastIntentPayload {
        ArcanaProtocol.requireCompatible(protocolVersion);
        Objects.requireNonNull(castId, "castId");
        Objects.requireNonNull(spellId, "spellId");
        Objects.requireNonNull(targetHint, "targetHint");
        ArcanaCastId.parse(castId);
        ArcanaSpellId.parse(spellId);
        if (loadoutSlot < 0 || loadoutSlot >= ArcanaProtocol.MAX_LOADOUT_SLOTS) {
            throw new IllegalArgumentException("loadoutSlot out of bounds");
        }
        if (targetHint.length() > ArcanaProtocol.MAX_TARGET_HINT_LENGTH) {
            throw new IllegalArgumentException("targetHint exceeds protocol bound");
        }
    }

    public ArcanaCastId parsedCastId() {
        return ArcanaCastId.parse(castId);
    }

    public ArcanaSpellId parsedSpellId() {
        return ArcanaSpellId.parse(spellId);
    }
}
