package dev.gustavopere.blackarcana.integration.curios;

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
import dev.gustavopere.blackarcana.core.hazard.ArcaneEquipmentSnapshotService;

import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.UUID;

/**
 * Read-only Curios contribution bridge. One root cast observes one frozen Curios snapshot across
 * both resistance channels and emergency-protection handoff; there is no global or per-tick
 * inventory scan.
 */
public final class CuriosHazardResistanceProvider
    implements ArcaneResistanceProvider, CorruptionResistanceProvider {

    public static final String PROVIDER_ID = "black_arcana:curios";
    private static final String SOURCE_ID = "curios:equipped_containment";
    public static final int MAX_ACTIVE_SNAPSHOTS = 4_096;
    public static final long MAX_SNAPSHOT_AGE_TICKS = 2L;

    @FunctionalInterface
    public interface SnapshotSource {
        ArcaneEquipmentSnapshotService.Snapshot snapshot(UUID playerId);
    }

    private final SnapshotSource source;
    private final Map<ArcanaCastId, FrozenSnapshot> snapshots = new LinkedHashMap<>();

    public CuriosHazardResistanceProvider(SnapshotSource source) {
        this.source = Objects.requireNonNull(source, "source");
    }

    @Override
    public String providerId() {
        return PROVIDER_ID;
    }

    @Override
    public synchronized List<ArcaneResistanceContribution> contributions(ArcaneResistanceQuery query) {
        Objects.requireNonNull(query, "query");
        FrozenSnapshot frozen = snapshotFor(query.rootCastId(), query.casterId(), query.serverTick());
        frozen.arcaneRead = true;
        double amount = frozen.snapshot.arcaneResistance();
        releaseIfComplete(query.rootCastId(), frozen);
        if (amount <= 0.0D) return List.of();
        return List.of(new ArcaneResistanceContribution(
            SOURCE_ID,
            ArcaneResistanceSourceCategory.CURIO,
            amount));
    }

    @Override
    public synchronized List<CorruptionResistanceContribution> contributions(CorruptionResistanceQuery query) {
        Objects.requireNonNull(query, "query");
        FrozenSnapshot frozen = snapshotFor(query.rootCastId(), query.subjectId(), query.serverTick());
        frozen.corruptionRead = true;
        double amount = frozen.snapshot.corruptionResistance();
        releaseIfComplete(query.rootCastId(), frozen);
        if (amount <= 0.0D) return List.of();
        return List.of(new CorruptionResistanceContribution(
            SOURCE_ID,
            CorruptionResistanceSourceCategory.CURIO,
            amount));
    }

    /**
     * Transfers emergency-protection facts from the same root-cast Curios snapshot and releases
     * the cached entry without re-reading Curios.
     */
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

    public synchronized void release(ArcanaCastId castId) {
        snapshots.remove(Objects.requireNonNull(castId, "castId"));
    }

    public synchronized int activeSnapshots() {
        return snapshots.size();
    }

    private FrozenSnapshot snapshotFor(ArcanaCastId castId, UUID casterId, long serverTick) {
        pruneExpired(serverTick);
        FrozenSnapshot existing = snapshots.get(castId);
        if (existing != null) {
            if (!existing.casterId.equals(casterId)) {
                throw new IllegalStateException("root cast id reused by a different caster");
            }
            return existing;
        }
        if (snapshots.size() >= MAX_ACTIVE_SNAPSHOTS) {
            throw new IllegalStateException("Curios equipment snapshot cache is full");
        }
        ArcaneEquipmentSnapshotService.Snapshot captured =
            Objects.requireNonNull(source.snapshot(casterId), "Curios equipment snapshot");
        FrozenSnapshot created = new FrozenSnapshot(casterId, serverTick, captured);
        snapshots.put(castId, created);
        return created;
    }

    private void pruneExpired(long serverTick) {
        Iterator<Map.Entry<ArcanaCastId, FrozenSnapshot>> iterator = snapshots.entrySet().iterator();
        while (iterator.hasNext()) {
            FrozenSnapshot frozen = iterator.next().getValue();
            if (serverTick > frozen.serverTick
                && serverTick - frozen.serverTick > MAX_SNAPSHOT_AGE_TICKS) {
                iterator.remove();
            }
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

        private FrozenSnapshot(
            UUID casterId,
            long serverTick,
            ArcaneEquipmentSnapshotService.Snapshot snapshot
        ) {
            this.casterId = Objects.requireNonNull(casterId, "casterId");
            this.serverTick = serverTick;
            this.snapshot = Objects.requireNonNull(snapshot, "snapshot");
        }
    }
}
