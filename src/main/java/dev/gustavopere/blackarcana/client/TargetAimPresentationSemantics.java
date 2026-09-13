package dev.gustavopere.blackarcana.client;

/**
 * Pure presentation semantics for Stage 05.13 local aim observation.
 *
 * These states describe only what the physical client currently observes under
 * its crosshair. They do not claim server target validity, range, line of sight,
 * cast admission or world-effect permission.
 */
final class TargetAimPresentationSemantics {
    enum Observation {
        MISS,
        BLOCK,
        ENTITY
    }

    private TargetAimPresentationSemantics() {
    }

    static boolean shouldRender(
            boolean contextualHudEnabled,
            boolean worldInputAvailable,
            boolean selectionRecent,
            boolean hasSelectedSpell
    ) {
        return contextualHudEnabled
                && worldInputAvailable
                && selectionRecent
                && hasSelectedSpell;
    }

    static String marker(Observation observation) {
        return switch (observation) {
            case MISS -> "·";
            case BLOCK -> "□";
            case ENTITY -> "◇";
        };
    }

    static String translationKey(Observation observation) {
        return switch (observation) {
            case MISS -> "hud.black_arcana.aim.local.miss";
            case BLOCK -> "hud.black_arcana.aim.local.block";
            case ENTITY -> "hud.black_arcana.aim.local.entity";
        };
    }
}
