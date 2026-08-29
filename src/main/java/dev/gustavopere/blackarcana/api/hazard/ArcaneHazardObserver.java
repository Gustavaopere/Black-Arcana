package dev.gustavopere.blackarcana.api.hazard;

/**
 * Public observer hook for consumers that need the final, server-authoritative hazard settlement.
 */
@FunctionalInterface
public interface ArcaneHazardObserver {
    void onSettled(ArcaneHazardSettledEvent event);
}
