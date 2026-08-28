package dev.gustavopere.blackarcana.core.targeting;

import dev.gustavopere.blackarcana.api.ArcanaTargetGeometry;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class TargetGeometryMathTest {
    @Test
    void coneAcceptsInsideAndBoundaryDirectionsButRejectsOutsideAndZeroVectors() {
        ArcanaTargetGeometry.Cone cone = new ArcanaTargetGeometry.Cone(60.0D);

        assertTrue(TargetGeometryMath.withinCone(1, 0, 0, 1, 0, 0, cone));
        assertTrue(TargetGeometryMath.withinCone(1, 0, 0, 0.5D, 0, Math.sqrt(3.0D) / 2.0D, cone));
        assertFalse(TargetGeometryMath.withinCone(1, 0, 0, 0, 0, 1, cone));
        assertFalse(TargetGeometryMath.withinCone(0, 0, 0, 1, 0, 0, cone));
        assertFalse(TargetGeometryMath.withinCone(1, 0, 0, 0, 0, 0, cone));
    }

    @Test
    void cylinderHonorsHorizontalRadiusAndVerticalHalfHeightInclusively() {
        ArcanaTargetGeometry.Cylinder cylinder = new ArcanaTargetGeometry.Cylinder(4.0D, 3.0D);

        assertTrue(TargetGeometryMath.withinCylinder(4.0D, 0.0D, 0.0D, cylinder));
        assertTrue(TargetGeometryMath.withinCylinder(0.0D, 3.0D, 0.0D, cylinder));
        assertFalse(TargetGeometryMath.withinCylinder(4.01D, 0.0D, 0.0D, cylinder));
        assertFalse(TargetGeometryMath.withinCylinder(0.0D, 3.01D, 0.0D, cylinder));
    }

    @Test
    void geometryContractsRejectNonFiniteOrOutOfBoundsValues() {
        assertThrows(IllegalArgumentException.class, () -> new ArcanaTargetGeometry.Cone(Double.NaN));
        assertThrows(IllegalArgumentException.class, () -> new ArcanaTargetGeometry.Cone(0.0D));
        assertThrows(IllegalArgumentException.class, () -> new ArcanaTargetGeometry.Cone(180.01D));
        assertThrows(IllegalArgumentException.class, () -> new ArcanaTargetGeometry.Cylinder(0.0D, 1.0D));
        assertThrows(IllegalArgumentException.class, () -> new ArcanaTargetGeometry.Cylinder(1.0D, Double.POSITIVE_INFINITY));
    }
}
