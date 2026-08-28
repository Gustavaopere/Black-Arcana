package dev.gustavopere.blackarcana.core.world;

import dev.gustavopere.blackarcana.api.ArcanaDecision;
import org.junit.jupiter.api.Test;

import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class EntityInteractionAdmissionServiceTest {
    private static final UUID CASTER = UUID.fromString("11111111-1111-1111-1111-111111111111");

    @Test
    void basePolicyDenialRunsBeforeProtectionAdapters() {
        ProtectionAdapterRegistry adapters = new ProtectionAdapterRegistry(4);
        adapters.register("must-not-run", query -> {
            throw new AssertionError("adapter must not run after core policy denial");
        });
        EntityInteractionAdmissionService service = new EntityInteractionAdmissionService(
            DefaultEntityInteractionPolicy.safeDefaults(),
            adapters);

        EntityInteractionAuthorization result = service.authorize(
            EntityInteractionType.DAMAGE,
            new EntityProtectionFacts(true, false, false, false, false),
            query(EntityInteractionType.DAMAGE));

        assertFalse(result.decision().allowed());
        assertEquals("pvp_disabled", result.decision().code());
    }

    @Test
    void protectionAdapterCanDenyOtherwiseAllowedInteractionWithoutChangingCaps() {
        ProtectionAdapterRegistry adapters = new ProtectionAdapterRegistry(4);
        adapters.register("claims", query -> ArcanaDecision.deny("claim_protected", "protected test target"));
        EntityInteractionAdmissionService service = new EntityInteractionAdmissionService(
            DefaultEntityInteractionPolicy.safeDefaults(),
            adapters);

        EntityInteractionAuthorization result = service.authorize(
            EntityInteractionType.DAMAGE,
            new EntityProtectionFacts(false, false, false, false, true),
            query(EntityInteractionType.DAMAGE));

        assertFalse(result.decision().allowed());
        assertEquals("claim_protected", result.decision().code());
        assertEquals(EntityEffectLimits.standard(), result.limits());
    }

    @Test
    void bossDamageRemainsAllowedButUsesBossCaps() {
        EntityInteractionAdmissionService service = new EntityInteractionAdmissionService(
            DefaultEntityInteractionPolicy.safeDefaults(),
            new ProtectionAdapterRegistry(4));

        EntityInteractionAuthorization result = service.authorize(
            EntityInteractionType.DAMAGE,
            new EntityProtectionFacts(false, false, true, false, true),
            query(EntityInteractionType.DAMAGE));

        assertTrue(result.decision().allowed());
        assertEquals(EntityEffectLimits.bossSafeDefaults(), result.limits());
    }

    @Test
    void mismatchedProtectionQueryFailsClosed() {
        EntityInteractionAdmissionService service = new EntityInteractionAdmissionService(
            DefaultEntityInteractionPolicy.safeDefaults(),
            new ProtectionAdapterRegistry(4));

        EntityInteractionAuthorization result = service.authorize(
            EntityInteractionType.CONTROL,
            new EntityProtectionFacts(false, false, false, false, true),
            query(EntityInteractionType.DAMAGE));

        assertFalse(result.decision().allowed());
        assertEquals("protection_query_mismatch", result.decision().code());
    }

    private static ProtectionQuery query(EntityInteractionType type) {
        return new ProtectionQuery(CASTER, "minecraft:overworld", "target:test", type);
    }
}
