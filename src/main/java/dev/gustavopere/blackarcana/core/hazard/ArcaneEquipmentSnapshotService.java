package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.hazard.ArcaneEmergencyProtectionSnapshot;
import dev.gustavopere.blackarcana.api.hazard.ArcaneEquipmentProfile;
import dev.gustavopere.blackarcana.api.hazard.ArcaneEquipmentSetBonus;
import dev.gustavopere.blackarcana.api.hazard.ArcaneEquipmentSlotSnapshot;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Set;

/** Resolves an immutable hazard-session equipment snapshot from server-observed slots. */
public final class ArcaneEquipmentSnapshotService {
    public static final int MAX_EQUIPPED_SLOTS = 32;

    private final ArcaneEquipmentProfileRegistry profiles;
    private final ArcaneEquipmentSetBonusRegistry setBonuses;

    public ArcaneEquipmentSnapshotService(ArcaneEquipmentProfileRegistry profiles) {
        this(profiles, new ArcaneEquipmentSetBonusRegistry());
    }

    public ArcaneEquipmentSnapshotService(
        ArcaneEquipmentProfileRegistry profiles,
        ArcaneEquipmentSetBonusRegistry setBonuses
    ) {
        this.profiles = Objects.requireNonNull(profiles, "profiles");
        this.setBonuses = Objects.requireNonNull(setBonuses, "setBonuses");
    }

    public Snapshot capture(List<ArcaneEquipmentSlotSnapshot> equipped) {
        Objects.requireNonNull(equipped, "equipped");
        if (equipped.size() > MAX_EQUIPPED_SLOTS) throw new IllegalArgumentException("too many equipped slots");

        List<ResolvedItem> resolved = new ArrayList<>();
        Map<String, Integer> setCounts = new LinkedHashMap<>();
        List<ArcaneEmergencyProtectionSnapshot.Candidate> emergencyCandidates = new ArrayList<>();
        Set<String> emergencyResources = new HashSet<>();
        double arcane = 0.0D;
        double corruption = 0.0D;
        double strainCapacity = 0.0D;
        double strainRecovery = 0.0D;

        for (ArcaneEquipmentSlotSnapshot slot : equipped) {
            ArcaneEquipmentProfile profile = profiles.resolve(slot.itemId()).orElse(null);
            if (profile == null) continue;
            resolved.add(new ResolvedItem(slot, profile));
            arcane = boundedAdd(arcane, profile.arcaneResistance(), ArcaneEquipmentProfile.ABSOLUTE_MAX_RESISTANCE);
            corruption = boundedAdd(corruption, profile.corruptionResistance(), ArcaneEquipmentProfile.ABSOLUTE_MAX_RESISTANCE);
            strainCapacity = boundedAdd(strainCapacity, profile.strainCapacityBonus(), ArcaneEquipmentProfile.ABSOLUTE_MAX_STRAIN_CAPACITY);
            strainRecovery = boundedAdd(strainRecovery, profile.strainRecoveryPerTick(), ArcaneEquipmentProfile.ABSOLUTE_MAX_STRAIN_RECOVERY);
            if (profile.setId() != null) setCounts.merge(profile.setId(), 1, Integer::sum);
            if (profile.emergencyAbsorption() > 0.0D
                && slot.durabilityRemaining() > 0
                && emergencyResources.add(profile.profileId())) {
                emergencyCandidates.add(new ArcaneEmergencyProtectionSnapshot.Candidate(
                    profile.profileId(),
                    profile.profileId(),
                    profile.emergencyAbsorption(),
                    profile.emergencyCooldownTicks()));
            }
        }

        List<ResolvedSetBonus> activeSetBonuses = new ArrayList<>();
        for (ArcaneEquipmentSetBonus bonus : setBonuses.resolve(setCounts)) {
            int equippedPieces = setCounts.getOrDefault(bonus.setId(), 0);
            activeSetBonuses.add(new ResolvedSetBonus(bonus, equippedPieces));
            arcane = boundedAdd(arcane, bonus.arcaneResistance(), ArcaneEquipmentProfile.ABSOLUTE_MAX_RESISTANCE);
            corruption = boundedAdd(corruption, bonus.corruptionResistance(), ArcaneEquipmentProfile.ABSOLUTE_MAX_RESISTANCE);
            strainCapacity = boundedAdd(strainCapacity, bonus.strainCapacityBonus(), ArcaneEquipmentProfile.ABSOLUTE_MAX_STRAIN_CAPACITY);
            strainRecovery = boundedAdd(strainRecovery, bonus.strainRecoveryPerTick(), ArcaneEquipmentProfile.ABSOLUTE_MAX_STRAIN_RECOVERY);
        }

        return new Snapshot(
            List.copyOf(resolved),
            Map.copyOf(setCounts),
            arcane,
            corruption,
            strainCapacity,
            strainRecovery,
            List.copyOf(emergencyCandidates),
            List.copyOf(activeSetBonuses));
    }

