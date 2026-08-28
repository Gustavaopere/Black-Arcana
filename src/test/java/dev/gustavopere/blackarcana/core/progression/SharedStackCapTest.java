package dev.gustavopere.blackarcana.core.progression;

import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class SharedStackCapTest {
    @Test void multipleSourcesCannotCrossSharedCap() {
        var cap = new SharedStackCap(2D);
        assertEquals(2D, cap.combine(List.of(0.75D, 0.75D, 100D)));
        assertEquals(1.5D, cap.combine(List.of(0.75D, 0.75D)));
    }
}
