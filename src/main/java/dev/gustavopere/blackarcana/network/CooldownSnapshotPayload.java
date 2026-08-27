package dev.gustavopere.blackarcana.network;

import dev.gustavopere.blackarcana.api.ArcanaSpellId;

import java.util.List;
import java.util.Objects;

public record CooldownSnapshotPayload(int protocolVersion, List<Entry> entries) {
    public CooldownSnapshotPayload {
        ArcanaProtocol.requireCompatible(protocolVersion);
        Objects.requireNonNull(entries, "entries");
        entries = List.copyOf(entries);
        if (entries.size() > ArcanaProtocol.MAX_COOLDOWN_ENTRIES) {
            throw new IllegalArgumentException("too many cooldown entries");
        }
    }

    public record Entry(String groupId, long remainingTicks) {
        public Entry {
            Objects.requireNonNull(groupId, "groupId");
            ArcanaSpellId.parse(groupId);
            if (remainingTicks < 0L) throw new IllegalArgumentException("remainingTicks cannot be negative");
        }
    }
}
