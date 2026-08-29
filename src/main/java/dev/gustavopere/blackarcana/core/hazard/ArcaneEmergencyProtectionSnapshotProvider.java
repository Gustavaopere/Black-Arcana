package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.hazard.ArcaneEmergencyProtectionSnapshot;

import java.util.UUID;

/**
 * Optional extension for resistance providers whose same frozen equipment snapshot also supplies
 * emergency-protection facts for a root cast.
 */
public interface ArcaneEmergencyProtectionSnapshotProvider {
    ArcaneEmergencyProtectionSnapshot takeEmergencySnapshot(
        ArcanaCastId castId,
        UUID casterId,
        long serverTick
    );

    /** Releases retained root-cast state when preflight aborts before handoff. */
    void release(ArcanaCastId castId);
}
