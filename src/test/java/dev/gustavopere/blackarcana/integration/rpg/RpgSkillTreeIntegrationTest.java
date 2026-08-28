package dev.gustavopere.blackarcana.integration.rpg;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;

import dev.gustavopere.blackarcana.api.ArcanaCastContext;
import dev.gustavopere.blackarcana.api.ArcanaCastEngine;
import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaCastResult;
import dev.gustavopere.blackarcana.api.ArcanaCost;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaIntegrationAvailability;
import dev.gustavopere.blackarcana.api.ArcanaIntegrationCapability;
import dev.gustavopere.blackarcana.api.ArcanaServices;
import dev.gustavopere.blackarcana.api.ArcanaSpellDefinition;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import java.util.HashSet;
import java.util.Map;
import java.util.Optional;
import java.util.Set;
import java.util.UUID;
import java.util.concurrent.atomic.AtomicInteger;
import org.junit.jupiter.api.Test;

class RpgSkillTreeIntegrationTest {
    @Test
    void requirementChecksCanonicalAttributeAndMasteryProjection() {
        FakeBridge bridge = new FakeBridge(new RpgProgressionSnapshot(
            20L,
            Map.of("intelligence", 12L),
            Map.of("fire", 250)));
        RpgSkillTreeProgressionGate gate = new RpgSkillTreeProgressionGate(
            bridge,
            new RpgProgressionRequirement(
                10L,
                Map.of("intelligence", 10L),
                Map.of("fire", 200)));

        assertEquals("ok", gate.check(request()).code());

        RpgSkillTreeProgressionGate tooHigh = new RpgSkillTreeProgressionGate(
            bridge,
            new RpgProgressionRequirement(
                10L,
                Map.of("intelligence", 15L),
                Map.of("fire", 200)));
        var denied = tooHigh.check(request());
        assertFalse(denied.allowed());
        assertEquals("rpg_attribute_too_low", denied.code());
    }

    @Test
    void successfulCastAwardsOnceAndReplayAwardsNothing() {
        FakeBridge bridge = new FakeBridge(new RpgProgressionSnapshot(20L, Map.of(), Map.of()));
        Set<ArcanaCastId> seen = new HashSet<>();
        ArcanaCastEngine engine = new ArcanaCastEngine(
            req -> ArcanaDecision.allow(),
            req -> seen.add(req.castId())
                ? ArcanaDecision.allow()
                : ArcanaDecision.deny("replay", "duplicate"),
            new RpgSkillTreeProgressionGate(bridge, RpgProgressionRequirement.none()),
            noCooldown(),
            req -> ArcanaServices.TargetResolution.resolved("target"),
            noCost(),
            (req, target) -> ArcanaDecision.allow(),
            (req, target) -> ArcanaServices.EffectResult.ok(),
            new RpgMasteryAwardObserver(
                bridge,
                req -> Optional.of(new RpgMasteryAwardSpec(
                    "black_arcana",
                    25,
                    req.spell().id().canonical()))));

        ArcanaCastRequest request = request();
        assertEquals(ArcanaCastResult.Status.SUCCESS, engine.execute(request).status());
        assertEquals(ArcanaCastResult.Status.DENIED_REPLAY, engine.execute(request).status());
        assertEquals(1, bridge.awards.get());
        assertEquals(25, bridge.lastAward.experience());
    }

    private static ArcanaServices.CooldownService noCooldown() {
        return new ArcanaServices.CooldownService() {
            @Override public ArcanaDecision check(ArcanaCastRequest request) { return ArcanaDecision.allow(); }
            @Override public void start(ArcanaCastRequest request) { }
        };
    }

    private static ArcanaServices.CostProvider noCost() {
        return new ArcanaServices.CostProvider() {
            @Override public ArcanaDecision check(ArcanaCastRequest request) { return ArcanaDecision.allow(); }
            @Override public ArcanaServices.CostReservation reserve(ArcanaCastRequest request) {
                return new ArcanaServices.CostReservation() {
                    @Override public ArcanaDecision decision() { return ArcanaDecision.allow(); }
                    @Override public void commit() { }
                    @Override public void refund() { }
                };
            }
        };
    }

    private static ArcanaCastRequest request() {
        ArcanaSpellDefinition spell = new ArcanaSpellDefinition(
            ArcanaSpellId.parse("black_arcana:rpg_test"),
            "spell.black_arcana.rpg_test",
            "black_arcana:textures/spell/rpg_test.png",
            ArcanaCost.none(),
            false);
        return new ArcanaCastRequest(
            ArcanaCastId.parse("22222222-2222-2222-2222-222222222222"),
            spell,
            new ArcanaCastContext(
                UUID.fromString("33333333-3333-3333-3333-333333333333"),
                40L,
                "minecraft:overworld"));
    }

    private static final class FakeBridge implements RpgSkillTreeBridge {
        private final RpgProgressionSnapshot snapshot;
        private final AtomicInteger awards = new AtomicInteger();
        private RpgMasteryAwardSpec lastAward;

        private FakeBridge(RpgProgressionSnapshot snapshot) {
            this.snapshot = snapshot;
        }

        @Override public String integrationId() { return MOD_ID; }
        @Override public boolean available() { return true; }
        @Override public String implementationVersion() { return "test"; }
        @Override public ArcanaIntegrationAvailability availability() { return ArcanaIntegrationAvailability.AVAILABLE; }
        @Override public Set<ArcanaIntegrationCapability> capabilities() {
            return Set.of(
                ArcanaIntegrationCapability.PROGRESSION_QUERY,
                ArcanaIntegrationCapability.MASTERY_AWARD);
        }
        @Override public RpgProgressionQuery query(UUID playerId) {
            return RpgProgressionQuery.success(snapshot);
        }
        @Override public ArcanaDecision awardMastery(UUID playerId, RpgMasteryAwardSpec award) {
            awards.incrementAndGet();
            lastAward = award;
            return ArcanaDecision.allow();
        }
    }
}
