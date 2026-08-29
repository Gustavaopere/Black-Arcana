package dev.gustavopere.blackarcana.api.hazard;

import java.util.Objects;
import java.util.regex.Pattern;

/** One server-observed equipped item captured when a hazard session begins. */
public record ArcaneEquipmentSlotSnapshot(String slotId, String itemId, int durabilityRemaining) {
    private static final Pattern SLOT = Pattern.compile("[a-z0-9_.-]{1,48}");
    private static final Pattern ITEM = Pattern.compile("[a-z0-9_.-]+:[a-z0-9/._-]+");

    public ArcaneEquipmentSlotSnapshot {
        Objects.requireNonNull(slotId, "slotId");
        Objects.requireNonNull(itemId, "itemId");
        if (!SLOT.matcher(slotId).matches()) throw new IllegalArgumentException("invalid equipment slot id");
        if (!ITEM.matcher(itemId).matches()) throw new IllegalArgumentException("invalid equipment item id");
        if (durabilityRemaining < 0) throw new IllegalArgumentException("durabilityRemaining cannot be negative");
    }
}
