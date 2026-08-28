package dev.gustavopere.blackarcana.content.projection;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;
import java.util.UUID;

/** Bounded server-owned sanitized profile memory for Echo Armament / Spectral Arsenal. */
public final class ProjectedWeaponProfileRegistry {
    public static final int ABSOLUTE_MAX_OWNERS = 4096;

    private final int maxOwners;
    private final int maxProfilesPerOwner;
    private final Map<UUID, LinkedHashMap<String, ProjectedWeaponProfile>> profiles = new LinkedHashMap<>();

    public ProjectedWeaponProfileRegistry(int maxOwners, int maxProfilesPerOwner) {
        if (maxOwners <= 0 || maxOwners > ABSOLUTE_MAX_OWNERS) throw new IllegalArgumentException("maxOwners outside hard bounds");
        if (maxProfilesPerOwner <= 0 || maxProfilesPerOwner > ProjectionSafetyCeilings.MAX_STORED_PROFILES) {
            throw new IllegalArgumentException("maxProfilesPerOwner outside hard ceiling");
        }
        this.maxOwners = maxOwners;
        this.maxProfilesPerOwner = maxProfilesPerOwner;
    }

    public synchronized void remember(UUID ownerId, ProjectedWeaponProfile profile) {
        Objects.requireNonNull(ownerId, "ownerId");
        Objects.requireNonNull(profile, "profile");
        LinkedHashMap<String, ProjectedWeaponProfile> owner = profiles.get(ownerId);
        if (owner == null) {
            if (profiles.size() >= maxOwners) throw new IllegalStateException("projected profile owner registry is full");
            owner = new LinkedHashMap<>();
            profiles.put(ownerId, owner);
        }
        boolean existing = owner.containsKey(profile.profileId());
        if (!existing && owner.size() >= maxProfilesPerOwner) {
            throw new IllegalStateException("projected profile registry is full for owner");
        }
        owner.put(profile.profileId(), profile);
    }

    public synchronized Optional<ProjectedWeaponProfile> find(UUID ownerId, String profileId) {
        LinkedHashMap<String, ProjectedWeaponProfile> owner = profiles.get(Objects.requireNonNull(ownerId, "ownerId"));
        return owner == null ? Optional.empty() : Optional.ofNullable(owner.get(Objects.requireNonNull(profileId, "profileId")));
    }

    public synchronized List<ProjectedWeaponProfile> snapshot(UUID ownerId) {
        LinkedHashMap<String, ProjectedWeaponProfile> owner = profiles.get(Objects.requireNonNull(ownerId, "ownerId"));
        return owner == null ? List.of() : List.copyOf(owner.values());
    }

    public synchronized void clear(UUID ownerId) {
        profiles.remove(Objects.requireNonNull(ownerId, "ownerId"));
    }
}
