package dev.gustavopere.blackarcana.content.forbidden;

import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.Map;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;

class InnerDominionSessionJournalTest {
    private static InnerDominionSessionJournal.ReturnRoute route() {
        return new InnerDominionSessionJournal.ReturnRoute(
            new DomainReturnPoint("minecraft:overworld", 0, 64, 0),
            new DomainReturnPoint("minecraft:overworld", 0, 80, 0));
    }

    @Test void nestedParticipationIsDeniedAndCloseReleasesParticipants() {
        var journal = new InnerDominionSessionJournal(2, 4, 200);
        UUID owner = UUID.randomUUID(); UUID guest = UUID.randomUUID(); UUID first = UUID.randomUUID();
        assertEquals(InnerDominionSessionJournal.OpenResult.OPENED, journal.open(first, owner, 10, 100, Map.of(owner, route(), guest, route())));
        assertEquals(InnerDominionSessionJournal.OpenResult.NESTED_PARTICIPANT, journal.open(UUID.randomUUID(), guest, 11, 100, Map.of(guest, route())));
        assertTrue(journal.close(first).isPresent());
        assertFalse(journal.participantActive(guest));
    }

    @Test void restoreDropsExpiredAndOverlappingSessions() {
        UUID owner = UUID.randomUUID(); UUID guest = UUID.randomUUID(); UUID expiredOwner = UUID.randomUUID();
        var valid = new InnerDominionSessionJournal.Session(UUID.randomUUID(), owner, 100, Map.of(owner, route(), guest, route()));
        var overlap = new InnerDominionSessionJournal.Session(UUID.randomUUID(), guest, 120, Map.of(guest, route()));
        var expired = new InnerDominionSessionJournal.Session(UUID.randomUUID(), expiredOwner, 5, Map.of(expiredOwner, route()));
        var journal = new InnerDominionSessionJournal(3, 4, 200);
        assertEquals(1, journal.restore(List.of(expired, valid, overlap), 10));
        assertEquals(1, journal.activeSessions());
    }

    @Test void returnSelectionUsesSafeFallbackAndNeverInventsDestination() {
        var origin = new DomainReturnPoint("minecraft:overworld", 1, 64, 1);
        var fallback = new DomainReturnPoint("minecraft:overworld", 0, 80, 0);
        assertEquals(fallback, DomainReturnSelector.choose(origin, fallback, point -> point.equals(fallback)).orElseThrow());
        assertTrue(DomainReturnSelector.choose(origin, fallback, point -> false).isEmpty());
    }
}
