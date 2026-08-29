package dev.gustavopere.blackarcana.integration.curios;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDangerProfile;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDangerTier;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceQuery;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceSourceCategory;
import dev.gustavopere.blackarcana.api.hazard.CorruptionResistanceQuery;
import dev.gustavopere.blackarcana.api.hazard.CorruptionResistanceSourceCategory;
import dev.gustavopere.blackarcana.core.hazard.ArcaneEquipmentSnapshotService;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.atomic.AtomicInteger;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class CuriosHazardResistanceProviderTest {
    private static final UUID PLAYER = UUID.fromString("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa");
    private static final ArcanaCastId CAST = ArcanaCastId.parse("bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb");
    private static final ArcanaSpellId SPELL = ArcanaSpellId.parse("black_arcana:test_curio");
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
    void curioSnapshotContributesToBothResistanceChannels() {
        CuriosHazardResistanceProvider provider = new CuriosHazardResistanceProvider(
            ignored -> snapshot(35.0D, 22.0D));

        var arcane = provider.contributions(new ArcaneResistanceQuery(
            CAST, SPELL, PLAYER, "minecraft:overworld", 100L, PROFILE));
        var corruption = provider.contributions(new CorruptionResistanceQuery(
            CAST, SPELL, PLAYER, "minecraft:overworld", 100L, PROFILE));

        assertEquals(1, arcane.size());
        assertEquals(35.0D, arcane.getFirst().amount());
        assertEquals(ArcaneResistanceSourceCategory.CURIO, arcane.getFirst().category());
        assertEquals(1, corruption.size());
        assertEquals(22.0D, corruption.getFirst().amount());
        assertEquals(CorruptionResistanceSourceCategory.CURIO, corruption.getFirst().category());
    }

    @Test
    void missingOrEmptyCuriosContributeExactlyZero() {
        CuriosHazardResistanceProvider provider = new CuriosHazardResistanceProvider(
            ignored -> snapshot(0.0D, 0.0D));

        assertTrue(provider.contributions(new ArcaneResistanceQuery(
            CAST, SPELL, PLAYER, "minecraft:overworld", 100L, PROFILE)).isEmpty());
        assertTrue(provider.contributions(new CorruptionResistanceQuery(
            CAST, SPELL, PLAYER, "minecraft:overworld", 100L, PROFILE)).isEmpty());
    }

    @Test
    void eachProviderQueryTakesOneBoundedSnapshotOnly() {
        AtomicInteger calls = new AtomicInteger();
        CuriosHazardResistanceProvider provider = new CuriosHazardResistanceProvider(ignored -> {
            calls.incrementAndGet();
            return snapshot(10.0D, 5.0D);
        });

        provider.contributions(new ArcaneResistanceQuery(
            CAST, SPELL, PLAYER, "minecraft:overworld", 100L, PROFILE));

        assertEquals(1, calls.get());
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
