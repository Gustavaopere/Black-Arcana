package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.core.hazard.ArcaneEquipmentSnapshotService;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

class StandardEquipmentHazardProviderInstallerTest {
    @Test
    void installsOneFrozenProviderIntoBothHazardChannels() {
        ArcanaServerRuntime runtime = ArcanaServerRuntime.createDefault();

        StandardEquipmentHazardProviderInstaller.install(runtime, ignored -> emptySnapshot());

        assertEquals(1, runtime.arcaneResistanceProviders().size());
        assertEquals(1, runtime.corruptionResistanceProviders().size());
    }

    @Test
    void duplicateInstallationFailsClosedInsteadOfDoubleCounting() {
        ArcanaServerRuntime runtime = ArcanaServerRuntime.createDefault();
        var source = (dev.gustavopere.blackarcana.core.hazard.ArcaneEquipmentHazardResistanceProvider.SnapshotSource)
            ignored -> emptySnapshot();

        StandardEquipmentHazardProviderInstaller.install(runtime, source);
        assertThrows(IllegalArgumentException.class,
            () -> StandardEquipmentHazardProviderInstaller.install(runtime, source));

        assertEquals(1, runtime.arcaneResistanceProviders().size());
        assertEquals(1, runtime.corruptionResistanceProviders().size());
    }

    private static ArcaneEquipmentSnapshotService.Snapshot emptySnapshot() {
        return new ArcaneEquipmentSnapshotService.Snapshot(List.of(), Map.of(), 0.0D, 0.0D, 0.0D, 0.0D);
    }
}
