package dev.gustavopere.blackarcana.network;

import java.util.Objects;
import java.util.UUID;

/** Client presentation command for Borrowed Sight. Carries identity only, never gameplay authority. */
public record BorrowedSightCameraPayload(boolean active, int entityId, UUID targetId) {
    private static final UUID NO_TARGET = new UUID(0L, 0L);

    public BorrowedSightCameraPayload {
        Objects.requireNonNull(targetId, "targetId");
        if (active) {
            if (entityId < 0) throw new IllegalArgumentException("active Borrowed Sight camera requires an entity id");
            if (NO_TARGET.equals(targetId)) throw new IllegalArgumentException("active Borrowed Sight camera requires a target UUID");
        } else {
            if (entityId != -1 || !NO_TARGET.equals(targetId)) {
                throw new IllegalArgumentException("inactive Borrowed Sight camera must not carry remote target identity");
            }
        }
    }

    public static BorrowedSightCameraPayload start(int entityId, UUID targetId) {
        return new BorrowedSightCameraPayload(true, entityId, Objects.requireNonNull(targetId, "targetId"));
    }

    public static BorrowedSightCameraPayload reset() {
        return new BorrowedSightCameraPayload(false, -1, NO_TARGET);
    }
}
