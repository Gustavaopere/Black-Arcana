package dev.gustavopere.blackarcana.content.souls;

import java.nio.charset.StandardCharsets;
import java.util.Objects;
import java.util.UUID;

/** Stable identity for one player's death transaction at an authoritative server tick. */
public final class SoulDeathTransactionIds {
    private static final String PREFIX = "black_arcana:soul_anchor_death:";

    private SoulDeathTransactionIds() { }

    public static UUID forPlayerTick(UUID playerId, long serverTick) {
        Objects.requireNonNull(playerId, "playerId");
        if (serverTick < 0L) throw new IllegalArgumentException("serverTick cannot be negative");
        String canonical = PREFIX + playerId + ':' + serverTick;
        return UUID.nameUUIDFromBytes(canonical.getBytes(StandardCharsets.UTF_8));
    }
}
