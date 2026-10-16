package dev.gustavopere.blackarcana.qa.catalog;

import net.neoforged.fml.common.Mod;
import net.neoforged.neoforge.common.NeoForge;
import net.neoforged.neoforge.event.server.ServerStartedEvent;

/**
 * Removable runtime-evidence companion for provider catalog closure.
 *
 * <p>This source set is packaged separately from Black Arcana production
 * content and is intended only for the exact assembled modpack under audit.</p>
 */
@Mod(CatalogQaProbeMod.MOD_ID)
public final class CatalogQaProbeMod {
    public static final String MOD_ID = "black_arcana_catalog_qa";

    public CatalogQaProbeMod() {
        NeoForge.EVENT_BUS.addListener(CatalogQaProbeMod::onServerStarted);
        if (Boolean.getBoolean("black_arcana.catalog_qa.arrow_volley")) {
            ArrowVolleyRuntimeEvidence.install();
        }
        if (Boolean.getBoolean("black_arcana.catalog_qa.irons_event_phase")) {
            IronsEventPhaseRuntimeEvidence.install();
        }
    }

    private static void onServerStarted(ServerStartedEvent event) {
        CatalogRuntimeEvidence.emit();
        if (Boolean.getBoolean("black_arcana.catalog_qa.arrow_volley")
                || Boolean.getBoolean("black_arcana.catalog_qa.irons_event_phase")) {
            // One shared publisher checksum record, even when both probes run.
            ArrowVolleyRuntimeEvidence.emitProviderFingerprint();
        }
    }
}
