package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.hazard.CorruptionResistanceContribution;
import dev.gustavopere.blackarcana.api.hazard.CorruptionResistanceProvider;
import dev.gustavopere.blackarcana.api.hazard.CorruptionResistanceQuery;
import dev.gustavopere.blackarcana.api.hazard.CorruptionResistanceSnapshot;
import dev.gustavopere.blackarcana.api.hazard.CorruptionResistanceSourceCategory;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.EnumMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.regex.Pattern;

/** Bounded deterministic aggregation for Corruption Resistance only. */
public final class CorruptionResistanceProviderRegistry {
    public static final int ABSOLUTE_MAX_PROVIDERS = 64;
    public static final int MAX_CONTRIBUTIONS_PER_PROVIDER = 64;
    public static final int ABSOLUTE_MAX_CONTRIBUTIONS = 512;
    private static final Pattern PROVIDER_ID = Pattern.compile("[a-z0-9_.:-]{1,64}");

    private final int maxProviders;
    private final CorruptionResistanceCurve curve;
    private final Map<CorruptionResistanceSourceCategory, Double> bucketCaps;
    private final Map<String, CorruptionResistanceProvider> providers = new LinkedHashMap<>();

    public CorruptionResistanceProviderRegistry(
        int maxProviders,
        CorruptionResistanceCurve curve,
        Map<CorruptionResistanceSourceCategory, Double> bucketCaps
    ) {
        if (maxProviders <= 0 || maxProviders > ABSOLUTE_MAX_PROVIDERS) {
            throw new IllegalArgumentException("maxProviders outside absolute bounds");
        }
        this.maxProviders = maxProviders;
        this.curve = Objects.requireNonNull(curve, "curve");
        Objects.requireNonNull(bucketCaps, "bucketCaps");
        EnumMap<CorruptionResistanceSourceCategory, Double> checked =
            new EnumMap<>(CorruptionResistanceSourceCategory.class);
        for (CorruptionResistanceSourceCategory category : CorruptionResistanceSourceCategory.values()) {
            Double cap = bucketCaps.get(category);
            if (cap == null || !Double.isFinite(cap) || cap < 0.0D
                || cap > CorruptionResistanceCurve.ABSOLUTE_MAX_RESISTANCE) {
                throw new IllegalArgumentException("missing/invalid corruption resistance bucket cap: " + category);
            }
            checked.put(category, cap);
        }
        this.bucketCaps = Map.copyOf(checked);
    }

    public static CorruptionResistanceProviderRegistry canonical(int maxProviders) {
        EnumMap<CorruptionResistanceSourceCategory, Double> caps =
            new EnumMap<>(CorruptionResistanceSourceCategory.class);
        for (CorruptionResistanceSourceCategory category : CorruptionResistanceSourceCategory.values()) {
            caps.put(category, CorruptionResistanceCurve.CANONICAL_MAX_RESISTANCE);
        }
        return new CorruptionResistanceProviderRegistry(maxProviders, CorruptionResistanceCurve.canonical(), caps);
    }

    public synchronized void register(CorruptionResistanceProvider provider) {
        Objects.requireNonNull(provider, "provider");
        String id = validateProviderId(provider.providerId());
        if (providers.containsKey(id)) throw new IllegalArgumentException("duplicate corruption resistance provider: " + id);
        if (providers.size() >= maxProviders) throw new IllegalStateException("corruption resistance provider registry is full");
        providers.put(id, provider);
    }

