package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.ArcanaCastContext;
import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaCost;
import dev.gustavopere.blackarcana.api.ArcanaServices.TargetResolution;
import dev.gustavopere.blackarcana.api.ArcanaSpellDefinition;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.api.hazard.ArcanaDamageInstanceId;
import dev.gustavopere.blackarcana.api.hazard.ArcanaDamageProvenance;
import dev.gustavopere.blackarcana.api.hazard.ArcaneBacklashPolicy;
import dev.gustavopere.blackarcana.api.hazard.ArcaneBacklashSettlement;
import dev.gustavopere.blackarcana.api.hazard.ArcaneConfirmedDamage;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDamageFamily;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDangerProfile;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDangerTier;
import dev.gustavopere.blackarcana.api.hazard.ArcaneHazardSnapshot;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceContribution;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceProvider;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceQuery;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceSnapshot;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceSourceCategory;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.atomic.AtomicReference;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ArcaneOptionalProviderSnapshotHardeningTest {
    private static final UUID CASTER = UUID.fromString("81000000-0000-0000-0000-000000000001");
    private static final ArcanaSpellId SPELL = ArcanaSpellId.parse("black_arcana:optional_snapshot_probe");
    private static final ArcanaCastId FIRST_CAST = ArcanaCastId.parse("81000000-0000-0000-0000-000000000002");
    private static final ArcanaCastId SECOND_CAST = ArcanaCastId.parse("81000000-0000-0000-0000-000000000003");

    @Test
    void curioAndRpgSwapsAfterActivationCannotRewriteDelayedBacklashSnapshot() {
        AtomicReference<Double> curioResistance = new AtomicReference<>(40.0D);
        AtomicReference<Double> rpgResistance = new AtomicReference<>(40.0D);
        ArcaneResistanceProviderRegistry providers = ArcaneResistanceProviderRegistry.canonical(8);
        providers.register(mutableProvider(
            "test:curio",
            "test:warded_ring",
            ArcaneResistanceSourceCategory.CURIO,
            curioResistance));
        providers.register(mutableProvider(
            "test:rpg",
            "test:arcane_perk",
            ArcaneResistanceSourceCategory.RPG,
            rpgResistance));

        ArcaneHazardRuntime runtime = new ArcaneHazardRuntime(4);
        ArcaneHazardCastGate gate = new ArcaneHazardCastGate(
            profiles(),
            providers,
            runtimeActivator(runtime));

        var first = gate.preflight(request(FIRST_CAST, 100L), TargetResolution.resolved("target"));
        assertTrue(first.decision().allowed());
        assertTrue(first.activate().allowed());

        ArcaneResistanceSnapshot frozenFirst = runtime.backlashLedgers()
            .find(FIRST_CAST)
            .orElseThrow()
            .snapshot()
            .arcaneResistance();
        assertEquals(80.0D, frozenFirst.effectiveResistance(), 0.0D);

        // Simulate removing a Curio and an RPG perk after this root cast is already active.
        curioResistance.set(0.0D);
        rpgResistance.set(0.0D);

        ArcaneBacklashSettlement delayed = runtime.settle(damage(
            FIRST_CAST,
            105L,
            "81000000-0000-0000-0000-000000000004"));
        assertEquals(ArcaneBacklashSettlement.Status.SETTLED, delayed.status());
        assertEquals(
            10.0D * frozenFirst.residualBacklashMultiplier(),
            delayed.backlashDamage(),
            1.0E-12D);
        assertEquals(
            80.0D,
            runtime.backlashLedgers()
                .find(FIRST_CAST)
                .orElseThrow()
                .snapshot()
                .arcaneResistance()
                .effectiveResistance(),
            0.0D);

        // A later root cast must capture the provider state that exists at its own boundary.
        var second = gate.preflight(request(SECOND_CAST, 106L), TargetResolution.resolved("target"));
        assertTrue(second.decision().allowed());
        assertTrue(second.activate().allowed());

        ArcaneResistanceSnapshot frozenSecond = runtime.backlashLedgers()
            .find(SECOND_CAST)
            .orElseThrow()
            .snapshot()
            .arcaneResistance();
        assertEquals(0.0D, frozenSecond.effectiveResistance(), 0.0D);

        ArcaneBacklashSettlement future = runtime.settle(damage(
            SECOND_CAST,
            107L,
            "81000000-0000-0000-0000-000000000005"));
        assertEquals(ArcaneBacklashSettlement.Status.SETTLED, future.status());
        assertEquals(10.0D, future.backlashDamage(), 0.0D);
    }

    private static ArcaneResistanceProvider mutableProvider(
        String providerId,
        String sourceId,
        ArcaneResistanceSourceCategory category,
        AtomicReference<Double> amount
    ) {
        return new ArcaneResistanceProvider() {
            @Override
            public String providerId() {
                return providerId;
            }

            @Override
            public List<ArcaneResistanceContribution> contributions(ArcaneResistanceQuery query) {
                double current = amount.get();
                return current <= 0.0D
                    ? List.of()
                    : List.of(new ArcaneResistanceContribution(sourceId, category, current));
            }
        };
    }

    private static ArcaneHazardCastGate.HazardSessionActivator runtimeActivator(ArcaneHazardRuntime runtime) {
        return new ArcaneHazardCastGate.HazardSessionActivator() {
            @Override
            public ArcaneHazardRuntime.ActivationResult activate(
                ArcaneHazardSnapshot snapshot,
                ArcaneResistanceSnapshot resistance,
                ArcaneBacklashPolicy policy
            ) {
                return runtime.activate(snapshot, resistance, policy);
            }

            @Override
            public boolean close(ArcanaCastId castId) {
                return runtime.close(castId);
            }
        };
    }

    private static ArcaneDangerProfileRegistry profiles() {
        ArcaneDangerProfileRegistry registry = new ArcaneDangerProfileRegistry();
        registry.replaceAll(Map.of(
            SPELL,
            new ArcaneDangerProfile(
                ArcaneDangerTier.FORBIDDEN,
                1.0D,
                0.0D,
                0.0D,
                200L,
                16)));
        return registry;
    }

    private static ArcanaCastRequest request(ArcanaCastId castId, long tick) {
        ArcanaSpellDefinition spell = new ArcanaSpellDefinition(
            SPELL,
            "spell.black_arcana.optional_snapshot_probe",
            "black_arcana:textures/spell/optional_snapshot_probe.png",
            new ArcanaCost("black_arcana:test_resource", 1.0D),
            true);
        return new ArcanaCastRequest(
            castId,
            spell,
            new ArcanaCastContext(CASTER, tick, "minecraft:overworld"));
    }

    private static ArcaneConfirmedDamage damage(ArcanaCastId castId, long tick, String damageId) {
        return new ArcaneConfirmedDamage(
            new ArcanaDamageProvenance(
                castId,
                ArcanaDamageInstanceId.parse(damageId),
                CASTER,
                SPELL,
                ArcaneDamageFamily.DAMAGE_OVER_TIME,
                true),
            10.0D,
            tick);
    }
}
