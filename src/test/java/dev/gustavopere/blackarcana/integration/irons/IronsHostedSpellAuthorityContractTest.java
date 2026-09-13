package dev.gustavopere.blackarcana.integration.irons;

import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class IronsHostedSpellAuthorityContractTest {
    private static final Path ROOT = repositoryRoot();
    private static final Path IRONS_ROOT = ROOT.resolve("src/main/java/dev/gustavopere/blackarcana/integration/irons");

    @Test
    void hostedProbeDisablesProviderSettlement() throws IOException {
        String probe = read("IronsArcanaProbeSpell.java");

        assertTrue(probe.contains("public int getManaCost(int level)"));
        assertTrue(probe.contains("public int getSpellCooldown()"));
        assertEquals(2, occurrences(probe, "return 0;"),
            "hosted probe must expose zero Iron's mana cost and zero Iron's cooldown");
        assertTrue(probe.contains("this.baseManaCost = IronsIntegrationIds.PROBE_MANA_COST;"),
            "the canonical Black Arcana resource amount remains explicit in integration metadata");
    }

    @Test
    void oneHostInvocationConvergesThroughOneBlackArcanaIngress() throws IOException {
        String probe = read("IronsArcanaProbeSpell.java");
        String dispatcher = read("IronsHostedCastDispatcher.java");

        assertEquals(1, occurrences(probe, "IronsHostedCastDispatcher.cast("));
        assertEquals(1, occurrences(dispatcher, "ArcanaServerRuntimeManager.handleCastIntent("));
        assertEquals(1, occurrences(dispatcher, "ArcanaCastId.random()"));
    }

    @Test
    void nativeManaNeutralizationRemainsDefenseInDepth() throws IOException {
        String events = read("IronsHostedSpellEvents.java");

        assertTrue(events.contains("EventPriority.HIGHEST"));
        assertTrue(events.contains("EventPriority.LOWEST"));
        assertEquals(2, occurrences(events, "event.setManaCost(0)"));
    }

    @Test
    void blackArcanaRemainsSoleCooldownAuthorityForHostedProbe() throws IOException {
        String synthetic = read("IronsSyntheticContent.java");

        assertTrue(synthetic.contains("public static final long COOLDOWN_TICKS = 40L;"));
        assertTrue(synthetic.contains("new ArcanaCooldownSpec(IronsIntegrationIds.PROBE_ARCANA_ID.canonical(), COOLDOWN_TICKS, false)"));
    }

    @Test
    void optionalEntrypointDoesNotHardImportIronClasses() throws IOException {
        String entrypoints = Files.readString(ROOT.resolve(
            "src/main/java/dev/gustavopere/blackarcana/integration/neoforge/OptionalModEntrypoints.java"));

        assertTrue(entrypoints.contains("dev.gustavopere.blackarcana.integration.irons.IronsOptionalModBootstrap"));
        assertTrue(entrypoints.contains("dev.gustavopere.blackarcana.integration.irons.IronsServerIntegrationBootstrap"));
        assertFalse(entrypoints.contains("import dev.gustavopere.blackarcana.integration.irons."));
    }

    private static String read(String file) throws IOException {
        return Files.readString(IRONS_ROOT.resolve(file));
    }

    private static int occurrences(String source, String needle) {
        int count = 0;
        int cursor = 0;
        while ((cursor = source.indexOf(needle, cursor)) >= 0) {
            count++;
            cursor += needle.length();
        }
        return count;
    }

    private static Path repositoryRoot() {
        String workspace = System.getenv("GITHUB_WORKSPACE");
        if (workspace != null && !workspace.isBlank()) return Path.of(workspace);
        Path candidate = Path.of("").toAbsolutePath();
        while (candidate != null) {
            if (Files.exists(candidate.resolve("settings.gradle")) && Files.isDirectory(candidate.resolve(".github"))) {
                return candidate;
            }
            candidate = candidate.getParent();
        }
        throw new IllegalStateException("repository root not found");
    }
}
