package dev.gustavopere.blackarcana.content.noetic;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.UUID;

/** Bounded registry for familiar ownership providers. Provider faults never grant ownership. */
public final class FamiliarOwnershipRegistry {
    private static final int MAX_PROVIDER_ID_LENGTH = 96;

    private final int maxProviders;
    private final Map<String, FamiliarOwnershipProvider> providers = new LinkedHashMap<>();

    public FamiliarOwnershipRegistry(int maxProviders) {
        if (maxProviders <= 0 || maxProviders > NoeticSafetyCeilings.MAX_FAMILIAR_PROVIDERS) {
            throw new IllegalArgumentException("Familiar provider limit exceeds the hard Noetic ceiling");
        }
        this.maxProviders = maxProviders;
    }

    public synchronized boolean register(FamiliarOwnershipProvider provider) {
        Objects.requireNonNull(provider, "provider");
        final String id;
        try {
            id = normalizeProviderId(provider.providerId());
        } catch (RuntimeException | LinkageError failure) {
            return false;
        }
        if (id == null || providers.containsKey(id) || providers.size() >= maxProviders) return false;
        providers.put(id, provider);
        return true;
    }

    public FamiliarOwnershipProvider.Result ownership(UUID ownerId, Object candidate) {
        Objects.requireNonNull(ownerId, "ownerId");
        Objects.requireNonNull(candidate, "candidate");

        final List<FamiliarOwnershipProvider> snapshot;
        synchronized (this) {
            snapshot = new ArrayList<>(providers.values());
        }
        if (snapshot.isEmpty()) return FamiliarOwnershipProvider.Result.UNSUPPORTED;

        boolean sawNotOwned = false;
        for (FamiliarOwnershipProvider provider : snapshot) {
            final FamiliarOwnershipProvider.Result result;
            try {
                result = provider.ownership(ownerId, candidate);
            } catch (RuntimeException | LinkageError failure) {
                continue;
            }
            if (result == FamiliarOwnershipProvider.Result.OWNED) {
                return FamiliarOwnershipProvider.Result.OWNED;
            }
            if (result == FamiliarOwnershipProvider.Result.NOT_OWNED) {
                sawNotOwned = true;
            }
        }
        return sawNotOwned
                ? FamiliarOwnershipProvider.Result.NOT_OWNED
                : FamiliarOwnershipProvider.Result.UNSUPPORTED;
    }

    public synchronized int providerCount() {
        return providers.size();
    }

    private static String normalizeProviderId(String providerId) {
        if (providerId == null) return null;
        String normalized = providerId.trim();
        if (normalized.isEmpty() || normalized.length() > MAX_PROVIDER_ID_LENGTH) return null;
        for (int i = 0; i < normalized.length(); i++) {
            if (Character.isISOControl(normalized.charAt(i))) return null;
        }
        return normalized;
    }
}
