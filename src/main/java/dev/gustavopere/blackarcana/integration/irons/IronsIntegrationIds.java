package dev.gustavopere.blackarcana.integration.irons;

import dev.gustavopere.blackarcana.api.ArcanaSpellId;

/** Constants safe to load even when Iron's is absent. */
public final class IronsIntegrationIds {
    public static final String PROBE_PATH = "irons_integration_probe";
    public static final ArcanaSpellId PROBE_ARCANA_ID = ArcanaSpellId.parse("black_arcana:" + PROBE_PATH);
    public static final int PROBE_MANA_COST = 20;

    private IronsIntegrationIds() { }
}
