package dev.gustavopere.blackarcana.content.souls;

public final class SoulSafetyCeilings {
    private SoulSafetyCeilings() { }

    public static final int MAX_SOUL_ANCHORS = 5;
    public static final long MIN_RECOVERY_LOCKOUT_TICKS = 200L;
    public static final int MAX_RECENT_DEATH_EVENTS_PER_OWNER = 64;
    public static final int MAX_TRACKED_OWNERS = 4096;
}
