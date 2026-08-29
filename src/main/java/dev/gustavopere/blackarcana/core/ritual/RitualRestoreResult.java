package dev.gustavopere.blackarcana.core.ritual;

public record RitualRestoreResult(int restored, int rejected) {
    public RitualRestoreResult {
        if (restored < 0 || rejected < 0) throw new IllegalArgumentException("restore counts cannot be negative");
    }
}
