package dev.gustavopere.blackarcana.core.ritual;

import java.util.HashSet;
import java.util.List;
import java.util.Objects;
import java.util.UUID;

public record RitualContext(UUID casterId, List<UUID> participantIds, RitualAnchor anchor) {
    public static final int MAX_PARTICIPANTS = 16;

    public RitualContext {
        Objects.requireNonNull(casterId, "casterId");
        Objects.requireNonNull(participantIds, "participantIds");
        Objects.requireNonNull(anchor, "anchor");
        if (participantIds.size() > MAX_PARTICIPANTS) {
            throw new IllegalArgumentException("too many ritual participants");
        }
        participantIds = List.copyOf(participantIds);
        if (participantIds.stream().anyMatch(Objects::isNull)) {
            throw new IllegalArgumentException("participantIds cannot contain null");
        }
        if (new HashSet<>(participantIds).size() != participantIds.size()) {
            throw new IllegalArgumentException("participantIds cannot contain duplicates");
        }
    }
}
