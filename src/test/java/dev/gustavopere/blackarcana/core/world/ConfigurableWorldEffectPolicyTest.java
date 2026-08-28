package dev.gustavopere.blackarcana.core.world;

import dev.gustavopere.blackarcana.api.ArcanaCastContext;
import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaCost;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaServices;
import dev.gustavopere.blackarcana.api.ArcanaSpellDefinition;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import org.junit.jupiter.api.Test;

import java.util.Map;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ConfigurableWorldEffectPolicyTest {
    private static final ArcanaSpellId SPELL_ID = ArcanaSpellId.parse("black_arcana:world_probe");

    @Test
    void nonMutatingSpellDoesNotRequireProfile() {
        var policy = new ConfigurableWorldEffectPolicy(
            new WorldEffectProfileRegistry(),
            WorldEffectPolicyConfig.safeDefaults());

        assertTrue(policy.authorize(request(false), target()).allowed());
    }

    @Test
    void mutatingSpellWithoutProfileFailsClosed() {
        var policy = new ConfigurableWorldEffectPolicy(
            new WorldEffectProfileRegistry(),
            WorldEffectPolicyConfig.safeDefaults());

        ArcanaDecision decision = policy.authorize(request(true), target());
        assertFalse(decision.allowed());
        assertEquals("world_profile_missing", decision.code());
    }

    @Test
    void defaultTemporaryModeRejectsLimitedOrPermanentMutation() {
        var profiles = new WorldEffectProfileRegistry();
        profiles.register(SPELL_ID, new WorldEffectProfile(
            WorldMutationType.EXPLOSION_TERRAIN,
            WorldMutationClass.LIMITED,
            32,
            false));
        var policy = new ConfigurableWorldEffectPolicy(profiles, WorldEffectPolicyConfig.safeDefaults());

        ArcanaDecision decision = policy.authorize(request(true), target());
        assertFalse(decision.allowed());
        assertEquals("world_effect_mode", decision.code());
    }

    @Test
    void perSpellOverrideCanNarrowButNeverElevateGlobalMode() {
        var profiles = new WorldEffectProfileRegistry();
        profiles.register(SPELL_ID, new WorldEffectProfile(
            WorldMutationType.BLOCK_REPLACEMENT,
            WorldMutationClass.LIMITED,
            32,
            false));
        var config = new WorldEffectPolicyConfig(
            WorldEffectMode.TEMPORARY,
            4096,
            true,
            Map.of(SPELL_ID, new WorldEffectOverride(WorldEffectMode.FULL, 4096, true)));

        ArcanaDecision decision = new ConfigurableWorldEffectPolicy(profiles, config).authorize(request(true), target());
        assertFalse(decision.allowed());
        assertEquals("world_effect_mode", decision.code());
    }

    @Test
    void unitCapAndEntityDamageAreIndependentSafetyGates() {
        var profiles = new WorldEffectProfileRegistry();
        profiles.register(SPELL_ID, new WorldEffectProfile(
            WorldMutationType.TEMPORARY_BLOCK,
            WorldMutationClass.TEMPORARY,
            64,
            true));

        var capped = new ConfigurableWorldEffectPolicy(
            profiles,
            new WorldEffectPolicyConfig(WorldEffectMode.FULL, 32, true, Map.of()));
        assertEquals("world_effect_budget", capped.authorize(request(true), target()).code());

        var noEntityDamage = new ConfigurableWorldEffectPolicy(
            profiles,
            new WorldEffectPolicyConfig(WorldEffectMode.FULL, 64, false, Map.of()));
        assertEquals("world_entity_damage_disabled", noEntityDamage.authorize(request(true), target()).code());
    }

    @Test
    void compatibleTemporaryProfileIsAllowed() {
        var profiles = new WorldEffectProfileRegistry();
        profiles.register(SPELL_ID, new WorldEffectProfile(
            WorldMutationType.TEMPORARY_BLOCK,
            WorldMutationClass.TEMPORARY,
            128,
            false));

        assertTrue(new ConfigurableWorldEffectPolicy(profiles, WorldEffectPolicyConfig.safeDefaults())
            .authorize(request(true), target()).allowed());
    }

    private static ArcanaCastRequest request(boolean worldMutation) {
        var spell = new ArcanaSpellDefinition(
            SPELL_ID,
            "spell.black_arcana.world_probe",
            "black_arcana:textures/spell/world_probe.png",
            new ArcanaCost("black_arcana:test", 1),
            worldMutation);
        return new ArcanaCastRequest(
            new ArcanaCastId(UUID.fromString("11111111-1111-1111-1111-111111111111")),
            spell,
            new ArcanaCastContext(
                UUID.fromString("22222222-2222-2222-2222-222222222222"),
                100L,
                "minecraft:overworld"));
    }

    private static ArcanaServices.TargetResolution target() {
        return ArcanaServices.TargetResolution.resolved("minecraft:overworld@0,64,0");
    }
}
