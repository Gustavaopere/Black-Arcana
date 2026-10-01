package dev.gustavopere.blackarcana.integration.rpg;

import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaIntegration;
import java.util.UUID;

/** Optional binary bridge to the user's canonical RPG Skill Tree mod. */
public interface RpgSkillTreeBridge extends ArcanaIntegration {
    String MOD_ID = "rpgskilltree";

    /**
     * Read-only progression projection for hazard resistance.
     *
     * <p>Implementations must not bootstrap, persist, migrate, synchronize or award progression
     * while serving this query. Mastery is not required by the hazard resistance adapter.</p>
     */
    RpgProgressionQuery queryHazardProgression(UUID playerId);

    RpgProgressionQuery query(UUID playerId);

    ArcanaDecision awardMastery(UUID playerId, RpgMasteryAwardSpec award);
}
