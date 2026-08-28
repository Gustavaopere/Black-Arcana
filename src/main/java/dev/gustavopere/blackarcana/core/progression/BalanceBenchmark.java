package dev.gustavopere.blackarcana.core.progression;

import java.util.Objects;

public record BalanceBenchmark(String source, String version, String note) {
    public BalanceBenchmark {
        Objects.requireNonNull(source, "source");
        Objects.requireNonNull(version, "version");
        Objects.requireNonNull(note, "note");
        if (source.isBlank() || source.length() > 128 || version.isBlank() || version.length() > 64 || note.length() > 512) {
            throw new IllegalArgumentException("benchmark metadata must be bounded and identify source/version");
        }
    }
}
