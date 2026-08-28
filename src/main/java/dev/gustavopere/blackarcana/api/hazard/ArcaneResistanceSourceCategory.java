package dev.gustavopere.blackarcana.api.hazard;

/** Source buckets stay distinct so later balance can cap build channels independently. */
public enum ArcaneResistanceSourceCategory {
    NATIVE,
    EQUIPMENT,
    CURIO,
    EFFECT,
    RITUAL,
    RPG,
    EXTERNAL
}
