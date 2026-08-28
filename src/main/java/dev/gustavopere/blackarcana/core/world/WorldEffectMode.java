package dev.gustavopere.blackarcana.core.world;

/** Server safety ceiling for policy-governed world effects. */
public enum WorldEffectMode {
    OFF(0),
    COSMETIC(1),
    TEMPORARY(2),
    LIMITED(3),
    FULL(4);

    private final int rank;

    WorldEffectMode(int rank) {
        this.rank = rank;
    }

    public boolean allows(WorldMutationClass mutationClass) {
        return rank >= mutationClass.requiredRank();
    }

    public static WorldEffectMode mostRestrictive(WorldEffectMode first, WorldEffectMode second) {
        return first.rank <= second.rank ? first : second;
    }
}
