package dev.gustavopere.blackarcana.core.runtime;

import dev.gustavopere.blackarcana.core.hazard.ArcaneStrainStateService;
import dev.gustavopere.blackarcana.core.hazard.CorruptionStateService;
import org.junit.jupiter.api.Test;

import java.util.LinkedHashMap;
import java.util.Map;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;

class ArcanaServerRuntimeHazardStateTest {
    @Test
    void runtimeOwnsIndependentCorruptionAndStrainState() {
        ArcanaServerRuntime runtime = ArcanaServerRuntime.createDefault();
        assertNotNull(runtime.corruption());
        assertNotNull(runtime.strain());
        assertNotNull(runtime.strain().recoveryProviders());
    }

    @Test
    void runtimeHazardCapacityMatchesPersistedOfflinePopulationCeiling() {
        ArcanaServerRuntime runtime = ArcanaServerRuntime.createDefault();
        Map<UUID, CorruptionStateService.PersistedState> corruption = new LinkedHashMap<>();
        Map<UUID, ArcaneStrainStateService.PersistedState> strain = new LinkedHashMap<>();
        for (int i = 0; i < 5_000; i++) {
            UUID id = new UUID(0L, i + 1L);
            corruption.put(id, new CorruptionStateService.PersistedState(1.0D, 0L, -1L, 1L, 0L, CorruptionStateService.STATE_SCHEMA_VERSION));
            strain.put(id, new ArcaneStrainStateService.PersistedState(1.0D, 0L, 1L, 0L, ArcaneStrainStateService.STATE_SCHEMA_VERSION));
        }
        runtime.corruption().restoreSnapshot(corruption);
        runtime.strain().restoreSnapshot(strain);
        assertEquals(5_000, runtime.corruption().size());
        assertEquals(5_000, runtime.strain().size());
    }
}
