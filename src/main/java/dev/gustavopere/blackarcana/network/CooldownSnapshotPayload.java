package dev.gustavopere.blackarcana.network;

import dev.gustavopere.blackarcana.api.ArcanaSpellId;

import java.util.HashSet;
import java.util.List;
import java.util.Objects;
import java.util.Set;

public record CooldownSnapshotPayload(int protocolVersion, List<Entry> entries) {
    public CooldownSnapshotPayload {
        ArcanaProtocol.requireCompatible(protocolVersion);
        Objects.requireNonNull(entries, "entries");
        entries = List.copyOf(entries);
        if (entries.size() > ArcanaProtocol.MAX_COOLDOWN_ENTRIES) {
            throw new IllegalArgumentException("too many cooldown entries");
        }

        Set<String> groupIds = new HashSet<>(entries.size());
        for (Entry entry : entries) {
            Objects.requireNonNull(entry, "cooldown entry");
            if (!groupIds.add(entry.groupId())) {
                throw new IllegalArgumentException("duplicate cooldown group id: " + entry.groupId());
            }
        }
    }

    public record Entry(String groupId, long remainingTicks) {
        public Entry {
            Objects.requireNonNull(groupId, "groupId");
            if (groupId.length() > ArcanaProtocol.MAX_RESOURCE_ID_LENGTH) {
                throw new IllegalArgumentException("groupId exceeds protocol bound");
            }
            ArcanaSpellId.parse(groupId);
            if (remainingTicks < 0L) throw new IllegalArgumentException("remainingTicks cannot be negative");
        }
    }
}
