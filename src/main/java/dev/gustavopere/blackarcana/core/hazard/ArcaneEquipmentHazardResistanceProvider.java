package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.hazard.ArcaneEmergencyProtectionSnapshot;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceContribution;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceProvider;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceQuery;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceSourceCategory;
import dev.gustavopere.blackarcana.api.hazard.CorruptionResistanceContribution;
import dev.gustavopere.blackarcana.api.hazard.CorruptionResistanceProvider;
import dev.gustavopere.blackarcana.api.hazard.CorruptionResistanceQuery;
import dev.gustavopere.blackarcana.api.hazard.CorruptionResistanceSourceCategory;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.UUID;

/**
 * Bridges one frozen standard-equipment snapshot into both hazard resistance channels and the
 * emergency-protection handoff for the same root cast.
 */
public final class ArcaneEquipmentHazardResistanceProvider
    implements ArcaneResistanceProvider, CorruptionResistanceProvider, ArcaneEmergencyProtectionSnapshotProvider {

    public static final String PROVIDER_ID = "black_arcana:standard_equipment";
    public static final String SOURCE_ID = "black_arcana:standard_equipment";
    public static final int MAX_ACTIVE_SNAPSHOTS = 4_096;
    public static final long MAX_SNAPSHOT_AGE_TICKS = 2L;

    @FunctionalInterface
    public interface SnapshotSource {
        ArcaneEquipmentSnapshotService.Snapshot capture(UUID playerId);
    }

    private final SnapshotSource source;
    private final Map<ArcanaCastId, FrozenSnapshot> snapshots = new LinkedHashMap<>();

    public ArcaneEquipmentHazardResistanceProvider(SnapshotSource source) {
        this.source = Objects.requireNonNull(source, "source");
    }

    @Override
    public String providerId() { return PROVIDER_ID; }

    @Override
    public synchronized List<ArcaneResistanceContribution> contributions(ArcaneResistanceQuery query) {
        Objects.requireNonNull(query, "query");
        FrozenSnapshot frozen = snapshotFor(query.rootCastId(), query.casterId(), query.serverTick());
        frozen.arcaneRead = true;
        List<ArcaneResistanceContribution> result = arcaneContributions(frozen.snapshot);
        releaseIfComplete(query.rootCastId(), frozen);
        return result;
    }

    @Override
    public synchronized List<CorruptionResistanceContribution> contributions(CorruptionResistanceQuery query) {
        Objects.requireNonNull(query, "query");
        FrozenSnapshot frozen = snapshotFor(query.rootCastId(), query.subjectId(), query.serverTick());
        frozen.corruptionRead = true;
        List<CorruptionResistanceContribution> result = corruptionContributions(frozen.snapshot);
        releaseIfComplete(query.rootCastId(), frozen);
        return result;
    }

    @Override
    public synchronized ArcaneEmergencyProtectionSnapshot takeEmergencySnapshot(
        ArcanaCastId castId,
        UUID casterId,
        long serverTick
    ) {
        Objects.requireNonNull(castId, "castId");
        Objects.requireNonNull(casterId, "casterId");
        FrozenSnapshot frozen = snapshotFor(castId, casterId, serverTick);
        ArcaneEmergencyProtectionSnapshot emergency = frozen.snapshot.emergencyProtectionSnapshot();
        snapshots.remove(castId);
        return emergency;
    }

    @Override
    public synchronized void release(ArcanaCastId castId) {
        snapshots.remove(Objects.requireNonNull(castId, "castId"));
    }

    public synchronized int activeSnapshots() { return snapshots.size(); }

    private static List<ArcaneResistanceContribution> arcaneContributions(
        ArcaneEquipmentSnapshotService.Snapshot snapshot
    ) {
        double total = snapshot.arcaneResistance();
        if (total <= 0.0D) return List.of();
        List<ArcaneResistanceContribution> result = new ArrayList<>();
        double remaining = total;
        double itemTotal = itemArcaneResistance(snapshot);
        if (snapshot.items().isEmpty() && snapshot.activeSetBonuses().isEmpty()) itemTotal = total;
        double base = Math.min(remaining, itemTotal);
        if (base > 0.0D) {
            result.add(new ArcaneResistanceContribution(SOURCE_ID, ArcaneResistanceSourceCategory.EQUIPMENT, base));
            remaining -= base;
        }
        for (ArcaneEquipmentSnapshotService.ResolvedSetBonus resolved : snapshot.activeSetBonuses()) {
            if (remaining <= 0.0D) break;
            double amount = Math.min(remaining, resolved.bonus().arcaneResistance());
            if (amount <= 0.0D) continue;
            result.add(new ArcaneResistanceContribution(
                resolved.bonus().bonusId(), ArcaneResistanceSourceCategory.EQUIPMENT, amount));
            remaining -= amount;
        }
        if (remaining > 0.0D) {
            result.add(new ArcaneResistanceContribution(SOURCE_ID, ArcaneResistanceSourceCategory.EQUIPMENT, remaining));
        }
        return List.copyOf(result);
    }

    private static List<CorruptionResistanceContribution> corruptionContributions(
        ArcaneEquipmentSnapshotService.Snapshot snapshot
    ) {
        double total = snapshot.corruptionResistance();
        if (total <= 0.0D) return List.of();
        List<CorruptionResistanceContribution> result = new ArrayList<>();
        double remaining = total;
        double itemTotal = itemCorruptionResistance(snapshot);
        if (snapshot.items().isEmpty() && snapshot.activeSetBonuses().isEmpty()) itemTotal = total;
        double base = Math.min(remaining, itemTotal);
        if (base > 0.0D) {
            result.add(new CorruptionResistanceContribution(
                SOURCE_ID, CorruptionResistanceSourceCategory.EQUIPMENT, base));
            remaining -= base;
        }
        for (ArcaneEquipmentSnapshotService.ResolvedSetBonus resolved : snapshot.activeSetBonuses()) {
            if (remaining <= 0.0D) break;
            double amount = Math.min(remaining, resolved.bonus().corruptionResistance());
            if (amount <= 0.0D) continue;
            result.add(new CorruptionResistanceContribution(
                resolved.bonus().bonusId(), CorruptionResistanceSourceCategory.EQUIPMENT, amount));
            remaining -= amount;
        }
        if (remaining > 0.0D) {
            result.add(new CorruptionResistanceContribution(
                SOURCE_ID, CorruptionResistanceSourceCategory.EQUIPMENT, remaining));
        }
        return List.copyOf(result);
    }

    private static double itemArcaneResistance(ArcaneEquipmentSnapshotService.Snapshot snapshot) {
        double total = 0.0D;
        for (ArcaneEquipmentSnapshotService.ResolvedItem item : snapshot.items()) {
            total = Math.min(
                dev.gustavopere.blackarcana.api.hazard.ArcaneEquipmentProfile.ABSOLUTE_MAX_RESISTANCE,
                total + item.profile().arcaneResistance());
        }
        return total;
    }

    private static double itemCorruptionResistance(ArcaneEquipmentSnapshotService.Snapshot snapshot) {
        double total = 0.0D;
        for (ArcaneEquipmentSnapshotService.ResolvedItem item : snapshot.items()) {
            total = Math.min(
                dev.gustavopere.blackarcana.api.hazard.ArcaneEquipmentProfile.ABSOLUTE_MAX_RESISTANCE,
                total + item.profile().corruptionResistance());
        }
        return total;
    }

    private FrozenSnapshot snapshotFor(ArcanaCastId castId, UUID casterId, long serverTick) {
        pruneExpired(serverTick);
        FrozenSnapshot existing = snapshots.get(castId);
        if (existing != null) {
            if (!existing.casterId.equals(casterId)) throw new IllegalStateException("root cast id reused by a different caster");
            return existing;
        }
        if (snapshots.size() >= MAX_ACTIVE_SNAPSHOTS) {
            throw new IllegalStateException("standard equipment snapshot cache is full");
        }
        ArcaneEquipmentSnapshotService.Snapshot captured =
            Objects.requireNonNull(source.capture(casterId), "equipment snapshot");
        FrozenSnapshot created = new FrozenSnapshot(casterId, serverTick, captured);
        snapshots.put(castId, created);
        return created;
    }

    private void pruneExpired(long serverTick) {
        Iterator<Map.Entry<ArcanaCastId, FrozenSnapshot>> iterator = snapshots.entrySet().iterator();
        while (iterator.hasNext()) {
            FrozenSnapshot frozen = iterator.next().getValue();
            if (serverTick > frozen.serverTick && serverTick - frozen.serverTick > MAX_SNAPSHOT_AGE_TICKS) iterator.remove();
        }
    }

    private void releaseIfComplete(ArcanaCastId castId, FrozenSnapshot frozen) {
        if (!frozen.arcaneRead || !frozen.corruptionRead) return;
        if (frozen.snapshot.emergencyProtectionCandidates().isEmpty()) snapshots.remove(castId);
    }

    private static final class FrozenSnapshot {
        private final UUID casterId;
        private final long serverTick;
        private final ArcaneEquipmentSnapshotService.Snapshot snapshot;
        private boolean arcaneRead;
        private boolean corruptionRead;

        private FrozenSnapshot(UUID casterId, long serverTick, ArcaneEquipmentSnapshotService.Snapshot snapshot) {
            this.casterId = Objects.requireNonNull(casterId, "casterId");
            this.serverTick = serverTick;
            this.snapshot = Objects.requireNonNull(snapshot, "snapshot");
        }
    }
}