    public synchronized CorruptionResistanceSnapshot snapshot(CorruptionResistanceQuery query) {
        Objects.requireNonNull(query, "query");
        List<Map.Entry<String, CorruptionResistanceProvider>> orderedProviders = new ArrayList<>(providers.entrySet());
        orderedProviders.sort(Map.Entry.comparingByKey());

        List<CorruptionResistanceSnapshot.ResolvedContribution> contributions = new ArrayList<>();
        List<String> diagnostics = new ArrayList<>();
        for (Map.Entry<String, CorruptionResistanceProvider> entry : orderedProviders) {
            if (contributions.size() >= ABSOLUTE_MAX_CONTRIBUTIONS) {
                diagnostics.add("corruption resistance contribution cap reached before provider " + entry.getKey());
                break;
            }
            collectProvider(entry.getKey(), entry.getValue(), query, contributions, diagnostics);
        }
        contributions.sort(Comparator
            .comparing(CorruptionResistanceSnapshot.ResolvedContribution::providerId)
            .thenComparing(CorruptionResistanceSnapshot.ResolvedContribution::sourceId)
            .thenComparing(contribution -> contribution.category().name()));

        EnumMap<CorruptionResistanceSourceCategory, Double> rawByCategory = zeroCategoryMap();
        for (CorruptionResistanceSnapshot.ResolvedContribution contribution : contributions) {
            double current = rawByCategory.get(contribution.category());
            rawByCategory.put(contribution.category(), saturatingFiniteAdd(current, contribution.amount()));
        }

        EnumMap<CorruptionResistanceSourceCategory, Double> effectiveByCategory = zeroCategoryMap();
        double effectiveTotal = 0.0D;
        for (CorruptionResistanceSourceCategory category : CorruptionResistanceSourceCategory.values()) {
            double effective = Math.min(rawByCategory.get(category), bucketCaps.get(category));
            effectiveByCategory.put(category, effective);
            effectiveTotal = saturatingFiniteAdd(effectiveTotal, effective);
        }
        effectiveTotal = Math.min(effectiveTotal, curve.maxResistance());
        return new CorruptionResistanceSnapshot(
            effectiveTotal,
            curve.residualMultiplier(effectiveTotal),
            curve.k(),
            curve.maxResistance(),
            contributions,
            effectiveByCategory,
            diagnostics);
    }

    public synchronized int size() {
        return providers.size();
    }

    private static void collectProvider(
        String providerId,
        CorruptionResistanceProvider provider,
        CorruptionResistanceQuery query,
        List<CorruptionResistanceSnapshot.ResolvedContribution> output,
        List<String> diagnostics
    ) {
        final List<CorruptionResistanceContribution> provided;
        try {
            provided = Objects.requireNonNull(provider.contributions(query), "provider contributions");
        } catch (RuntimeException | LinkageError failure) {
            diagnostics.add("corruption resistance provider failed closed: " + providerId);
            return;
        }
        if (provided.size() > MAX_CONTRIBUTIONS_PER_PROVIDER) {
            diagnostics.add("corruption resistance provider exceeded contribution cap: " + providerId);
            return;
        }
        if (output.size() + provided.size() > ABSOLUTE_MAX_CONTRIBUTIONS) {
            diagnostics.add("corruption resistance provider would exceed global contribution cap: " + providerId);
            return;
        }
        for (CorruptionResistanceContribution contribution : provided) {
            if (contribution == null) {
                diagnostics.add("corruption resistance provider returned null contribution: " + providerId);
                continue;
            }
            output.add(new CorruptionResistanceSnapshot.ResolvedContribution(
                providerId,
                contribution.sourceId(),
                contribution.category(),
                contribution.amount()));
        }
    }

    private static EnumMap<CorruptionResistanceSourceCategory, Double> zeroCategoryMap() {
        EnumMap<CorruptionResistanceSourceCategory, Double> result =
            new EnumMap<>(CorruptionResistanceSourceCategory.class);
        for (CorruptionResistanceSourceCategory category : CorruptionResistanceSourceCategory.values()) {
            result.put(category, 0.0D);
        }
        return result;
    }

    private static String validateProviderId(String providerId) {
        Objects.requireNonNull(providerId, "providerId");
        if (!PROVIDER_ID.matcher(providerId).matches()) {
            throw new IllegalArgumentException("invalid corruption resistance provider id: " + providerId);
        }
        return providerId;
    }

    private static double saturatingFiniteAdd(double first, double second) {
        double result = first + second;
        return Double.isFinite(result) ? result : CorruptionResistanceCurve.ABSOLUTE_MAX_RESISTANCE;
    }
}
