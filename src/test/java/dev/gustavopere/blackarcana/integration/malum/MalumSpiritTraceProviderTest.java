package dev.gustavopere.blackarcana.integration.malum;

import dev.gustavopere.blackarcana.content.souls.SpiritSightPolicy;
import net.minecraft.resources.ResourceLocation;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class MalumSpiritTraceProviderTest {
    @Test
    void classifiesOnlySupportedMalumEntityIdsAndKeepsSoulTagsPrivate() {
        var naturalSpirit = MalumSpiritTraceProvider.classifyEntityType(
            ResourceLocation.fromNamespaceAndPath("malum", "natural_spirit")).orElseThrow();
        assertEquals(SpiritSightPolicy.TraceKind.MALUM_SPIRIT, naturalSpirit.kind());
        assertFalse(naturalSpirit.privateData());

        var soulTag = MalumSpiritTraceProvider.classifyEntityType(
            ResourceLocation.fromNamespaceAndPath("malum", "soul_tag_entity")).orElseThrow();
        assertEquals(SpiritSightPolicy.TraceKind.MALUM_SPIRIT, soulTag.kind());
        assertTrue(soulTag.privateData(), "SoulTagEntity carries target identity and must default to private visibility");

        assertTrue(MalumSpiritTraceProvider.classifyEntityType(
            ResourceLocation.fromNamespaceAndPath("minecraft", "item")).isEmpty());
        assertTrue(MalumSpiritTraceProvider.classifyEntityType(
            ResourceLocation.fromNamespaceAndPath("malum", "unrelated_entity")).isEmpty());
    }
}
