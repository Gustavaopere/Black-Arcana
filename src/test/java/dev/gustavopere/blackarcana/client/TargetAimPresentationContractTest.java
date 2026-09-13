package dev.gustavopere.blackarcana.client;

import net.minecraft.world.phys.HitResult;
import org.junit.jupiter.api.Test;

import java.lang.reflect.Method;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Arrays;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assertions.fail;

class TargetAimPresentationContractTest {
    private static final Path ROOT = repositoryRoot();
    private static final Path SEMANTICS = ROOT.resolve(
            "src/main/java/dev/gustavopere/blackarcana/client/TargetAimPresentationSemantics.java");
    private static final Path LAYER = ROOT.resolve(
            "src/main/java/dev/gustavopere/blackarcana/client/TargetAimPresentationLayer.java");
    private static final Path CLIENT = ROOT.resolve(
            "src/main/java/dev/gustavopere/blackarcana/client/BlackArcanaClient.java");
    private static final Path EN_US = ROOT.resolve(
            "src/main/resources/assets/black_arcana/lang/en_us.json");
    private static final Path PT_BR = ROOT.resolve(
            "src/main/resources/assets/black_arcana/lang/pt_br.json");

    @Test
    void localObservationSemanticsStayNeutralAndOnlyRenderInsideRecentSelectionContext() throws Exception {
        assertTrue(Files.exists(SEMANTICS),
                "05.13 requires an explicit local-observation semantics boundary before rendering");

        Class<?> semantics = Class.forName(
                "dev.gustavopere.blackarcana.client.TargetAimPresentationSemantics");
        Class<?> observation = Arrays.stream(semantics.getDeclaredClasses())
                .filter(Class::isEnum)
                .filter(type -> type.getSimpleName().equals("Observation"))
                .findFirst()
                .orElseGet(() -> fail("TargetAimPresentationSemantics.Observation enum is missing"));

        Object miss = enumValue(observation, "MISS");
        Object block = enumValue(observation, "BLOCK");
        Object entity = enumValue(observation, "ENTITY");

        Method fromHitType = requiredMethod(semantics, "fromHitType", HitResult.Type.class);
        assertEquals(miss, fromHitType.invoke(null, HitResult.Type.MISS));
        assertEquals(block, fromHitType.invoke(null, HitResult.Type.BLOCK));
        assertEquals(entity, fromHitType.invoke(null, HitResult.Type.ENTITY));

        Method marker = semantics.getDeclaredMethod("marker", observation);
        marker.setAccessible(true);
        String missMarker = (String) marker.invoke(null, miss);
        String blockMarker = (String) marker.invoke(null, block);
        String entityMarker = (String) marker.invoke(null, entity);
        assertNotEquals(missMarker, blockMarker);
        assertNotEquals(blockMarker, entityMarker);
        assertNotEquals(missMarker, entityMarker);

        Method translationKey = semantics.getDeclaredMethod("translationKey", observation);
        translationKey.setAccessible(true);
        assertEquals("hud.black_arcana.aim.local.miss", translationKey.invoke(null, miss));
        assertEquals("hud.black_arcana.aim.local.block", translationKey.invoke(null, block));
        assertEquals("hud.black_arcana.aim.local.entity", translationKey.invoke(null, entity));

        Method shouldRender = semantics.getDeclaredMethod(
                "shouldRender", boolean.class, boolean.class, boolean.class, boolean.class);
        shouldRender.setAccessible(true);
        assertEquals(true, shouldRender.invoke(null, true, true, true, true));
        assertEquals(false, shouldRender.invoke(null, false, true, true, true));
        assertEquals(false, shouldRender.invoke(null, true, false, true, true));
        assertEquals(false, shouldRender.invoke(null, true, true, false, true));
        assertEquals(false, shouldRender.invoke(null, true, true, true, false));
    }

    @Test
    void physicalClientLayerUsesOnlyCurrentHitResultAndExistingSelectionWindow() throws Exception {
        assertTrue(Files.exists(LAYER), "05.13 local-observation GUI layer is missing");
        String layer = Files.readString(LAYER);
        String client = Files.readString(CLIENT);

        assertTrue(layer.contains("RegisterGuiLayersEvent"));
        assertTrue(layer.contains("event.registerAboveAll("));
        assertTrue(layer.contains("Minecraft.getInstance()"));
        assertTrue(layer.contains("minecraft.hitResult"));
        assertTrue(layer.contains("minecraft.hitResult.getType()"));
        assertTrue(layer.contains("TargetAimPresentationSemantics.fromHitType("));
        assertFalse(layer.contains("instanceof EntityHitResult"));
        assertFalse(layer.contains("instanceof BlockHitResult"));
        assertTrue(layer.contains("HudLayout.isRecent("));
        assertTrue(layer.contains("ClientUxState.selectionChangedTick()"));
        assertTrue(layer.contains("BlackArcanaClientConfig.SELECTION_DURATION_TICKS.get()"));
        assertTrue(layer.contains("TargetAimPresentationSemantics.shouldRender("));
        assertTrue(client.contains("modEventBus.addListener(TargetAimPresentationLayer::register);"));
    }

    @Test
    void localObservationNeverCreatesTargetGameplayOrServerTruth() throws Exception {
        assertTrue(Files.exists(LAYER), "05.13 local-observation GUI layer is missing");
        String layer = Files.readString(LAYER);
        String semantics = Files.readString(SEMANTICS);

        assertFalse(layer.contains("ArcanaNetworkBridge"));
        assertFalse(layer.contains("sendCastIntent"));
        assertFalse(layer.contains("requestCast"));
        assertFalse(layer.contains("WorldEffectAdmissionService"));
        assertFalse(layer.contains("ArcanaTargetSpec"));
        assertFalse(layer.contains("getEntities("));
        assertFalse(layer.contains("getEntitiesOfClass"));
        assertFalse(semantics.contains("VALID"));
        assertFalse(semantics.contains("ALLOWED"));
        assertFalse(semantics.contains("DENIED"));
    }

    @Test
    void localObservationLabelsExplicitlyRemainAdvisoryInBothLanguages() throws Exception {
        String en = Files.readString(EN_US);
        String pt = Files.readString(PT_BR);

        assertTrue(en.contains("\"hud.black_arcana.aim.local.miss\""));
        assertTrue(en.contains("\"hud.black_arcana.aim.local.block\""));
        assertTrue(en.contains("\"hud.black_arcana.aim.local.entity\""));
        assertTrue(en.contains("Local aim"));

        assertTrue(pt.contains("\"hud.black_arcana.aim.local.miss\""));
        assertTrue(pt.contains("\"hud.black_arcana.aim.local.block\""));
        assertTrue(pt.contains("\"hud.black_arcana.aim.local.entity\""));
        assertTrue(pt.contains("Mira local"));
    }

    private static Method requiredMethod(Class<?> owner, String name, Class<?>... parameterTypes) {
        try {
            Method method = owner.getDeclaredMethod(name, parameterTypes);
            method.setAccessible(true);
            return method;
        } catch (ReflectiveOperationException exception) {
            return fail(owner.getSimpleName() + "." + name + " is missing or invalid", exception);
        }
    }

    @SuppressWarnings({"unchecked", "rawtypes"})
    private static Object enumValue(Class<?> enumType, String name) {
        return Enum.valueOf((Class<? extends Enum>) enumType, name);
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
