package dev.gustavopere.blackarcana.core.progression;

import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.Map;
import java.util.Objects;
import java.util.Set;

/** Resolves server-owned operational defaults. Overrides can only lower or disable a preset value. */
public final class ServerBalancePresetResolver {
    public record Snapshot(ServerBalancePreset preset, boolean fallbackUsed, Map<String, Long> values, Set<String> rejectedOverrides) {
        public Snapshot {
            Objects.requireNonNull(preset, "preset");
            values = Map.copyOf(Objects.requireNonNull(values, "values"));
            rejectedOverrides = Set.copyOf(Objects.requireNonNull(rejectedOverrides, "rejectedOverrides"));
        }
    }

    public Snapshot resolve(String presetName, Map<String, Long> technicalCeilings, Map<String, Long> overrides) {
        Objects.requireNonNull(technicalCeilings, "technicalCeilings");
        Objects.requireNonNull(overrides, "overrides");
        var parsed = ServerBalancePreset.parseOrBalanced(presetName);
        Map<String, Long> values = new LinkedHashMap<>();
        technicalCeilings.forEach((key, ceiling) -> {
            validateKey(key);
            if (ceiling == null || ceiling < 0L) throw new IllegalArgumentException("technical ceilings must be non-negative");
            long presetValue = (long) Math.floor(ceiling * parsed.preset().technicalCeilingFraction());
            values.put(key, Math.min(ceiling, Math.max(0L, presetValue)));
        });

        Set<String> rejected = new LinkedHashSet<>();
        overrides.forEach((key, value) -> {
            Long presetValue = values.get(key);
            if (presetValue == null || value == null || value < 0L || value > presetValue) {
                rejected.add(key);
            } else {
                values.put(key, value);
            }
        });
        return new Snapshot(parsed.preset(), parsed.fallbackUsed(), values, rejected);
    }

    private static void validateKey(String key) {
        if (key == null || key.isBlank() || key.length() > 160) throw new IllegalArgumentException("balance setting key must be non-blank and bounded");
    }
}
