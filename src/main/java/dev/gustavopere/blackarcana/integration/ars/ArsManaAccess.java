package dev.gustavopere.blackarcana.integration.ars;

import dev.gustavopere.blackarcana.api.ArcanaDecision;

import java.util.UUID;

/** Minimal Ars mana boundary; provider-specific synchronization stays in the NeoForge adapter. */
public interface ArsManaAccess {
    ArsManaSnapshot snapshot(UUID playerId);
    ArcanaDecision adjust(UUID playerId, double delta);
}
