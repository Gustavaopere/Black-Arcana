package dev.gustavopere.blackarcana.content.noetic;

import org.junit.jupiter.api.Test;

import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;

class FamiliarBondRegistryTest {
    @Test void ownershipIsExplicitBoundedAndCannotBeStolen() {
        var registry = new FamiliarBondRegistry(1);
        UUID owner = UUID.randomUUID(); UUID other = UUID.randomUUID(); UUID familiar = UUID.randomUUID();
        assertEquals(FamiliarBondRegistry.BindResult.BOUND, registry.bind(owner, familiar));
        assertEquals(FamiliarBondRegistry.BindResult.ALREADY_BOUND, registry.bind(owner, familiar));
        assertEquals(FamiliarBondRegistry.BindResult.OWNED_BY_OTHER, registry.bind(other, familiar));
        assertTrue(registry.isOwnedBy(familiar, owner));
        assertTrue(registry.unbind(owner, familiar));
        assertFalse(registry.isOwnedBy(familiar, owner));
    }
}
