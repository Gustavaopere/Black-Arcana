package dev.gustavopere.blackarcana.core.world;

/** Hard upper bounds returned by entity protection policy for the effect implementation to obey. */
public record EntityEffectLimits(
    int maxControlTicks,
    double maxDisplacementBlocks,
    double damageMultiplierCap,
    boolean executionAllowed,
    boolean resurrectionDenialAllowed,
    boolean domainCaptureAllowed
) {
    public static final int ABSOLUTE_MAX_CONTROL_TICKS = 1_200;
    public static final double ABSOLUTE_MAX_DISPLACEMENT_BLOCKS = 128.0;
    public static final double ABSOLUTE_MAX_DAMAGE_MULTIPLIER = 4.0;

    public EntityEffectLimits {
        if (maxControlTicks < 0 || maxControlTicks > ABSOLUTE_MAX_CONTROL_TICKS) {
            throw new IllegalArgumentException("maxControlTicks outside absolute bounds");
        }
        if (!Double.isFinite(maxDisplacementBlocks) || maxDisplacementBlocks < 0
            || maxDisplacementBlocks > ABSOLUTE_MAX_DISPLACEMENT_BLOCKS) {
            throw new IllegalArgumentException("maxDisplacementBlocks outside absolute bounds");
        }
        if (!Double.isFinite(damageMultiplierCap) || damageMultiplierCap < 0
            || damageMultiplierCap > ABSOLUTE_MAX_DAMAGE_MULTIPLIER) {
            throw new IllegalArgumentException("damageMultiplierCap outside absolute bounds");
        }
    }

    public static EntityEffectLimits standard() {
        return new EntityEffectLimits(200, 32.0, 2.0, true, true, true);
    }

    public static EntityEffectLimits bossSafeDefaults() {
        return new EntityEffectLimits(40, 4.0, 1.0, false, false, false);
    }
}
