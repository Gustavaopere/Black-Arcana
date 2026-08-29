package dev.gustavopere.blackarcana.content.blood;

/** Hard technical ceilings frozen by docs/design/server-safety-ceilings.md. */
public final class BloodSafetyCeilings {
    private BloodSafetyCeilings() { }

    public static final int MAX_HARVEST_TARGETS = 64;
    public static final double MAX_BLOOD_PRICE_FRACTION = 0.50D;
    public static final double MIN_BLOOD_PRICE_REMAINING_HEALTH = 1.0D;
    public static final double MAX_SYMPATHETIC_MIRROR_FRACTION = 0.50D;
    public static final double MAX_SYMPATHETIC_DAMAGE_PER_EVENT = 40.0D;
    public static final double MAX_SYMPATHETIC_LIFETIME_BUDGET = 200.0D;
    public static final double MAX_EQUILIBRIUM_TRANSFER = 40.0D;
}
