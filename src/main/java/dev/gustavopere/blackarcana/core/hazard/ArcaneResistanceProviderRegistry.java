package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.hazard.ArcaneEmergencyProtectionSnapshot;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceContribution;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceProvider;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceQuery;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceSnapshot;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceSourceCategory;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.EnumMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.UUID;
import java.util.regex.Pattern;

/** Bounded deterministic provider aggregation for one Arcane Resistance snapshot. */
public final class ArcaneResistanceProviderRegistry {
    public static final int ABSOLUTE_MAX_PROVIDERS = 64;
    public static final int MAX_CONTRIBUTIONS_PER_PROVIDER = 64;
    public static final int ABSOLUTE_MAX_CONTRIBUTIONS = 512;
    private static final Pattern PROVIDER_ID = Pattern.compile("[a-z0-9_.:-]{1,64}");

    private final int maxProviders;
    private final ArcaneResistanceCurve curve;
    private final Map<ArcaneResistanceSourceCategory, Double> bucketCaps;
    private final Map<String, ArcaneResistanceProvider> providers = new LinkedHashMap<>();

    public ArcaneResistanceProviderRegistry(
        int maxProviders,
        ArcaneResistanceCurve curve,
        Map<ArcaneResistanceSourceCategory, Double> bucketCaps
    ) {
        if (maxProviders <= 0 || maxProviders > ABSOLUTE_MAX_PROVIDERS) {
            throw new IllegalArgumentException("maxProviders outside absolute bounds");
        }
        this.maxProviders = maxProviders;
        this.curve = Objects.requireNonNull(curve, "curve");
        Objects.requireNonNull(bucketCaps, "bucketCaps");
        EnumMap<ArcaneResistanceSourceCategory, Double> checked =
            new EnumMap<>(ArcaneResistanceSourceCategory.class);
        for (ArcaneResistanceSourceCategory category : ArcaneResistanceSourceCategory.values()) {
            Double cap = bucketCaps.get(category);
            if (cap == null || !Double.isFinite(cap) || cap < 0.0D
                || cap > ArcaneResistanceCurve.ABSOLUTE_MAX_RESISTANCE) {
                throw new IllegalArgumentException("missing/invalid bucket cap: " + category);
            }
            checked.put(category, cap);
        }
        this.bucketCaps = Map.copyOf(checked);
    }

    public static ArcaneResistanceProviderRegistry canonical(int maxProviders) {
        EnumMap<ArcaneResistanceSourceCategory, Double> caps =
            new EnumMap<>(ArcaneResistanceSourceCategory.class);
        for (ArcaneResistanceSourceCategory category : ArcaneResistanceSourceCategory.values()) {
            caps.put(category, ArcaneResistanceCurve.CANONICAL_MAX_RESISTANCE);
        }
        return new ArcaneResistanceProviderRegistry(maxProviders, ArcaneResistanceCurve.canonical(), caps);
    }

    public synchronized void register(ArcaneResistanceProvider provider) {
        Objects.requireNonNull(provider, "provider");
        String id = validateProviderId(provider.providerId());
        if (providers.containsKey(id)) throw new IllegalArgumentException("duplicate resistance provider: " + id);
        if (providers.size() >= maxProviders) throw new IllegalStateException("resistance provider registry is full");
        providers.put(id, provider);
    }

    public synchronized ArcaneResistanceSnapshot snapshot(ArcaneResistanceQuery query) {
        Objects.requireNonNull(query, "query");
        List<Map.Entry<String, ArcaneResistanceProvider>> orderedProviders = orderedProviders();

        List<ArcaneResistanceSnapshot.ResolvedContribution> contributions = new ArrayList<>();
        List<String> diagnostics = new ArrayList<>();
        for (Map.Entry<String, ArcaneResistanceProvider> entry : orderedProviders) {
            if (contributions.size() >= ABSOLUTE_MAX_CONTRIBUTIONS) {
                diagnostics.add("resistance contribution cap reached before provider " + entry.getKey());
                break;
            }
            collectProvider(entry.getKey(), entry.getValue(), query, contributions, diagnostics);
        }
        contributions.sort(Comparator
            .comparing(ArcaneResistanceSnapshot.ResolvedContribution::providerId)
            .thenComparing(ArcaneResistanceSnapshot.ResolvedContribution::sourceId)
            .thenComparing(contribution -> contribution.category().name()));

        EnumMap<ArcaneResistanceSourceCategory, Double> rawByCategory = zeroCategoryMap();
        for (ArcaneResistanceSnapshot.ResolvedContribution contribution : contributions) {
            double current = rawByCategory.get(contribution.category());
            rawByCategory.put(contribution.category(), saturatingFiniteAdd(current, contribution.amount()));
        }

        EnumMap<ArcaneResistanceSourceCategory, Double> effectiveByCategory = zeroCategoryMap();
        double effectiveTotal = 0.0D;
        for (ArcaneResistanceSourceCategory category : ArcaneResistanceSourceCategory.values()) {
            double effective = Math.min(rawByCategory.get(category), bucketCaps.get(category));
            effectiveByCategory.put(category, effective);
            effectiveTotal = saturatingFiniteAdd(effectiveTotal, effective);
        }
        effectiveTotal = Math.min(effectiveTotal, curve.maxResistance());
        double residual = curve.residualMultiplier(effectiveTotal);
        return new ArcaneResistanceSnapshot(
            effectiveTotal,
            residual,
            curve.k(),
            curve.maxResistance(),
            contributions,
            effectiveByCategory,
            diagnostics);
    }

