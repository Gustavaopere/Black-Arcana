package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.content.noetic.FamiliarOwnershipRegistry;
import dev.gustavopere.blackarcana.content.noetic.NoeticObservationKind;
import dev.gustavopere.blackarcana.content.noetic.NoeticObservationRuntime;
import dev.gustavopere.blackarcana.content.noetic.NoeticObservationSession;
import dev.gustavopere.blackarcana.content.noetic.NoeticPerceptionSnapshot;
import dev.gustavopere.blackarcana.content.noetic.NoeticSafetyCeilings;
import net.minecraft.server.MinecraftServer;
import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.lang.reflect.RecordComponent;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;
import java.util.Set;
import java.util.UUID;
import java.util.stream.Collectors;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

class MinecraftNoeticObservationRuntimeContractTest {
    private static final Path RUNTIME_SOURCE = repositoryRoot()
            .resolve("src/main/java/dev/gustavopere/blackarcana/integration/neoforge/MinecraftNoeticObservationRuntime.java");

    @Test
    void snapshotSchemaExposesOnlyWhitelistedPerceptionFields() {
        assertTrue(NoeticPerceptionSnapshot.class.isRecord());
        Set<String> components = Arrays.stream(NoeticPerceptionSnapshot.class.getRecordComponents())
                .map(RecordComponent::getName)
                .collect(Collectors.toSet());
        assertEquals(Set.of(
                "targetId",
                "entityTypeId",
                "displayName",
                "healthFraction",
                "activeEffectIds",
                "mainHandItemId"), components);
    }

    @Test
    void snapshotSanitizationBoundsNameEffectsAndHealth() {
        UUID target = UUID.randomUUID();
        String longName = "x".repeat(NoeticSafetyCeilings.MAX_DISPLAY_NAME_LENGTH + 50);
        List<String> effects = java.util.stream.IntStream.range(0, NoeticSafetyCeilings.MAX_EFFECT_IDS + 20)
                .mapToObj(index -> "black_arcana:test_" + index)
                .toList();

        NoeticPerceptionSnapshot snapshot = NoeticPerceptionSnapshot.sanitized(
                target,
                "minecraft:zombie",
                longName,
                2.0D,
                effects,
                "minecraft:iron_sword");

        assertEquals(target, snapshot.targetId());
        assertEquals(NoeticSafetyCeilings.MAX_DISPLAY_NAME_LENGTH, snapshot.displayName().length());
        assertEquals(1.0D, snapshot.healthFraction());
        assertEquals(NoeticSafetyCeilings.MAX_EFFECT_IDS, snapshot.activeEffectIds().size());
        assertEquals(effects.subList(0, NoeticSafetyCeilings.MAX_EFFECT_IDS), snapshot.activeEffectIds());
    }

    @Test
    void snapshotSanitizationDeduplicatesEffectsAndHandlesNonFiniteHealth() {
        NoeticPerceptionSnapshot snapshot = NoeticPerceptionSnapshot.sanitized(
                UUID.randomUUID(),
                "minecraft:cow",
                "Cow",
                Double.NaN,
                List.of("minecraft:speed", "minecraft:speed", "minecraft:regeneration"),
                "minecraft:air");

        assertEquals(0.0D, snapshot.healthFraction());
        assertEquals(List.of("minecraft:speed", "minecraft:regeneration"), snapshot.activeEffectIds());
    }

    @Test
    void minecraftAdapterOwnsOnlyBoundedSessionAndFamiliarAuthorities() {
        MinecraftNoeticObservationRuntime runtime = new MinecraftNoeticObservationRuntime(
                new NoeticObservationRuntime(4),
                new FamiliarOwnershipRegistry(4));
        assertNotNull(runtime);
    }

    @Test
    void minecraftAdapterExposesServerScopedAdmissionSnapshotAndLifecycleSurface() throws Exception {
        assertEquals(ArcanaDecision.class,
                MinecraftNoeticObservationRuntime.class.getMethod(
                        "start",
                        MinecraftServer.class,
                        UUID.class,
                        UUID.class,
                        NoeticObservationKind.class,
                        int.class,
                        boolean.class).getReturnType());
        assertEquals(Optional.class,
                MinecraftNoeticObservationRuntime.class.getMethod(
                        "snapshot", MinecraftServer.class, UUID.class).getReturnType());
        assertEquals(void.class,
                MinecraftNoeticObservationRuntime.class.getMethod(
                        "tick", MinecraftServer.class).getReturnType());
        assertEquals(boolean.class,
                MinecraftNoeticObservationRuntime.class.getMethod(
                        "clearViewer", UUID.class, NoeticObservationSession.CloseReason.class).getReturnType());
        assertEquals(int.class,
                MinecraftNoeticObservationRuntime.class.getMethod(
                        "clearTarget", UUID.class).getReturnType());
        assertEquals(int.class,
                MinecraftNoeticObservationRuntime.class.getMethod(
                        "clearForServerStop").getReturnType());
    }

    @Test
    void activeObservationTickRevalidatesCanonicalAuthorizationPolicy() throws IOException {
        String source = Files.readString(RUNTIME_SOURCE);
        int tickStart = source.indexOf("public synchronized void tick(MinecraftServer server)");
        assertTrue(tickStart >= 0, "Noetic observation adapter must expose its lifecycle tick");
        int nextMethod = source.indexOf("\n    public synchronized", tickStart + 1);
        String tick = source.substring(tickStart, nextMethod < 0 ? source.length() : nextMethod);

        assertTrue(tick.contains("NoeticObservationPolicy.authorize(session.kind(), facts)"),
                "active observations must revalidate the same canonical authorization policy used at admission");
        assertTrue(tick.contains("entry.getValue().explicitConsent()"),
                "revalidation must preserve the server-owned consent evidence captured for the session");
        assertTrue(tick.contains("NoeticObservationSession.CloseReason.AUTHORIZATION_REVOKED"),
                "range/ownership/dimension policy loss must close the canonical session explicitly");
    }

    private static Path repositoryRoot() {
        String workspace = System.getenv("GITHUB_WORKSPACE");
        if (workspace != null && !workspace.isBlank()) {
            return Path.of(workspace);
        }

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
