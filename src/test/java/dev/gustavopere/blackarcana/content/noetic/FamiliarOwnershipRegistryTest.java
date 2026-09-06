package dev.gustavopere.blackarcana.content.noetic;

import com.hollingsworth.arsnouveau.api.familiar.IFamiliar;
import dev.gustavopere.blackarcana.integration.ars.ArsFamiliarOwnershipProvider;
import net.minecraft.resources.ResourceLocation;
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
    void arsProviderUsesOnlyPublicFamiliarOwnerIdentity() {
        UUID owner = UUID.randomUUID();
        UUID foreign = UUID.randomUUID();
        ArsFamiliarOwnershipProvider provider = new ArsFamiliarOwnershipProvider();
        IFamiliar familiar = new FakeFamiliar(owner);

        assertEquals(FamiliarOwnershipProvider.Result.OWNED, provider.ownership(owner, familiar));
        assertEquals(FamiliarOwnershipProvider.Result.NOT_OWNED, provider.ownership(foreign, familiar));
        assertEquals(FamiliarOwnershipProvider.Result.NOT_OWNED, provider.ownership(owner, new Object()));
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

    private static final class FakeFamiliar implements IFamiliar {
        private UUID ownerId;
        private ResourceLocation holderId = ResourceLocation.fromNamespaceAndPath("black_arcana", "test_familiar");

        private FakeFamiliar(UUID ownerId) {
            this.ownerId = ownerId;
        }

        @Override public ResourceLocation getHolderID() { return holderId; }
        @Override public void setHolderID(ResourceLocation id) { holderId = id; }
        @Override public UUID getOwnerID() { return ownerId; }
        @Override public void setOwnerID(UUID uuid) { ownerId = uuid; }
    }
}
