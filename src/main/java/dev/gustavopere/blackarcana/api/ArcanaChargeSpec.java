package dev.gustavopere.blackarcana.api;

import java.util.Objects;

public record ArcanaChargeSpec(String groupId, int maxCharges, long rechargeTicks, boolean persistent) {
    public static final int ABSOLUTE_MAX_CHARGES = 16;

    public ArcanaChargeSpec {
        Objects.requireNonNull(groupId, "groupId");
        ArcanaSpellId.parse(groupId);
        if (maxCharges <= 0 || maxCharges > ABSOLUTE_MAX_CHARGES) {
            throw new IllegalArgumentException("maxCharges must be between 1 and " + ABSOLUTE_MAX_CHARGES);
        }
        if (rechargeTicks <= 0L || rechargeTicks > ArcanaCooldownSpec.ABSOLUTE_MAX_DURATION_TICKS) {
            throw new IllegalArgumentException("rechargeTicks outside allowed cooldown duration");
        }
    }
}
