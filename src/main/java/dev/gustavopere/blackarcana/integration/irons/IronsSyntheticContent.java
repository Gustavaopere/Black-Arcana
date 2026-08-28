package dev.gustavopere.blackarcana.integration.irons;

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

/** Installs the Stage 03 synthetic Iron-hosted spell into the Black Arcana runtime. */
public final class IronsSyntheticContent {
    public static final long COOLDOWN_TICKS = 40L;

    private IronsSyntheticContent() { }

    public static void install(
        ArcanaServerRuntime runtime,
        IronsManaAccess manaAccess,
        Optional<RpgSkillTreeBridge> rpg
    ) {
        Objects.requireNonNull(runtime, "runtime");
        Objects.requireNonNull(manaAccess, "manaAccess");
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
                    3,
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
                new IronsManaCostProvider(manaAccess)),
            runtime.worldEffectPolicy(),
            (request, target) -> EffectResult.ok(),
            mastery);
        runtime.installEngine(definition.id(), engine);
    }

    public static ArcanaSpellDefinition definition() {
        return new ArcanaSpellDefinition(
            IronsIntegrationIds.PROBE_ARCANA_ID,
            "spell.black_arcana.irons_integration_probe",
            "black_arcana:textures/gui/spell_icons/irons_integration_probe.png",
            new ArcanaCost(IronsManaCostProvider.RESOURCE_ID, IronsIntegrationIds.PROBE_MANA_COST),
            false);
    }

    private static void installDefinition(ArcanaServerRuntime runtime, ArcanaSpellDefinition definition) {
        ArcanaSpellDefinition existing = runtime.spells().resolve(definition.id()).orElse(null);
        if (existing != null) {
            if (!existing.equals(definition)) {
                throw new IllegalStateException("Iron's integration spell id already has a different definition");
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
            IronsIntegrationIds.PROBE_ARCANA_ID,
            new ArcanaCooldownSpec(IronsIntegrationIds.PROBE_ARCANA_ID.canonical(), COOLDOWN_TICKS, false));
        runtime.cooldownPolicies().replaceAll(cooldowns, runtime.cooldownPolicies().chargeSnapshot());
    }
}
