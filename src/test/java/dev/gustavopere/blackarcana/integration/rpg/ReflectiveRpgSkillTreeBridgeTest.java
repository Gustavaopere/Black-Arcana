package dev.gustavopere.blackarcana.integration.rpg;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import dev.gustavopere.blackarcana.api.ArcanaIntegrationAvailability;
import dev.gustavopere.blackarcana.api.ArcanaIntegrationCapability;
import java.util.UUID;
import org.junit.jupiter.api.Test;

class ReflectiveRpgSkillTreeBridgeTest {
    @Test
    void absentModAdvertisesNoCapabilities() {
        ReflectiveRpgSkillTreeBridge bridge = ReflectiveRpgSkillTreeBridge.probe(
            false,
            "not-loaded",
            ignored -> null);

        assertFalse(bridge.available());
        assertEquals(ArcanaIntegrationAvailability.MISSING_MOD, bridge.availability());
        assertTrue(bridge.capabilities().isEmpty());
        assertFalse(bridge.query(UUID.randomUUID()).decision().allowed());
    }

    @Test
    void loadedFlagWithoutBinaryApiIsIncompatibleRatherThanFreeAccess() {
        ReflectiveRpgSkillTreeBridge bridge = ReflectiveRpgSkillTreeBridge.probe(
            true,
            "test",
            ignored -> null);

        assertFalse(bridge.available());
        assertEquals(ArcanaIntegrationAvailability.API_INCOMPATIBLE, bridge.availability());
        assertFalse(bridge.capabilities().contains(ArcanaIntegrationCapability.PROGRESSION_QUERY));
        assertEquals("rpg_integration_unavailable", bridge.query(UUID.randomUUID()).decision().code());
    }
}
