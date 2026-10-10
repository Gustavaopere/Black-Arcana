package dev.gustavopere.blackarcana.core.ritual;

import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;

import java.util.List;
import java.util.Objects;
import java.util.UUID;

/** Server-only transition from an authorized world interaction into the canonical ritual pipeline. */
public final class VeilAnchorActivationService {
    private VeilAnchorActivationService() { }

    /** Caster identity and activation nonce must originate on the server, never in client payloads. */
    public static RitualResult start(ArcanaServerRuntime runtime, UUID casterId, RitualAnchor anchor, long nowTick) {
        Objects.requireNonNull(runtime, "runtime");
        Objects.requireNonNull(casterId, "casterId");
        Objects.requireNonNull(anchor, "anchor");
        if (nowTick < 0L) throw new IllegalArgumentException("nowTick cannot be negative");

        var id = BlackArcanaGrandRituals.VEIL_ANCHOR_CONSECRATION_ID;
        RitualDefinition definition = runtime.ritualDefinitions().resolve(id).orElse(null);
        if (definition == null || !runtime.ritualBindings().contains(id)) {
            return RitualResult.denied(RitualResult.Status.DENIED_REQUIREMENT,
                    ArcanaDecision.deny("grand_ritual_provider_missing", "the Malum ritual binding is unavailable"));
        }

        RitualContext context = new RitualContext(casterId, List.of(), anchor);
        // Preflight resources now, but reserve/commit them only inside RitualEngine at tick 100.
        ArcanaDecision available = runtime.ritualBindings().components().check(definition, context, nowTick);
        if (!available.allowed()) {
            return RitualResult.denied(RitualResult.Status.DENIED_REQUIREMENT, available);
        }

        return runtime.rituals().start(definition, new RitualActivationId(UUID.randomUUID()), context, nowTick);
    }
}
