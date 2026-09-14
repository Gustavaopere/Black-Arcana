package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.content.noetic.AstralSeveranceRuntime;
import dev.gustavopere.blackarcana.network.AstralViewTransitionTracker;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.Map;
import java.util.OptionalInt;
import java.util.Set;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;

class AstralViewSyncPlannerTest {
    @Test
    void projectsExactCanonicalProjectionIdentityToLoadedRepresentation() {
        UUID caster = UUID.randomUUID();
        UUID projection = UUID.randomUUID();
        AstralSeveranceRuntime.ActiveProjection active = projection(caster, projection);

        assertEquals(Map.of(
                caster,
                new AstralViewTransitionTracker.Desired(projection, 17)),
                AstralViewSyncPlanner.project(
                        List.of(active),
                        (casterId, projectionId) -> casterId.equals(caster) && projectionId.equals(projection)
                                ? OptionalInt.of(17)
                                : OptionalInt.empty()));
    }

    @Test
    void missingNegativeOrSuppressedRepresentationsFailClosed() {
        UUID caster = UUID.randomUUID();
        UUID projection = UUID.randomUUID();
        AstralSeveranceRuntime.ActiveProjection active = projection(caster, projection);

        assertEquals(Map.of(), AstralViewSyncPlanner.project(
                List.of(active),
                (casterId, projectionId) -> OptionalInt.empty()));
        assertEquals(Map.of(), AstralViewSyncPlanner.project(
                List.of(active),
                (casterId, projectionId) -> OptionalInt.of(-1)));
        assertEquals(Map.of(), AstralViewSyncPlanner.project(
                List.of(active),
                Set.of(caster),
                (casterId, projectionId) -> OptionalInt.of(17)));
    }

    private static AstralSeveranceRuntime.ActiveProjection projection(UUID caster, UUID projection) {
        AstralSeveranceRuntime.ProjectionPose pose =
                new AstralSeveranceRuntime.ProjectionPose(1.0D, 2.0D, 3.0D, 0.0F, 0.0F);
        return new AstralSeveranceRuntime.ActiveProjection(
                projection,
                caster,
                caster,
                10L,
                30L,
                16.0D,
                pose,
                pose,
                0L);
    }
}
