package dev.gustavopere.blackarcana.integration.malum;

import java.util.Objects;
import java.util.regex.Pattern;

public record MalumRitualSpiritRequirement(String affinity, int amount) {
    private static final Pattern AFFINITY = Pattern.compile("[a-z0-9_./-]{1,48}");
    public static final int MAX_SPIRITS_PER_AFFINITY = 64;

    public MalumRitualSpiritRequirement {
        Objects.requireNonNull(affinity, "affinity");
        if (!AFFINITY.matcher(affinity).matches()) {
            throw new IllegalArgumentException("invalid Malum spirit affinity");
        }
        if (amount <= 0 || amount > MAX_SPIRITS_PER_AFFINITY) {
            throw new IllegalArgumentException("Malum ritual spirit amount outside bounds");
        }
    }
}
