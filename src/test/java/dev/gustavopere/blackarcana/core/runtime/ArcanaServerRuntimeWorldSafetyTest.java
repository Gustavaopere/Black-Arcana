package dev.gustavopere.blackarcana.core.runtime;

import dev.gustavopere.blackarcana.core.world.WorldEffectMode;
import dev.gustavopere.blackarcana.core.world.WorldEffectPolicyConfig;
import org.junit.jupiter.api.Test;

import java.util.Map;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;

class ArcanaServerRuntimeWorldSafetyTest {
    @Test
    void defaultRuntimeOwnsSingleWorldSafetyServiceSet() {
        ArcanaServerRuntime runtime = ArcanaServerRuntime.createDefault();

        assertNotNull(runtime.worldEffectProfiles());
        assertNotNull(runtime.worldEffectPolicy());
        assertNotNull(runtime.worldEffectBudgets());
        assertNotNull(runtime.temporaryMutations());
        assertNotNull(runtime.entityInteractionPolicy());
        assertNotNull(runtime.protectionAdapters());
        assertEquals(WorldEffectMode.TEMPORARY, runtime.worldEffectPolicy().config().globalMode());
    }

    @Test
    void runtimeCanApplyStricterServerWorldPolicyWithoutReplacingEngineReferences() {
        ArcanaServerRuntime runtime = ArcanaServerRuntime.createDefault();
        var samePolicy = runtime.worldEffectPolicy();

        runtime.configureWorldEffects(new WorldEffectPolicyConfig(
            WorldEffectMode.OFF,
            64,
            false,
            Map.of()));

        assertEquals(samePolicy, runtime.worldEffectPolicy());
        assertEquals(WorldEffectMode.OFF, samePolicy.config().globalMode());
        assertEquals(64, samePolicy.config().globalMaxAffectedUnits());
    }
}
