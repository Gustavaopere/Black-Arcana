package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.api.hazard.*;
import org.junit.jupiter.api.Test;

import java.util.EnumMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;

class ArcaneHazardRuntimeTest {
    private static final UUID CASTER = UUID.fromString("50000000-0000-0000-0000-000000000001");
    private static final ArcanaSpellId SPELL = ArcanaSpellId.parse("black_arcana:hazard_runtime_probe");

    @Test
    void dangerousActivationOpensSessionAndBacklashAtomically() {
        ArcaneHazardRuntime runtime = new ArcaneHazardRuntime(4);
        ArcaneHazardSnapshot snapshot = snapshot(
            ArcanaCastId.parse("50000000-0000-0000-0000-000000000002"),
            ArcaneDangerTier.FORBIDDEN,
            10L,
            20L);

        var result = runtime.activate(snapshot, zeroResistance(), ArcaneBacklashPolicy.canonical());
        assertTrue(result.activated());
        assertTrue(result.backlashActive());
        assertEquals(1, runtime.sessions().size());
        assertEquals(1, runtime.backlashLedgers().size());
    }

    @Test
    void unstableSessionCanExistWithoutBacklashLedger() {
        ArcaneHazardRuntime runtime = new ArcaneHazardRuntime(4);
        ArcaneHazardSnapshot snapshot = snapshot(
            ArcanaCastId.parse("50000000-0000-0000-0000-000000000003"),
            ArcaneDangerTier.UNSTABLE,
            10L,
            20L);

        var result = runtime.activate(snapshot, zeroResistance(), ArcaneBacklashPolicy.canonical());
        assertTrue(result.activated());
        assertFalse(result.backlashActive());
        assertEquals(1, runtime.sessions().size());
        assertEquals(0, runtime.backlashLedgers().size());
    }

    @Test
    void tickPrunesExpiredLedgerAndSessionWithoutOverflow() {
        ArcaneHazardRuntime runtime = new ArcaneHazardRuntime(4);
        ArcanaCastId cast = ArcanaCastId.parse("50000000-0000-0000-0000-000000000004");
        ArcaneDangerProfile profile = new ArcaneDangerProfile(
            ArcaneDangerTier.FORBIDDEN, 1.0D, 0.0D, 0.0D,
            ArcaneDangerProfile.ABSOLUTE_MAX_DAMAGE_LEASE_TICKS, 4);
        long start = Long.MAX_VALUE - 5L;
        ArcaneHazardSnapshot snapshot = new ArcaneHazardSnapshot(
            cast, SPELL, CASTER, "minecraft:overworld", start, profile);
        assertTrue(runtime.activate(snapshot, zeroResistance(), ArcaneBacklashPolicy.canonical()).activated());

        assertEquals(new ArcaneHazardRuntime.TickResult(0, 0), runtime.tick(Long.MAX_VALUE - 1L));
        assertEquals(new ArcaneHazardRuntime.TickResult(1, 1), runtime.tick(Long.MAX_VALUE));
    }

    private static ArcaneHazardSnapshot snapshot(ArcanaCastId cast, ArcaneDangerTier tier, long start, long lease) {
        double backlash = tier.requiresBacklashRisk() ? 1.0D : 0.0D;
        return new ArcaneHazardSnapshot(
            cast,
            SPELL,
            CASTER,
            "minecraft:overworld",
            start,
            new ArcaneDangerProfile(tier, backlash, 0.2D, 0.2D, lease, 16));
    }

    private static ArcaneResistanceSnapshot zeroResistance() {
        Map<ArcaneResistanceSourceCategory, Double> categories = new EnumMap<>(ArcaneResistanceSourceCategory.class);
        for (ArcaneResistanceSourceCategory category : ArcaneResistanceSourceCategory.values()) categories.put(category, 0.0D);
        return new ArcaneResistanceSnapshot(0.0D, 1.0D, 100.0D, 1_000.0D, List.of(), categories, List.of());
    }
}
