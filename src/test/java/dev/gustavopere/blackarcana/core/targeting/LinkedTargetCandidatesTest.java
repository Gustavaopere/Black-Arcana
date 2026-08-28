package dev.gustavopere.blackarcana.core.targeting;

import org.junit.jupiter.api.Test;

import java.util.Arrays;
import java.util.List;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class LinkedTargetCandidatesTest {
    private static final UUID A = UUID.fromString("11111111-1111-1111-1111-111111111111");
    private static final UUID B = UUID.fromString("22222222-2222-2222-2222-222222222222");

    @Test
    void deduplicatesInStableServerOrder() {
        var result = LinkedTargetCandidates.normalize(List.of(A, B, A), 4);
        assertTrue(result.valid());
        assertEquals(List.of(A, B), result.uniqueIds());
    }

    @Test
    void nullListAndNullIdsFailClosedWithStructuredDetail() {
        var nullList = LinkedTargetCandidates.normalize(null, 4);
        assertFalse(nullList.valid());
        assertEquals("linked target resolver returned null list", nullList.detail());

        var nullId = LinkedTargetCandidates.normalize(Arrays.asList(A, null), 4);
        assertFalse(nullId.valid());
        assertEquals("linked target resolver returned null id", nullId.detail());
    }

    @Test
    void candidateCountIsBoundedBeforeDeduplication() {
        var result = LinkedTargetCandidates.normalize(List.of(A, A, A), 2);
        assertFalse(result.valid());
        assertEquals("linked target candidate set exceeds hard bound", result.detail());
    }
}
