package dev.gustavopere.blackarcana.api.hazard;

import java.util.List;

/** Provider-neutral recovery extension point. */
public interface ArcaneStrainRecoveryProvider {
    String providerId();

    List<ArcaneStrainRecoveryContribution> contributions(ArcaneStrainRecoveryQuery query);
}
