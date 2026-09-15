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
import dev.gustavopere.blackarcana.config.AstralInvocationDataDefinition;
import dev.gustavopere.blackarcana.config.AstralInvocationResourceResolver;
import dev.gustavopere.blackarcana.core.cost.ResourceCostProvider;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;

import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;
import java.util.UUID;

/**
 * Stage 07.07 composition seam for Astral Severance.
 *
 * <p>The invocation profile is never supplied by the caller. Cost, cooldown, channel bounds,
 * projection duration and range are resolved from the strict server-owned Astral invocation
 * authority, and the cost provider is resolved from the target server runtime's exact
 * {@link ResourceCostProvider} registry. Progression and replay policy remain explicit external
 * authorities until their production contracts are reviewed.</p>
 *
 * <p>This class does not install production values or register itself automatically. A caller must
 * provide the canonical spell identity/presentation definition, explicit progression/replay
 * authorities and the already-authorized projection activator. Cast ordering, transactional cost
 * settlement, cooldown start and hazard/world gates remain owned by {@link ArcanaCastEngine}.</p>
 */
public final class AstralSeveranceCastBinding {
    public static final ArcanaSpellId SPELL_ID = ArcanaSpellId.parse(AstralInvocationDataDefinition.ASTRAL_SEVERANCE_ID);

    private AstralSeveranceCastBinding() { }

    /**
     * Resolves the current invocation/resource authorities and atomically installs the canonical
     * Stage 02 spell, cooldown, channel and engine surfaces when every prerequisite is coherent.
     * Missing invocation/provider authority fails closed without publishing partial runtime state.
     */
    public static Resolution install(
            ArcanaServerRuntime runtime,
            ArcanaSpellDefinition definition,
            Authorities authorities,
            ProjectionActivator projectionActivator
    ) {
        ArcanaServerRuntime checkedRuntime = Objects.requireNonNull(runtime, "runtime");
        ArcanaSpellDefinition checkedDefinition = Objects.requireNonNull(definition, "definition");
        Authorities checkedAuthorities = Objects.requireNonNull(authorities, "authorities");
        ProjectionActivator checkedActivator = Objects.requireNonNull(projectionActivator, "projectionActivator");

        validateDefinitionIdentity(checkedDefinition);

        AstralInvocationResourceResolver.Resolution resourceResolution =
                AstralInvocationResourceResolver.resolve(checkedRuntime);
        if (!resourceResolution.decision().allowed()) {
            return Resolution.denied(resourceResolution.decision());
        }

        AstralInvocationDataDefinition.Invocation invocation = resourceResolution.invocation().orElseThrow();
        ResourceCostProvider resourceProvider = resourceResolution.resourceProvider().orElseThrow();
        validateDefinitionAgainstInvocation(checkedDefinition, invocation);

        ArcanaDecision runtimeState = validateRuntimeState(checkedRuntime, checkedDefinition, invocation);
        if (!runtimeState.allowed()) {
            return Resolution.denied(runtimeState);
        }

        ArcanaCastEngine engine = buildEngine(
                checkedRuntime,
                invocation,
                resourceProvider,
                checkedAuthorities,
                checkedActivator);

        Map<ArcanaSpellId, ArcanaSpellDefinition> definitions =
                new LinkedHashMap<>(checkedRuntime.spells().snapshot());
        definitions.putIfAbsent(SPELL_ID, checkedDefinition);

        Map<ArcanaSpellId, ArcanaCooldownSpec> cooldowns =
                new LinkedHashMap<>(checkedRuntime.cooldownPolicies().cooldownSnapshot());
        cooldowns.putIfAbsent(SPELL_ID, invocation.cooldown());

        Optional<ArcanaChannelSpec> existingChannel = checkedRuntime.channelSpecs().resolve(SPELL_ID);
        if (existingChannel.isEmpty() && !checkedRuntime.channelSpecs().register(SPELL_ID, invocation.channelSpec())) {
            return Resolution.denied(ArcanaDecision.deny(
                    "astral_channel_registry_unavailable",
                    "Astral Severance channel specification could not be registered"));
        }

        // Every fallible external authority check happens above. These publications consume only
        // already-validated immutable snapshots and complete the canonical runtime composition.
        checkedRuntime.spells().replaceAll(definitions.values());
        checkedRuntime.cooldownPolicies().replaceAll(
                cooldowns,
                checkedRuntime.cooldownPolicies().chargeSnapshot());
        checkedRuntime.installEngine(SPELL_ID, engine);

        return Resolution.installed(new Installed(
                SPELL_ID,
                resourceProvider.resourceId(),
                invocation.channelSpec()));
    }

    private static ArcanaCastEngine buildEngine(
            ArcanaServerRuntime runtime,
            AstralInvocationDataDefinition.Invocation invocation,
            ResourceCostProvider resourceProvider,
            Authorities authorities,
            ProjectionActivator projectionActivator
    ) {
        return new ArcanaCastEngine(
                runtime.spells(),
                authorities.replayGuard(),
                authorities.progressionGate(),
                runtime.cooldowns(),
                request -> ArcanaServices.TargetResolution.resolved(
                        new ArcanaTargetReference.EntityRef(request.context().casterId()).canonical()),
                resourceProvider,
                runtime.worldEffectPolicy(),
                (request, target) -> applyProjection(invocation, projectionActivator, request),
                authorities.successObserver()
        ).withChannelGate(request -> checkChannelMinimum(invocation.channelSpec(), request));
    }

