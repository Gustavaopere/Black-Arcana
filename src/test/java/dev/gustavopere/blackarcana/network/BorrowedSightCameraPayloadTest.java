package dev.gustavopere.blackarcana.network;

import org.junit.jupiter.api.Test;

import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;

class BorrowedSightCameraPayloadTest {
    @Test
    void activePayloadCarriesOnlyBoundedAuthoritativeTargetIdentity() throws Exception {
        Class<?> type = payloadType();
        UUID target = UUID.randomUUID();
        Object payload = type.getMethod("start", int.class, UUID.class).invoke(null, 42, target);

        assertTrue((boolean) type.getMethod("active").invoke(payload));
        assertEquals(42, type.getMethod("entityId").invoke(payload));
        assertEquals(target, type.getMethod("targetId").invoke(payload));
    }

    @Test
    void resetPayloadContainsNoRemoteEntityIdentity() throws Exception {
        Class<?> type = payloadType();
        Object payload = type.getMethod("reset").invoke(null);

        assertFalse((boolean) type.getMethod("active").invoke(payload));
        assertEquals(-1, type.getMethod("entityId").invoke(payload));
        assertEquals(new UUID(0L, 0L), type.getMethod("targetId").invoke(payload));
    }

    @Test
    void invalidActiveEntityIdFailsClosed() throws Exception {
        Class<?> type = payloadType();
        Method start = type.getMethod("start", int.class, UUID.class);
        InvocationTargetException failure = assertThrows(
            InvocationTargetException.class,
            () -> start.invoke(null, -1, UUID.randomUUID()));
        assertInstanceOf(IllegalArgumentException.class, failure.getCause());
    }

    @Test
    void zeroUuidCannotAuthorizeActiveRemoteCamera() throws Exception {
        Class<?> type = payloadType();
        Method start = type.getMethod("start", int.class, UUID.class);
        InvocationTargetException failure = assertThrows(
            InvocationTargetException.class,
            () -> start.invoke(null, 7, new UUID(0L, 0L)));
        assertInstanceOf(IllegalArgumentException.class, failure.getCause());
    }

    private static Class<?> payloadType() throws ClassNotFoundException {
        return Class.forName("dev.gustavopere.blackarcana.network.BorrowedSightCameraPayload");
    }
}
