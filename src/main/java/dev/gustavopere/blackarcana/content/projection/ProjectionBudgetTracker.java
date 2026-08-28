package dev.gustavopere.blackarcana.content.projection;

import java.util.HashMap;
import java.util.Map;
import java.util.Objects;
import java.util.UUID;

/** Admission accounting for temporary echoes and projectile volleys. */
public final class ProjectionBudgetTracker {
    private final int maxActiveEchoes;
    private final Map<UUID, Integer> activeEchoes = new HashMap<>();

    public ProjectionBudgetTracker(int maxActiveEchoes) {
        if (maxActiveEchoes <= 0 || maxActiveEchoes > ProjectionSafetyCeilings.MAX_ACTIVE_ECHOES) {
            throw new IllegalArgumentException("maxActiveEchoes outside hard ceiling");
        }
        this.maxActiveEchoes = maxActiveEchoes;
    }

    public synchronized boolean tryAcquireEchoes(UUID ownerId, int count) {
        Objects.requireNonNull(ownerId, "ownerId");
        if (count <= 0 || count > ProjectionSafetyCeilings.MAX_PROJECTILES_PER_VOLLEY) {
            throw new IllegalArgumentException("count outside hard volley ceiling");
        }
        int current = activeEchoes.getOrDefault(ownerId, 0);
        if (count > maxActiveEchoes - current) return false;
        activeEchoes.put(ownerId, current + count);
        return true;
    }

    public synchronized void releaseEchoes(UUID ownerId, int count) {
        Objects.requireNonNull(ownerId, "ownerId");
        if (count <= 0) throw new IllegalArgumentException("count must be positive");
        int current = activeEchoes.getOrDefault(ownerId, 0);
        int remaining = Math.max(0, current - count);
        if (remaining == 0) activeEchoes.remove(ownerId);
        else activeEchoes.put(ownerId, remaining);
    }

    public synchronized int activeEchoes(UUID ownerId) {
        return activeEchoes.getOrDefault(Objects.requireNonNull(ownerId, "ownerId"), 0);
    }

    public static int validateVolleySize(int requested) {
        if (requested <= 0 || requested > ProjectionSafetyCeilings.MAX_PROJECTILES_PER_VOLLEY) {
            throw new IllegalArgumentException("volley size outside hard ceiling");
        }
        return requested;
    }
}
