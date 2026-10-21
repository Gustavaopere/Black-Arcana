package dev.gustavopere.blackarcana.integration.neoforge;

import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.world.entity.Entity;

import java.util.Objects;

/**
 * GameTest-only fixture barrier for the server's UUID entity index.
 *
 * Spawning a fixture can precede ServerLevel.getEntity(UUID) visibility. Wait for exact
 * object identity before executing an existing behavioral assertion; never relax runtime
 * admission, skip a failed gameplay assertion or turn fixture registration into a PASS.
 */
final class GameTestEntityIndexGate {
    private static final long FIRST_PROBE_TICK = 1L;
    private static final long LAST_PROBE_TICK = 20L;

    private GameTestEntityIndexGate() { }

    static void whenIndexed(GameTestHelper helper, Runnable assertions, Entity... requiredEntities) {
        Objects.requireNonNull(helper, "helper");
        Objects.requireNonNull(assertions, "assertions");
        Objects.requireNonNull(requiredEntities, "requiredEntities");
        if (requiredEntities.length == 0) throw new IllegalArgumentException("At least one fixture entity is required");
        Entity[] fixtures = requiredEntities.clone();
        for (Entity entity : fixtures) Objects.requireNonNull(entity, "fixture entity");
        helper.runAtTickTime(FIRST_PROBE_TICK,
                () -> runIfIndexed(helper, assertions, fixtures, FIRST_PROBE_TICK));
    }

    private static void runIfIndexed(GameTestHelper helper, Runnable assertions, Entity[] fixtures, long tick) {
        for (Entity fixture : fixtures) {
            if (helper.getLevel().getEntity(fixture.getUUID()) != fixture) {
                if (tick >= LAST_PROBE_TICK) {
                    helper.fail("GameTest fixture still absent from ServerLevel UUID index at tick "
                            + tick + ": " + fixture.getUUID() + " (" + fixture.getType() + ")");
                    return;
                }
                helper.runAtTickTime(tick + 1L,
                        () -> runIfIndexed(helper, assertions, fixtures, tick + 1L));
                return;
            }
        }
        assertions.run();
    }
}
