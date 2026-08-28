package dev.gustavopere.blackarcana.api;

import java.util.Objects;

public record ArcanaCastRequest(
        ArcanaCastId castId,
        ArcanaSpellDefinition spell,
        ArcanaCastContext context,
        int loadoutSlot,
        String targetHint,
        long channelTicks
) {
    public static final int MAX_LOADOUT_SLOTS = 16;
    public static final int MAX_TARGET_HINT_LENGTH = 96;

    public ArcanaCastRequest {
        Objects.requireNonNull(castId, "castId");
        Objects.requireNonNull(spell, "spell");
        Objects.requireNonNull(context, "context");
        Objects.requireNonNull(targetHint, "targetHint");
        if (loadoutSlot < 0 || loadoutSlot >= MAX_LOADOUT_SLOTS) {
            throw new IllegalArgumentException("loadoutSlot must be between 0 and " + (MAX_LOADOUT_SLOTS - 1));
        }
        if (targetHint.length() > MAX_TARGET_HINT_LENGTH) {
            throw new IllegalArgumentException("targetHint exceeds request bound");
        }
        if (channelTicks < 0L || channelTicks > ArcanaChannelSpec.ABSOLUTE_MAX_CHANNEL_TICKS) {
            throw new IllegalArgumentException("channelTicks outside absolute channel bounds");
        }
    }

    public ArcanaCastRequest(
            ArcanaCastId castId,
            ArcanaSpellDefinition spell,
            ArcanaCastContext context,
            int loadoutSlot,
            String targetHint
    ) {
        this(castId, spell, context, loadoutSlot, targetHint, 0L);
    }

    public ArcanaCastRequest(ArcanaCastId castId, ArcanaSpellDefinition spell, ArcanaCastContext context, int loadoutSlot) {
        this(castId, spell, context, loadoutSlot, "", 0L);
    }

    public ArcanaCastRequest(ArcanaCastId castId, ArcanaSpellDefinition spell, ArcanaCastContext context) {
        this(castId, spell, context, 0, "", 0L);
    }

    public ArcanaCastRequest(ArcanaSpellDefinition spell, ArcanaCastContext context) {
        this(ArcanaCastId.random(), spell, context, 0, "", 0L);
    }
}
