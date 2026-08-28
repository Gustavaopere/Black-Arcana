package dev.gustavopere.blackarcana.integration.malum;

import dev.gustavopere.blackarcana.api.ArcanaSpellId;

/** Constants safe to load when Malum is absent. */
public final class MalumIntegrationIds {
    public static final String MOD_ID = "malum";
    public static final String RESOURCE_PREFIX = "malum:spirit/";
    public static final String PROBE_AFFINITY = "arcane";
    public static final int PROBE_SPIRIT_COST = 2;
    public static final ArcanaSpellId PROBE_ARCANA_ID = ArcanaSpellId.parse("black_arcana:malum_integration_probe");

    private MalumIntegrationIds() { }

    public static String resourceId(String affinity) {
        return RESOURCE_PREFIX + affinity;
    }
}
