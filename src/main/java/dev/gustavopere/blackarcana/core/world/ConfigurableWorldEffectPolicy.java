package dev.gustavopere.blackarcana.core.world;

import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaServices;

import java.util.Objects;

/** Central fail-closed safety gate for every spell declaring world mutation. */
public final class ConfigurableWorldEffectPolicy implements ArcanaServices.WorldEffectPolicy {
    private final WorldEffectProfileRegistry profiles;
    private final WorldEffectPolicyConfig config;

    public ConfigurableWorldEffectPolicy(WorldEffectProfileRegistry profiles, WorldEffectPolicyConfig config) {
        this.profiles = Objects.requireNonNull(profiles, "profiles");
        this.config = Objects.requireNonNull(config, "config");
    }

    @Override
    public ArcanaDecision authorize(ArcanaCastRequest request, ArcanaServices.TargetResolution target) {
        Objects.requireNonNull(request, "request");
        Objects.requireNonNull(target, "target");
        if (!request.spell().requestsWorldMutation()) return ArcanaDecision.allow();

        WorldEffectProfile profile = profiles.find(request.spell().id()).orElse(null);
        if (profile == null) {
            return ArcanaDecision.deny(
                "world_profile_missing",
                "World-mutating spell has no registered safety profile");
        }

        WorldEffectOverride override = config.spellOverrides().get(request.spell().id());
        WorldEffectMode effectiveMode = override == null
            ? config.globalMode()
            : WorldEffectMode.mostRestrictive(config.globalMode(), override.modeCap());
        int effectiveUnits = override == null
            ? config.globalMaxAffectedUnits()
            : Math.min(config.globalMaxAffectedUnits(), override.maxAffectedUnits());
        boolean entityDamageAllowed = config.entityDamageAllowed()
            && (override == null || override.entityDamageAllowed());

        if (!effectiveMode.allows(profile.mutationClass())) {
            return ArcanaDecision.deny(
                "world_effect_mode",
                "World effect requires " + profile.mutationClass() + " but effective mode is " + effectiveMode);
        }
        if (profile.maxAffectedUnits() > effectiveUnits) {
            return ArcanaDecision.deny(
                "world_effect_budget",
                "World effect declares " + profile.maxAffectedUnits() + " units but server cap is " + effectiveUnits);
        }
        if (profile.includesEntityDamage() && !entityDamageAllowed) {
            return ArcanaDecision.deny(
                "world_entity_damage_disabled",
                "Entity damage is disabled for this world-effect spell");
        }

        return ArcanaDecision.allow();
    }
}
