package dev.gustavopere.blackarcana.api;

public record ArcanaChannelSpec(long minimumTicks, long maximumTicks) {
    public static final long ABSOLUTE_MAX_CHANNEL_TICKS = 20L * 60L * 5L;

    public ArcanaChannelSpec {
        if (minimumTicks < 0L) throw new IllegalArgumentException("minimumTicks cannot be negative");
        if (maximumTicks <= 0L || maximumTicks > ABSOLUTE_MAX_CHANNEL_TICKS) {
            throw new IllegalArgumentException("maximumTicks outside channel bounds");
        }
        if (minimumTicks > maximumTicks) throw new IllegalArgumentException("minimumTicks cannot exceed maximumTicks");
    }
}