    /**
     * Takes emergency facts from emergency-capable providers in provider-id order. Duplicate
     * resource identities are collapsed deterministically and the canonical snapshot cap is
     * enforced without skipping provider handoff/cleanup.
     */
    public synchronized ArcaneEmergencyProtectionSnapshot takeEmergencyProtectionSnapshot(
        ArcanaCastId castId,
        UUID casterId,
        long serverTick
    ) {
        Objects.requireNonNull(castId, "castId");
        Objects.requireNonNull(casterId, "casterId");
        if (serverTick < 0L) throw new IllegalArgumentException("serverTick cannot be negative");

        Map<String, ArcaneEmergencyProtectionSnapshot.Candidate> candidates = new LinkedHashMap<>();
        for (Map.Entry<String, ArcaneResistanceProvider> entry : orderedProviders()) {
            if (!(entry.getValue() instanceof ArcaneEmergencyProtectionSnapshotProvider provider)) continue;
            final ArcaneEmergencyProtectionSnapshot snapshot;
            try {
                snapshot = Objects.requireNonNull(
                    provider.takeEmergencySnapshot(castId, casterId, serverTick),
                    "emergency protection snapshot");
            } catch (RuntimeException | LinkageError failure) {
                continue;
            }
            for (ArcaneEmergencyProtectionSnapshot.Candidate candidate : snapshot.candidates()) {
                if (candidates.size() >= ArcaneEmergencyProtectionSnapshot.MAX_CANDIDATES) continue;
                candidates.putIfAbsent(candidate.resourceId(), candidate);
            }
        }
        return new ArcaneEmergencyProtectionSnapshot(new ArrayList<>(candidates.values()));
    }

    /** Releases emergency-capable provider caches when preflight terminates before handoff. */
    public synchronized void releaseEmergencyProtectionSnapshots(ArcanaCastId castId) {
        Objects.requireNonNull(castId, "castId");
        for (Map.Entry<String, ArcaneResistanceProvider> entry : orderedProviders()) {
            if (!(entry.getValue() instanceof ArcaneEmergencyProtectionSnapshotProvider provider)) continue;
            try {
                provider.release(castId);
            } catch (RuntimeException | LinkageError ignored) {
                // Emergency protection is optional; cleanup failures must not change cast semantics.
            }
        }
    }

    public synchronized int size() {
        return providers.size();
    }

    private List<Map.Entry<String, ArcaneResistanceProvider>> orderedProviders() {
        List<Map.Entry<String, ArcaneResistanceProvider>> ordered = new ArrayList<>(providers.entrySet());
        ordered.sort(Map.Entry.comparingByKey());
        return ordered;
    }

    private static void collectProvider(
        String providerId,
        ArcaneResistanceProvider provider,
        ArcaneResistanceQuery query,
        List<ArcaneResistanceSnapshot.ResolvedContribution> output,
        List<String> diagnostics
    ) {
        final List<ArcaneResistanceContribution> provided;
        try {
            provided = Objects.requireNonNull(provider.contributions(query), "provider contributions");
        } catch (RuntimeException | LinkageError failure) {
            diagnostics.add("resistance provider failed closed: " + providerId);
            return;
        }
        if (provided.size() > MAX_CONTRIBUTIONS_PER_PROVIDER) {
            diagnostics.add("resistance provider exceeded contribution cap: " + providerId);
            return;
        }
        if (output.size() + provided.size() > ABSOLUTE_MAX_CONTRIBUTIONS) {
            diagnostics.add("resistance provider would exceed global contribution cap: " + providerId);
            return;
        }
        for (ArcaneResistanceContribution contribution : provided) {
            if (contribution == null) {
                diagnostics.add("resistance provider returned null contribution: " + providerId);
                continue;
            }
            output.add(new ArcaneResistanceSnapshot.ResolvedContribution(
                providerId,
                contribution.sourceId(),
                contribution.category(),
                contribution.amount()));
        }
    }

    private static EnumMap<ArcaneResistanceSourceCategory, Double> zeroCategoryMap() {
        EnumMap<ArcaneResistanceSourceCategory, Double> result =
            new EnumMap<>(ArcaneResistanceSourceCategory.class);
        for (ArcaneResistanceSourceCategory category : ArcaneResistanceSourceCategory.values()) {
            result.put(category, 0.0D);
        }
        return result;
    }

    private static String validateProviderId(String providerId) {
        Objects.requireNonNull(providerId, "providerId");
        if (!PROVIDER_ID.matcher(providerId).matches()) {
            throw new IllegalArgumentException("invalid resistance provider id: " + providerId);
        }
        return providerId;
    }

    private static double saturatingFiniteAdd(double first, double second) {
        double result = first + second;
        return Double.isFinite(result) ? result : ArcaneResistanceCurve.ABSOLUTE_MAX_RESISTANCE;
    }
}
