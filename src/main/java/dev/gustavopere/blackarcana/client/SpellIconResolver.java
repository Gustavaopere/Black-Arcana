package dev.gustavopere.blackarcana.client;

import net.minecraft.resources.ResourceLocation;

import java.util.Objects;
import java.util.function.Predicate;

/** Client-only presentation resolver. Icon availability never changes spell identity or gameplay authority. */
final class SpellIconResolver {
    static final ResourceLocation PLACEHOLDER = ResourceLocation.fromNamespaceAndPath(
            "black_arcana", "textures/gui/spell_placeholder.png");

    private SpellIconResolver() {
    }

    static ResourceLocation resolve(
            String iconId,
            Predicate<ResourceLocation> resourceExists
    ) {
        Objects.requireNonNull(resourceExists, "resourceExists");
        if (iconId == null || iconId.isBlank()) return PLACEHOLDER;

        ResourceLocation requested = ResourceLocation.tryParse(iconId);
        if (requested == null) return PLACEHOLDER;

        try {
            return resourceExists.test(requested) ? requested : PLACEHOLDER;
        } catch (RuntimeException ignored) {
            return PLACEHOLDER;
        }
    }
}
