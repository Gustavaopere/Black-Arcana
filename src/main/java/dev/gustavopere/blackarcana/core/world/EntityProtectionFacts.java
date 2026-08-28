package dev.gustavopere.blackarcana.core.world;

/** Server-computed facts only; no client-authored protection flags are accepted. */
public record EntityProtectionFacts(
    boolean player,
    boolean alliedWithCaster,
    boolean boss,
    boolean invulnerable,
    boolean serverPvpEnabled
) { }
