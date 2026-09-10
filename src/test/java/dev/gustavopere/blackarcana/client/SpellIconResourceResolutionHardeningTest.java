package dev.gustavopere.blackarcana.client;

import net.minecraft.resources.ResourceLocation;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.Test;

import java.lang.reflect.Method;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.function.Predicate;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assertions.fail;

class SpellIconResourceResolutionHardeningTest {
    private static final Path ROOT = repositoryRoot();
    private static final Path RESOLVER = ROOT.resolve(
            "src/main/java/dev/gustavopere/blackarcana/client/SpellIconResolver.java");
    private static final Path CLIENT = ROOT.resolve(
            "src/main/java/dev/gustavopere/blackarcana/client/BlackArcanaClient.java");
    private static final Path LOADOUT = ROOT.resolve(
            "src/main/java/dev/gustavopere/blackarcana/client/BlackArcanaLoadoutScreen.java");
    private static final Path RADIAL = ROOT.resolve(
            "src/main/java/dev/gustavopere/blackarcana/client/BlackArcanaRadialScreen.java");
    private static final Path HUD = ROOT.resolve(
            "src/main/java/dev/gustavopere/blackarcana/client/BlackArcanaHudLayer.java");

    @AfterEach
    void clearSharedResolutionState() {
        invokeNoArgs("invalidate");
    }

    @Test
    void positiveAndNegativeResolutionAssumptionsAreCachedUntilExplicitReloadInvalidation() {
        invokeNoArgs("invalidate");
        ResourceLocation icon = ResourceLocation.fromNamespaceAndPath(
                "black_arcana", "textures/spell/reload_probe.png");
        ResourceLocation placeholder = placeholder();
        AtomicInteger lookups = new AtomicInteger();
        Predicate<ResourceLocation> present = id -> {
            lookups.incrementAndGet();
            return id.equals(icon);
        };

        assertEquals(icon, SpellIconResolver.resolve(icon.toString(), present));
        assertEquals(icon, SpellIconResolver.resolve(icon.toString(), id -> {
            lookups.incrementAndGet();
            return false;
        }));
        assertEquals(1, lookups.get(), "positive lookup should be cached inside one resource epoch");

        invokeNoArgs("invalidate");
        assertEquals(placeholder, SpellIconResolver.resolve(icon.toString(), id -> {
            lookups.incrementAndGet();
            return false;
        }));
        assertEquals(2, lookups.get(), "reload invalidation must re-evaluate a prior positive result");
        assertEquals(placeholder, SpellIconResolver.resolve(icon.toString(), present));
        assertEquals(2, lookups.get(), "negative lookup should also be cached inside one resource epoch");

        invokeNoArgs("invalidate");
        assertEquals(icon, SpellIconResolver.resolve(icon.toString(), present));
        assertEquals(3, lookups.get(), "reload invalidation must re-evaluate a prior negative result");
    }

    @Test
    void sharedResolutionCacheIsBoundedToPresentationProtocolCardinality() {
        invokeNoArgs("invalidate");
        for (int index = 0; index < 600; index++) {
            String id = "black_arcana:textures/spell/cache_probe_" + index + ".png";
            SpellIconResolver.resolve(id, ignored -> false);
        }
        assertTrue(invokeIntNoArgs("cachedEntryCount") <= 512,
                "icon resolution cache must remain bounded by presentation protocol cardinality");
    }

    @Test
    void exactNeoForgeClientReloadHookInvalidatesSharedResolverOnThePhysicalClient() throws Exception {
        String resolver = Files.readString(RESOLVER);
        String client = Files.readString(CLIENT);

        assertTrue(resolver.contains("RegisterClientReloadListenersEvent"),
                "NeoForge 21.1.x client reload event must own cache invalidation");
        assertTrue(resolver.contains("ResourceManagerReloadListener"));
        assertTrue(resolver.contains("registerReloadListener"));
        assertTrue(client.contains("modEventBus.addListener(SpellIconResolver::registerReloadListener);"));
        assertFalse(client.contains("NeoForge.EVENT_BUS.addListener(SpellIconResolver"),
                "client reload registration belongs to the mod bus, not the gameplay event bus");
    }

    @Test
    void loadoutAndRadialShareCurrentSynchronizedIconResolutionWithoutHudAttribution() throws Exception {
        String loadout = Files.readString(LOADOUT);
        String radial = Files.readString(RADIAL);
        String hud = Files.readString(HUD);

        assertFalse(loadout.contains("private final Map<ArcanaSpellId, ResourceLocation> icons;"),
                "loadout must not freeze resolved icon outcomes for the lifetime of the screen");
        assertTrue(loadout.contains("ClientArcanaSyncState.presentationSnapshot().get(spell)"),
                "loadout must consult the newest synchronized icon association when rendering");
        assertTrue(loadout.contains("SpellIconResolver.resolve("));
        assertTrue(radial.contains("ClientArcanaSyncState.presentationSnapshot().get(spell)"),
                "radial must consume the newest synchronized icon association");
        assertTrue(radial.contains("entry.iconId()"));
        assertTrue(radial.contains("SpellIconResolver.resolve("));
        assertTrue(radial.contains("graphics.blit("));
        assertFalse(hud.contains("SpellIconResolver"),
                "05.12 Phase D is not automatically authorized; result-only HUD must not borrow selection art");
    }

    @Test
    void resourceResolutionNeverBecomesASecondGameplayOrNetworkPath() throws Exception {
        String resolver = Files.readString(RESOLVER);
        String loadout = Files.readString(LOADOUT);
        String radial = Files.readString(RADIAL);

        assertFalse(resolver.contains("http://"));
        assertFalse(resolver.contains("https://"));
        assertFalse(resolver.contains("Files."));
        assertFalse(resolver.contains("JarFile"));
        assertFalse(resolver.contains("ClientArcanaSyncState"));
        assertEquals(1, occurrences(loadout, "LoadoutNetworkBridge.requestUpdate("));
        assertFalse(radial.contains("requestCast("),
                "radial icon consumption must not create a cast path; wedge activation remains selection-only");
    }

    private static ResourceLocation placeholder() {
        try {
            var field = SpellIconResolver.class.getDeclaredField("PLACEHOLDER");
            field.setAccessible(true);
            return (ResourceLocation) field.get(null);
        } catch (ReflectiveOperationException exception) {
            return fail("SpellIconResolver.PLACEHOLDER is missing", exception);
        }
    }

    private static void invokeNoArgs(String name) {
        try {
            Method method = SpellIconResolver.class.getDeclaredMethod(name);
            method.setAccessible(true);
            method.invoke(null);
        } catch (ReflectiveOperationException exception) {
            fail("SpellIconResolver." + name + "() is missing or invalid", exception);
        }
    }

    private static int invokeIntNoArgs(String name) {
        try {
            Method method = SpellIconResolver.class.getDeclaredMethod(name);
            method.setAccessible(true);
            Object value = method.invoke(null);
            assertNotNull(value);
            return (int) value;
        } catch (ReflectiveOperationException exception) {
            return fail("SpellIconResolver." + name + "() is missing or invalid", exception);
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
