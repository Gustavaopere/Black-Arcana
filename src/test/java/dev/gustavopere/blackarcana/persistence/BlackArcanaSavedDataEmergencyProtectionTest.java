package dev.gustavopere.blackarcana.persistence;

import dev.gustavopere.blackarcana.core.hazard.ArcaneEmergencyProtectionStateService;
import dev.gustavopere.blackarcana.core.hazard.ArcaneStrainStateService;
import dev.gustavopere.blackarcana.core.hazard.CorruptionStateService;
import net.minecraft.nbt.CompoundTag;
import org.junit.jupiter.api.Test;

import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;

class BlackArcanaSavedDataEmergencyProtectionTest {
    private static final UUID PLAYER = UUID.fromString("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa");
    private static final String RESOURCE = "black_arcana:containment_mask";

    @Test
    void committedEmergencyCooldownRoundTripsWithHazardState() {
        CorruptionStateService corruption = CorruptionStateService.canonical(16);
        ArcaneStrainStateService strain = ArcaneStrainStateService.canonical(16);
        ArcaneEmergencyProtectionStateService emergency = ArcaneEmergencyProtectionStateService.canonical(16);
        emergency.reserve(PLAYER, RESOURCE, 100L, 200L).commit();

        BlackArcanaSavedData saved = new BlackArcanaSavedData();
        saved.captureHazards(corruption, strain, emergency);
        CompoundTag root = saved.save(new CompoundTag(), null);
        BlackArcanaSavedData loaded = BlackArcanaSavedData.load(root, null);

        ArcaneEmergencyProtectionStateService restored = ArcaneEmergencyProtectionStateService.canonical(16);
        loaded.restoreHazards(
            CorruptionStateService.canonical(16),
            ArcaneStrainStateService.canonical(16),
            restored);

        assertEquals(300L, restored.readyAtTick(PLAYER, RESOURCE));
        assertFalse(restored.reserve(PLAYER, RESOURCE, 299L, 200L).decision().allowed());
    }

    @Test
    void transientReservationIsNeverPersisted() {
        CorruptionStateService corruption = CorruptionStateService.canonical(16);
        ArcaneStrainStateService strain = ArcaneStrainStateService.canonical(16);
        ArcaneEmergencyProtectionStateService emergency = ArcaneEmergencyProtectionStateService.canonical(16);
        emergency.reserve(PLAYER, RESOURCE, 100L, 200L);

        BlackArcanaSavedData saved = new BlackArcanaSavedData();
        saved.captureHazards(corruption, strain, emergency);
        BlackArcanaSavedData loaded = BlackArcanaSavedData.load(saved.save(new CompoundTag(), null), null);

        ArcaneEmergencyProtectionStateService restored = ArcaneEmergencyProtectionStateService.canonical(16);
        loaded.restoreHazards(
            CorruptionStateService.canonical(16),
            ArcaneStrainStateService.canonical(16),
            restored);

        assertEquals(0L, restored.readyAtTick(PLAYER, RESOURCE));
    }
}
