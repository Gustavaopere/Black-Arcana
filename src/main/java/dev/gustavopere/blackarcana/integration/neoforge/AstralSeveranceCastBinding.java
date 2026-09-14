package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.api.ArcanaCastEngine;
import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaChannelSpec;
import dev.gustavopere.blackarcana.api.ArcanaCooldownSpec;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaServices;
import dev.gustavopere.blackarcana.api.ArcanaSpellDefinition;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.api.ArcanaTargetReference;
import dev.gustavopere.blackarcana.content.noetic.NoeticSafetyCeilings;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;

import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Objects;
import java.util.UUID;

/**
 * Stage 07.07 binding for Astral Severance.
 *
 * <p>The binding owns only spell-specific configuration and collaborators. Cast ordering,
 * transactional cost handling, cooldown start and hazard/world gates remain owned by the
 * canonical {@link ArcanaCastEngine}.</p>
 */
public final class AstralSeveranceCastBinding {
    public static final ArcanaSpellId SPELL_ID = ArcanaSpellId.parse("black_arcana:astral_severance");

    private AstralSeveranceCastBinding() { }

    public static Installed install(
        ArcanaServerRuntime runtime,
        Profile profile,
        Authorities authorities,
        ProjectionActivator projectionActivator
    ) {
        Objects.requireNonNull(runtime, "runtime");
        Profile checkedProfile = Objects.requireNonNull(profile, "profile");
        Authorities checkedAuthorities = Objects.requireNonNull(authorities, "authorities");
        ProjectionActivator checkedActivator = Objects.requireNonNull(projectionActivator, "projectionActivator");

        // Validate every external authority before mutating runtime registries.
        validateResourceAuthority(checkedProfile, checkedAuthorities.resourceAuthority());
        ArcanaCastEngine engine = buildEngine(runtime, checkedProfile, checkedAuthorities, checkedActivator);

        Map<ArcanaSpellId, ArcanaSpellDefinition> definitions =
            new LinkedHashMap<>(runtime.spells().snapshot());
        definitions.put(SPELL_ID, checkedProfile.definition());

        Map<ArcanaSpellId, ArcanaCooldownSpec> cooldowns =
            new LinkedHashMap<>(runtime.cooldownPolicies().cooldownSnapshot());
        cooldowns.put(SPELL_ID, checkedProfile.cooldown());

        runtime.spells().replaceAll(definitions.values());
        runtime.cooldownPolicies().replaceAll(cooldowns, runtime.cooldownPolicies().chargeSnapshot());
        runtime.installEngine(SPELL_ID, engine);

        return new Installed(SPELL_ID, checkedProfile.channelSpec());
    }

    public static ArcanaCastEngine buildEngine(
        ArcanaServerRuntime runtime,
        Profile profile,
        Authorities authorities,
        ProjectionActivator projectionActivator
    ) {
        ArcanaServerRuntime checkedRuntime = Objects.requireNonNull(runtime, "runtime");
        Profile checkedProfile = Objects.requireNonNull(profile, "profile");
        Authorities checkedAuthorities = Objects.requireNonNull(authorities, "authorities");
        ProjectionActivator checkedActivator = Objects.requireNonNull(projectionActivator, "projectionActivator");

        validateResourceAuthority(checkedProfile, checkedAuthorities.resourceAuthority());

        return new ArcanaCastEngine(
            checkedRuntime.spells(),
            checkedAuthorities.replayGuard(),
            checkedAuthorities.progressionGate(),
            checkedRuntime.cooldowns(),
            request -> ArcanaServices.TargetResolution.resolved(
                new ArcanaTargetReference.EntityRef(request.context().casterId()).canonical()),
            checkedAuthorities.resourceAuthority(),
            checkedRuntime.worldEffectPolicy(),
            (request, target) -> applyProjection(checkedProfile, checkedActivator, request),
            checkedAuthorities.successObserver()
        );
    }

    private static ArcanaServices.EffectResult applyProjection(
        Profile profile,
        ProjectionActivator projectionActivator,
        ArcanaCastRequest request
    ) {
        ArcanaDecision decision = Objects.requireNonNull(
            projectionActivator.activate(
                request.context().casterId(),
                profile.projectionDurationTicks(),
                profile.maxRangeBlocks()),
            "projection activation decision");
        if (decision.allowed()) {
            return ArcanaServices.EffectResult.ok();
        }
        String detail = decision.detail().isBlank()
            ? decision.code()
            : decision.code() + ": " + decision.detail();
        return ArcanaServices.EffectResult.failed(detail);
    }

    private static void validateResourceAuthority(Profile profile, ResourceAuthority resourceAuthority) {
        ResourceAuthority checked = Objects.requireNonNull(resourceAuthority, "resourceAuthority");
        String expected = profile.definition().cost().resourceId();
        String actual = Objects.requireNonNull(checked.resourceId(), "resourceAuthority.resourceId");
        if (!expected.equals(actual)) {
            throw new IllegalArgumentException(
                "Resource authority mismatch: spell requires " + expected + " but authority owns " + actual);
        }
    }

    public record Profile(
        ArcanaSpellDefinition definition,
        ArcanaCooldownSpec cooldown,
        ArcanaChannelSpec channelSpec,
        int projectionDurationTicks,
        double maxRangeBlocks
    ) {
        public Profile {
            Objects.requireNonNull(definition, "definition");
            Objects.requireNonNull(cooldown, "cooldown");
            Objects.requireNonNull(channelSpec, "channelSpec");

            if (!SPELL_ID.equals(definition.id())) {
                throw new IllegalArgumentException("Astral Severance profile must use " + SPELL_ID.canonical());
            }
            if (definition.requestsWorldMutation()) {
                throw new IllegalArgumentException("Astral Severance profile cannot request world mutation");
            }
            if (projectionDurationTicks <= 0 || projectionDurationTicks > NoeticSafetyCeilings.MAX_DURATION_TICKS) {
                throw new IllegalArgumentException(
                    "Projection duration must be between 1 and " + NoeticSafetyCeilings.MAX_DURATION_TICKS + " ticks");
            }
            if (!Double.isFinite(maxRangeBlocks)
                || maxRangeBlocks <= 0.0D
                || maxRangeBlocks > NoeticSafetyCeilings.MAX_RANGE_BLOCKS) {
                throw new IllegalArgumentException(
                    "Projection range must be finite, positive and at most "
                        + NoeticSafetyCeilings.MAX_RANGE_BLOCKS + " blocks");
            }
        }
    }

    public record Authorities(
        ResourceAuthority resourceAuthority,
        ArcanaServices.ProgressionGate progressionGate,
        ArcanaServices.ReplayGuard replayGuard,
        ArcanaServices.CastSuccessObserver successObserver
    ) {
        public Authorities {
            Objects.requireNonNull(resourceAuthority, "resourceAuthority");
            Objects.requireNonNull(progressionGate, "progressionGate");
            Objects.requireNonNull(replayGuard, "replayGuard");
            Objects.requireNonNull(successObserver, "successObserver");
        }
    }

    public record Installed(ArcanaSpellId spellId, ArcanaChannelSpec channelSpec) {
        public Installed {
            Objects.requireNonNull(spellId, "spellId");
            Objects.requireNonNull(channelSpec, "channelSpec");
        }
    }

    public interface ResourceAuthority extends ArcanaServices.CostProvider {
        String resourceId();
    }

    @FunctionalInterface
    public interface ProjectionActivator {
        ArcanaDecision activate(UUID casterId, int durationTicks, double maxRangeBlocks);
    }
}