    private static double boundedAdd(double left, double right, double max) {
        return Math.min(max, left + right);
    }

    public record ResolvedItem(ArcaneEquipmentSlotSnapshot slot, ArcaneEquipmentProfile profile) {
        public ResolvedItem {
            Objects.requireNonNull(slot, "slot");
            Objects.requireNonNull(profile, "profile");
        }
    }

    /** Frozen diagnostic record for one cumulative threshold satisfied at capture time. */
    public record ResolvedSetBonus(ArcaneEquipmentSetBonus bonus, int equippedPieces) {
        public ResolvedSetBonus {
            Objects.requireNonNull(bonus, "bonus");
            if (equippedPieces < bonus.requiredPieces() || equippedPieces > MAX_EQUIPPED_SLOTS) {
                throw new IllegalArgumentException("equippedPieces does not satisfy set threshold");
            }
        }
    }

    public record Snapshot(
        List<ResolvedItem> items,
        Map<String, Integer> setCounts,
        double arcaneResistance,
        double corruptionResistance,
        double strainCapacityBonus,
        double strainRecoveryPerTick,
        List<ArcaneEmergencyProtectionSnapshot.Candidate> emergencyProtectionCandidates,
        List<ResolvedSetBonus> activeSetBonuses
    ) {
        /** Backward-compatible constructor for snapshots created before set-bonus metadata existed. */
        public Snapshot(
            List<ResolvedItem> items,
            Map<String, Integer> setCounts,
            double arcaneResistance,
            double corruptionResistance,
            double strainCapacityBonus,
            double strainRecoveryPerTick,
            List<ArcaneEmergencyProtectionSnapshot.Candidate> emergencyProtectionCandidates
        ) {
            this(
                items,
                setCounts,
                arcaneResistance,
                corruptionResistance,
                strainCapacityBonus,
                strainRecoveryPerTick,
                emergencyProtectionCandidates,
                List.of());
        }

        /** Backward-compatible constructor for snapshots created before emergency protection metadata existed. */
        public Snapshot(
            List<ResolvedItem> items,
            Map<String, Integer> setCounts,
            double arcaneResistance,
            double corruptionResistance,
            double strainCapacityBonus,
            double strainRecoveryPerTick
        ) {
            this(
                items,
                setCounts,
                arcaneResistance,
                corruptionResistance,
                strainCapacityBonus,
                strainRecoveryPerTick,
                List.of(),
                List.of());
        }

        public Snapshot {
            items = List.copyOf(Objects.requireNonNull(items, "items"));
            setCounts = Map.copyOf(Objects.requireNonNull(setCounts, "setCounts"));
            emergencyProtectionCandidates = List.copyOf(Objects.requireNonNull(
                emergencyProtectionCandidates, "emergencyProtectionCandidates"));
            activeSetBonuses = List.copyOf(Objects.requireNonNull(activeSetBonuses, "activeSetBonuses"));
            new ArcaneEmergencyProtectionSnapshot(emergencyProtectionCandidates);
        }

        public int setPieces(String setId) {
            return setCounts.getOrDefault(setId, 0);
        }

        public ArcaneEmergencyProtectionSnapshot emergencyProtectionSnapshot() {
            return new ArcaneEmergencyProtectionSnapshot(emergencyProtectionCandidates);
        }
    }
}
