package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.hazard.ArcaneEquipmentProfile;
import dev.gustavopere.blackarcana.api.hazard.ArcaneEquipmentSlotSnapshot;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;

/** Resolves an immutable hazard-session equipment snapshot from server-observed slots. */
public final class ArcaneEquipmentSnapshotService {
    public static final int MAX_EQUIPPED_SLOTS = 32;

    private final ArcaneEquipmentProfileRegistry profiles;

    public ArcaneEquipmentSnapshotService(ArcaneEquipmentProfileRegistry profiles) {
        this.profiles = Objects.requireNonNull(profiles, "profiles");
    }

    public Snapshot capture(List<ArcaneEquipmentSlotSnapshot> equipped) {
        Objects.requireNonNull(equipped, "equipped");
        if (equipped.size() > MAX_EQUIPPED_SLOTS) throw new IllegalArgumentException("too many equipped slots");

        List<ResolvedItem> resolved = new ArrayList<>();
        Map<String, Integer> setCounts = new LinkedHashMap<>();
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
        }

        return new Snapshot(List.copyOf(resolved), Map.copyOf(setCounts), arcane, corruption, strainCapacity, strainRecovery);
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

    public record Snapshot(
        List<ResolvedItem> items,
        Map<String, Integer> setCounts,
        double arcaneResistance,
        double corruptionResistance,
        double strainCapacityBonus,
        double strainRecoveryPerTick
    ) {
        public Snapshot {
            items = List.copyOf(items);
            setCounts = Map.copyOf(setCounts);
        }

        public int setPieces(String setId) {
            return setCounts.getOrDefault(setId, 0);
        }
    }
}
