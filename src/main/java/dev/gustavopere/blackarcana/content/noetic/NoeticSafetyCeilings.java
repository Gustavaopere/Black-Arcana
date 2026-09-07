package dev.gustavopere.blackarcana.content.noetic;

/** Absolute safety ceilings for Stage 07.07. Stage 08 may tune below these values. */
public final class NoeticSafetyCeilings {
    public static final double MAX_RANGE_BLOCKS = 128.0D;
    public static final int MAX_DURATION_TICKS = 600;
    public static final int MAX_ACTIVE_SESSIONS = 64;
    public static final int MAX_EFFECT_IDS = 16;
    public static final int MAX_DISPLAY_NAME_LENGTH = 96;
    public static final int MAX_FAMILIAR_PROVIDERS = 16;
    public static final int MAX_NULLIFICATIONS_PER_ACTION = 8;
    public static final int MAX_ACTIVE_GAZES = 64;
    public static final double MAX_GAZE_RANGE_BLOCKS = 24.0D;
    public static final int MAX_GAZE_DURATION_TICKS = 160;
    /** Conservative Stage 07.07 PvP cap; Stage 08 may tune lower but never above the generic ceiling. */
    public static final int MAX_PLAYER_GAZE_DURATION_TICKS = 40;
    public static final int GAZE_PLAYER_REAPPLICATION_IMMUNITY_TICKS = 80;
    public static final int MIN_GAZE_PLAYER_REAPPLICATION_IMMUNITY_TICKS = 40;
    public static final int MAX_NULLIFIABLE_EFFECT_TYPES = 128;
    public static final int MAX_GAZE_DR_STACKS = 3;
    public static final int MAX_GAZE_DR_TRACKED_TARGETS = 256;
    public static final int GAZE_DR_RESET_TICKS = 600;
    public static final int MAX_SANCTUARY_RADIUS = 16;
    public static final int MAX_SANCTUARY_DURATION_TICKS = 600;
    public static final int MAX_SANCTUARY_MEMBERS = 8;
    public static final int MAX_ACTIVE_SANCTUARIES = 32;
    public static final int MAX_SANCTUARY_MOBS_PER_TICK = 32;
    public static final int SANCTUARY_REFRESH_INTERVAL_TICKS = 20;
    public static final int MIN_SANCTUARY_REFRESH_INTERVAL_TICKS = 5;
    public static final int MAX_PENDING_DEATH_CLEANUPS = 256;

    private NoeticSafetyCeilings() { }
}
