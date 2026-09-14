package dev.gustavopere.blackarcana.network;

import dev.gustavopere.blackarcana.api.ArcanaChannelSpec;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;

import java.util.Comparator;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Set;

/** Server-authored client capability snapshot for channel-capable spells. */
public record ChannelCapabilityPayload(int protocolVersion, List<Entry> entries) {
    public static final int MAX_ENTRIES = 512;

    public ChannelCapabilityPayload {
        ArcanaProtocol.requireCompatible(protocolVersion);
        Objects.requireNonNull(entries, "entries");
        if (entries.size() > MAX_ENTRIES) throw new IllegalArgumentException("too many channel capability entries");
        entries = List.copyOf(entries);
        Set<String> ids = new HashSet<>();
        for (Entry entry : entries) {
            Objects.requireNonNull(entry, "entry");
            if (!ids.add(entry.spellId())) {
                throw new IllegalArgumentException("duplicate channel capability entry: " + entry.spellId());
            }
        }
    }

    public static ChannelCapabilityPayload from(Map<ArcanaSpellId, ArcanaChannelSpec> specs) {
        Objects.requireNonNull(specs, "specs");
        if (specs.size() > MAX_ENTRIES) throw new IllegalArgumentException("too many channel capability entries");
        List<Entry> entries = specs.entrySet().stream()
                .sorted(Comparator.comparing(entry -> entry.getKey().canonical()))
                .map(entry -> new Entry(
                        entry.getKey().canonical(),
                        entry.getValue().minimumTicks(),
                        entry.getValue().maximumTicks()))
                .toList();
        return new ChannelCapabilityPayload(ArcanaProtocol.VERSION, entries);
    }

    public record Entry(String spellId, long minimumTicks, long maximumTicks) {
        public Entry {
            Objects.requireNonNull(spellId, "spellId");
            if (spellId.length() > ArcanaProtocol.MAX_RESOURCE_ID_LENGTH) {
                throw new IllegalArgumentException("spellId exceeds protocol bound");
            }
            ArcanaSpellId.parse(spellId);
            new ArcanaChannelSpec(minimumTicks, maximumTicks);
        }

        public ArcanaSpellId parsedSpellId() {
            return ArcanaSpellId.parse(spellId);
        }

        public ArcanaChannelSpec spec() {
            return new ArcanaChannelSpec(minimumTicks, maximumTicks);
        }
    }
}
