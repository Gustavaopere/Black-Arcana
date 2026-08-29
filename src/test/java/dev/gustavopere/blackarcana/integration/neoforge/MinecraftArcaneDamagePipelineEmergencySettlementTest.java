package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.api.hazard.ArcanaDamageInstanceId;
import dev.gustavopere.blackarcana.api.hazard.ArcanaDamageProvenance;
import dev.gustavopere.blackarcana.api.hazard.ArcaneBacklashPolicy;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDamageFamily;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDangerProfile;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDangerTier;
import dev.gustavopere.blackarcana.api.hazard.ArcaneEmergencyProtectionSnapshot;
import dev.gustavopere.blackarcana.api.hazard.ArcaneHazardSnapshot;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceSnapshot;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceSourceCategory;
import dev.gustavopere.blackarcana.core.hazard.ArcaneHazardRuntime;
import org.junit.jupiter.api.Test;

import java.util.EnumMap;
import java.util.List;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class MinecraftArcaneDamagePipelineEmergencySettlementTest {
    private static final ArcanaCastId CAST = ArcanaCastId.parse("11111111-2222-3333-4444-555555555555");
    private static final ArcanaSpellId SPELL = ArcanaSpellId.parse("black_arcana:emergency_settlement_probe");
    private static final UUID CASTER = UUID.fromString("aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee");

    @Test
    void causalSessionProducesFrozenBacklashProtectionAttempt() {
        ArcaneHazardRuntime hazards = new ArcaneHazardRuntime(8);
        ArcaneEmergencyProtectionSnapshot emergency = new ArcaneEmergencyProtectionSnapshot(List.of(
            new ArcaneEmergencyProtectionSnapshot.Candidate(
                "black_arcana:test_seal", "black_arcana:test_seal", 8.0D, 200L)));
        activate(hazards, emergency, true);
        ArcanaDamageProvenance provenance = provenance(CAST, SPELL, CASTER);

        var attempt = MinecraftArcaneDamagePipeline.protectionAttempt(hazards, provenance).orElseThrow();

        assertEquals(CAST, attempt.rootCastId());
        assertEquals(provenance.damageInstanceId(), attempt.damageInstanceId());
        assertEquals(CASTER, attempt.casterId());
        assertTrue(attempt.protectionAllowed());
        assertEquals(emergency, attempt.emergencyProtectionSnapshot());
    }

    @Test
    void missingOrMismatchedSessionCannotFabricateEmergencyAttempt() {
        ArcaneHazardRuntime hazards = new ArcaneHazardRuntime(8);
        activate(hazards, ArcaneEmergencyProtectionSnapshot.empty(), true);

        assertTrue(MinecraftArcaneDamagePipeline.protectionAttempt(
            hazards,
            provenance(
                ArcanaCastId.parse("99999999-2222-3333-4444-555555555555"),
                SPELL,
                CASTER)).isEmpty());
        assertTrue(MinecraftArcaneDamagePipeline.protectionAttempt(
            hazards,
            provenance(CAST, ArcanaSpellId.parse("black_arcana:other_spell"), CASTER)).isEmpty());
        assertTrue(MinecraftArcaneDamagePipeline.protectionAttempt(
            hazards,
            provenance(CAST, SPELL, UUID.fromString("ffffffff-bbbb-cccc-dddd-eeeeeeeeeeee"))).isEmpty());
    }

    private static void activate(
        ArcaneHazardRuntime hazards,
        ArcaneEmergencyProtectionSnapshot emergency,
        boolean allowed
    ) {
        ArcaneHazardSnapshot snapshot = new ArcaneHazardSnapshot(
            CAST,
            SPELL,
            CASTER,
            "minecraft:overworld",
            100L,
            new ArcaneDangerProfile(
                ArcaneDangerTier.DANGEROUS, 1.0D, 0.0D, 0.0D, 100L, 16, 0.0D, 0.0D, allowed));
        hazards.activate(snapshot, zeroResistance(), ArcaneBacklashPolicy.canonical(), emergency);
    }

    private static ArcanaDamageProvenance provenance(ArcanaCastId cast, ArcanaSpellId spell, UUID caster) {
        return new ArcanaDamageProvenance(
            cast,
            ArcanaDamageInstanceId.random(),
            caster,
            spell,
            ArcaneDamageFamily.DIRECT,
            true);
    }

    private static ArcaneResistanceSnapshot zeroResistance() {
        EnumMap<ArcaneResistanceSourceCategory, Double> byCategory =
            new EnumMap<>(ArcaneResistanceSourceCategory.class);
        for (ArcaneResistanceSourceCategory category : ArcaneResistanceSourceCategory.values()) {
            byCategory.put(category, 0.0D);
        }
        return new ArcaneResistanceSnapshot(
            0.0D, 1.0D, 40.0D, 240.0D, List.of(), byCategory, List.of());
    }
}
