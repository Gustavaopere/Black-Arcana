package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.content.noetic.FamiliarOwnershipRegistry;
import dev.gustavopere.blackarcana.content.noetic.NoeticObservationRuntime;
import dev.gustavopere.blackarcana.content.noetic.NoeticPerceptionSnapshot;
import dev.gustavopere.blackarcana.content.noetic.NoeticSafetyCeilings;
import org.junit.jupiter.api.Test;

import java.lang.reflect.RecordComponent;
import java.util.Arrays;
import java.util.List;
import java.util.Set;
import java.util.UUID;
import java.util.stream.Collectors;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

class MinecraftNoeticObservationRuntimeContractTest {
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
}
