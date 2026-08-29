package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDangerProfile;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDangerTier;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceQuery;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceSourceCategory;
import dev.gustavopere.blackarcana.api.hazard.CorruptionResistanceQuery;
import dev.gustavopere.blackarcana.api.hazard.CorruptionResistanceSourceCategory;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicReference;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ArcaneEquipmentHazardResistanceProviderTest {
    private static final UUID PLAYER = UUID.fromString("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa");
    private static final ArcanaCastId CAST = ArcanaCastId.parse("bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb");
    private static final ArcanaCastId NEXT_CAST = ArcanaCastId.parse("cccccccc-cccc-cccc-cccc-cccccccccccc");
    private static final ArcanaSpellId SPELL = ArcanaSpellId.parse("black_arcana:test_equipment");
    private static final ArcaneDangerProfile PROFILE = new ArcaneDangerProfile(
        ArcaneDangerTier.DANGEROUS,
        1.0D,
        2.0D,
        3.0D,
        40L,
        16,
        10.0D,
        20.0D,
        false);

    @Test
    void sameRootCastSharesOneFrozenSnapshotAcrossResistanceChannels() {
        AtomicInteger calls = new AtomicInteger();
        AtomicReference<ArcaneEquipmentSnapshotService.Snapshot> current =
            new AtomicReference<>(snapshot(35.0D, 22.0D));
        ArcaneEquipmentHazardResistanceProvider provider = new ArcaneEquipmentHazardResistanceProvider(playerId -> {
            assertEquals(PLAYER, playerId);
            calls.incrementAndGet();
            return current.get();
        });

        var arcane = provider.contributions(arcane(CAST));
        current.set(snapshot(90.0D, 5.0D));
        var corruption = provider.contributions(corruption(CAST));

        assertEquals(1, calls.get());
        assertEquals(35.0D, arcane.getFirst().amount());
        assertEquals(ArcaneResistanceSourceCategory.EQUIPMENT, arcane.getFirst().category());
        assertEquals(22.0D, corruption.getFirst().amount());
        assertEquals(CorruptionResistanceSourceCategory.EQUIPMENT, corruption.getFirst().category());
    }

    @Test
    void differentRootCastTakesFreshSnapshot() {
        AtomicInteger calls = new AtomicInteger();
        AtomicReference<ArcaneEquipmentSnapshotService.Snapshot> current =
            new AtomicReference<>(snapshot(10.0D, 4.0D));
        ArcaneEquipmentHazardResistanceProvider provider = new ArcaneEquipmentHazardResistanceProvider(playerId -> {
            calls.incrementAndGet();
            return current.get();
        });

        assertEquals(10.0D, provider.contributions(arcane(CAST)).getFirst().amount());
        current.set(snapshot(45.0D, 12.0D));
        assertEquals(45.0D, provider.contributions(arcane(NEXT_CAST)).getFirst().amount());
        assertEquals(2, calls.get());
    }

    @Test
    void explicitReleaseAllowsFreshSnapshotForAbortedPreflight() {
        AtomicInteger calls = new AtomicInteger();
        AtomicReference<ArcaneEquipmentSnapshotService.Snapshot> current =
            new AtomicReference<>(snapshot(10.0D, 4.0D));
        ArcaneEquipmentHazardResistanceProvider provider = new ArcaneEquipmentHazardResistanceProvider(playerId -> {
            calls.incrementAndGet();
            return current.get();
        });

        provider.contributions(arcane(CAST));
        provider.release(CAST);
        current.set(snapshot(45.0D, 12.0D));

        assertEquals(12.0D, provider.contributions(corruption(CAST)).getFirst().amount());
        assertEquals(2, calls.get());
    }

    @Test
    void zeroEquipmentResistanceContributesNothing() {
        ArcaneEquipmentHazardResistanceProvider provider =
            new ArcaneEquipmentHazardResistanceProvider(playerId -> snapshot(0.0D, 0.0D));

        assertTrue(provider.contributions(arcane(CAST)).isEmpty());
        assertTrue(provider.contributions(corruption(CAST)).isEmpty());
    }

    private static ArcaneResistanceQuery arcane(ArcanaCastId castId) {
        return new ArcaneResistanceQuery(
            castId, SPELL, PLAYER, "minecraft:overworld", 100L, PROFILE);
    }

    private static CorruptionResistanceQuery corruption(ArcanaCastId castId) {
        return new CorruptionResistanceQuery(
            castId, SPELL, PLAYER, "minecraft:overworld", 100L, PROFILE);
    }

    private static ArcaneEquipmentSnapshotService.Snapshot snapshot(double arcane, double corruption) {
        return new ArcaneEquipmentSnapshotService.Snapshot(
            List.of(),
            Map.of(),
            arcane,
            corruption,
            0.0D,
            0.0D);
    }
}