    private static ArcanaDecision validateRuntimeState(
            ArcanaServerRuntime runtime,
            ArcanaSpellDefinition definition,
            AstralInvocationDataDefinition.Invocation invocation
    ) {
        Optional<ArcanaSpellDefinition> existingDefinition = runtime.spells().resolve(SPELL_ID);
        if (existingDefinition.isPresent() && !existingDefinition.orElseThrow().equals(definition)) {
            return ArcanaDecision.deny(
                    "astral_spell_definition_conflict",
                    "Astral Severance already has a different canonical spell definition");
        }

        ArcanaCooldownSpec existingCooldown = runtime.cooldownPolicies().cooldownSnapshot().get(SPELL_ID);
        if (existingCooldown != null && !existingCooldown.equals(invocation.cooldown())) {
            return ArcanaDecision.deny(
                    "astral_cooldown_conflict",
                    "Astral Severance already has a different cooldown policy");
        }

        Optional<ArcanaChannelSpec> existingChannel = runtime.channelSpecs().resolve(SPELL_ID);
        if (existingChannel.isPresent() && !existingChannel.orElseThrow().equals(invocation.channelSpec())) {
            return ArcanaDecision.deny(
                    "astral_channel_conflict",
                    "Astral Severance already has a different channel policy");
        }

        if (runtime.hasInstalledEngine(SPELL_ID)) {
            return ArcanaDecision.deny(
                    "astral_engine_already_installed",
                    "Astral Severance already has an installed execution engine");
        }
        return ArcanaDecision.allow();
    }

    private static void validateDefinitionIdentity(ArcanaSpellDefinition definition) {
        if (!SPELL_ID.equals(definition.id())) {
            throw new IllegalArgumentException("Astral Severance definition must use " + SPELL_ID.canonical());
        }
        if (definition.requestsWorldMutation()) {
            throw new IllegalArgumentException("Astral Severance definition cannot request world mutation");
        }
    }

    private static void validateDefinitionAgainstInvocation(
            ArcanaSpellDefinition definition,
            AstralInvocationDataDefinition.Invocation invocation
    ) {
        if (!definition.cost().equals(invocation.cost())) {
            throw new IllegalArgumentException(
                    "Astral Severance definition cost must exactly match the resolved invocation authority");
        }
    }

    private static ArcanaDecision checkChannelMinimum(ArcanaChannelSpec channelSpec, ArcanaCastRequest request) {
        if (request.channelTicks() < channelSpec.minimumTicks()) {
            return ArcanaDecision.deny("channel_too_short", "channel has not reached minimum duration");
        }
        return ArcanaDecision.allow();
    }

    private static ArcanaServices.EffectResult applyProjection(
            AstralInvocationDataDefinition.Invocation invocation,
            ProjectionActivator projectionActivator,
            ArcanaCastRequest request
    ) {
        ArcanaDecision decision = Objects.requireNonNull(
                projectionActivator.activate(
                        request.context().casterId(),
                        invocation.projectionDurationTicks(),
                        invocation.maxRangeBlocks()),
                "projection activation decision");
        if (decision.allowed()) {
            return ArcanaServices.EffectResult.ok();
        }
        String detail = decision.detail().isBlank()
                ? decision.code()
                : decision.code() + ": " + decision.detail();
        return ArcanaServices.EffectResult.failed(detail);
    }

    public record Authorities(
            ArcanaServices.ProgressionGate progressionGate,
            ArcanaServices.ReplayGuard replayGuard,
            ArcanaServices.CastSuccessObserver successObserver
    ) {
        public Authorities {
            Objects.requireNonNull(progressionGate, "progressionGate");
            Objects.requireNonNull(replayGuard, "replayGuard");
            Objects.requireNonNull(successObserver, "successObserver");
        }
    }

    public record Installed(ArcanaSpellId spellId, String resourceId, ArcanaChannelSpec channelSpec) {
        public Installed {
            Objects.requireNonNull(spellId, "spellId");
            resourceId = ResourceCostProvider.requireResourceId(resourceId);
            Objects.requireNonNull(channelSpec, "channelSpec");
        }
    }

    public record Resolution(ArcanaDecision decision, Optional<Installed> installed) {
        public Resolution {
            Objects.requireNonNull(decision, "decision");
            installed = Objects.requireNonNull(installed, "installed");
            if (decision.allowed() != installed.isPresent()) {
                throw new IllegalArgumentException("Astral binding resolution must be all-or-nothing");
            }
        }

        private static Resolution denied(ArcanaDecision decision) {
            ArcanaDecision checked = Objects.requireNonNull(decision, "decision");
            if (checked.allowed()) throw new IllegalArgumentException("denied resolution requires denial");
            return new Resolution(checked, Optional.empty());
        }

        private static Resolution installed(Installed installed) {
            return new Resolution(ArcanaDecision.allow(), Optional.of(Objects.requireNonNull(installed, "installed")));
        }
    }

    @FunctionalInterface
    public interface ProjectionActivator {
        ArcanaDecision activate(UUID casterId, int durationTicks, double maxRangeBlocks);
    }
}
