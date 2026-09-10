package dev.gustavopere.blackarcana.client;

import net.minecraft.resources.ResourceLocation;
import org.junit.jupiter.api.Test;

import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.function.Predicate;

import static org.junit.jupiter.api.Assertions.assertArrayEquals;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assertions.fail;

class SpellIconPresentationContractTest {
    private static final Path ROOT = repositoryRoot();
    private static final Path SCREEN = ROOT.resolve(
            "src/main/java/dev/gustavopere/blackarcana/client/BlackArcanaLoadoutScreen.java");
    private static final Path PLACEHOLDER = ROOT.resolve(
            "src/main/resources/assets/black_arcana/textures/gui/spell_placeholder.png");

    @Test
    void resolverUsesLiteralResourceIdsAndFallsBackWithoutHeuristics() throws Exception {
        Class<?> resolver = resolverClass();
        Method resolve = resolver.getDeclaredMethod("resolve", String.class, Predicate.class);
        resolve.setAccessible(true);
        Field placeholderField = resolver.getDeclaredField("PLACEHOLDER");
        placeholderField.setAccessible(true);

        ResourceLocation placeholder = (ResourceLocation) placeholderField.get(null);
        ResourceLocation literal = ResourceLocation.fromNamespaceAndPath(
                "black_arcana", "textures/spell/test_spell.png");
        Predicate<ResourceLocation> onlyLiteralExists = literal::equals;

        assertEquals(
                ResourceLocation.fromNamespaceAndPath(
                        "black_arcana", "textures/gui/spell_placeholder.png"),
                placeholder);
        assertEquals(literal, resolve.invoke(null, literal.toString(), onlyLiteralExists));
        assertEquals(placeholder, resolve.invoke(
                null, "black_arcana:irons_integration_probe", onlyLiteralExists));
        assertEquals(placeholder, resolve.invoke(
                null, "NOT A VALID RESOURCE ID", onlyLiteralExists));
    }

    @Test
    void loadoutScreenConsumesSynchronizedIconIdWithoutAddingNetworkAuthority() throws Exception {
        String source = Files.readString(SCREEN);

        assertTrue(source.contains("SpellIconResolver.resolve("));
        assertTrue(source.contains("entry.iconId()"));
        assertTrue(source.contains("graphics.blit("));
        assertTrue(source.contains("displayName(spell"), "text identity must remain available beside the icon");
        assertEquals(1, occurrences(source, "LoadoutNetworkBridge.requestUpdate("));
    }

    @Test
    void fallbackArtworkIsARealPackagedPng() throws Exception {
        assertTrue(Files.isRegularFile(PLACEHOLDER), "fallback texture must be physically packaged");
        byte[] bytes = Files.readAllBytes(PLACEHOLDER);
        assertTrue(bytes.length > 8, "fallback texture cannot be an empty marker file");
        assertArrayEquals(
                new byte[] {(byte) 0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A},
                java.util.Arrays.copyOf(bytes, 8),
                "fallback resource must be a PNG");
    }

    private static Class<?> resolverClass() {
        try {
            return Class.forName("dev.gustavopere.blackarcana.client.SpellIconResolver");
        } catch (ClassNotFoundException exception) {
            return fail("SpellIconResolver production boundary is not implemented yet", exception);
        }
    }

    private static int occurrences(String haystack, String needle) {
        int count = 0;
        int from = 0;
        while ((from = haystack.indexOf(needle, from)) >= 0) {
            count++;
            from += needle.length();
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
        return fail("Unable to locate repository root from test working directory");
    }
}
