package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.ArcanaCastContext;
import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaCost;
import dev.gustavopere.blackarcana.api.ArcanaServices.TargetResolution;
import dev.gustavopere.blackarcana.api.ArcanaSpellDefinition;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.api.hazard.ArcaneBacklashPolicy;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDangerProfile;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDangerTier;
import dev.gustavopere.blackarcana.api.hazard.ArcaneHazardSnapshot;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceSnapshot;
import dev.gustavopere.blackarcana.api.hazard.ArcaneStrainProfile;
import dev.gustavopere.blackarcana.api.hazard.CorruptionAcquisitionProfile;
import dev.gustavopere.blackarcana.api.hazard.CorruptionResistanceContribution;
import dev.gustavopere.blackarcana.api.hazard.CorruptionResistanceProvider;
import dev.gustavopere.blackarcana.api.hazard.CorruptionResistanceQuery;
import dev.gustavopere.blackarcana.api.hazard.CorruptionResistanceSourceCategory;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.atomic.AtomicReference;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ArcaneHazardStateSettlementTest {
    private static final ArcanaSpellId SPELL_ID = ArcanaSpellId.parse("black_arcana:test_state_settlement");
    private static final UUID CASTER_ID = UUID.fromString("aaaaaaaa-1111-2222-3333-bbbbbbbbbbbb");

    @Test
    void committedCastUsesFrozenCorruptionResistanceAndStrainPreflight() {
        ArcaneDangerProfileRegistry profiles = profiles(profile(20.0D, 12.0D));
        ArcaneResistanceProviderRegistry arcane = ArcaneResistanceProviderRegistry.canonical(4);
        CorruptionResistanceProviderRegistry corruptionResistance = CorruptionResistanceProviderRegistry.canonical(4);
        AtomicReference<Double> corruptionAmount = new AtomicReference<>(40.0D);
        corruptionResistance.register(fixedCorruptionProvider(corruptionAmount));
        CorruptionStateService corruption = CorruptionStateService.canonical(16);
        ArcaneStrainStateService strain = ArcaneStrainStateService.canonical(16);

        strain.commitCast(CASTER_ID, 100L, baseStrain(20.0D), 1.0D, 0.0D, 0L);

        ArcaneHazardCastGate gate = new ArcaneHazardCastGate(
            profiles,
            arcane,
            corruptionResistance,
            corruption,
            strain,
            16,
            successfulActivator());

        var preparation = gate.preflight(request(), TargetResolution.resolved("target"));
        assertTrue(preparation.decision().allowed());
        assertEquals(0.0D, corruption.snapshot(CASTER_ID).units());
        assertEquals(20.0D, strain.snapshot(CASTER_ID, 100L).units());

        corruptionAmount.set(0.0D);
        strain.recover(CASTER_ID, 100L, 20.0D);
        assertEquals(0.0D, strain.snapshot(CASTER_ID, 100L).units());

        assertTrue(preparation.activate().allowed());
        preparation.commit();

        // Corruption Resistance is independent: canonical K=60, so R=40 -> 0.6 residual.
        assertEquals(12.0D, corruption.snapshot(CASTER_ID).units());
        assertEquals(32.0D, strain.snapshot(CASTER_ID, 100L).units());
    }

    @Test
    void overlappingSameTickCastsAccumulateFrozenStrainWithoutLostUpdates() {
        ArcaneDangerProfileRegistry profiles = profiles(profile(0.0D, 12.0D));
        ArcaneResistanceProviderRegistry arcane = ArcaneResistanceProviderRegistry.canonical(4);
        CorruptionResistanceProviderRegistry corruptionResistance = CorruptionResistanceProviderRegistry.canonical(4);
        CorruptionStateService corruption = CorruptionStateService.canonical(16);
        ArcaneStrainStateService strain = ArcaneStrainStateService.canonical(16);
        strain.commitCast(CASTER_ID, 100L, baseStrain(20.0D), 1.0D, 0.0D, 0L);

        ArcaneHazardCastGate gate = new ArcaneHazardCastGate(
            profiles,
            arcane,
            corruptionResistance,
            corruption,
            strain,
            16,
            successfulActivator());

        var first = gate.preflight(
            request(CASTER_ID, "11111111-aaaa-bbbb-cccc-222222222221"),
            TargetResolution.resolved("target"));
        var second = gate.preflight(
            request(CASTER_ID, "11111111-aaaa-bbbb-cccc-222222222222"),
            TargetResolution.resolved("target"));

        assertTrue(first.decision().allowed());
        assertTrue(second.decision().allowed());
        assertTrue(first.activate().allowed());
        assertTrue(second.activate().allowed());
        first.commit();
        second.commit();

        assertEquals(44.0D, strain.snapshot(CASTER_ID, 100L).units());
    }

    @Test
    void corruptionStateSnapshotCannotBeEvadedAfterPreflight() {
        ArcaneDangerProfileRegistry profiles = profiles(profile(10.0D, 0.0D));
        ArcaneResistanceProviderRegistry arcane = ArcaneResistanceProviderRegistry.canonical(4);
        CorruptionResistanceProviderRegistry corruptionResistance = CorruptionResistanceProviderRegistry.canonical(4);
        CorruptionStateService corruption = CorruptionStateService.canonical(16);
        ArcaneStrainStateService strain = ArcaneStrainStateService.canonical(16);

        var emptyResistance = corruptionResistance.snapshot(new CorruptionResistanceQuery(
            ArcanaCastId.parse("33333333-aaaa-bbbb-cccc-444444444444"),
            SPELL_ID,
            CASTER_ID,
            "minecraft:overworld",
            100L,
            profile(10.0D, 0.0D)));
        corruption.acquireFromCommittedCast(
            CASTER_ID,
            100L,
            CorruptionAcquisitionProfile.committedCastOnly(30.0D, 0.0D),
            emptyResistance);

        ArcaneHazardCastGate gate = new ArcaneHazardCastGate(
            profiles,
            arcane,
            corruptionResistance,
            corruption,
            strain,
            16,
            successfulActivator());

        var preparation = gate.preflight(request(), TargetResolution.resolved("target"));
        assertTrue(preparation.decision().allowed());
        assertEquals(30.0D, corruption.snapshot(CASTER_ID).units());

        corruption.recover(CASTER_ID, 100L, 30.0D);
        assertEquals(0.0D, corruption.snapshot(CASTER_ID).units());

        assertTrue(preparation.activate().allowed());
        preparation.commit();

        assertEquals(40.0D, corruption.snapshot(CASTER_ID).units());
    }

    @Test
    void activationFailsClosedWhenAnotherCasterClaimsTheFinalStateSlot() {
        ArcaneDangerProfileRegistry profiles = profiles(profile(5.0D, 5.0D));
        ArcaneResistanceProviderRegistry arcane = ArcaneResistanceProviderRegistry.canonical(4);
        CorruptionResistanceProviderRegistry corruptionResistance = CorruptionResistanceProviderRegistry.canonical(4);
        CorruptionStateService corruption = CorruptionStateService.canonical(1);
        ArcaneStrainStateService strain = ArcaneStrainStateService.canonical(1);

        ArcaneHazardCastGate gate = new ArcaneHazardCastGate(
            profiles,
            arcane,
            corruptionResistance,
            corruption,
            strain,
            1,
            successfulActivator());

        UUID secondCaster = UUID.fromString("cccccccc-1111-2222-3333-dddddddddddd");
        var first = gate.preflight(
            request(CASTER_ID, "55555555-aaaa-bbbb-cccc-666666666661"),
            TargetResolution.resolved("target"));
        var second = gate.preflight(
            request(secondCaster, "55555555-aaaa-bbbb-cccc-666666666662"),
            TargetResolution.resolved("target"));

        assertTrue(first.decision().allowed());
        assertTrue(second.decision().allowed());
        assertTrue(first.activate().allowed());

        var secondActivation = second.activate();
        assertFalse(secondActivation.allowed());
        assertEquals("hazard_state_capacity", secondActivation.code());

        first.commit();
        second.cancel();
        assertEquals(1, corruption.size());
        assertEquals(1, strain.size());
    }

    @Test
    void cancelledCastCreatesNoCorruptionOrStrainState() {
        ArcaneDangerProfileRegistry profiles = profiles(profile(8.0D, 6.0D));
        ArcaneResistanceProviderRegistry arcane = ArcaneResistanceProviderRegistry.canonical(4);
        CorruptionResistanceProviderRegistry corruptionResistance = CorruptionResistanceProviderRegistry.canonical(4);
        CorruptionStateService corruption = CorruptionStateService.canonical(16);
        ArcaneStrainStateService strain = ArcaneStrainStateService.canonical(16);

        ArcaneHazardCastGate gate = new ArcaneHazardCastGate(
            profiles,
            arcane,
            corruptionResistance,
            corruption,
            strain,
            16,
            successfulActivator());

        var preparation = gate.preflight(request(), TargetResolution.resolved("target"));
        assertTrue(preparation.decision().allowed());
        assertTrue(preparation.activate().allowed());
        preparation.cancel();

        assertEquals(0.0D, corruption.snapshot(CASTER_ID).units());
        assertEquals(0.0D, strain.snapshot(CASTER_ID, 100L).units());
        assertEquals(0, corruption.size());
        assertEquals(0, strain.size());
    }

    @Test
    void preflightFailsClosedWhenCommittedStateCannotBeTracked() {
        ArcaneDangerProfileRegistry profiles = profiles(profile(5.0D, 5.0D));
        ArcaneResistanceProviderRegistry arcane = ArcaneResistanceProviderRegistry.canonical(4);
        CorruptionResistanceProviderRegistry corruptionResistance = CorruptionResistanceProviderRegistry.canonical(4);
        CorruptionStateService corruption = CorruptionStateService.canonical(1);
        ArcaneStrainStateService strain = ArcaneStrainStateService.canonical(1);

        UUID other = UUID.fromString("cccccccc-1111-2222-3333-dddddddddddd");
        var emptyCorruptionResistance = corruptionResistance.snapshot(new CorruptionResistanceQuery(
            ArcanaCastId.parse("eeeeeeee-1111-2222-3333-ffffffffffff"),
            SPELL_ID,
            other,
            "minecraft:overworld",
            100L,
            profile(5.0D, 5.0D)));
        corruption.acquireFromCommittedCast(
            other,
            100L,
            CorruptionAcquisitionProfile.committedCastOnly(1.0D, 0.0D),
            emptyCorruptionResistance);
        strain.commitCast(other, 100L, baseStrain(1.0D), 1.0D, 0.0D, 0L);

        ArcaneHazardCastGate gate = new ArcaneHazardCastGate(
            profiles,
            arcane,
            corruptionResistance,
            corruption,
            strain,
            1,
            successfulActivator());

        var preparation = gate.preflight(request(), TargetResolution.resolved("target"));
        assertFalse(preparation.decision().allowed());
        assertEquals("hazard_state_capacity", preparation.decision().code());
    }

    private static CorruptionResistanceProvider fixedCorruptionProvider(AtomicReference<Double> amount) {
        return new CorruptionResistanceProvider() {
            @Override public String providerId() { return "test:corruption"; }
            @Override
            public List<CorruptionResistanceContribution> contributions(CorruptionResistanceQuery query) {
                return List.of(new CorruptionResistanceContribution(
                    "test:ward",
                    CorruptionResistanceSourceCategory.RITUAL,
                    amount.get()));
            }
        };
    }

    private static ArcaneHazardCastGate.HazardSessionActivator successfulActivator() {
        return new ArcaneHazardCastGate.HazardSessionActivator() {
            @Override
            public ArcaneHazardRuntime.ActivationResult activate(
                ArcaneHazardSnapshot snapshot,
                ArcaneResistanceSnapshot resistance,
                ArcaneBacklashPolicy policy
            ) {
                return ArcaneHazardRuntime.ActivationResult.success(true);
            }

            @Override public boolean close(ArcanaCastId castId) { return true; }
        };
    }

    private static ArcaneDangerProfileRegistry profiles(ArcaneDangerProfile profile) {
        ArcaneDangerProfileRegistry registry = new ArcaneDangerProfileRegistry();
        registry.replaceAll(Map.of(SPELL_ID, profile));
        return registry;
    }

    private static ArcaneDangerProfile profile(double corruption, double strain) {
        return new ArcaneDangerProfile(
            ArcaneDangerTier.DANGEROUS,
            1.0D,
            corruption,
            strain,
            100L,
            16,
            0.0D,
            0.0D,
            false);
    }

    private static ArcaneStrainProfile baseStrain(double units) {
        return new ArcaneStrainProfile(units, 0.0D, 0.0D, 0.0D, 0.0D, 0.0D, 0.0D);
    }

    private static ArcanaCastRequest request() {
        return request(CASTER_ID, "11111111-aaaa-bbbb-cccc-222222222222");
    }

    private static ArcanaCastRequest request(UUID casterId, String castId) {
        ArcanaSpellDefinition spell = new ArcanaSpellDefinition(
            SPELL_ID,
            "spell.black_arcana.test_state_settlement",
            "black_arcana:textures/spell/test_state_settlement.png",
            new ArcanaCost("black_arcana:test_resource", 1.0D),
            true);
        return new ArcanaCastRequest(
            ArcanaCastId.parse(castId),
            spell,
            new ArcanaCastContext(casterId, 100L, "minecraft:overworld"));
    }
}
