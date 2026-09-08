package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.content.noetic.NoeticObservationKind;
import dev.gustavopere.blackarcana.content.noetic.NoeticObservationRuntime;
import dev.gustavopere.blackarcana.network.NoeticViewTransitionTracker;

import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.OptionalInt;
import java.util.UUID;
import java.util.function.BiFunction;

/** Pure bounded projection from canonical Noetic sessions to Borrowed Sight presentation intent. */
final class NoeticViewSyncPlanner {
    private NoeticViewSyncPlanner() {
    }

    static Map<UUID, NoeticViewTransitionTracker.Desired> project(
            List<NoeticObservationRuntime.ActiveSession> sessions,
            BiFunction<UUID, UUID, OptionalInt> loadedEntityIdResolver
    ) {
        Objects.requireNonNull(sessions, "sessions");
        Objects.requireNonNull(loadedEntityIdResolver, "loadedEntityIdResolver");

        Map<UUID, NoeticViewTransitionTracker.Desired> desiredByViewer = new LinkedHashMap<>();
        for (NoeticObservationRuntime.ActiveSession session : sessions) {
            Objects.requireNonNull(session, "session");
            if (session.kind() != NoeticObservationKind.BORROWED_SIGHT) {
                continue;
            }

            OptionalInt targetEntityId = Objects.requireNonNull(
                    loadedEntityIdResolver.apply(session.viewerId(), session.targetId()), "targetEntityId");
            if (targetEntityId.isEmpty() || targetEntityId.getAsInt() < 0) {
                continue;
            }
            desiredByViewer.put(
                    session.viewerId(),
                    new NoeticViewTransitionTracker.Desired(
                            NoeticObservationKind.BORROWED_SIGHT,
                            targetEntityId.getAsInt()));
        }
        return Collections.unmodifiableMap(desiredByViewer);
    }
}
