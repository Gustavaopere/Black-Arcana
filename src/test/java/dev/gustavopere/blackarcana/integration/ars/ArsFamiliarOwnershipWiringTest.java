package dev.gustavopere.blackarcana.integration.ars;

import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

import static org.junit.jupiter.api.Assertions.assertTrue;

class ArsFamiliarOwnershipWiringTest {
    private static final Path ROOT = repositoryRoot();
    private static final Path OPTIONAL_ENTRYPOINTS = ROOT.resolve(
            "src/main/java/dev/gustavopere/blackarcana/integration/neoforge/OptionalModEntrypoints.java");
    private static final Path ARS_BOOTSTRAP = ROOT.resolve(
            "src/main/java/dev/gustavopere/blackarcana/integration/ars/ArsServerIntegrationBootstrap.java");
    private static final Path ARS_PROVIDER = ROOT.resolve(
            "src/main/java/dev/gustavopere/blackarcana/integration/ars/ArsFamiliarOwnershipProvider.java");

    @Test
    void arsFamiliarProviderLoadsOnlyBehindOptionalServerEntrypoint() throws IOException {
        String optional = Files.readString(OPTIONAL_ENTRYPOINTS);
        String bootstrap = Files.readString(ARS_BOOTSTRAP);
        String provider = Files.readString(ARS_PROVIDER);

        assertTrue(optional.contains("\"ars_nouveau\""),
                "optional server entrypoints must explicitly identify ars_nouveau");
        assertTrue(optional.contains("dev.gustavopere.blackarcana.integration.ars.ArsServerIntegrationBootstrap"),
                "ars_nouveau must resolve only to its isolated optional server bootstrap");
        assertTrue(optional.contains("if (!mods.isLoaded(modId))"),
                "optional server adapters must remain gated by NeoForge ModList presence");

        assertTrue(bootstrap.contains("if (!bridge.available()) return;"),
                "familiar provider registration must occur only after the exact Ars API probe succeeds");
        assertTrue(bootstrap.contains("bridge.familiarOwnershipProvider().ifPresent"),
                "Ars bridge must expose familiar ownership only as an optional verified capability");
        assertTrue(bootstrap.contains("MinecraftNoeticRuntime.registerFamiliarOwnershipProvider"),
                "verified Ars ownership evidence must be installed into the bounded Noetic registry");

        assertTrue(provider.contains("instanceof IFamiliar"),
                "Ars familiar ownership must use the published IFamiliar API rather than reflection/private state");
        assertTrue(provider.contains("familiar.getOwnerID()"),
                "Ars ownership must be resolved through IFamiliar#getOwnerID");
        assertTrue(!provider.contains("getDeclared") && !provider.contains("setAccessible") && !provider.contains("getPersistentData"),
                "Ars ownership adapter must not inspect private members or arbitrary entity NBT");
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
        throw new IllegalStateException("Unable to locate repository root from test working directory");
    }
}
