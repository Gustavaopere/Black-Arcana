package dev.gustavopere.blackarcana.config;

import dev.gustavopere.blackarcana.api.hazard.ArcaneEquipmentSetBonus;

import java.util.Objects;

/** Validated datapack definition for one cumulative containment-set threshold. */
public record ArcaneEquipmentSetBonusDataDefinition(
    int schemaVersion,
    String id,
    ArcaneEquipmentSetBonus bonus
) {
    public static final int CURRENT_SCHEMA_VERSION = 1;

    public ArcaneEquipmentSetBonusDataDefinition {
        if (schemaVersion != CURRENT_SCHEMA_VERSION) {
            throw new IllegalArgumentException("unsupported equipment set bonus schema version: " + schemaVersion);
        }
        Objects.requireNonNull(id, "id");
        Objects.requireNonNull(bonus, "bonus");
        if (!id.equals(bonus.bonusId())) throw new IllegalArgumentException("bonus id does not match definition id");
    }
}
