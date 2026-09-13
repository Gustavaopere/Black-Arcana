package dev.gustavopere.blackarcana.client;

import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.packs.resources.ResourceManagerReloadListener;
import net.neoforged.neoforge.client.event.RegisterClientReloadListenersEvent;

import java.util.EnumMap;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;
import java.util.function.Predicate;

/**
 * Project-owned Stage 05.15 audiovisual resource catalog.
 *
 * <p>Resource availability is presentation-only. Missing or malformed resources resolve to an
 * empty optional and must never change cast legality, settlement, cooldown, cost, target, or world
 * mutation authority.</p>
 */
final class CastPresentationResources {
    private static final Map<CastAudiovisualOrchestration.Kind, ResourceLocation> SOUND_EVENTS = Map.of(
            CastAudiovisualOrchestration.Kind.ANTICIPATION, id("cast.intent"),
            CastAudiovisualOrchestration.Kind.RESULT_SUCCESS, id("cast.success"),
            CastAudiovisualOrchestration.Kind.RESULT_DENIED, id("cast.denied"),
            CastAudiovisualOrchestration.Kind.RESULT_FAILED, id("cast.failed"));

    private static final Map<CastAudiovisualOrchestration.Kind, ResourceLocation> SOUND_ASSETS = Map.of(
            CastAudiovisualOrchestration.Kind.ANTICIPATION, asset("intent"),
            CastAudiovisualOrchestration.Kind.RESULT_SUCCESS, asset("success"),
            CastAudiovisualOrchestration.Kind.RESULT_DENIED, asset("denied"),
            CastAudiovisualOrchestration.Kind.RESULT_FAILED, asset("failed"));

    private static final EnumMap<CastAudiovisualOrchestration.Kind, Optional<ResourceLocation>> CACHE =
            new EnumMap<>(CastAudiovisualOrchestration.Kind.class);

    private CastPresentationResources() { }

    static ResourceLocation soundAsset(CastAudiovisualOrchestration.Kind kind) {
        return SOUND_ASSETS.get(Objects.requireNonNull(kind, "kind"));
    }

    static synchronized Optional<ResourceLocation> resolveSoundEvent(
            CastAudiovisualOrchestration.Kind kind,
            Predicate<ResourceLocation> resourceExists
    ) {
        Objects.requireNonNull(kind, "kind");
        Objects.requireNonNull(resourceExists, "resourceExists");

        Optional<ResourceLocation> cached = CACHE.get(kind);
        if (cached != null) return cached;

        Optional<ResourceLocation> resolved;
        try {
            resolved = resourceExists.test(soundAsset(kind))
                    ? Optional.of(SOUND_EVENTS.get(kind))
                    : Optional.empty();
        } catch (RuntimeException ignored) {
            resolved = Optional.empty();
        }
        CACHE.put(kind, resolved);
        return resolved;
    }

    static synchronized void invalidate() {
        CACHE.clear();
    }

    static synchronized int cachedEntryCount() {
        return CACHE.size();
    }

    static void registerReloadListener(RegisterClientReloadListenersEvent event) {
        Objects.requireNonNull(event, "event").registerReloadListener(
                (ResourceManagerReloadListener) resourceManager -> invalidate());
    }

    private static ResourceLocation id(String path) {
        return ResourceLocation.fromNamespaceAndPath("black_arcana", path);
    }

    private static ResourceLocation asset(String name) {
        return ResourceLocation.fromNamespaceAndPath("black_arcana", "sounds/cast/" + name + ".ogg");
    }
}
