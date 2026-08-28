package dev.gustavopere.blackarcana.integration.ars;

import dev.gustavopere.blackarcana.api.ArcanaSpellId;

/** Constants safe to load even when Ars Nouveau is absent. */
public final class ArsIntegrationIds {
    public static final ArcanaSpellId PROBE_ARCANA_ID = ArcanaSpellId.parse("black_arcana:ars_integration_probe");
    public static final double PROBE_MANA_COST = 25.0D;

    private ArsIntegrationIds() { }
}
