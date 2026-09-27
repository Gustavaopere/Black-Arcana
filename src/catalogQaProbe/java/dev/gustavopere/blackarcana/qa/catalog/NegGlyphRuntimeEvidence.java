package dev.gustavopere.blackarcana.qa.catalog;

import com.hollingsworth.arsnouveau.api.registry.GlyphRegistry;
import com.hollingsworth.arsnouveau.api.spell.AbstractSpellPart;
import com.mojang.logging.LogUtils;
import net.minecraft.resources.ResourceLocation;
import org.slf4j.Logger;

import java.util.List;

/**
 * Emits only the exact 39 Not Enough Glyphs candidate IDs already present in
 * the canonical catalog. It does not enumerate the global Ars glyph registry.
 */
final class NegGlyphRuntimeEvidence {
    private static final Logger LOGGER = LogUtils.getLogger();

    private static final List<ResourceLocation> TARGET_GLYPHS = List.of(
        id("not_enough_glyphs", "glyph_plow"),
        id("not_enough_glyphs", "glyph_trail"),
        id("not_enough_glyphs", "glyph_ride"),
        id("not_enough_glyphs", "glyph_feed"),
        id("not_enough_glyphs", "glyph_filter_light"),
        id("not_enough_glyphs", "glyph_filter_dark"),
        id("not_enough_glyphs", "glyph_contingency_fall"),
        id("not_enough_glyphs", "glyph_contingency_heal"),
        id("not_enough_glyphs", "glyph_contingency_health"),
        id("not_enough_glyphs", "glyph_contingency_death"),
        id("not_enough_glyphs", "glyph_contingency_fire"),
        id("not_enough_glyphs", "glyph_contingency_blink"),
        id("not_enough_glyphs", "glyph_contingency_time"),
        id("not_enough_glyphs", "glyph_propagate_plane"),
        id("toomanyglyphs", "glyph_ray"),
        id("toomanyglyphs", "glyph_reverse_direction"),
        id("toomanyglyphs", "glyph_chaining"),
        id("toomanyglyphs", "glyph_filter_block"),
        id("toomanyglyphs", "glyph_filter_entity"),
        id("toomanyglyphs", "glyph_filter_living"),
        id("toomanyglyphs", "glyph_filter_living_not_monster"),
        id("toomanyglyphs", "glyph_filter_living_not_player"),
        id("toomanyglyphs", "glyph_filter_monster"),
        id("toomanyglyphs", "glyph_filter_player"),
        id("toomanyglyphs", "glyph_filter_item"),
        id("toomanyglyphs", "glyph_filter_animal"),
        id("toomanyglyphs", "glyph_filter_is_baby"),
        id("toomanyglyphs", "glyph_filter_is_mature"),
        id("ars_trinkets", "glyph_filter_self"),
        id("ars_trinkets", "glyph_filter_not_self"),
        id("arsomega", "glyph_flatten"),
        id("arsomega", "glyph_propagate_underfoot"),
        id("arsomega", "glyph_propagate_projectile"),
        id("arsomega", "glyph_propagate_self"),
        id("arsomega", "glyph_missile"),
        id("arsomega", "glyph_overhead"),
        id("arsomega", "glyph_propagate_missile"),
        id("arsomega", "glyph_propagate_overhead"),
        id("ars_scalaes", "glyph_resize")
    );

    private NegGlyphRuntimeEvidence() {
    }

    static void emit() {
        for (ResourceLocation id : TARGET_GLYPHS) {
            emitGlyph(id);
        }
    }

    private static void emitGlyph(ResourceLocation id) {
        AbstractSpellPart part = GlyphRegistry.getSpellPart(id);
        if (part == null) {
            LOGGER.warn(
                "{} type=glyph id={} status=NOT_REGISTERED",
                CatalogRuntimeEvidence.PREFIX,
                id
            );
            return;
        }

        try {
            LOGGER.info(
                "{} type=glyph id={} status=OBSERVED enabled={}",
                CatalogRuntimeEvidence.PREFIX,
                id,
                part.isEnabled()
            );
        } catch (RuntimeException unavailable) {
            LOGGER.warn(
                "{} type=glyph id={} status=HOST_VALUE_UNAVAILABLE error={}",
                CatalogRuntimeEvidence.PREFIX,
                id,
                unavailable.getClass().getSimpleName()
            );
        }
    }

    private static ResourceLocation id(String namespace, String path) {
        return ResourceLocation.fromNamespaceAndPath(namespace, path);
    }
}
