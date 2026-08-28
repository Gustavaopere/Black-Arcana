package dev.gustavopere.blackarcana.core.progression;

import dev.gustavopere.blackarcana.content.cinder.BlackPyreSafetyCeilings;
import dev.gustavopere.blackarcana.content.forbidden.ForbiddenDomainSafetyCeilings;
import dev.gustavopere.blackarcana.content.noetic.FamiliarSafetyCeilings;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;

import java.util.Map;

/** Cross-stage ceilings Stage 08 is allowed to tune below, never above. */
public final class FrozenTechnicalCeilings {
    private FrozenTechnicalCeilings() { }

    public static Map<String, Long> defaults() {
        return Map.ofEntries(
            Map.entry("world.units_per_cast", (long) ArcanaServerRuntime.DEFAULT_WORLD_UNITS_PER_CAST),
            Map.entry("world.chunks_per_effect", (long) ArcanaServerRuntime.DEFAULT_MAX_WORLD_CHUNKS_PER_EFFECT),
            Map.entry("black_pyre.radius", (long) BlackPyreSafetyCeilings.MAX_RADIUS_BLOCKS),
            Map.entry("black_pyre.cells", (long) BlackPyreSafetyCeilings.MAX_CELLS_PER_FRONTIER),
            Map.entry("black_pyre.spread_per_tick", (long) BlackPyreSafetyCeilings.MAX_SPREAD_PER_TICK),
            Map.entry("black_pyre.frontiers", (long) BlackPyreSafetyCeilings.MAX_CONCURRENT_FRONTIERS),
            Map.entry("black_pyre.lifetime", BlackPyreSafetyCeilings.MAX_LIFETIME_TICKS),
            Map.entry("inner_dominion.radius", (long) ForbiddenDomainSafetyCeilings.MAX_RADIUS_BLOCKS),
            Map.entry("inner_dominion.duration", ForbiddenDomainSafetyCeilings.MAX_DURATION_TICKS),
            Map.entry("inner_dominion.participants", (long) ForbiddenDomainSafetyCeilings.MAX_PARTICIPANTS),
            Map.entry("inner_dominion.sessions", (long) ForbiddenDomainSafetyCeilings.MAX_ACTIVE_SESSIONS),
            Map.entry("familiar.per_owner", (long) FamiliarSafetyCeilings.MAX_FAMILIARS_PER_OWNER),
            Map.entry("divination.range", (long) FamiliarSafetyCeilings.MAX_SCRY_RANGE),
            Map.entry("divination.remote_view_ticks", FamiliarSafetyCeilings.MAX_REMOTE_VIEW_TICKS),
            Map.entry("pact_sanctuary.targets", (long) FamiliarSafetyCeilings.MAX_SANCTUARY_TARGETS)
        );
    }
}
