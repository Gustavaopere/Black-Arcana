package dev.gustavopere.blackarcana.client;

import org.junit.jupiter.api.Test;

import java.lang.reflect.Method;
import java.util.Arrays;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class RadialToggleInputTest {
    @Test
    void toggleOpenKeyRequestsCloseButHoldReleaseRemainsSeparate() throws Exception {
        Method policy = Arrays.stream(BlackArcanaRadialScreen.class.getDeclaredMethods())
                .filter(method -> method.getName().equals("shouldCloseFromOpenKey"))
                .findFirst()
                .orElseThrow(() -> new AssertionError(
                        "radial screen has no same-key TOGGLE close policy"));
        policy.setAccessible(true);

        assertTrue((boolean) policy.invoke(
                null, BlackArcanaClientConfig.RadialBehavior.TOGGLE, true));
        assertFalse((boolean) policy.invoke(
                null, BlackArcanaClientConfig.RadialBehavior.HOLD, true));
        assertFalse((boolean) policy.invoke(
                null, BlackArcanaClientConfig.RadialBehavior.TOGGLE, false));
    }
}
