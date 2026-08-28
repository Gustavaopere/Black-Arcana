package dev.gustavopere.blackarcana.integration.malum;

import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.core.ritual.ArcanaRitualId;
import dev.gustavopere.blackarcana.core.ritual.RitualAnchor;
import dev.gustavopere.blackarcana.core.ritual.RitualContext;
import dev.gustavopere.blackarcana.core.ritual.RitualDefinition;
import org.junit.jupiter.api.Test;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class MalumRitualSpiritComponentProviderTest {
    private static final ArcanaRitualId ID = ArcanaRitualId.parse("black_arcana:soul_rite");
    private static final RitualDefinition DEFINITION = new RitualDefinition(ID, 20L, 40L);
    private static final UUID CASTER = UUID.fromString("11111111-1111-1111-1111-111111111111");
    private static final RitualContext CONTEXT = new RitualContext(
            CASTER, List.of(), new RitualAnchor("minecraft:overworld", 42L));

    @Test
    void mixedSpiritRequirementConsumesExactCountsAndRefundsExactlyOnce() {
        FakeAccess access = new FakeAccess(Map.of("arcane", 5, "wicked", 4));
        MalumRitualSpiritComponentProvider provider = new MalumRitualSpiritComponentProvider(
                access,
                Map.of(ID, List.of(
                        new MalumRitualSpiritRequirement("arcane", 3),
                        new MalumRitualSpiritRequirement("wicked", 2))));

        assertTrue(provider.check(DEFINITION, CONTEXT, 100L).allowed());
        var reservation = provider.reserve(DEFINITION, CONTEXT, 120L);
        assertTrue(reservation.decision().allowed());
        assertEquals(2, access.count(CASTER, "arcane"));
        assertEquals(2, access.count(CASTER, "wicked"));

        reservation.refund();
        reservation.refund();
        assertEquals(5, access.count(CASTER, "arcane"));
        assertEquals(4, access.count(CASTER, "wicked"));
    }

    @Test
    void insufficientOneAffinityConsumesNothing() {
        FakeAccess access = new FakeAccess(Map.of("arcane", 5, "wicked", 1));
        MalumRitualSpiritComponentProvider provider = new MalumRitualSpiritComponentProvider(
                access,
                Map.of(ID, List.of(
                        new MalumRitualSpiritRequirement("arcane", 3),
                        new MalumRitualSpiritRequirement("wicked", 2))));

        ArcanaDecision check = provider.check(DEFINITION, CONTEXT, 100L);
        assertFalse(check.allowed());
        assertEquals("insufficient_malum_ritual_spirits", check.code());
        assertFalse(provider.reserve(DEFINITION, CONTEXT, 120L).decision().allowed());
        assertEquals(5, access.count(CASTER, "arcane"));
        assertEquals(1, access.count(CASTER, "wicked"));
    }

    @Test
    void missingRequirementDefinitionFailsClosed() {
        FakeAccess access = new FakeAccess(Map.of("arcane", 64));
        MalumRitualSpiritComponentProvider provider = new MalumRitualSpiritComponentProvider(access, Map.of());

        ArcanaDecision decision = provider.check(DEFINITION, CONTEXT, 100L);
        assertFalse(decision.allowed());
        assertEquals("malum_ritual_requirements_missing", decision.code());
    }

    private static final class FakeAccess implements MalumSpiritAccess {
        private final Map<String, Integer> counts = new HashMap<>();

        FakeAccess(Map<String, Integer> initial) {
            counts.putAll(initial);
        }

        @Override
        public int count(UUID playerId, String affinity) {
            return counts.getOrDefault(affinity, 0);
        }

        @Override
        public ArcanaDecision adjust(UUID playerId, String affinity, int delta) {
            int current = count(playerId, affinity);
            int next = current + delta;
            if (next < 0) return ArcanaDecision.deny("insufficient", "not enough spirits");
            counts.put(affinity, next);
            return ArcanaDecision.allow();
        }
    }
}
