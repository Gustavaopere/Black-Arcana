package dev.gustavopere.blackarcana.content.space;

import org.junit.jupiter.api.Test;

import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class AnchorRecallValidatorTest {
    @Test
    void ownRecentLoadedProjectileSucceedsAndForeignExpiredOrUnloadedFails() {
        UUID owner = UUID.randomUUID();
        AnchorRecallValidator validator = new AnchorRecallValidator(new SafeDestinationPolicy());
        var valid = new AnchorRecallValidator.Anchor(owner, 10L, 200L, 20.0D, 48.0D, SafeDestinationPolicyTest.valid());
        assertTrue(validator.validate(owner, 50L, valid).allowed());
        assertEquals("foreign_projectile", validator.validate(UUID.randomUUID(), 50L, valid).code());
        assertEquals("projectile_expired", validator.validate(owner, 211L, valid).code());
        var unloaded = new AnchorRecallValidator.Anchor(owner, 10L, 200L, 20.0D, 48.0D,
            new SafeDestinationPolicy.Facts(false, true, true, true, true, true, true, false));
        assertEquals("destination_unloaded", validator.validate(owner, 50L, unloaded).code());
    }
}
