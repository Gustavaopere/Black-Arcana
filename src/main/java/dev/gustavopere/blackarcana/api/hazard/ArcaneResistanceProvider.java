package dev.gustavopere.blackarcana.api.hazard;

import java.util.List;

/** Optional/server-owned source of Arcane Resistance. Queries must be read-only. */
public interface ArcaneResistanceProvider {
    String providerId();
    List<ArcaneResistanceContribution> contributions(ArcaneResistanceQuery query);
}
