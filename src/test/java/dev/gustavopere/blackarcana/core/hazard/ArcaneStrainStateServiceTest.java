package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.hazard.ArcaneStrainProfile;
import dev.gustavopere.blackarcana.api.hazard.ArcaneStrainRecoveryContribution;
import dev.gustavopere.blackarcana.api.hazard.ArcaneStrainRecoveryProvider;
import dev.gustavopere.blackarcana.api.hazard.ArcaneStrainRecoveryQuery;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.Map;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ArcaneStrainStateServiceTest {
    private static final ArcaneStrainProfile TEN = new ArcaneStrainProfile(10.0D, 0.0D, 0.0D, 0.0D, 0.0D, 0.0D, 0.0D);

    @Test
    void repeatedSameTickCastsAreDeterministic() {
        ArcaneStrainStateService service = service(0.0D);
        UUID player = UUID.randomUUID();

        assertEquals(10.0D, service.commitCast(player, 100L, TEN, 1.0D, 0.0D, 0L).after().units());
        assertEquals(20.0D, service.commitCast(player, 100L, TEN, 1.0D, 0.0D, 0L).after().units());
        assertEquals(2L, service.snapshot(player, 100L).acquisitionEvents());
    }

    @Test
    void lazyRecoveryIsMonotonicBoundedAndDoesNotRequireTickScan() {
        ArcaneStrainStateService service = service(0.5D);
        UUID player = UUID.randomUUID();
        service.commitCast(player, 100L, new ArcaneStrainProfile(100.0D, 0.0D, 0.0D, 0.0D, 0.0D, 0.0D, 0.0D), 1.0D, 0.0D, 0L);

        assertEquals(95.0D, service.snapshot(player, 110L).units(), 1.0E-9D);
        assertEquals(0.0D, service.snapshot(player, 400L).units(), 1.0E-9D);
        assertEquals(0.0D, service.snapshot(player, 10_000L).units(), 1.0E-9D);
    }

    @Test
    void persistencePreservesStoredLoadAndContinuesLazyRecoveryAfterRestart() {
        ArcaneStrainStateService first = service(0.5D);
        UUID player = UUID.randomUUID();
        first.commitCast(player, 100L, new ArcaneStrainProfile(100.0D, 0.0D, 0.0D, 0.0D, 0.0D, 0.0D, 0.0D), 1.0D, 0.0D, 0L);
        Map<UUID, ArcaneStrainStateService.PersistedState> persisted = first.persistentSnapshot();

        ArcaneStrainStateService restored = service(0.5D);
        restored.restoreSnapshot(persisted);
        assertEquals(75.0D, restored.snapshot(player, 150L).units(), 1.0E-9D);
    }

    @Test
    void recoveryProvidersAccelerateLazyDecay() {
        ArcaneStrainRecoveryProviderRegistry providers = ArcaneStrainRecoveryProviderRegistry.canonical();
        providers.register(new ArcaneStrainRecoveryProvider() {
            @Override public String providerId() { return "test:rest"; }
            @Override public List<ArcaneStrainRecoveryContribution> contributions(ArcaneStrainRecoveryQuery query) {
                return List.of(new ArcaneStrainRecoveryContribution("test:rest_bonus", 0.5D));
            }
        });
        ArcaneStrainStateService service = new ArcaneStrainStateService(16, 1_000.0D, 0.5D, providers);
        UUID player = UUID.randomUUID();
        service.commitCast(player, 100L, new ArcaneStrainProfile(100.0D, 0.0D, 0.0D, 0.0D, 0.0D, 0.0D, 0.0D), 1.0D, 0.0D, 0L);

        assertEquals(90.0D, service.snapshot(player, 110L).units(), 1.0E-9D);
    }

    @Test
    void zeroStrainProfileDoesNotCreateStateAndProfileControlsPreflightEffects() {
        ArcaneStrainStateService service = service(0.0D);
        UUID player = UUID.randomUUID();
        var update = service.commitCast(player, 100L, ArcaneStrainProfile.none(), 1.0D, 0.0D, 0L);
        assertEquals(0, service.size());
        assertEquals(0.0D, update.appliedDelta());

        service.commitCast(player, 101L, new ArcaneStrainProfile(900.0D, 0.0D, 0.0D, 0.0D, 0.0D, 0.0D, 0.0D), 1.0D, 0.0D, 0L);
        var neutral = service.preflight(player, 101L, ArcaneStrainProfile.none(), 1.0D, 0.0D, 0L);
        assertEquals(1.0D, neutral.backlashMultiplier());
        assertEquals(1.0D, neutral.corruptionMultiplier());
        assertFalse(neutral.hardGateActive());

        var hazardous = service.preflight(player, 101L,
            new ArcaneStrainProfile(1.0D, 0.0D, 0.0D, 0.0D, 1.0D, 2.0D, 800.0D),
            1.0D, 0.0D, 0L);
        assertTrue(hazardous.hardGateActive());
        assertTrue(hazardous.backlashMultiplier() > 1.0D);
        assertTrue(hazardous.corruptionMultiplier() > 1.0D);
    }

    @Test
    void stateClampsWithoutOverflowAndExplicitRecoveryNeverGoesNegative() {
        ArcaneStrainStateService service = new ArcaneStrainStateService(
            16, 100.0D, 0.0D, ArcaneStrainRecoveryProviderRegistry.canonical());
        UUID player = UUID.randomUUID();
        ArcaneStrainProfile huge = new ArcaneStrainProfile(4_096.0D, 4_096.0D, 4_096.0D, 0.0D, 0.0D, 0.0D, 0.0D);
        assertEquals(100.0D, service.commitCast(player, 1L, huge, 1.0D, 1.0E300D, 36_000L).after().units());
        assertEquals(0.0D, service.recover(player, 2L, 1.0E300D).after().units());
        assertEquals(0, service.size());
    }

    private static ArcaneStrainStateService service(double baseRecovery) {
        return new ArcaneStrainStateService(16, 1_000.0D, baseRecovery, ArcaneStrainRecoveryProviderRegistry.canonical());
    }
}
