package dev.gustavopere.blackarcana.integration.rpg;

import dev.gustavopere.blackarcana.api.ArcanaCastContext;
import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaCost;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaIntegrationAvailability;
import dev.gustavopere.blackarcana.api.ArcanaIntegrationCapability;
import dev.gustavopere.blackarcana.api.ArcanaServices;
import dev.gustavopere.blackarcana.api.ArcanaSpellDefinition;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.api.hazard.ArcanaDamageInstanceId;
import dev.gustavopere.blackarcana.api.hazard.ArcanaDamageProvenance;
import dev.gustavopere.blackarcana.api.hazard.ArcaneBacklashPolicy;
import dev.gustavopere.blackarcana.api.hazard.ArcaneBacklashSnapshot;
import dev.gustavopere.blackarcana.api.hazard.ArcaneConfirmedDamage;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDamageFamily;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDangerProfile;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDangerTier;
import dev.gustavopere.blackarcana.api.hazard.ArcaneHazardSnapshot;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceSnapshot;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceSourceCategory;
import dev.gustavopere.blackarcana.core.hazard.ArcaneBacklashLedger;
import dev.gustavopere.blackarcana.core.hazard.ArcaneHazardSession;
import org.junit.jupiter.api.Test;

import java.util.EnumMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.Set;
import java.util.UUID;
import java.util.concurrent.atomic.AtomicInteger;

import static org.junit.jupiter.api.Assertions.assertEquals;

class RpgMasteryBacklashExclusionTest {
    private static final UUID CASTER = UUID.fromString("77000000-0000-0000-0000-000000000001");
    private static final ArcanaCastId CAST = ArcanaCastId.parse("77000000-0000-0000-0000-000000000002");
    private static final ArcanaSpellId SPELL = ArcanaSpellId.parse("black_arcana:mastery_backlash_probe");

    @Test
    void terminalBacklashSettlementCannotInvokeCastSuccessMasteryAward() {
        FakeBridge bridge = new FakeBridge();
        RpgMasteryAwardObserver observer = new RpgMasteryAwardObserver(
            bridge,
            request -> Optional.of(new RpgMasteryAwardSpec("black_arcana", 25, request.spell().id().canonical())));

        ArcaneDangerProfile profile = new ArcaneDangerProfile(
            ArcaneDangerTier.FORBIDDEN,
            1.0D,
            0.0D,
            0.0D,
            200L,
            16);
        ArcaneHazardSnapshot hazard = new ArcaneHazardSnapshot(
            CAST,
            SPELL,
            CASTER,
            "minecraft:overworld",
            10L,
            profile);
        ArcaneHazardSession session = new ArcaneHazardSession(hazard);
        ArcaneBacklashLedger ledger = new ArcaneBacklashLedger(
            session,
            new ArcaneBacklashSnapshot(hazard, zeroResistance(), ArcaneBacklashPolicy.canonical()));
        ArcanaDamageProvenance terminal = new ArcanaDamageProvenance(
            CAST,
            ArcanaDamageInstanceId.parse("77000000-0000-0000-0000-000000000003"),
            CASTER,
            SPELL,
            ArcaneDamageFamily.ARCANE_BACKLASH,
            false);

        assertEquals("backlash_non_recursive", ledger.settle(new ArcaneConfirmedDamage(terminal, 5.0D, 20L)).code());
        assertEquals(0, bridge.awards.get(), "hazard/Backlash settlement must never award RPG mastery");

        observer.onSuccess(
            request(),
            ArcanaServices.TargetResolution.resolved("target"),
            ArcanaServices.EffectResult.ok());
        assertEquals(1, bridge.awards.get(), "the mastery bridge must remain reachable only through committed cast success");
    }

    private static ArcanaCastRequest request() {
        ArcanaSpellDefinition spell = new ArcanaSpellDefinition(
            SPELL,
            "spell.black_arcana.mastery_backlash_probe",
            "black_arcana:textures/spell/mastery_backlash_probe.png",
            ArcanaCost.none(),
            false);
        return new ArcanaCastRequest(
            CAST,
            spell,
            new ArcanaCastContext(CASTER, 20L, "minecraft:overworld"));
    }

    private static ArcaneResistanceSnapshot zeroResistance() {
        Map<ArcaneResistanceSourceCategory, Double> byCategory = new EnumMap<>(ArcaneResistanceSourceCategory.class);
        for (ArcaneResistanceSourceCategory category : ArcaneResistanceSourceCategory.values()) {
            byCategory.put(category, 0.0D);
        }
        return new ArcaneResistanceSnapshot(
            0.0D,
            1.0D,
            100.0D,
            1_000.0D,
            List.of(),
            byCategory,
            List.of());
    }

    private static final class FakeBridge implements RpgSkillTreeBridge {
        private final AtomicInteger awards = new AtomicInteger();

        @Override public String integrationId() { return MOD_ID; }
        @Override public boolean available() { return true; }
        @Override public String implementationVersion() { return "test"; }
        @Override public ArcanaIntegrationAvailability availability() { return ArcanaIntegrationAvailability.AVAILABLE; }
        @Override public Set<ArcanaIntegrationCapability> capabilities() {
            return Set.of(ArcanaIntegrationCapability.MASTERY_AWARD);
        }
        @Override public RpgProgressionQuery query(UUID playerId) {
            return RpgProgressionQuery.denied("not_required", "mastery exclusion fixture does not query progression");
        }
        @Override public ArcanaDecision awardMastery(UUID playerId, RpgMasteryAwardSpec award) {
            awards.incrementAndGet();
            return ArcanaDecision.allow();
        }
    }
}
