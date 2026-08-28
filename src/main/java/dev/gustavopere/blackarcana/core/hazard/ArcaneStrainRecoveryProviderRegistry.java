package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.hazard.ArcaneStrainRecoveryContribution;
import dev.gustavopere.blackarcana.api.hazard.ArcaneStrainRecoveryProvider;
import dev.gustavopere.blackarcana.api.hazard.ArcaneStrainRecoveryQuery;
import dev.gustavopere.blackarcana.api.hazard.ArcaneStrainRecoverySnapshot;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.regex.Pattern;

/** Bounded deterministic recovery-provider aggregation. */
public final class ArcaneStrainRecoveryProviderRegistry {
    public static final int ABSOLUTE_MAX_PROVIDERS = 64;
    public static final int MAX_CONTRIBUTIONS_PER_PROVIDER = 32;
    public static final int ABSOLUTE_MAX_CONTRIBUTIONS = 256;
    public static final double ABSOLUTE_MAX_TOTAL_BONUS_PER_TICK = 100.0D;
    private static final Pattern PROVIDER_ID = Pattern.compile("[a-z0-9_.:-]{1,64}");

    private final int maxProviders;
    private final Map<String, ArcaneStrainRecoveryProvider> providers = new LinkedHashMap<>();

    public ArcaneStrainRecoveryProviderRegistry(int maxProviders) {
        if (maxProviders <= 0 || maxProviders > ABSOLUTE_MAX_PROVIDERS) {
            throw new IllegalArgumentException("maxProviders outside absolute bounds");
        }
        this.maxProviders = maxProviders;
    }

    public static ArcaneStrainRecoveryProviderRegistry canonical() {
        return new ArcaneStrainRecoveryProviderRegistry(32);
    }

    public synchronized void register(ArcaneStrainRecoveryProvider provider) {
        Objects.requireNonNull(provider, "provider");
        String id = Objects.requireNonNull(provider.providerId(), "providerId");
        if (!PROVIDER_ID.matcher(id).matches()) throw new IllegalArgumentException("invalid strain recovery provider id: " + id);
        if (providers.containsKey(id)) throw new IllegalArgumentException("duplicate strain recovery provider: " + id);
        if (providers.size() >= maxProviders) throw new IllegalStateException("strain recovery provider registry is full");
        providers.put(id, provider);
    }

    public synchronized ArcaneStrainRecoverySnapshot snapshot(
        ArcaneStrainRecoveryQuery query,
        double baseUnitsPerTick
    ) {
        Objects.requireNonNull(query, "query");
        if (!Double.isFinite(baseUnitsPerTick) || baseUnitsPerTick < 0.0D
            || baseUnitsPerTick > ArcaneStrainRecoveryContribution.ABSOLUTE_MAX_BONUS_PER_TICK) {
            throw new IllegalArgumentException("baseUnitsPerTick outside absolute bounds");
        }
        List<Map.Entry<String, ArcaneStrainRecoveryProvider>> ordered = new ArrayList<>(providers.entrySet());
        ordered.sort(Map.Entry.comparingByKey());
        List<ArcaneStrainRecoverySnapshot.ResolvedContribution> contributions = new ArrayList<>();
        List<String> diagnostics = new ArrayList<>();

        for (Map.Entry<String, ArcaneStrainRecoveryProvider> entry : ordered) {
            collect(entry.getKey(), entry.getValue(), query, contributions, diagnostics);
            if (contributions.size() >= ABSOLUTE_MAX_CONTRIBUTIONS) break;
        }
        contributions.sort(Comparator
            .comparing(ArcaneStrainRecoverySnapshot.ResolvedContribution::providerId)
            .thenComparing(ArcaneStrainRecoverySnapshot.ResolvedContribution::sourceId));

        double bonus = 0.0D;
        for (var contribution : contributions) {
            bonus = Math.min(ABSOLUTE_MAX_TOTAL_BONUS_PER_TICK, bonus + contribution.bonusUnitsPerTick());
        }
        double total = Math.min(
            ArcaneStrainRecoveryContribution.ABSOLUTE_MAX_BONUS_PER_TICK,
            baseUnitsPerTick + bonus);
        return new ArcaneStrainRecoverySnapshot(baseUnitsPerTick, bonus, total, contributions, diagnostics);
    }

    public synchronized int size() {
        return providers.size();
    }

    private static void collect(
        String providerId,
        ArcaneStrainRecoveryProvider provider,
        ArcaneStrainRecoveryQuery query,
        List<ArcaneStrainRecoverySnapshot.ResolvedContribution> output,
        List<String> diagnostics
    ) {
        final List<ArcaneStrainRecoveryContribution> provided;
        try {
            provided = Objects.requireNonNull(provider.contributions(query), "provider contributions");
        } catch (RuntimeException | LinkageError failure) {
            diagnostics.add("strain recovery provider failed: " + providerId);
            return;
        }
        if (provided.size() > MAX_CONTRIBUTIONS_PER_PROVIDER) {
            diagnostics.add("strain recovery provider exceeded contribution cap: " + providerId);
            return;
        }
        if (output.size() + provided.size() > ABSOLUTE_MAX_CONTRIBUTIONS) {
            diagnostics.add("strain recovery provider would exceed global contribution cap: " + providerId);
            return;
        }
        for (ArcaneStrainRecoveryContribution contribution : provided) {
            if (contribution == null) {
                diagnostics.add("strain recovery provider returned null contribution: " + providerId);
                continue;
            }
            output.add(new ArcaneStrainRecoverySnapshot.ResolvedContribution(
                providerId,
                contribution.sourceId(),
                contribution.bonusUnitsPerTick()));
        }
    }
}
