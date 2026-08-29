package dev.gustavopere.blackarcana.integration.curios;

import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceContribution;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceProvider;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceQuery;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceSourceCategory;
import dev.gustavopere.blackarcana.api.hazard.CorruptionResistanceContribution;
import dev.gustavopere.blackarcana.api.hazard.CorruptionResistanceProvider;
import dev.gustavopere.blackarcana.api.hazard.CorruptionResistanceQuery;
import dev.gustavopere.blackarcana.api.hazard.CorruptionResistanceSourceCategory;
import dev.gustavopere.blackarcana.core.hazard.ArcaneEquipmentSnapshotService;

import java.util.List;
import java.util.Objects;
import java.util.UUID;

/**
 * Read-only Curios contribution bridge. The physical Curios inventory is sampled only when
 * the hazard registries request a preflight snapshot; no global or per-tick scan exists.
 */
public final class CuriosHazardResistanceProvider
    implements ArcaneResistanceProvider, CorruptionResistanceProvider {

    public static final String PROVIDER_ID = "black_arcana:curios";
    private static final String SOURCE_ID = "curios:equipped_containment";

    @FunctionalInterface
    public interface SnapshotSource {
        ArcaneEquipmentSnapshotService.Snapshot snapshot(UUID playerId);
    }

    private final SnapshotSource snapshots;

    public CuriosHazardResistanceProvider(SnapshotSource snapshots) {
        this.snapshots = Objects.requireNonNull(snapshots, "snapshots");
    }

    @Override
    public String providerId() {
        return PROVIDER_ID;
    }

    @Override
    public List<ArcaneResistanceContribution> contributions(ArcaneResistanceQuery query) {
        Objects.requireNonNull(query, "query");
        ArcaneEquipmentSnapshotService.Snapshot snapshot =
            Objects.requireNonNull(snapshots.snapshot(query.casterId()), "Curios equipment snapshot");
        if (snapshot.arcaneResistance() <= 0.0D) return List.of();
        return List.of(new ArcaneResistanceContribution(
            SOURCE_ID,
            ArcaneResistanceSourceCategory.CURIO,
            snapshot.arcaneResistance()));
    }

    @Override
    public List<CorruptionResistanceContribution> contributions(CorruptionResistanceQuery query) {
        Objects.requireNonNull(query, "query");
        ArcaneEquipmentSnapshotService.Snapshot snapshot =
            Objects.requireNonNull(snapshots.snapshot(query.subjectId()), "Curios equipment snapshot");
        if (snapshot.corruptionResistance() <= 0.0D) return List.of();
        return List.of(new CorruptionResistanceContribution(
            SOURCE_ID,
            CorruptionResistanceSourceCategory.CURIO,
            snapshot.corruptionResistance()));
    }
}
