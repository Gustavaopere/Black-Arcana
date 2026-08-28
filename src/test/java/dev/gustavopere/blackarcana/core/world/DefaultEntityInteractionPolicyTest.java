package dev.gustavopere.blackarcana.core.world;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class DefaultEntityInteractionPolicyTest {
    private final DefaultEntityInteractionPolicy policy = DefaultEntityInteractionPolicy.safeDefaults();

    @Test
    void pvpAndAlliedTargetsAreProtected() {
        var pvpOff = new EntityProtectionFacts(true, false, false, false, false);
        var ally = new EntityProtectionFacts(true, true, false, false, true);

        assertEquals("pvp_disabled", policy.authorize(EntityInteractionType.DAMAGE, pvpOff).decision().code());
        assertEquals("target_allied", policy.authorize(EntityInteractionType.CONTROL, ally).decision().code());
    }

    @Test
    void bossesUseExplicitCapsInsteadOfBlanketImmunity() {
        var boss = new EntityProtectionFacts(false, false, true, false, true);

        var damage = policy.authorize(EntityInteractionType.DAMAGE, boss);
        var control = policy.authorize(EntityInteractionType.CONTROL, boss);
        var execution = policy.authorize(EntityInteractionType.EXECUTION, boss);

        assertTrue(damage.decision().allowed());
        assertTrue(control.decision().allowed());
        assertEquals(1.0, damage.limits().damageMultiplierCap());
        assertEquals(40, control.limits().maxControlTicks());
        assertFalse(execution.decision().allowed());
        assertFalse(execution.limits().executionAllowed());
    }

    @Test
    void invulnerableTargetFailsClosed() {
        var invulnerable = new EntityProtectionFacts(false, false, false, true, true);
        assertEquals("target_invulnerable",
            policy.authorize(EntityInteractionType.DISPLACEMENT, invulnerable).decision().code());
    }
}
