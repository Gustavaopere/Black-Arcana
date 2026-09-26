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
        id("not_enough_glyphs", "plow"),
        id("not_enough_glyphs", "trail"),
        id("not_enough_glyphs", "ride"),
        id("not_enough_glyphs", "feed"),
        id("not_enough_glyphs", "filter_light"),
        id("not_enough_glyphs", "filter_dark"),
        id("not_enough_glyphs", "contingency_fall"),
        id("not_enough_glyphs", "contingency_heal"),
        id("not_enough_glyphs", "contingency_health"),
        id("not_enough_glyphs", "contingency_death"),
        id("not_enough_glyphs", "contingency_fire"),
        id("not_enough_glyphs", "contingency_blink"),
        id("not_enough_glyphs", "contingency_time"),
        id("not_enough_glyphs", "propagate_plane"),
        id("toomanyglyphs", "ray"),
        id("toomanyglyphs", "reverse_direction"),
        id("toomanyglyphs", "chaining"),
        id("toomanyglyphs", "filter_block"),
        id("toomanyglyphs", "filter_entity"),
        id("toomanyglyphs", "filter_living"),
        id("toomanyglyphs", "filter_living_not_monster"),
        id("toomanyglyphs", "filter_living_not_player"),
        id("toomanyglyphs", "filter_monster"),
        id("toomanyglyphs", "filter_player"),
        id("toomanyglyphs", "filter_item"),
        id("toomanyglyphs", "filter_animal"),
        id("toomanyglyphs", "filter_is_baby"),
        id("toomanyglyphs", "filter_is_mature"),
        id("ars_trinkets", "filter_self"),
        id("ars_trinkets", "filter_not_self"),
        id("arsomega", "flatten"),
        id("arsomega", "propagate_underfoot"),
        id("arsomega", "propagate_projectile"),
        id("arsomega", "propagate_self"),
        id("arsomega", "missile"),
        id("arsomega", "overhead"),
        id("arsomega", "propagate_missile"),
        id("arsomega", "propagate_overhead"),
        id("ars_scalaes", "resize")
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
