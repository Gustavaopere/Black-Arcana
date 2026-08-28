package dev.gustavopere.blackarcana.integration.irons;

import dev.gustavopere.blackarcana.api.ArcanaDecision;

import java.util.UUID;

/**
 * Minimal mana mutation boundary. The NeoForge/Iron implementation owns client
 * synchronization; core cost logic never references Iron's runtime types.
 */
public interface IronsManaAccess {
    IronsManaSnapshot snapshot(UUID playerId);

    /** Applies a signed delta atomically on the server and synchronizes the provider state. */
    ArcanaDecision adjust(UUID playerId, float delta);
}
