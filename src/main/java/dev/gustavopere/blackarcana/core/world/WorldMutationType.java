package dev.gustavopere.blackarcana.core.world;

/** Taxonomy for operations that may grief or persist in the world. */
public enum WorldMutationType {
    VISUAL_FIELD,
    TEMPORARY_BLOCK,
    BLOCK_REPLACEMENT,
    EXPLOSION_TERRAIN,
    FIRE_SPREAD,
    TERRAIN_CARVING,
    FLUID_MUTATION,
    PERSISTENT_STRUCTURE
}
