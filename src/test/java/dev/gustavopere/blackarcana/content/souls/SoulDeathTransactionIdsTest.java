package dev.gustavopere.blackarcana.content.souls;

import org.junit.jupiter.api.Test;

import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

class SoulDeathTransactionIdsTest {
    @Test
    void playerAndServerTickProduceStableReplaySafeDeathIdentity() {
        UUID playerA = UUID.fromString("11111111-1111-1111-1111-111111111111");
        UUID playerB = UUID.fromString("22222222-2222-2222-2222-222222222222");

        UUID first = SoulDeathTransactionIds.forPlayerTick(playerA, 12_345L);
        assertEquals(first, SoulDeathTransactionIds.forPlayerTick(playerA, 12_345L),
            "replayed callback for the same player/tick must retain one death transaction id");
        assertNotEquals(first, SoulDeathTransactionIds.forPlayerTick(playerA, 12_346L),
            "a later eligible death tick must receive a new transaction id");
        assertNotEquals(first, SoulDeathTransactionIds.forPlayerTick(playerB, 12_345L),
            "different players must never share the same death transaction id");
        assertThrows(IllegalArgumentException.class,
            () -> SoulDeathTransactionIds.forPlayerTick(playerA, -1L));
    }
}
