package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.content.noetic.AstralSeveranceRuntime;
import dev.gustavopere.blackarcana.network.AstralViewTransitionTracker;

import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.OptionalInt;
import java.util.Set;
import java.util.UUID;
import java.util.function.BiFunction;

/** Pure bounded projection from canonical Astral sessions to presentation intent. */
final class AstralViewSyncPlanner {
    private AstralViewSyncPlanner() { }

    static Map<UUID, AstralViewTransitionTracker.Desired> project(
            List<AstralSeveranceRuntime.ActiveProjection> projections,
            BiFunction<UUID, UUID, OptionalInt> loadedEntityIdResolver
    ) {
        return project(projections, Set.of(), loadedEntityIdResolver);
    }

    static Map<UUID, AstralViewTransitionTracker.Desired> project(
            List<AstralSeveranceRuntime.ActiveProjection> projections,
            Set<UUID> suppressedViewers,
            BiFunction<UUID, UUID, OptionalInt> loadedEntityIdResolver
    ) {
        Objects.requireNonNull(projections, "projections");
        Objects.requireNonNull(suppressedViewers, "suppressedViewers");
        Objects.requireNonNull(loadedEntityIdResolver, "loadedEntityIdResolver");

        Map<UUID, AstralViewTransitionTracker.Desired> desiredByViewer = new LinkedHashMap<>();
        for (AstralSeveranceRuntime.ActiveProjection projection : projections) {
            Objects.requireNonNull(projection, "projection");
            if (suppressedViewers.contains(projection.casterId())) {
                continue;
            }
            OptionalInt entityId = Objects.requireNonNull(
                    loadedEntityIdResolver.apply(projection.casterId(), projection.projectionId()), "entityId");
            if (entityId.isEmpty() || entityId.getAsInt() < 0) {
                continue;
            }
            desiredByViewer.put(
                    projection.casterId(),
                    new AstralViewTransitionTracker.Desired(
                            projection.projectionId(),
                            entityId.getAsInt()));
        }
        return Collections.unmodifiableMap(desiredByViewer);
    }
}
