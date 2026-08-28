package dev.gustavopere.blackarcana.core.targeting;

import dev.gustavopere.blackarcana.api.ArcanaTargetGeometry;

/** Pure geometry predicates shared by the Minecraft targeting bridge and unit tests. */
public final class TargetGeometryMath {
    private static final double DOT_EPSILON = 1.0E-12D;

    private TargetGeometryMath() { }

    public static boolean withinCone(
            double facingX,
            double facingY,
            double facingZ,
            double deltaX,
            double deltaY,
            double deltaZ,
            ArcanaTargetGeometry.Cone cone
    ) {
        double facingLengthSquared = facingX * facingX + facingY * facingY + facingZ * facingZ;
        double deltaLengthSquared = deltaX * deltaX + deltaY * deltaY + deltaZ * deltaZ;
        if (facingLengthSquared == 0.0D || deltaLengthSquared == 0.0D) return false;

        double dot = facingX * deltaX + facingY * deltaY + facingZ * deltaZ;
        double normalizedDot = dot / Math.sqrt(facingLengthSquared * deltaLengthSquared);
        double minimumDot = Math.cos(Math.toRadians(cone.halfAngleDegrees()));
        return normalizedDot + DOT_EPSILON >= minimumDot;
    }

    public static boolean withinCylinder(
            double deltaX,
            double deltaY,
            double deltaZ,
            ArcanaTargetGeometry.Cylinder cylinder
    ) {
        if (Math.abs(deltaY) > cylinder.halfHeight()) return false;
        double horizontalSquared = deltaX * deltaX + deltaZ * deltaZ;
        return horizontalSquared <= cylinder.radius() * cylinder.radius();
    }
}
