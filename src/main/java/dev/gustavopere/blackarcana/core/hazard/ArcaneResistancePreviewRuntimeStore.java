package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceProvider;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceQuery;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceSnapshot;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;

import java.util.Collections;
import java.util.IdentityHashMap;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;

/**
 * Runtime-scoped mirror containing only providers that explicitly support side-effect-free
 * presentation queries. The gameplay registry remains authoritative; previews fail closed if
 * the mirror does not cover every currently installed Arcane Resistance provider.
 */
public final class ArcaneResistancePreviewRuntimeStore {
    private static final Map<ArcanaServerRuntime, ArcaneResistanceProviderRegistry> PREVIEWS =
        Collections.synchronizedMap(new IdentityHashMap<>());

    private ArcaneResistancePreviewRuntimeStore() { }

    public static void register(ArcanaServerRuntime runtime, ArcaneResistanceProvider provider) {
        Objects.requireNonNull(runtime, "runtime");
        Objects.requireNonNull(provider, "provider");
        previewRegistry(runtime).register(provider);
    }

    public static Optional<ArcaneResistanceSnapshot> snapshotIfComplete(
        ArcanaServerRuntime runtime,
        ArcaneResistanceQuery query
    ) {
        Objects.requireNonNull(runtime, "runtime");
        Objects.requireNonNull(query, "query");
        ArcaneResistanceProviderRegistry preview;
        synchronized (PREVIEWS) {
            preview = PREVIEWS.get(runtime);
        }
        if (preview == null || preview.size() != runtime.arcaneResistanceProviders().size()) {
            return Optional.empty();
        }
        return Optional.of(preview.snapshot(query));
    }

    public static int previewProviderCount(ArcanaServerRuntime runtime) {
        Objects.requireNonNull(runtime, "runtime");
        synchronized (PREVIEWS) {
            ArcaneResistanceProviderRegistry preview = PREVIEWS.get(runtime);
            return preview == null ? 0 : preview.size();
        }
    }

    public static void remove(ArcanaServerRuntime runtime) {
        if (runtime == null) return;
        synchronized (PREVIEWS) {
            PREVIEWS.remove(runtime);
        }
    }

    private static ArcaneResistanceProviderRegistry previewRegistry(ArcanaServerRuntime runtime) {
        synchronized (PREVIEWS) {
            return PREVIEWS.computeIfAbsent(
                runtime,
                ignored -> ArcaneResistanceProviderRegistry.canonical(
                    ArcaneResistanceProviderRegistry.ABSOLUTE_MAX_PROVIDERS));
        }
    }
}
