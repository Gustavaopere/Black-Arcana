package dev.gustavopere.blackarcana.core.world;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import org.junit.jupiter.api.Test;

import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class WorldMutationProtectionAdapterRegistryTest {
    private static final UUID CASTER = UUID.fromString("22222222-2222-2222-2222-222222222222");
    private static final ArcanaCastId CAST = ArcanaCastId.parse("11111111-1111-1111-1111-111111111111");
    private static final ArcanaSpellId SPELL = ArcanaSpellId.parse("black_arcana:black_pyre");
    private static final TemporaryMutationKey KEY = new TemporaryMutationKey("minecraft:overworld", 42L);

    @Test
    void emptyRegistryIsNeutralAllowAndQueryPreservesMutationProvenance() {
        var registry = new WorldMutationProtectionAdapterRegistry(4);
        var query = query();

        assertTrue(registry.authorize(query).allowed());
        assertEquals(CASTER, query.casterId());
        assertEquals(CAST, query.castId());
        assertEquals(SPELL, query.spellId());
        assertEquals(KEY, query.key());
        assertEquals(WorldMutationType.FIRE_SPREAD, query.mutationType());
        assertEquals(WorldMutationClass.TEMPORARY, query.mutationClass());
    }

    @Test
    void everyInstalledAdapterMustAllowAndDenialPropagates() {
        var registry = new WorldMutationProtectionAdapterRegistry(4);
        registry.register("allow", ignored -> ArcanaDecision.allow());
        registry.register("deny", ignored -> ArcanaDecision.deny("claim_denied", "protected cell"));

        var decision = registry.authorize(query());
        assertFalse(decision.allowed());
        assertEquals("claim_denied", decision.code());
    }

    @Test
    void adapterExceptionAndNullDecisionFailClosed() {
        var throwing = new WorldMutationProtectionAdapterRegistry(2);
        throwing.register("broken", ignored -> { throw new IllegalStateException("boom"); });
        assertEquals("world_mutation_protection_adapter_failed", throwing.authorize(query()).code());

        var nullDecision = new WorldMutationProtectionAdapterRegistry(2);
        nullDecision.register("null", ignored -> null);
        assertEquals("world_mutation_protection_adapter_failed", nullDecision.authorize(query()).code());
    }

    @Test
    void registryCapacityAndIdentityAreBounded() {
        assertThrows(IllegalArgumentException.class, () -> new WorldMutationProtectionAdapterRegistry(33));
        var registry = new WorldMutationProtectionAdapterRegistry(1);
        registry.register("one", ignored -> ArcanaDecision.allow());
        assertThrows(IllegalStateException.class,
            () -> registry.register("one", ignored -> ArcanaDecision.allow()));
        assertThrows(IllegalStateException.class,
            () -> registry.register("two", ignored -> ArcanaDecision.allow()));
    }

    private static WorldMutationProtectionQuery query() {
        return new WorldMutationProtectionQuery(
            CASTER,
            CAST,
            SPELL,
            KEY,
            WorldMutationType.FIRE_SPREAD,
            WorldMutationClass.TEMPORARY);
    }
}
