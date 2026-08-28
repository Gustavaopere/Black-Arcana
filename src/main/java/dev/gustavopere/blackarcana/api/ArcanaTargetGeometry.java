package dev.gustavopere.blackarcana.api;

/**
 * Additional server-owned geometry for target kinds that cannot be fully
 * described by maxRange alone. Values are hard-bounded independently of data
 * or progression so later scaling cannot escape technical safety ceilings.
 */
public sealed interface ArcanaTargetGeometry permits
        ArcanaTargetGeometry.None,
        ArcanaTargetGeometry.Cone,
        ArcanaTargetGeometry.Cylinder {

    static ArcanaTargetGeometry none() {
        return None.INSTANCE;
    }

    final class None implements ArcanaTargetGeometry {
        private static final None INSTANCE = new None();
        private None() { }
    }

    record Cone(double halfAngleDegrees) implements ArcanaTargetGeometry {
        public static final double ABSOLUTE_MAX_HALF_ANGLE_DEGREES = 180.0D;

        public Cone {
            if (!Double.isFinite(halfAngleDegrees)
                    || halfAngleDegrees <= 0.0D
                    || halfAngleDegrees > ABSOLUTE_MAX_HALF_ANGLE_DEGREES) {
                throw new IllegalArgumentException(
                        "halfAngleDegrees must be finite and in (0, "
                                + ABSOLUTE_MAX_HALF_ANGLE_DEGREES + "]");
            }
        }
    }

    record Cylinder(double radius, double halfHeight) implements ArcanaTargetGeometry {
        public Cylinder {
            if (!Double.isFinite(radius) || radius <= 0.0D || radius > ArcanaTargetSpec.ABSOLUTE_MAX_RANGE) {
                throw new IllegalArgumentException("cylinder radius outside absolute range bounds");
            }
            if (!Double.isFinite(halfHeight)
                    || halfHeight <= 0.0D
                    || halfHeight > ArcanaTargetSpec.ABSOLUTE_MAX_RANGE) {
                throw new IllegalArgumentException("cylinder halfHeight outside absolute range bounds");
            }
        }
    }
}
