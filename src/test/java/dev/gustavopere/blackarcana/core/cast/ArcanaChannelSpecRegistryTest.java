package dev.gustavopere.blackarcana.core.cast;

import dev.gustavopere.blackarcana.api.ArcanaChannelSpec;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ArcanaChannelSpecRegistryTest {
    @Test
    void registryPublishesOnlyExplicitServerOwnedSpecs() {
        ArcanaChannelSpecRegistry registry = new ArcanaChannelSpecRegistry(2);
        ArcanaSpellId first = ArcanaSpellId.parse("black_arcana:first_channel");
        ArcanaSpellId second = ArcanaSpellId.parse("black_arcana:second_channel");
        ArcanaChannelSpec firstSpec = new ArcanaChannelSpec(5L, 100L);

        assertTrue(registry.register(first, firstSpec));
        assertEquals(firstSpec, registry.resolve(first).orElseThrow());
        assertFalse(registry.register(first, new ArcanaChannelSpec(10L, 120L)),
                "an already-owned spell id must not be silently replaced by another channel contract");
        assertEquals(firstSpec, registry.resolve(first).orElseThrow());
        assertTrue(registry.register(second, new ArcanaChannelSpec(0L, 20L)));
        assertEquals(2, registry.snapshot().size());
    }

    @Test
    void registryFailsClosedAtBoundedCapacity() {
        ArcanaChannelSpecRegistry registry = new ArcanaChannelSpecRegistry(1);
        assertTrue(registry.register(
                ArcanaSpellId.parse("black_arcana:first"),
                new ArcanaChannelSpec(0L, 20L)));
        assertFalse(registry.register(
                ArcanaSpellId.parse("black_arcana:second"),
                new ArcanaChannelSpec(0L, 20L)));
        assertThrows(UnsupportedOperationException.class,
                () -> registry.snapshot().clear(),
                "published channel authority snapshots must be immutable");
    }
}
