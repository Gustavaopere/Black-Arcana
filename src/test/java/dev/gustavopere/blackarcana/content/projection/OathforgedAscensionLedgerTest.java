package dev.gustavopere.blackarcana.content.projection;

import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class OathforgedAscensionLedgerTest {
    private static final AscensionPointAllocator.Policy POLICY =
        new AscensionPointAllocator.Policy(10.0D, 0.5D, ProjectionSafetyCeilings.MAX_ASCENSION_POINTS);

    @Test
    void validBatchSettlesOnceUsingAggregateDiminishingReturnCurve() {
        var ledger = new OathforgedAscensionLedger(8, 64, 8);
        var track = new OathforgedAscensionLedger.TrackKey("weapon:alpha", "black_arcana:edge");
        var first = token(40.0D, false);
        var second = token(120.0D, false);

        var result = ledger.settle(track, List.of(first, second), POLICY, 12);

        assertTrue(result.accepted());
        assertEquals(4, result.awardedPoints(), "aggregate eligible value 160 must use the existing sqrt-style diminishing curve once");
        assertEquals(4, result.totalTrackPoints());
        assertEquals(4, ledger.points(track));
        assertTrue(ledger.consumed(first.sacrificeId()));
        assertTrue(ledger.consumed(second.sacrificeId()));

        var replay = ledger.settle(track, List.of(first), POLICY, 12);
        assertFalse(replay.accepted());
        assertEquals("sacrifice_already_consumed", replay.denialCode());
        assertEquals(4, ledger.points(track), "replayed sacrifice must never mint additional points");
    }

    @Test
    void recursiveOrDuplicateInputRollsBackEntireBatch() {
        var ledger = new OathforgedAscensionLedger(8, 64, 8);
        var track = new OathforgedAscensionLedger.TrackKey("weapon:beta", "black_arcana:guard");
        var clean = token(40.0D, false);
        var recursive = token(120.0D, true);

        var recursiveResult = ledger.settle(track, List.of(clean, recursive), POLICY, 12);
        assertFalse(recursiveResult.accepted());
        assertEquals("recursive_input", recursiveResult.denialCode());
        assertEquals(0, ledger.points(track));
        assertFalse(ledger.consumed(clean.sacrificeId()), "clean sibling must roll back when any batch input is recursive");
        assertFalse(ledger.consumed(recursive.sacrificeId()));

        var duplicate = token(160.0D, false);
        var duplicateResult = ledger.settle(track, List.of(duplicate, duplicate), POLICY, 12);
        assertFalse(duplicateResult.accepted());
        assertEquals("duplicate_sacrifice", duplicateResult.denialCode());
        assertEquals(0, ledger.points(track));
        assertFalse(ledger.consumed(duplicate.sacrificeId()), "duplicate-ID rejection must occur before any consumption marker is committed");
    }

    @Test
    void hardTrackCapClampsFinalAwardAndDenialsConsumeNothing() {
        var ledger = new OathforgedAscensionLedger(8, 64, 8);
        var track = new OathforgedAscensionLedger.TrackKey("weapon:gamma", "black_arcana:edge");
        var first = token(160.0D, false);
        var second = token(160.0D, false);
        var rejected = token(160.0D, false);

        var initial = ledger.settle(track, List.of(first), POLICY, 5);
        assertTrue(initial.accepted());
        assertEquals(4, initial.awardedPoints());

        var capped = ledger.settle(track, List.of(second), POLICY, 5);
        assertTrue(capped.accepted());
        assertEquals(1, capped.awardedPoints(), "the final rite must clamp to the remaining hard track capacity");
        assertEquals(5, capped.totalTrackPoints());

        var full = ledger.settle(track, List.of(rejected), POLICY, 5);
        assertFalse(full.accepted());
        assertEquals("track_cap", full.denialCode());
        assertEquals(5, ledger.points(track));
        assertFalse(ledger.consumed(rejected.sacrificeId()), "a rite denied by a full track must not consume its inputs");

        assertThrows(IllegalArgumentException.class,
            () -> ledger.settle(track, List.of(token(40.0D, false)), POLICY,
                ProjectionSafetyCeilings.MAX_ASCENSION_POINTS + 1));
    }

    @Test
    void configuredLedgerCapacitiesFailClosedWithoutPartialMutation() {
        var ledger = new OathforgedAscensionLedger(1, 2, 2);
        var firstTrack = new OathforgedAscensionLedger.TrackKey("weapon:one", "black_arcana:edge");
        var secondTrack = new OathforgedAscensionLedger.TrackKey("weapon:two", "black_arcana:edge");
        var first = token(40.0D, false);
        assertTrue(ledger.settle(firstTrack, List.of(first), POLICY, 20).accepted());

        var other = token(40.0D, false);
        var trackCapacity = ledger.settle(secondTrack, List.of(other), POLICY, 20);
        assertFalse(trackCapacity.accepted());
        assertEquals("track_capacity", trackCapacity.denialCode());
        assertFalse(ledger.consumed(other.sacrificeId()));

        var second = token(40.0D, false);
        var third = token(40.0D, false);
        var sacrificeCapacity = ledger.settle(firstTrack, List.of(second, third), POLICY, 20);
        assertFalse(sacrificeCapacity.accepted());
        assertEquals("sacrifice_capacity", sacrificeCapacity.denialCode());
        assertFalse(ledger.consumed(second.sacrificeId()));
        assertFalse(ledger.consumed(third.sacrificeId()));
        assertEquals(2, ledger.points(firstTrack), "capacity denial must leave the prior committed track state unchanged");
    }

    private static OathforgedAscensionLedger.SacrificeToken token(double eligibleValue, boolean recursive) {
        return new OathforgedAscensionLedger.SacrificeToken(UUID.randomUUID(), eligibleValue, recursive);
    }
}
