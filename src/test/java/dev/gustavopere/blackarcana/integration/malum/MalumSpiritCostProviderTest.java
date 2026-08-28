package dev.gustavopere.blackarcana.integration.malum;

import dev.gustavopere.blackarcana.api.ArcanaCastContext;
import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaCost;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaServices.CostReservation;
import dev.gustavopere.blackarcana.api.ArcanaSpellDefinition;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import org.junit.jupiter.api.Test;

import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class MalumSpiritCostProviderTest {
    private static final UUID CASTER = UUID.fromString("12121212-1212-1212-1212-121212121212");

    @Test
    void reservesCommitsAndRefundsDiscreteAffinity() {
        FakeSpirits access = new FakeSpirits(Map.of("arcane", 5));
        MalumSpiritCostProvider provider = new MalumSpiritCostProvider(access);

        CostReservation first = provider.reserve(request(new ArcanaCost("malum:spirit/arcane", 2)));
        assertTrue(first.reserved());
        assertEquals(3, access.count(CASTER, "arcane"));
        first.refund();
        assertEquals(5, access.count(CASTER, "arcane"));
        first.refund();
        assertEquals(5, access.count(CASTER, "arcane"));

        CostReservation second = provider.reserve(request(new ArcanaCost("malum:spirit/arcane", 2)));
        second.commit();
        second.refund();
        assertEquals(3, access.count(CASTER, "arcane"));
    }

    @Test
    void rejectsInsufficientFractionalPercentAndOversizedCosts() {
        FakeSpirits access = new FakeSpirits(Map.of("arcane", 1));
        MalumSpiritCostProvider provider = new MalumSpiritCostProvider(access);

        assertFalse(provider.check(request(new ArcanaCost("malum:spirit/arcane", 2))).allowed());
        assertFalse(provider.check(request(new ArcanaCost("malum:spirit/arcane", 1.5))).allowed());
        assertFalse(provider.check(request(ArcanaCost.percentOfMax("malum:spirit/arcane", 0.5))).allowed());
        assertFalse(provider.check(request(new ArcanaCost("malum:spirit/arcane", 65))).allowed());
    }

    @Test
    void parserRejectsNonMalumResource() {
        assertThrows(
            IllegalArgumentException.class,
            () -> MalumSpiritCostProvider.parse(new ArcanaCost("black_arcana:mana", 1)));
    }

    private static ArcanaCastRequest request(ArcanaCost cost) {
        return new ArcanaCastRequest(
            ArcanaCastId.parse("13131313-1313-1313-1313-131313131313"),
            new ArcanaSpellDefinition(
                ArcanaSpellId.parse("black_arcana:test_malum_cost"),
                "spell.black_arcana.test_malum_cost",
                "black_arcana:textures/gui/spell_icons/test.png",
                cost,
                false),
            new ArcanaCastContext(CASTER, 20L, "minecraft:overworld"));
    }

    private static final class FakeSpirits implements MalumSpiritAccess {
        private final Map<String, Integer> counts = new HashMap<>();

        private FakeSpirits(Map<String, Integer> initial) {
            counts.putAll(initial);
        }

        @Override
        public int count(UUID playerId, String affinity) {
            assertEquals(CASTER, playerId);
            return counts.getOrDefault(affinity, 0);
        }

        @Override
        public ArcanaDecision adjust(UUID playerId, String affinity, int delta) {
            assertEquals(CASTER, playerId);
            int next = counts.getOrDefault(affinity, 0) + delta;
            if (next < 0) return ArcanaDecision.deny("fake_spirit_bounds", "negative count");
            counts.put(affinity, next);
            return ArcanaDecision.allow();
        }
    }
}
