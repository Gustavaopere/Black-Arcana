package dev.gustavopere.blackarcana.integration.rpg;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDangerProfile;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDangerTier;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceQuery;
import dev.gustavopere.blackarcana.api.hazard.CorruptionResistanceQuery;
import org.junit.jupiter.api.Test;

import java.util.Map;
import java.util.UUID;
import java.util.concurrent.atomic.AtomicInteger;

import static org.junit.jupiter.api.Assertions.assertEquals;

class RpgHazardResistanceProviderTest {
    @Test
    void configuredAttributesContributeWithoutReadingMastery() {
        UUID player = UUID.randomUUID();
        StubBridge bridge = new StubBridge(true, new RpgProgressionSnapshot(
            50L,
            Map.of("determination", 20L, "intelligence", 8L, "constitution", 30L),
            Map.of("black_arcana:casting", 999_999)));
        RpgHazardResistanceProvider provider = new RpgHazardResistanceProvider(
            bridge,
            RpgHazardResistanceConfig.canonical());

        assertEquals(22.0D, provider.contributions(arcaneQuery(player)).getFirst().amount());
        assertEquals(35.0D, provider.contributions(corruptionQuery(player)).getFirst().amount());
        assertEquals(0, bridge.masteryAwards);
    }

    @Test
    void hazardResistanceUsesDedicatedReadOnlyProgressionQuery() {
        UUID player = UUID.randomUUID();
        AtomicInteger genericQueries = new AtomicInteger();
        AtomicInteger hazardQueries = new AtomicInteger();
        RpgSkillTreeBridge bridge = new RpgSkillTreeBridge() {
            @Override public String integrationId() { return MOD_ID; }
            @Override public boolean available() { return true; }
            @Override public String implementationVersion() { return "test"; }

            @Override
            public RpgProgressionQuery queryHazardProgression(UUID playerId) {
                hazardQueries.incrementAndGet();
                return RpgProgressionQuery.success(new RpgProgressionSnapshot(
                    10L,
                    Map.of("determination", 12L),
                    Map.of()));
            }

            @Override
            public RpgProgressionQuery query(UUID playerId) {
                genericQueries.incrementAndGet();
                return RpgProgressionQuery.denied(
                    "generic_query_forbidden",
                    "hazard resistance must not query mastery or mutating progression state");
            }

            @Override
            public ArcanaDecision awardMastery(UUID playerId, RpgMasteryAwardSpec award) {
                return ArcanaDecision.deny("not_required", "hazard fixture");
            }
        };
        RpgHazardResistanceProvider provider = new RpgHazardResistanceProvider(
            bridge,
            RpgHazardResistanceConfig.canonical());

        assertEquals(12.0D, provider.contributions(arcaneQuery(player)).getFirst().amount());
        assertEquals(1, hazardQueries.get());
        assertEquals(0, genericQueries.get());
    }

    @Test
    void unavailableOrFailedBridgeContributesZero() {
        UUID player = UUID.randomUUID();
        RpgHazardResistanceProvider unavailable = new RpgHazardResistanceProvider(
            new StubBridge(false, null), RpgHazardResistanceConfig.canonical());
        assertEquals(0, unavailable.contributions(arcaneQuery(player)).size());

        RpgHazardResistanceProvider denied = new RpgHazardResistanceProvider(
            new StubBridge(true, null), RpgHazardResistanceConfig.canonical());
        assertEquals(0, denied.contributions(corruptionQuery(player)).size());
    }

    @Test
    void contributionIsCappedBeforeEnteringPublicRegistry() {
        UUID player = UUID.randomUUID();
        StubBridge bridge = new StubBridge(true, new RpgProgressionSnapshot(
            1L, Map.of("determination", Long.MAX_VALUE, "intelligence", Long.MAX_VALUE), Map.of()));
        RpgHazardResistanceConfig config = new RpgHazardResistanceConfig(
            Map.of("determination", 100.0D, "intelligence", 100.0D), Map.of(), 50.0D, 0.0D);
        RpgHazardResistanceProvider provider = new RpgHazardResistanceProvider(bridge, config);
        assertEquals(50.0D, provider.contributions(arcaneQuery(player)).getFirst().amount());
    }

    private static ArcaneResistanceQuery arcaneQuery(UUID player) {
        return new ArcaneResistanceQuery(
            ArcanaCastId.random(), ArcanaSpellId.parse("black_arcana:test"), player,
            "minecraft:overworld", 100L, dangerous());
    }

    private static CorruptionResistanceQuery corruptionQuery(UUID player) {
        return new CorruptionResistanceQuery(
            ArcanaCastId.random(), ArcanaSpellId.parse("black_arcana:test"), player,
            "minecraft:overworld", 100L, dangerous());
    }

    private static ArcaneDangerProfile dangerous() {
        return new ArcaneDangerProfile(ArcaneDangerTier.DANGEROUS, 1.0D, 1.0D, 1.0D, 100L, 8);
    }

    private static final class StubBridge implements RpgSkillTreeBridge {
        private final boolean available;
        private final RpgProgressionSnapshot snapshot;
        private int masteryAwards;
        private StubBridge(boolean available, RpgProgressionSnapshot snapshot) {
            this.available = available;
            this.snapshot = snapshot;
        }
        @Override public String integrationId() { return MOD_ID; }
        @Override public boolean available() { return available; }
        @Override public String implementationVersion() { return "test"; }
        @Override public RpgProgressionQuery queryHazardProgression(UUID playerId) {
            return snapshot == null
                ? RpgProgressionQuery.denied("test_denied", "synthetic denial")
                : RpgProgressionQuery.success(snapshot);
        }
        @Override public RpgProgressionQuery query(UUID playerId) {
            return snapshot == null
                ? RpgProgressionQuery.denied("test_denied", "synthetic denial")
                : RpgProgressionQuery.success(snapshot);
        }
        @Override public ArcanaDecision awardMastery(UUID playerId, RpgMasteryAwardSpec award) {
            masteryAwards++;
            return ArcanaDecision.allow();
        }
    }
}
