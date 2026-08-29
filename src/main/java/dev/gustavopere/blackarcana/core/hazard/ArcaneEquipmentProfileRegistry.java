package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.hazard.ArcaneEquipmentProfile;

import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;
import java.util.regex.Pattern;

/**
 * Server-owned registry for explicit containment profiles.
 * An item not present here contributes nothing, including all ordinary vanilla armor.
 */
public final class ArcaneEquipmentProfileRegistry {
    public static final int MAX_PROFILES = 4_096;
    private static final Pattern ITEM_ID = Pattern.compile("[a-z0-9_.-]+:[a-z0-9/._-]+", Pattern.CASE_INSENSITIVE);
    private final Map<String, ArcaneEquipmentProfile> profiles = new LinkedHashMap<>();

    public synchronized void register(String itemId, ArcaneEquipmentProfile profile) {
        String canonical = canonicalItemId(itemId);
        Objects.requireNonNull(profile, "profile");
        if (profiles.containsKey(canonical)) throw new IllegalStateException("duplicate arcane equipment profile: " + canonical);
        if (profiles.size() >= MAX_PROFILES) throw new IllegalStateException("arcane equipment profile registry is full");
        profiles.put(canonical, profile);
    }

    public synchronized Optional<ArcaneEquipmentProfile> resolve(String itemId) {
        return Optional.ofNullable(profiles.get(canonicalItemId(itemId)));
    }

    public synchronized Map<String, ArcaneEquipmentProfile> snapshot() {
        return Map.copyOf(profiles);
    }

    public synchronized int size() {
        return profiles.size();
    }

    private static String canonicalItemId(String itemId) {
        Objects.requireNonNull(itemId, "itemId");
        if (!ITEM_ID.matcher(itemId).matches()) throw new IllegalArgumentException("invalid item id: " + itemId);
        return itemId.toLowerCase(java.util.Locale.ROOT);
    }
}
