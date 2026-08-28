package dev.gustavopere.blackarcana.api;

import java.util.Objects;

public record ArcanaCooldownSpec(String groupId, long durationTicks, boolean persistent) {
    public static final long ABSOLUTE_MAX_DURATION_TICKS = 20L * 60L * 60L * 24L * 30L;

    public ArcanaCooldownSpec {
        Objects.requireNonNull(groupId, "groupId");
        ArcanaSpellId.parse(groupId);
        if (durationTicks < 0L || durationTicks > ABSOLUTE_MAX_DURATION_TICKS) {
            throw new IllegalArgumentException("durationTicks must be between 0 and " + ABSOLUTE_MAX_DURATION_TICKS);
        }
    }

    public static ArcanaCooldownSpec none(String groupId) {
        return new ArcanaCooldownSpec(groupId, 0L, false);
    }
}
