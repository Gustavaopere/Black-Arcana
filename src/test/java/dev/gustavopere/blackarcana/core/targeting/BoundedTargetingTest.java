package dev.gustavopere.blackarcana.core.targeting;

import dev.gustavopere.blackarcana.api.ArcanaTargetSpec;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;

class BoundedTargetingTest {
    @Test
    void filtersInvalidUnloadedOutOfRangePlayersAndFriendliesThenCapsDeterministically() {
        ArcanaTargetSpec spec = new ArcanaTargetSpec(ArcanaTargetSpec.Kind.SPHERE, 10.0, 2, true, false, false);
        List<TargetCandidate> candidates = List.of(
                new TargetCandidate("far", 121.0, true, true, true, false, false),
                new TargetCandidate("unloaded", 1.0, false, true, true, false, false),
                new TargetCandidate("dead", 1.0, true, false, true, false, false),
                new TargetCandidate("hidden", 1.0, true, true, false, false, false),
                new TargetCandidate("player", 1.0, true, true, true, true, false),
                new TargetCandidate("friendly", 1.0, true, true, true, false, true),
                new TargetCandidate("b", 9.0, true, true, true, false, false),
                new TargetCandidate("a", 9.0, true, true, true, false, false),
                new TargetCandidate("nearest", 4.0, true, true, true, false, false));

        List<TargetCandidate> selected = BoundedTargeting.select(spec, candidates);
        assertEquals(List.of("nearest", "a"), selected.stream().map(TargetCandidate::targetId).toList());
    }

    @Test
    void permissivePolicyStillHonorsHardTargetCap() {
        ArcanaTargetSpec spec = new ArcanaTargetSpec(ArcanaTargetSpec.Kind.CONE, 50.0, 1, false, true, true);
        List<TargetCandidate> selected = BoundedTargeting.select(spec, List.of(
                new TargetCandidate("two", 4.0, true, true, false, true, true),
                new TargetCandidate("one", 1.0, true, true, false, false, false)));
        assertEquals(List.of("one"), selected.stream().map(TargetCandidate::targetId).toList());
    }
}
