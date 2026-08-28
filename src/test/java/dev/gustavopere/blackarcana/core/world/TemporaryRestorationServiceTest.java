package dev.gustavopere.blackarcana.core.world;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import org.junit.jupiter.api.Test;

import java.util.Optional;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;

class TemporaryRestorationServiceTest {
    @Test
    void backendReadFailureLeavesRollbackPendingWithoutEscapingTick() {
        TemporaryMutationKey key = new TemporaryMutationKey("minecraft:overworld", 42L);
        TemporaryMutationTracker tracker = new TemporaryMutationTracker(4);
        tracker.register(
            key,
            UUID.fromString("11111111-1111-1111-1111-111111111111"),
            ArcanaCastId.parse("22222222-2222-2222-2222-222222222222"),
            "minecraft:stone",
            "minecraft:obsidian",
            20L);

        TemporaryBlockBackend backend = new TemporaryBlockBackend() {
            @Override
            public Optional<String> readLoadedState(TemporaryMutationKey ignored) {
                throw new IllegalStateException("simulated read failure");
            }

            @Override
            public boolean replaceIfCurrent(TemporaryMutationKey ignored, String expected, String replacement) {
                throw new AssertionError("write must not run when read failed");
            }
        };

        TemporaryRestorationService.TickResult result =
            new TemporaryRestorationService(tracker, backend).tick(20L, 4);

        assertEquals(0, result.restored());
        assertEquals(1, result.unavailable());
        assertEquals(1, result.failures());
        assertEquals(1, tracker.size());
    }
}
