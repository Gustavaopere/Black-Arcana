package dev.gustavopere.blackarcana.api.hazard;

/** Causal damage family used by hazard attribution, not a Minecraft damage type. */
public enum ArcaneDamageFamily {
    DIRECT,
    PROJECTILE,
    DAMAGE_OVER_TIME,
    CHAIN,
    OWNED_SUMMON,
    ARCANE_BACKLASH,
    OTHER
}
