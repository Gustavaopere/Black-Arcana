package dev.gustavopere.blackarcana.core.world;

/** Increasing persistence/destructiveness class used by {@link WorldEffectMode}. */
public enum WorldMutationClass {
    COSMETIC(1),
    TEMPORARY(2),
    LIMITED(3),
    PERMANENT(4);

    private final int requiredRank;

    WorldMutationClass(int requiredRank) {
        this.requiredRank = requiredRank;
    }

    int requiredRank() {
        return requiredRank;
    }
}
