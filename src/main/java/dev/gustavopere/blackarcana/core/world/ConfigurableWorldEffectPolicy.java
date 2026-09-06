package dev.gustavopere.blackarcana.core.world;

import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaServices;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;

import java.util.Objects;
import java.util.Optional;

/** Central fail-closed safety gate for every spell declaring world mutation. */
public final class ConfigurableWorldEffectPolicy implements ArcanaServices.WorldEffectPolicy {
    private final WorldEffectProfileRegistry profiles;
    private volatile WorldEffectPolicyConfig config;

    public ConfigurableWorldEffectPolicy(WorldEffectProfileRegistry profiles, WorldEffectPolicyConfig config) {
        this.profiles = Objects.requireNonNull(profiles, "profiles");
        this.config = Objects.requireNonNull(config, "config");
    }

    public void updateConfig(WorldEffectPolicyConfig config) {
        this.config = Objects.requireNonNull(config, "config");
    }

    public WorldEffectPolicyConfig config() {
        return config;
    }

    public Optional<WorldEffectProfile> profileFor(ArcanaSpellId spellId) {
        return profiles.find(Objects.requireNonNull(spellId, "spellId"));
    }

    @Override
    public ArcanaDecision authorize(ArcanaCastRequest request, ArcanaServices.TargetResolution target) {
        return authorizeInternal(request, target, null);
    }

    /**
     * Cast-level admission validates only that a declared world-mutating spell has a registered
     * safety profile. Concrete terrain class/mode/budget admission belongs to the mutation gateway,
     * which lets adaptive spells retain entity/visual fallback when terrain is OFF/COSMETIC or when
     * a less-destructive class is selected. The legacy {@link #authorize} method remains unchanged
     * for predecessor callers that explicitly request worst-case admission.
     */
    @Override
    public ArcanaDecision authorizeCast(ArcanaCastRequest request, ArcanaServices.TargetResolution target) {
        Objects.requireNonNull(request, "request");
        Objects.requireNonNull(target, "target");
        if (!request.spell().requestsWorldMutation()) return ArcanaDecision.allow();
        if (profiles.find(request.spell().id()).isEmpty()) {
            return ArcanaDecision.deny(
                "world_profile_missing",
                "World-mutating spell has no registered safety profile");
        }
        return ArcanaDecision.allow();
    }

    /**
     * Authorizes one concrete mutation operation against the spell's static worst-case profile.
     * Existing callers keep using {@link #authorize(ArcanaCastRequest, ArcanaServices.TargetResolution)}.
     */
    public ArcanaDecision authorize(
        ArcanaCastRequest request,
        ArcanaServices.TargetResolution target,
        WorldMutationClass requestedMutationClass
    ) {
        return authorizeInternal(request, target, Objects.requireNonNull(requestedMutationClass, "requestedMutationClass"));
    }

    private ArcanaDecision authorizeInternal(
        ArcanaCastRequest request,
        ArcanaServices.TargetResolution target,
        WorldMutationClass requestedMutationClass
    ) {
        Objects.requireNonNull(request, "request");
        Objects.requireNonNull(target, "target");
        if (!request.spell().requestsWorldMutation()) return ArcanaDecision.allow();

        WorldEffectProfile profile = profiles.find(request.spell().id()).orElse(null);
        if (profile == null) {
            return ArcanaDecision.deny(
                "world_profile_missing",
                "World-mutating spell has no registered safety profile");
        }

        WorldMutationClass effectiveClass = profile.mutationClass();
        if (requestedMutationClass != null) {
            if (requestedMutationClass.requiredRank() > profile.mutationClass().requiredRank()) {
                return ArcanaDecision.deny(
                    "world_effect_class_exceeds_profile",
                    "Requested mutation class exceeds the spell's registered worst-case profile");
            }
            effectiveClass = requestedMutationClass;
        }

        WorldEffectPolicyConfig snapshot = config;
        WorldEffectOverride override = snapshot.spellOverrides().get(request.spell().id());
        WorldEffectMode effectiveMode = override == null
            ? snapshot.globalMode()
            : WorldEffectMode.mostRestrictive(snapshot.globalMode(), override.modeCap());
        int effectiveUnits = override == null
            ? snapshot.globalMaxAffectedUnits()
            : Math.min(snapshot.globalMaxAffectedUnits(), override.maxAffectedUnits());
        boolean entityDamageAllowed = snapshot.entityDamageAllowed()
            && (override == null || override.entityDamageAllowed());

        if (!effectiveMode.allows(effectiveClass)) {
            return ArcanaDecision.deny(
                "world_effect_mode",
                "World effect requires " + effectiveClass + " but effective mode is " + effectiveMode);
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
