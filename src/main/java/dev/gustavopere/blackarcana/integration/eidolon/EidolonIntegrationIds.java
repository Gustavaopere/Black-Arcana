package dev.gustavopere.blackarcana.integration.eidolon;

import net.minecraft.resources.ResourceLocation;

/** Constants safe to load when Eidolon is absent. */
public final class EidolonIntegrationIds {
    public static final String MOD_ID = "eidolon_repraised";
    public static final ResourceLocation PROBE_RITUAL_ID = ResourceLocation.fromNamespaceAndPath(
        "black_arcana",
        "eidolon_integration_probe");
    public static final ResourceLocation ANCHOR_ATTUNEMENT_RITUAL_ID = ResourceLocation.fromNamespaceAndPath(
        "black_arcana",
        "eidolon_anchor_attunement");

    private EidolonIntegrationIds() { }
}
