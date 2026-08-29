package dev.gustavopere.blackarcana.content.noetic;

import org.junit.jupiter.api.Test;

import java.util.Set;

import static org.junit.jupiter.api.Assertions.*;

class DivinationVisibilityPolicyTest {
    @Test void namescryNeverForceLoadsOrBypassesPlayerConsent() {
        var policy = new DivinationVisibilityPolicy(64);
        assertFalse(policy.canNamescry(new DivinationVisibilityPolicy.Facts(false, true, false, false, false, 10)));
        assertFalse(policy.canNamescry(new DivinationVisibilityPolicy.Facts(true, true, true, false, false, 10)));
        assertTrue(policy.canNamescry(new DivinationVisibilityPolicy.Facts(true, true, true, true, false, 10)));
        assertFalse(policy.canNamescry(new DivinationVisibilityPolicy.Facts(true, true, false, false, false, 65)));
    }

    @Test void borrowedSightRequiresOwnedFamiliarAndMetadataIsAllowlisted() {
        var policy = new DivinationVisibilityPolicy(64);
        assertFalse(policy.canBorrowSight(new DivinationVisibilityPolicy.Facts(true, true, false, false, false, 10)));
        assertTrue(policy.canBorrowSight(new DivinationVisibilityPolicy.Facts(true, true, false, false, true, 10)));
        assertEquals(Set.of("health", "held_item"), policy.filterMetadata(Set.of("health", "held_item", "full_nbt", "container_inventory")));
    }
}
