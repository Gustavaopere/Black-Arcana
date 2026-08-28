package dev.gustavopere.blackarcana.content.noetic;

import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.Map;
import java.util.Objects;
import java.util.Set;
import java.util.UUID;

public final class FamiliarBondRegistry {
    public enum BindResult { BOUND, ALREADY_BOUND, OWNER_LIMIT, OWNED_BY_OTHER }
    private final int maxPerOwner;
    private final Map<UUID, UUID> ownersByFamiliar = new LinkedHashMap<>();
    private final Map<UUID, LinkedHashSet<UUID>> familiarsByOwner = new LinkedHashMap<>();

    public FamiliarBondRegistry(int maxPerOwner) {
        if (maxPerOwner <= 0 || maxPerOwner > FamiliarSafetyCeilings.MAX_FAMILIARS_PER_OWNER) throw new IllegalArgumentException("maxPerOwner outside safety ceiling");
        this.maxPerOwner = maxPerOwner;
    }

    public synchronized BindResult bind(UUID ownerId, UUID familiarId) {
        Objects.requireNonNull(ownerId, "ownerId"); Objects.requireNonNull(familiarId, "familiarId");
        UUID existing = ownersByFamiliar.get(familiarId);
        if (ownerId.equals(existing)) return BindResult.ALREADY_BOUND;
        if (existing != null) return BindResult.OWNED_BY_OTHER;
        LinkedHashSet<UUID> familiars = familiarsByOwner.computeIfAbsent(ownerId, ignored -> new LinkedHashSet<>());
        if (familiars.size() >= maxPerOwner) return BindResult.OWNER_LIMIT;
        familiars.add(familiarId); ownersByFamiliar.put(familiarId, ownerId);
        return BindResult.BOUND;
    }

    public synchronized boolean unbind(UUID ownerId, UUID familiarId) {
        if (!Objects.equals(ownersByFamiliar.get(familiarId), ownerId)) return false;
        ownersByFamiliar.remove(familiarId);
        LinkedHashSet<UUID> familiars = familiarsByOwner.get(ownerId);
        if (familiars != null) {
            familiars.remove(familiarId);
            if (familiars.isEmpty()) familiarsByOwner.remove(ownerId);
        }
        return true;
    }

    public synchronized boolean isOwnedBy(UUID familiarId, UUID ownerId) { return Objects.equals(ownersByFamiliar.get(familiarId), ownerId); }
    public synchronized Set<UUID> familiars(UUID ownerId) { return Set.copyOf(familiarsByOwner.getOrDefault(ownerId, new LinkedHashSet<>())); }
}
