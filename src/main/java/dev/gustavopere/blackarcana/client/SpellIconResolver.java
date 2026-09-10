package dev.gustavopere.blackarcana.client;

import dev.gustavopere.blackarcana.network.ArcanaProtocol;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.packs.resources.ResourceManagerReloadListener;
import net.neoforged.neoforge.client.event.RegisterClientReloadListenersEvent;

import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Objects;
import java.util.function.Predicate;

/** Client-only presentation resolver. Icon availability never changes spell identity or gameplay authority. */
final class SpellIconResolver {
    static final ResourceLocation PLACEHOLDER = ResourceLocation.fromNamespaceAndPath(
            "black_arcana", "textures/gui/spell_placeholder.png");
    private static final int MAX_CACHE_ENTRIES = ArcanaProtocol.MAX_PRESENTATION_ENTRIES;
    private static final Map<ResourceLocation, ResourceLocation> CACHE = new LinkedHashMap<>(16, 0.75F, true) {
        @Override
        protected boolean removeEldestEntry(Map.Entry<ResourceLocation, ResourceLocation> eldest) {
            return size() > MAX_CACHE_ENTRIES;
        }
    };

    private SpellIconResolver() {
    }

    static synchronized ResourceLocation resolve(
            String iconId,
            Predicate<ResourceLocation> resourceExists
    ) {
        Objects.requireNonNull(resourceExists, "resourceExists");
        if (iconId == null || iconId.isBlank()) return PLACEHOLDER;

        ResourceLocation requested = ResourceLocation.tryParse(iconId);
        if (requested == null) return PLACEHOLDER;

        ResourceLocation cached = CACHE.get(requested);
        if (cached != null) return cached;

        ResourceLocation resolved;
        try {
            resolved = resourceExists.test(requested) ? requested : PLACEHOLDER;
        } catch (RuntimeException ignored) {
            resolved = PLACEHOLDER;
        }
        CACHE.put(requested, resolved);
        return resolved;
    }

    static synchronized void invalidate() {
        CACHE.clear();
    }

    static synchronized int cachedEntryCount() {
        return CACHE.size();
    }

    static void registerReloadListener(RegisterClientReloadListenersEvent event) {
        Objects.requireNonNull(event, "event");
        event.registerReloadListener((ResourceManagerReloadListener) resourceManager -> invalidate());
    }
}
