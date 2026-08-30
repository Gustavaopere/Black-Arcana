package dev.gustavopere.blackarcana.content.projection;

import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Set;
import java.util.UUID;

/**
 * Atomic clean-room ledger for Oathforged Ascension.
 *
 * Host adapters own the physical ritual inventory/material/spirit inputs and translate them into
 * stable sacrifice tokens. This ledger owns only the replay/recursion guard and the finite
 * augmentation-point state. No mutation occurs until every token, capacity and allocator rule has
 * been validated, so a denied rite cannot partially consume logical sacrifices or partially award
 * points.
 */
public final class OathforgedAscensionLedger {
    private static final int MAX_KEY_LENGTH = 128;

    private final int maxTrackedTracks;
    private final int maxConsumedSacrifices;
    private final int maxSacrificesPerRite;
    private final Map<TrackKey, Integer> pointsByTrack = new LinkedHashMap<>();
    private final Set<UUID> consumedSacrifices = new HashSet<>();

    public OathforgedAscensionLedger(
            int maxTrackedTracks,
            int maxConsumedSacrifices,
            int maxSacrificesPerRite
    ) {
        if (maxTrackedTracks <= 0) {
            throw new IllegalArgumentException("maxTrackedTracks must be positive");
        }
        if (maxConsumedSacrifices <= 0) {
            throw new IllegalArgumentException("maxConsumedSacrifices must be positive");
        }
        if (maxSacrificesPerRite <= 0 || maxSacrificesPerRite > maxConsumedSacrifices) {
            throw new IllegalArgumentException("maxSacrificesPerRite must fit consumed-sacrifice capacity");
        }
        this.maxTrackedTracks = maxTrackedTracks;
        this.maxConsumedSacrifices = maxConsumedSacrifices;
        this.maxSacrificesPerRite = maxSacrificesPerRite;
    }

    public synchronized Settlement settle(
            TrackKey track,
            List<SacrificeToken> sacrifices,
            AscensionPointAllocator.Policy allocationPolicy,
            int maxTrackPoints
    ) {
        Objects.requireNonNull(track, "track");
        Objects.requireNonNull(sacrifices, "sacrifices");
        Objects.requireNonNull(allocationPolicy, "allocationPolicy");
        if (maxTrackPoints <= 0 || maxTrackPoints > ProjectionSafetyCeilings.MAX_ASCENSION_POINTS) {
            throw new IllegalArgumentException("maxTrackPoints outside hard Ascension ceiling");
        }
        if (sacrifices.isEmpty()) {
            return Settlement.denied("no_sacrifices", points(track));
        }
        if (sacrifices.size() > maxSacrificesPerRite) {
            return Settlement.denied("sacrifice_batch_cap", points(track));
        }

        int currentPoints = pointsByTrack.getOrDefault(track, 0);
        if (currentPoints >= maxTrackPoints) {
            return Settlement.denied("track_cap", currentPoints);
        }
        if (!pointsByTrack.containsKey(track) && pointsByTrack.size() >= maxTrackedTracks) {
            return Settlement.denied("track_capacity", currentPoints);
        }

        LinkedHashSet<UUID> batchIds = new LinkedHashSet<>(sacrifices.size());
        double totalEligibleValue = 0.0D;
        boolean recursivelyAugmented = false;
        for (SacrificeToken sacrifice : sacrifices) {
            Objects.requireNonNull(sacrifice, "sacrifice");
            if (!batchIds.add(sacrifice.sacrificeId())) {
                return Settlement.denied("duplicate_sacrifice", currentPoints);
            }
            if (consumedSacrifices.contains(sacrifice.sacrificeId())) {
                return Settlement.denied("sacrifice_already_consumed", currentPoints);
            }
            totalEligibleValue += sacrifice.eligibleValue();
            if (!Double.isFinite(totalEligibleValue)) {
                return Settlement.denied("eligible_value_overflow", currentPoints);
            }
            recursivelyAugmented |= sacrifice.alreadyBlackArcanaAugmented();
        }

        if (consumedSacrifices.size() > maxConsumedSacrifices - batchIds.size()) {
            return Settlement.denied("sacrifice_capacity", currentPoints);
        }

        AscensionPointAllocator.Allocation allocation = AscensionPointAllocator.allocate(
            new AscensionPointAllocator.Sacrifice(totalEligibleValue, recursivelyAugmented),
            allocationPolicy);
        if (!allocation.accepted()) {
            return Settlement.denied(allocation.denialCode(), currentPoints);
        }

        int remainingTrackCapacity = maxTrackPoints - currentPoints;
        int awardedPoints = Math.min(allocation.points(), remainingTrackCapacity);
        if (awardedPoints <= 0) {
            return Settlement.denied("track_cap", currentPoints);
        }

        // Commit boundary: all validation above is read-only. These two mutations form the entire
        // logical rite settlement while holding the ledger monitor.
        int totalTrackPoints = currentPoints + awardedPoints;
        pointsByTrack.put(track, totalTrackPoints);
        consumedSacrifices.addAll(batchIds);
        return Settlement.accepted(awardedPoints, totalTrackPoints);
    }

    public synchronized int points(TrackKey track) {
        Objects.requireNonNull(track, "track");
        return pointsByTrack.getOrDefault(track, 0);
    }

