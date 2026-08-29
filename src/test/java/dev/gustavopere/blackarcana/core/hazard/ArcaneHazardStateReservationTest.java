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
import org.junit.jupiter.api.Test;

import java.util.Map;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ArcaneHazardStateReservationTest {
    private static final ArcanaSpellId SPELL = ArcanaSpellId.parse("black_arcana:test_reservation");
    private static final UUID FIRST = UUID.fromString("10000000-0000-0000-0000-000000000001");
    private static final UUID SECOND = UUID.fromString("20000000-0000-0000-0000-000000000002");

    @Test
    void activationClaimsLastPersistentStateSlotAndCancelReleasesIt() {
        ArcaneHazardCastGate gate = gate(1);
        var first = gate.preflight(request(FIRST, "11111111-0000-0000-0000-000000000001"), TargetResolution.resolved("target"));
        var second = gate.preflight(request(SECOND, "22222222-0000-0000-0000-000000000002"), TargetResolution.resolved("target"));

        assertTrue(first.decision().allowed());
        assertTrue(second.decision().allowed());
        assertTrue(first.activate().allowed());

        var denied = second.activate();
        assertEquals("hazard_state_capacity", denied.code());

        first.cancel();
        var retried = gate.preflight(request(SECOND, "33333333-0000-0000-0000-000000000003"), TargetResolution.resolved("target"));
        assertTrue(retried.activate().allowed());
        retried.cancel();
    }

    @Test
    void overlappingStatefulCastsForSameCasterCannotCommitStaleStrainSnapshot() {
        ArcaneHazardCastGate gate = gate(4);
        var first = gate.preflight(request(FIRST, "44444444-0000-0000-0000-000000000004"), TargetResolution.resolved("target"));
        var second = gate.preflight(request(FIRST, "55555555-0000-0000-0000-000000000005"), TargetResolution.resolved("target"));

        assertTrue(first.activate().allowed());
        var denied = second.activate();
        assertEquals("hazard_state_busy", denied.code());

        first.commit();
        second.cancel();
    }

    private static ArcaneHazardCastGate gate(int maxPlayers) {
        ArcaneDangerProfileRegistry profiles = new ArcaneDangerProfileRegistry();
        profiles.replaceAll(Map.of(SPELL, new ArcaneDangerProfile(
            ArcaneDangerTier.DANGEROUS,
            1.0D,
            2.0D,
            3.0D,
            100L,
            16,
            0.0D,
            0.0D,
            false)));
        return new ArcaneHazardCastGate(
            profiles,
            ArcaneResistanceProviderRegistry.canonical(4),
            CorruptionResistanceProviderRegistry.canonical(4),
            CorruptionStateService.canonical(maxPlayers),
            ArcaneStrainStateService.canonical(maxPlayers),
            maxPlayers,
            new ArcaneHazardCastGate.HazardSessionActivator() {
                @Override
                public ArcaneHazardRuntime.ActivationResult activate(
                    ArcaneHazardSnapshot snapshot,
                    ArcaneResistanceSnapshot resistance,
                    ArcaneBacklashPolicy policy
                ) {
                    return ArcaneHazardRuntime.ActivationResult.success(true);
                }

                @Override public boolean close(ArcanaCastId castId) { return true; }
            });
    }

    private static ArcanaCastRequest request(UUID caster, String castId) {
        return new ArcanaCastRequest(
            ArcanaCastId.parse(castId),
            new ArcanaSpellDefinition(
                SPELL,
                "spell.black_arcana.test_reservation",
                "black_arcana:textures/spell/test_reservation.png",
                new ArcanaCost("black_arcana:test_resource", 1.0D),
                true),
            new ArcanaCastContext(caster, 100L, "minecraft:overworld"));
    }
}
