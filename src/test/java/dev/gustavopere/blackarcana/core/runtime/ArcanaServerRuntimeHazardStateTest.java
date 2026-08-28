package dev.gustavopere.blackarcana.core.runtime;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertNotNull;

class ArcanaServerRuntimeHazardStateTest {
    @Test
    void runtimeOwnsIndependentCorruptionAndStrainState() {
        ArcanaServerRuntime runtime = ArcanaServerRuntime.createDefault();
        assertNotNull(runtime.corruption());
        assertNotNull(runtime.strain());
        assertNotNull(runtime.strain().recoveryProviders());
    }
}
