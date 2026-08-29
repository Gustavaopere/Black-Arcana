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

import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.UUID;

/**
 * Bridges one frozen standard-equipment snapshot into both hazard resistance channels and the
 * emergency-protection handoff for the same root cast.
 *
 * <p>The first query for a root cast captures server-observed equipment. Arcane Resistance,
 * Corruption Resistance and emergency protection then read the same immutable snapshot even if
 * equipment changes between phases. Entries with emergency candidates remain retained until the
 * emergency facts are handed off, may be explicitly released for aborted preflights, and are
 * short-lived/bounded so an incomplete preflight cannot leak unbounded state.</p>
 */
public final class ArcaneEquipmentHazardResistanceProvider
    implements ArcaneResistanceProvider, CorruptionResistanceProvider {

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
            ArcaneResistanceSourceCategory.EQUIPMENT,
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
            CorruptionResistanceSourceCategory.EQUIPMENT,
            amount));
    }

    /**
     * Transfers emergency-protection facts from the same root-cast snapshot and releases the cache
     * entry. The equipment source is never re-queried when a resistance phase already captured it.
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

    /** Releases a snapshot retained by an aborted/short-circuited preflight. */
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
