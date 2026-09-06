package dev.gustavopere.blackarcana.content.noetic;

import net.minecraft.resources.ResourceLocation;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class NoeticGazeContractTest {
    @Test
    void stillnessRequiresLoadedLivingSameDimensionReciprocalSightFacingAndCanonicalControl() {
        NoeticGazePolicy.Facts safe = new NoeticGazePolicy.Facts(
                true, true, true, true, true, true, true, true, true);
        assertTrue(NoeticGazePolicy.authorizeStillness(safe).allowed());

        assertFalse(NoeticGazePolicy.authorizeStillness(new NoeticGazePolicy.Facts(
                false, true, true, true, true, true, true, true, true)).allowed());
        assertFalse(NoeticGazePolicy.authorizeStillness(new NoeticGazePolicy.Facts(
                true, false, true, true, true, true, true, true, true)).allowed());
        assertFalse(NoeticGazePolicy.authorizeStillness(new NoeticGazePolicy.Facts(
                true, true, false, true, true, true, true, true, true)).allowed());
        assertFalse(NoeticGazePolicy.authorizeStillness(new NoeticGazePolicy.Facts(
                true, true, true, false, true, true, true, true, true)).allowed());
        assertFalse(NoeticGazePolicy.authorizeStillness(new NoeticGazePolicy.Facts(
                true, true, true, true, false, true, true, true, true)).allowed());
        assertFalse(NoeticGazePolicy.authorizeStillness(new NoeticGazePolicy.Facts(
                true, true, true, true, true, false, true, true, true)).allowed());
        assertFalse(NoeticGazePolicy.authorizeStillness(new NoeticGazePolicy.Facts(
                true, true, true, true, true, true, false, true, true)).allowed());
        assertFalse(NoeticGazePolicy.authorizeStillness(new NoeticGazePolicy.Facts(
                true, true, true, true, true, true, true, false, true)).allowed());
        assertFalse(NoeticGazePolicy.authorizeStillness(new NoeticGazePolicy.Facts(
                true, true, true, true, true, true, true, true, false)).allowed());
    }

    @Test
    void gazeRangeActiveStateAndDiminishingReturnsHaveHardCeilings() {
        assertTrue(NoeticSafetyCeilings.MAX_GAZE_RANGE_BLOCKS > 0.0D);
        assertTrue(NoeticSafetyCeilings.MAX_GAZE_RANGE_BLOCKS <= NoeticSafetyCeilings.MAX_RANGE_BLOCKS);
        assertTrue(NoeticSafetyCeilings.MAX_ACTIVE_GAZES > 0);
        assertTrue(NoeticSafetyCeilings.MAX_GAZE_DURATION_TICKS > 0);
        assertTrue(NoeticSafetyCeilings.MAX_GAZE_DURATION_TICKS <= NoeticSafetyCeilings.MAX_DURATION_TICKS);
        assertTrue(NoeticSafetyCeilings.MAX_GAZE_DR_STACKS > 0);
        assertTrue(NoeticSafetyCeilings.MAX_GAZE_DR_TRACKED_TARGETS >= NoeticSafetyCeilings.MAX_ACTIVE_GAZES);
        assertTrue(NoeticSafetyCeilings.GAZE_DR_RESET_TICKS >= NoeticSafetyCeilings.MAX_GAZE_DURATION_TICKS);
    }

    @Test
    void nullificationPolicyFailsClosedForBossesAndCanonicalControlDenial() {
        assertTrue(NoeticGazePolicy.authorizeNullification(false, true).allowed());
        assertFalse(NoeticGazePolicy.authorizeNullification(true, true).allowed());
        assertFalse(NoeticGazePolicy.authorizeNullification(false, false).allowed());
    }

    @Test
    void nullificationRegistryIsBoundedDeduplicatedAndFailsClosedForUnknownEffects() {
        assertThrows(IllegalArgumentException.class,
                () -> new NullificationRegistry(NoeticSafetyCeilings.MAX_NULLIFIABLE_EFFECT_TYPES + 1));

        NullificationRegistry registry = new NullificationRegistry(4);
        ResourceLocation speed = ResourceLocation.parse("minecraft:speed");
        ResourceLocation weakness = ResourceLocation.parse("minecraft:weakness");
        ResourceLocation unknown = ResourceLocation.parse("black_arcana:private_provider_state");

        assertTrue(registry.register(speed));
        assertFalse(registry.register(speed));
        assertTrue(registry.register(weakness));
        assertTrue(registry.isNullifiable(speed));
        assertFalse(registry.isNullifiable(unknown));
        assertEquals(2, registry.size());
    }

    @Test
    void nullificationSelectionNeverExceedsPerActionRemovalBudget() {
        NullificationRegistry registry = new NullificationRegistry(NoeticSafetyCeilings.MAX_NULLIFIABLE_EFFECT_TYPES);
        List<ResourceLocation> registered = java.util.stream.IntStream
                .range(0, NoeticSafetyCeilings.MAX_NULLIFICATIONS_PER_ACTION + 4)
                .mapToObj(index -> ResourceLocation.parse("black_arcana:nullifiable_" + index))
                .toList();
        registered.forEach(registry::register);

        List<ResourceLocation> selected = registry.selectNullifiable(registered);
        assertEquals(NoeticSafetyCeilings.MAX_NULLIFICATIONS_PER_ACTION, selected.size());
        assertEquals(registered.subList(0, NoeticSafetyCeilings.MAX_NULLIFICATIONS_PER_ACTION), selected);
    }
}
