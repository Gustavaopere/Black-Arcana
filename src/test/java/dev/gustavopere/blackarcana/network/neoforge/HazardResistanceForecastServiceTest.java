package dev.gustavopere.blackarcana.network.neoforge;

import dev.gustavopere.blackarcana.api.ArcanaCastContext;
import dev.gustavopere.blackarcana.api.ArcanaCost;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaGatePreflight;
import dev.gustavopere.blackarcana.api.ArcanaSpellDefinition;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDangerProfile;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDangerTier;
import dev.gustavopere.blackarcana.api.hazard.ArcaneInsufficientResistancePolicy;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;
import dev.gustavopere.blackarcana.network.HazardResistanceForecastPayload;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class HazardResistanceForecastServiceTest {
    private static final UUID CASTER = UUID.fromString("aa11bb22-cc33-4455-8899-aabbccddeeff");
    private static final ArcanaSpellId SPELL_ID = ArcanaSpellId.parse("black_arcana:forecast_spell");
    private static final ArcanaSpellId OTHER_ID = ArcanaSpellId.parse("black_arcana:other_spell");

    @Test
    void previewRequestUsesCanonicalSpellAndServerOwnedLoadoutSlot() {
        ArcanaServerRuntime runtime = ArcanaServerRuntime.createDefault();
        ArcanaSpellDefinition spell = spell(SPELL_ID);
        runtime.spells().replaceAll(List.of(spell));
        runtime.loadouts().setLoadout(CASTER, List.of(OTHER_ID, SPELL_ID));
        ArcanaCastContext context = new ArcanaCastContext(CASTER, 44L, "minecraft:overworld");

        var request = HazardResistanceForecastService.previewRequest(runtime, SPELL_ID, context).orElseThrow();

        assertEquals(spell, request.spell());
        assertEquals(context, request.context());
        assertEquals(1, request.loadoutSlot());
        assertEquals("", request.targetHint());
        assertEquals(0L, request.channelTicks());
    }

    @Test
    void previewRequestFailsClosedForUnknownSpell() {
        ArcanaServerRuntime runtime = ArcanaServerRuntime.createDefault();
        ArcanaCastContext context = new ArcanaCastContext(CASTER, 44L, "minecraft:overworld");

        assertTrue(HazardResistanceForecastService.previewRequest(runtime, SPELL_ID, context).isEmpty());
    }

    @Test
    void belowMinimumStatusReflectsServerOwnedPolicy() {
        ArcaneDangerProfile denied = new ArcaneDangerProfile(
            ArcaneDangerTier.DANGEROUS, 1.0D, 0.0D, 0.0D, 100L, 8,
            20.0D, 40.0D, ArcaneInsufficientResistancePolicy.DENY_CAST, false);
        ArcaneDangerProfile allowed = new ArcaneDangerProfile(
            ArcaneDangerTier.DANGEROUS, 1.0D, 0.0D, 0.0D, 100L, 8,
            20.0D, 40.0D, ArcaneInsufficientResistancePolicy.ALLOW_WITH_RISK, false);

        assertEquals(
            HazardResistanceForecastPayload.Status.BELOW_MINIMUM,
            HazardResistanceForecastService.statusFor(denied, 10.0D));
        assertEquals(
            HazardResistanceForecastPayload.Status.BELOW_MINIMUM_ALLOWED,
            HazardResistanceForecastService.statusFor(allowed, 10.0D));
        assertEquals(
            HazardResistanceForecastPayload.Status.BELOW_RECOMMENDED,
            HazardResistanceForecastService.statusFor(allowed, 30.0D));
        assertEquals(
            HazardResistanceForecastPayload.Status.RECOMMENDED,
            HazardResistanceForecastService.statusFor(allowed, 40.0D));
    }

    @Test
    void gateStatusIsBoundedProjectionOfServerGate() {
        assertEquals(
            HazardResistanceForecastPayload.GateStatus.CLEAR,
            HazardResistanceForecastService.gateStatus(ArcanaGatePreflight.clear()));
        assertEquals(
            HazardResistanceForecastPayload.GateStatus.IDENTITY,
            HazardResistanceForecastService.gateStatus(
                ArcanaGatePreflight.blocked(ArcanaGatePreflight.Gate.IDENTITY, ArcanaDecision.deny("identity", "blocked"))));
        assertEquals(
            HazardResistanceForecastPayload.GateStatus.PROGRESSION,
            HazardResistanceForecastService.gateStatus(
                ArcanaGatePreflight.blocked(ArcanaGatePreflight.Gate.PROGRESSION, ArcanaDecision.deny("progression", "blocked"))));
        assertEquals(
            HazardResistanceForecastPayload.GateStatus.COOLDOWN,
            HazardResistanceForecastService.gateStatus(
                ArcanaGatePreflight.blocked(ArcanaGatePreflight.Gate.COOLDOWN, ArcanaDecision.deny("cooldown", "blocked"))));
        assertEquals(
            HazardResistanceForecastPayload.GateStatus.COST,
            HazardResistanceForecastService.gateStatus(
                ArcanaGatePreflight.blocked(ArcanaGatePreflight.Gate.COST, ArcanaDecision.deny("cost", "blocked"))));
    }

    private static ArcanaSpellDefinition spell(ArcanaSpellId id) {
        return new ArcanaSpellDefinition(
            id,
            "spell." + id.namespace() + "." + id.path(),
            id.namespace() + ":textures/spell/" + id.path() + ".png",
            new ArcanaCost("black_arcana:test_resource", 4.0D),
            true);
    }
}
