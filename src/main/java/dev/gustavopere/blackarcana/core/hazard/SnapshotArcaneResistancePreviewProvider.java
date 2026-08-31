package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceContribution;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceProvider;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceQuery;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceSourceCategory;

import java.util.List;
import java.util.Objects;
import java.util.UUID;

/** Side-effect-free presentation adapter over an immutable equipment snapshot source. */
public final class SnapshotArcaneResistancePreviewProvider implements ArcaneResistanceProvider {
    @FunctionalInterface
    public interface SnapshotSource {
        ArcaneEquipmentSnapshotService.Snapshot capture(UUID playerId);
    }

    private final String providerId;
    private final String sourceId;
    private final ArcaneResistanceSourceCategory category;
    private final SnapshotSource source;

    public SnapshotArcaneResistancePreviewProvider(
        String providerId,
        String sourceId,
        ArcaneResistanceSourceCategory category,
        SnapshotSource source
    ) {
        this.providerId = Objects.requireNonNull(providerId, "providerId");
        this.sourceId = Objects.requireNonNull(sourceId, "sourceId");
        this.category = Objects.requireNonNull(category, "category");
        this.source = Objects.requireNonNull(source, "source");
    }

    @Override
    public String providerId() {
        return providerId;
    }

    @Override
    public List<ArcaneResistanceContribution> contributions(ArcaneResistanceQuery query) {
        Objects.requireNonNull(query, "query");
        ArcaneEquipmentSnapshotService.Snapshot snapshot = Objects.requireNonNull(
            source.capture(query.casterId()), "preview equipment snapshot");
        double amount = snapshot.arcaneResistance();
        if (amount <= 0.0D) return List.of();
        return List.of(new ArcaneResistanceContribution(sourceId, category, amount));
    }
}
