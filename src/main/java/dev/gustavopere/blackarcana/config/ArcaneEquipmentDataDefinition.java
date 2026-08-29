package dev.gustavopere.blackarcana.config;

import dev.gustavopere.blackarcana.api.hazard.ArcaneEquipmentProfile;

import java.util.Objects;

/** Validated datapack definition that binds one explicit item id to one containment profile. */
public record ArcaneEquipmentDataDefinition(
    int schemaVersion,
    String id,
    String itemId,
    ArcaneEquipmentProfile profile
) {
    public static final int CURRENT_SCHEMA_VERSION = 1;

    public ArcaneEquipmentDataDefinition {
        if (schemaVersion != CURRENT_SCHEMA_VERSION) {
            throw new IllegalArgumentException("unsupported equipment profile schema version: " + schemaVersion);
        }
        Objects.requireNonNull(id, "id");
        Objects.requireNonNull(itemId, "itemId");
        Objects.requireNonNull(profile, "profile");
        if (!id.equals(profile.profileId())) {
            throw new IllegalArgumentException("profile id does not match definition id");
        }
    }
}
