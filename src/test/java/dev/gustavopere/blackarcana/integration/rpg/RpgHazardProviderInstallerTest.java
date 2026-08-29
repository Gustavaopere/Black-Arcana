package dev.gustavopere.blackarcana.integration.rpg;

import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;
import org.junit.jupiter.api.Test;

import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;

class RpgHazardProviderInstallerTest {
    @Test
    void installsOneReadOnlyProviderIntoBothHazardChannels() {
        ArcanaServerRuntime runtime = ArcanaServerRuntime.createDefault();
        RpgSkillTreeBridge bridge = unavailableBridge();

        RpgHazardProviderInstaller.install(runtime, bridge);

        assertEquals(1, runtime.arcaneResistanceProviders().size());
        assertEquals(1, runtime.corruptionResistanceProviders().size());
    }

    @Test
    void duplicateInstallationFailsClosedInsteadOfDoubleCounting() {
        ArcanaServerRuntime runtime = ArcanaServerRuntime.createDefault();
        RpgSkillTreeBridge bridge = unavailableBridge();

        RpgHazardProviderInstaller.install(runtime, bridge);
        org.junit.jupiter.api.Assertions.assertThrows(
                IllegalArgumentException.class,
                () -> RpgHazardProviderInstaller.install(runtime, bridge));

        assertEquals(1, runtime.arcaneResistanceProviders().size());
        assertEquals(1, runtime.corruptionResistanceProviders().size());
    }

    private static RpgSkillTreeBridge unavailableBridge() {
        return new RpgSkillTreeBridge() {
            @Override public String integrationId() { return "black_arcana:test_rpg"; }
            @Override public boolean available() { return false; }
            @Override public String implementationVersion() { return "test"; }
            @Override public RpgProgressionQuery query(UUID playerId) {
                return RpgProgressionQuery.denied("missing", "test bridge unavailable");
            }
            @Override public ArcanaDecision awardMastery(UUID playerId, RpgMasteryAwardSpec award) {
                return ArcanaDecision.deny("missing", "test bridge unavailable");
            }
        };
    }
}