    public synchronized boolean consumed(UUID sacrificeId) {
        Objects.requireNonNull(sacrificeId, "sacrificeId");
        return consumedSacrifices.contains(sacrificeId);
    }

    public synchronized int trackedTracks() {
        return pointsByTrack.size();
    }

    public synchronized int consumedSacrificeCount() {
        return consumedSacrifices.size();
    }

    /**
     * Returns an immutable policy-agnostic snapshot suitable for durable host persistence.
     * Physical ritual inventory is intentionally not represented here.
     */
    public synchronized Snapshot snapshot() {
        return new Snapshot(pointsByTrack, consumedSacrifices);
    }

    /**
     * Restores a previously validated logical ledger state. Validation completes before mutation,
     * so malformed/oversized snapshots cannot partially replace the current state.
     */
    public synchronized void restore(Snapshot snapshot) {
        Objects.requireNonNull(snapshot, "snapshot");
        if (snapshot.pointsByTrack().size() > maxTrackedTracks) {
            throw new IllegalArgumentException("snapshot exceeds tracked-track capacity");
        }
        if (snapshot.consumedSacrifices().size() > maxConsumedSacrifices) {
            throw new IllegalArgumentException("snapshot exceeds consumed-sacrifice capacity");
        }
        for (Map.Entry<TrackKey, Integer> entry : snapshot.pointsByTrack().entrySet()) {
            Objects.requireNonNull(entry.getKey(), "snapshot track");
            Integer value = Objects.requireNonNull(entry.getValue(), "snapshot points");
            if (value < 0 || value > ProjectionSafetyCeilings.MAX_ASCENSION_POINTS) {
                throw new IllegalArgumentException("snapshot track points outside hard Ascension ceiling");
            }
        }
        for (UUID sacrificeId : snapshot.consumedSacrifices()) {
            Objects.requireNonNull(sacrificeId, "snapshot sacrifice id");
        }

        pointsByTrack.clear();
        consumedSacrifices.clear();
        pointsByTrack.putAll(snapshot.pointsByTrack());
        consumedSacrifices.addAll(snapshot.consumedSacrifices());
    }

    public record TrackKey(String targetId, String trackId) {
        public TrackKey {
            targetId = validateKey(targetId, "targetId");
            trackId = validateKey(trackId, "trackId");
        }
    }

    public record SacrificeToken(
        UUID sacrificeId,
        double eligibleValue,
        boolean alreadyBlackArcanaAugmented
    ) {
        public SacrificeToken {
            Objects.requireNonNull(sacrificeId, "sacrificeId");
            if (!Double.isFinite(eligibleValue) || eligibleValue < 0.0D) {
                throw new IllegalArgumentException("eligibleValue must be finite and non-negative");
            }
        }
    }

    public record Settlement(
        boolean accepted,
        int awardedPoints,
        int totalTrackPoints,
        String denialCode
    ) {
        public Settlement {
            Objects.requireNonNull(denialCode, "denialCode");
            if (awardedPoints < 0 || awardedPoints > ProjectionSafetyCeilings.MAX_ASCENSION_POINTS) {
                throw new IllegalArgumentException("awardedPoints outside hard Ascension ceiling");
            }
            if (totalTrackPoints < 0 || totalTrackPoints > ProjectionSafetyCeilings.MAX_ASCENSION_POINTS) {
                throw new IllegalArgumentException("totalTrackPoints outside hard Ascension ceiling");
            }
            if (accepted && (awardedPoints <= 0 || !denialCode.isEmpty())) {
                throw new IllegalArgumentException("accepted Ascension settlement must award points without denial");
            }
            if (!accepted && (awardedPoints != 0 || denialCode.isEmpty())) {
                throw new IllegalArgumentException("denied Ascension settlement must carry only a denial code");
            }
        }

        private static Settlement accepted(int awardedPoints, int totalTrackPoints) {
            return new Settlement(true, awardedPoints, totalTrackPoints, "");
        }

        private static Settlement denied(String code, int currentTrackPoints) {
            return new Settlement(false, 0, currentTrackPoints, Objects.requireNonNull(code, "code"));
        }
    }

    public record Snapshot(Map<TrackKey, Integer> pointsByTrack, Set<UUID> consumedSacrifices) {
        public Snapshot {
            Objects.requireNonNull(pointsByTrack, "pointsByTrack");
            Objects.requireNonNull(consumedSacrifices, "consumedSacrifices");
            pointsByTrack = Map.copyOf(new LinkedHashMap<>(pointsByTrack));
            consumedSacrifices = Set.copyOf(new LinkedHashSet<>(consumedSacrifices));
        }
    }

    private static String validateKey(String value, String field) {
        Objects.requireNonNull(value, field);
        String normalized = value.trim();
        if (normalized.isEmpty() || normalized.length() > MAX_KEY_LENGTH) {
            throw new IllegalArgumentException(field + " must be non-empty and bounded");
        }
        for (int i = 0; i < normalized.length(); i++) {
            if (Character.isISOControl(normalized.charAt(i))) {
                throw new IllegalArgumentException(field + " cannot contain control characters");
            }
        }
        return normalized;
    }
}
