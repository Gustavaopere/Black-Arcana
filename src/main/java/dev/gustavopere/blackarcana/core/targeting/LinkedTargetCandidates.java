package dev.gustavopere.blackarcana.core.targeting;

import java.util.ArrayList;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Set;
import java.util.UUID;

/** Pure validation/deduplication for server-owned linked target ids. */
public final class LinkedTargetCandidates {
    private LinkedTargetCandidates() { }

    public static Result normalize(List<UUID> candidates, int maxCandidates) {
        if (maxCandidates <= 0) throw new IllegalArgumentException("maxCandidates must be positive");
        if (candidates == null) return Result.denied("linked target resolver returned null list");
        if (candidates.size() > maxCandidates) {
            return Result.denied("linked target candidate set exceeds hard bound");
        }

        Set<UUID> unique = new LinkedHashSet<>();
        for (UUID targetId : candidates) {
            if (targetId == null) return Result.denied("linked target resolver returned null id");
            unique.add(targetId);
        }
        return Result.accepted(new ArrayList<>(unique));
    }

    public record Result(boolean valid, List<UUID> uniqueIds, String detail) {
        public Result {
            uniqueIds = List.copyOf(uniqueIds);
            if (detail == null) throw new IllegalArgumentException("detail cannot be null");
            if (valid && !detail.isEmpty()) throw new IllegalArgumentException("valid result cannot carry denial detail");
            if (!valid && detail.isBlank()) throw new IllegalArgumentException("denied result requires detail");
            if (!valid && !uniqueIds.isEmpty()) throw new IllegalArgumentException("denied result cannot carry target ids");
        }

        public static Result accepted(List<UUID> uniqueIds) {
            return new Result(true, uniqueIds, "");
        }

        public static Result denied(String detail) {
            return new Result(false, List.of(), detail);
        }
    }
}
