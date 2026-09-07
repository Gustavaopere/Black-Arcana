package dev.gustavopere.blackarcana.content.noetic;

import org.junit.jupiter.api.Test;

import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class FamiliarOwnershipRegistryTest {
    @Test
    void registryIsBoundedDeduplicatedAndFailsClosedOnProviderErrors() {
        assertThrows(IllegalArgumentException.class,
                () -> new FamiliarOwnershipRegistry(NoeticSafetyCeilings.MAX_FAMILIAR_PROVIDERS + 1));

        UUID owner = UUID.randomUUID();
        Object candidate = new Object();
        FamiliarOwnershipRegistry empty = new FamiliarOwnershipRegistry(2);
        assertEquals(FamiliarOwnershipProvider.Result.UNSUPPORTED, empty.ownership(owner, candidate));

        FamiliarOwnershipRegistry registry = new FamiliarOwnershipRegistry(2);
        assertTrue(registry.register(new FixedProvider("first", FamiliarOwnershipProvider.Result.NOT_OWNED)));
        assertFalse(registry.register(new FixedProvider("first", FamiliarOwnershipProvider.Result.OWNED)));
        assertTrue(registry.register(new ThrowingProvider("broken")));
        assertFalse(registry.register(new FixedProvider("third", FamiliarOwnershipProvider.Result.OWNED)));
        assertEquals(FamiliarOwnershipProvider.Result.NOT_OWNED, registry.ownership(owner, candidate));

        FamiliarOwnershipRegistry unsupported = new FamiliarOwnershipRegistry(1);
        assertTrue(unsupported.register(new ThrowingProvider("broken")));
        assertEquals(FamiliarOwnershipProvider.Result.UNSUPPORTED, unsupported.ownership(owner, candidate));
    }

    @Test
    void explicitOwnedWinsButForeignOrUnknownCandidatesNeverGainOwnership() {
        UUID owner = UUID.randomUUID();
        Object candidate = new Object();
        FamiliarOwnershipRegistry registry = new FamiliarOwnershipRegistry(2);
        assertTrue(registry.register(new FixedProvider("negative", FamiliarOwnershipProvider.Result.NOT_OWNED)));
        assertTrue(registry.register(new FixedProvider("positive", FamiliarOwnershipProvider.Result.OWNED)));
        assertEquals(FamiliarOwnershipProvider.Result.OWNED, registry.ownership(owner, candidate));
    }

    @Test
    void invalidProviderIdsAndNullInputsFailClosed() {
        FamiliarOwnershipRegistry registry = new FamiliarOwnershipRegistry(2);
        assertFalse(registry.register(new FixedProvider("   ", FamiliarOwnershipProvider.Result.OWNED)));
        assertThrows(NullPointerException.class, () -> registry.ownership(null, new Object()));
        assertThrows(NullPointerException.class, () -> registry.ownership(UUID.randomUUID(), null));
        assertEquals(0, registry.providerCount());
    }

    private record FixedProvider(String providerId, FamiliarOwnershipProvider.Result result)
            implements FamiliarOwnershipProvider {
        @Override
        public Result ownership(UUID ownerId, Object candidate) {
            return result;
        }
    }

    private record ThrowingProvider(String providerId) implements FamiliarOwnershipProvider {
        @Override
        public Result ownership(UUID ownerId, Object candidate) {
            throw new IllegalStateException("provider failed");
        }
    }
}
