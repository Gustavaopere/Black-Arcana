package dev.gustavopere.blackarcana.content.forbidden;

/** Hard safety ceilings for Stage 07.06. Ordinary balance may only tune downward. */
public final class ForbiddenDomainSafetyCeilings {
    public static final int MAX_RADIUS = 24;
    public static final int MAX_DURATION_TICKS = 1_200;
    public static final int MAX_TRACKED_ENTITIES = 64;
    public static final int MAX_ACTIVE_DOMAINS = 8;
    public static final int MAX_RESTORATION_POSITIONS = 512;

    private ForbiddenDomainSafetyCeilings() {}
}
