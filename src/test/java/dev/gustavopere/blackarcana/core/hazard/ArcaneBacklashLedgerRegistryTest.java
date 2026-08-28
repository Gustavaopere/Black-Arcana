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

class ArcaneBacklashLedgerRegistryTest {
    private static final UUID CASTER = UUID.fromString("0dd96804-003f-4b6a-8292-fc684bd63aec");
    private static final ArcanaSpellId SPELL = ArcanaSpellId.parse("black_arcana:registry_probe");

    @Test
    void registryRoutesConfirmedDamageByRootCastAndPrunesExpiredLedgers() {
        ArcaneBacklashLedgerRegistry registry = new ArcaneBacklashLedgerRegistry(4);
        ArcanaCastId cast = ArcanaCastId.parse("30000000-0000-0000-0000-000000000001");
        ArcaneHazardSession session = session(cast, 10L, 20L);
        assertTrue(registry.open(session, zeroResistance(), ArcaneBacklashPolicy.canonical()).isPresent());

        ArcanaDamageProvenance provenance = new ArcanaDamageProvenance(
            cast,
            ArcanaDamageInstanceId.parse("30000000-0000-0000-0000-000000000002"),
            CASTER,
            SPELL,
            ArcaneDamageFamily.DIRECT,
            true);
        assertEquals(4.0D, registry.settle(new ArcaneConfirmedDamage(provenance, 4.0D, 15L)).backlashDamage());
        assertEquals(1, registry.size());
        assertEquals(1, registry.pruneExpired(30L));
        assertEquals(0, registry.size());
    }

    @Test
    void missingRootFailsClosedInsteadOfGuessingOwnership() {
        ArcaneBacklashLedgerRegistry registry = new ArcaneBacklashLedgerRegistry(4);
        ArcanaDamageProvenance provenance = new ArcanaDamageProvenance(
            ArcanaCastId.parse("30000000-0000-0000-0000-000000000003"),
            ArcanaDamageInstanceId.parse("30000000-0000-0000-0000-000000000004"),
            CASTER,
            SPELL,
            ArcaneDamageFamily.DIRECT,
            true);
        assertEquals("backlash_ledger_missing",
            registry.settle(new ArcaneConfirmedDamage(provenance, 2.0D, 15L)).code());
    }

    private static ArcaneHazardSession session(ArcanaCastId cast, long start, long lease) {
        ArcaneDangerProfile profile = new ArcaneDangerProfile(
            ArcaneDangerTier.FORBIDDEN, 1.0D, 0.25D, 0.25D, lease, 16);
        return new ArcaneHazardSession(new ArcaneHazardSnapshot(
            cast, SPELL, CASTER, "minecraft:overworld", start, profile));
    }

    private static ArcaneResistanceSnapshot zeroResistance() {
        Map<ArcaneResistanceSourceCategory, Double> categories = new EnumMap<>(ArcaneResistanceSourceCategory.class);
        for (ArcaneResistanceSourceCategory category : ArcaneResistanceSourceCategory.values()) categories.put(category, 0.0D);
        return new ArcaneResistanceSnapshot(0.0D, 1.0D, 100.0D, 1_000.0D, List.of(), categories, List.of());
    }
}
