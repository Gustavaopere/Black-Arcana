package dev.gustavopere.blackarcana.core.progression;

public enum ServerBalancePreset {
    SAFE(0.50D),
    BALANCED(0.75D),
    CHAOTIC_FULL(1.00D);

    private final double technicalCeilingFraction;
    ServerBalancePreset(double technicalCeilingFraction) { this.technicalCeilingFraction = technicalCeilingFraction; }
    public double technicalCeilingFraction() { return technicalCeilingFraction; }

    public static ParseResult parseOrBalanced(String value) {
        if (value != null) {
            for (ServerBalancePreset preset : values()) if (preset.name().equalsIgnoreCase(value.trim())) return new ParseResult(preset, false);
        }
        return new ParseResult(BALANCED, true);
    }

    public record ParseResult(ServerBalancePreset preset, boolean fallbackUsed) { }
}
