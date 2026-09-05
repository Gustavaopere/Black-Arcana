package dev.gustavopere.blackarcana.content.space;

import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;

class VeilstepCandidateSelectorTest {
    @Test
    void picksFirstSafeServerCandidateWithoutExpandingSearch() {
        var selector = new VeilstepCandidateSelector(new SafeDestinationPolicy());
        var blocked = new VeilstepCandidateSelector.Candidate("one",
            new SafeDestinationPolicy.Facts(true, true, false, true, true, true, true, false));
        var safe = new VeilstepCandidateSelector.Candidate("two", SafeDestinationPolicyTest.valid());
        assertEquals("two", selector.select(List.of(blocked, safe)).orElseThrow().destinationId());
    }
}
