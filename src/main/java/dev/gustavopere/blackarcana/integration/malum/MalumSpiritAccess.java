package dev.gustavopere.blackarcana.integration.malum;

import dev.gustavopere.blackarcana.api.ArcanaDecision;

import java.util.UUID;

/** Mod-agnostic access to discrete Malum spirit shards owned by a player. */
public interface MalumSpiritAccess {
    int count(UUID playerId, String affinity);
    ArcanaDecision adjust(UUID playerId, String affinity, int delta);
}
