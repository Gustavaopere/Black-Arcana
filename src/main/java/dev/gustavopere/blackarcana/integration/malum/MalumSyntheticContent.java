package dev.gustavopere.blackarcana.integration.malum;

import dev.gustavopere.blackarcana.api.ArcanaCastEngine;
import dev.gustavopere.blackarcana.api.ArcanaCooldownSpec;
import dev.gustavopere.blackarcana.api.ArcanaCost;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaPaymentPolicy;
import dev.gustavopere.blackarcana.api.ArcanaServices.CastSuccessObserver;
import dev.gustavopere.blackarcana.api.ArcanaServices.EffectResult;
import dev.gustavopere.blackarcana.api.ArcanaServices.TargetResolution;
import dev.gustavopere.blackarcana.api.ArcanaSpellDefinition;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.core.cast.BoundedReplayGuard;
import dev.gustavopere.blackarcana.core.cost.PolicyAwareCostProvider;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;
import dev.gustavopere.blackarcana.integration.rpg.RpgMasteryAwardObserver;
import dev.gustavopere.blackarcana.integration.rpg.RpgMasteryAwardSpec;
import dev.gustavopere.blackarcana.integration.rpg.RpgSkillTreeBridge;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;

/** Non-destructive Stage 03 probe that pays Black Arcana costs with Malum spirits. */
public final class MalumSyntheticContent {
    public static final long COOLDOWN_TICKS = 60L;

    private MalumSyntheticContent() { }

    public static void install(
        ArcanaServerRuntime runtime,
        MalumSpiritAccess spiritAccess,
        Optional<RpgSkillTreeBridge> rpg
    ) {
        Objects.requireNonNull(runtime, "runtime");
        Objects.requireNonNull(spiritAccess, "spiritAccess");
        Objects.requireNonNull(rpg, "rpg");

        ArcanaSpellDefinition definition = definition();
        installDefinition(runtime, definition);
        installCooldown(runtime);

        CastSuccessObserver mastery = rpg
            .filter(RpgSkillTreeBridge::available)
            .<CastSuccessObserver>map(bridge -> new RpgMasteryAwardObserver(
                bridge,
                request -> Optional.of(new RpgMasteryAwardSpec(
                    "black_arcana:casting",
                    4,
                    request.spell().id().canonical()))))
            .orElseGet(CastSuccessObserver::noop);

        ArcanaCastEngine engine = new ArcanaCastEngine(
            runtime.spells(),
            new BoundedReplayGuard(2048, 20L * 30L),
            request -> ArcanaDecision.allow(),
            runtime.cooldowns(),
            request -> TargetResolution.resolved(request.context().casterId().toString()),
            new PolicyAwareCostProvider(
                ArcanaPaymentPolicy.BYPASS_CREATIVE_AND_ADMIN,
                new MalumSpiritCostProvider(spiritAccess)),
            runtime.worldEffectPolicy(),
            (request, target) -> EffectResult.ok(),
            mastery);
        runtime.installEngine(definition.id(), engine);
    }

    public static ArcanaSpellDefinition definition() {
        return new ArcanaSpellDefinition(
            MalumIntegrationIds.PROBE_ARCANA_ID,
            "spell.black_arcana.malum_integration_probe",
            "black_arcana:textures/gui/spell_icons/malum_integration_probe.png",
            new ArcanaCost(
                MalumIntegrationIds.resourceId(MalumIntegrationIds.PROBE_AFFINITY),
                MalumIntegrationIds.PROBE_SPIRIT_COST),
            false);
    }

    private static void installDefinition(ArcanaServerRuntime runtime, ArcanaSpellDefinition definition) {
        ArcanaSpellDefinition existing = runtime.spells().resolve(definition.id()).orElse(null);
        if (existing != null) {
            if (!existing.equals(definition)) {
                throw new IllegalStateException("Malum integration spell id already has a different definition");
            }
            return;
        }
        var definitions = new ArrayList<>(runtime.spells().snapshot().values());
        definitions.add(definition);
        runtime.spells().replaceAll(definitions);
    }

    private static void installCooldown(ArcanaServerRuntime runtime) {
        Map<ArcanaSpellId, ArcanaCooldownSpec> cooldowns =
            new LinkedHashMap<>(runtime.cooldownPolicies().cooldownSnapshot());
        cooldowns.put(
            MalumIntegrationIds.PROBE_ARCANA_ID,
            new ArcanaCooldownSpec(MalumIntegrationIds.PROBE_ARCANA_ID.canonical(), COOLDOWN_TICKS, false));
        runtime.cooldownPolicies().replaceAll(cooldowns, runtime.cooldownPolicies().chargeSnapshot());
    }
}
