package dev.gustavopere.blackarcana.api.hazard;

import java.util.List;

/** Optional/server-owned source of Corruption Resistance. Queries must be read-only. */
public interface CorruptionResistanceProvider {
    String providerId();
    List<CorruptionResistanceContribution> contributions(CorruptionResistanceQuery query);
}
