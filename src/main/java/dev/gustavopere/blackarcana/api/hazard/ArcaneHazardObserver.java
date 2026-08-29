package dev.gustavopere.blackarcana.api.hazard;

/** Read-only post-settlement observer. Implementations must not mutate gameplay state synchronously. */
@FunctionalInterface
public interface ArcaneHazardObserver {
    void onSettled(ArcaneHazardSettledEvent event);
}
