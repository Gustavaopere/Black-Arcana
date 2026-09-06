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
    public static final int MAX_SANCTUARY_RADIUS = 16;
    public static final int MAX_SANCTUARY_DURATION_TICKS = 600;
    public static final int MAX_SANCTUARY_MEMBERS = 8;
    public static final int MAX_ACTIVE_SANCTUARIES = 32;
    public static final int MAX_SANCTUARY_MOBS_PER_TICK = 32;

    private NoeticSafetyCeilings() { }
}
