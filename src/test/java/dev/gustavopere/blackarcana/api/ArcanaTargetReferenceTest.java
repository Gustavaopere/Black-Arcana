package dev.gustavopere.blackarcana.api;

import org.junit.jupiter.api.Test;

import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertInstanceOf;
import static org.junit.jupiter.api.Assertions.assertThrows;

class ArcanaTargetReferenceTest {
    @Test
    void entityReferenceRoundTripsWithoutClientCoordinates() {
        UUID id = UUID.fromString("11111111-1111-1111-1111-111111111111");
        ArcanaTargetReference.EntityRef reference = new ArcanaTargetReference.EntityRef(id);

        ArcanaTargetReference parsed = ArcanaTargetReference.parse(reference.canonical());
        ArcanaTargetReference.EntityRef entity = assertInstanceOf(ArcanaTargetReference.EntityRef.class, parsed);
        assertEquals(id, entity.entityId());
    }

    @Test
    void blockReferenceRoundTripsDimensionAndServerCoordinates() {
        ArcanaTargetReference.BlockRef reference = new ArcanaTargetReference.BlockRef(
                "minecraft:the_nether", -12, 64, 128);

        ArcanaTargetReference parsed = ArcanaTargetReference.parse(reference.canonical());
        ArcanaTargetReference.BlockRef block = assertInstanceOf(ArcanaTargetReference.BlockRef.class, parsed);
        assertEquals("minecraft:the_nether", block.dimensionId());
        assertEquals(-12, block.x());
        assertEquals(64, block.y());
        assertEquals(128, block.z());
    }

    @Test
    void malformedReferencesFailClosed() {
        assertThrows(IllegalArgumentException.class, () -> ArcanaTargetReference.parse("entity|not-a-uuid"));
        assertThrows(IllegalArgumentException.class, () -> ArcanaTargetReference.parse("block|minecraft:overworld|x|0|0"));
        assertThrows(IllegalArgumentException.class, () -> ArcanaTargetReference.parse("unknown|payload"));
    }
}
