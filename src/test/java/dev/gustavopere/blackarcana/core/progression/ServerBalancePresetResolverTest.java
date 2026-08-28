package dev.gustavopere.blackarcana.core.progression;

import org.junit.jupiter.api.Test;

import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

class ServerBalancePresetResolverTest {
    @Test void presetsNeverExceedFrozenTechnicalCeilings() {
        var resolver = new ServerBalancePresetResolver();
        var ceilings = FrozenTechnicalCeilings.defaults();
        for (ServerBalancePreset preset : ServerBalancePreset.values()) {
            var snapshot = resolver.resolve(preset.name(), ceilings, Map.of());
            ceilings.forEach((key, cap) -> assertTrue(snapshot.values().get(key) <= cap, key));
        }
    }

    @Test void overrideCanOnlyLowerAndInvalidPresetFallsBackBalanced() {
        var resolver = new ServerBalancePresetResolver();
        var snapshot = resolver.resolve("invalid", Map.of("black_pyre.radius", 12L), Map.of("black_pyre.radius", 5L));
        assertEquals(ServerBalancePreset.BALANCED, snapshot.preset());
        assertTrue(snapshot.fallbackUsed());
        assertEquals(5L, snapshot.values().get("black_pyre.radius"));

        var rejected = resolver.resolve("SAFE", Map.of("black_pyre.radius", 12L), Map.of("black_pyre.radius", 7L));
        assertEquals(6L, rejected.values().get("black_pyre.radius"));
        assertTrue(rejected.rejectedOverrides().contains("black_pyre.radius"));
    }

    @Test void chaoticFullStillEqualsRatherThanExceedsTechnicalCap() {
        var snapshot = new ServerBalancePresetResolver().resolve("CHAOTIC_FULL", Map.of("inner_dominion.duration", 2400L), Map.of());
        assertEquals(2400L, snapshot.values().get("inner_dominion.duration"));
    }
}
