package dev.gustavopere.blackarcana.qa.catalog;

import com.mojang.logging.LogUtils;
import io.redspace.ironsspellbooks.api.registry.SpellRegistry;
import io.redspace.ironsspellbooks.api.spells.AbstractSpell;
import net.minecraft.resources.ResourceLocation;
import net.neoforged.fml.ModList;
import org.slf4j.Logger;

import java.util.Comparator;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;

/**
 * Emits a bounded, read-only runtime snapshot from public host APIs.
 *
 * <p>The output deliberately contains only target mod presence plus Iron's
 * spell registry identity and effective school/enabled/crafting values. It
 * never inspects provider implementation classes or reconstructs behavior.</p>
 */
final class CatalogRuntimeEvidence {
    static final String PREFIX = "[BLACK_ARCANA_CATALOG_PROBE]";
    static final int SCHEMA_VERSION = 1;

    private static final Logger LOGGER = LogUtils.getLogger();

    private static final List<String> TARGET_SPELL_NAMESPACES = List.of(
        "asterismarcanum",
        "gaze",
        "somakespells",
        "traveloptics"
    );

    private static final List<String> TARGET_MOD_IDS = List.of(
        "asterismarcanum",
        "gaze",
        "irons_spellbooks",
        "not_enough_glyphs",
        "somakespells",
        "traveloptics"
    );

    private CatalogRuntimeEvidence() {
    }

    static void emit() {
        LOGGER.info("{} type=begin schema={}", PREFIX, SCHEMA_VERSION);

        for (String modId : TARGET_MOD_IDS) {
            LOGGER.info("{} type=mod id={} loaded={}", PREFIX, modId, ModList.get().isLoaded(modId));
        }

        Map<String, Integer> counts = new TreeMap<>();
        SpellRegistry.REGISTRY.keySet().stream()
            .filter(CatalogRuntimeEvidence::isTargetSpell)
            .sorted(Comparator.comparing(ResourceLocation::toString))
            .forEach(id -> {
                counts.merge(id.getNamespace(), 1, Integer::sum);
                emitSpell(id);
            });

        for (String namespace : TARGET_SPELL_NAMESPACES) {
            LOGGER.info(
                "{} type=summary namespace={} registered_count={}",
                PREFIX,
                namespace,
                counts.getOrDefault(namespace, 0)
            );
        }

        LOGGER.info("{} type=end schema={}", PREFIX, SCHEMA_VERSION);
    }

    private static boolean isTargetSpell(ResourceLocation id) {
        return TARGET_SPELL_NAMESPACES.contains(id.getNamespace());
    }

    private static void emitSpell(ResourceLocation id) {
        AbstractSpell spell = SpellRegistry.REGISTRY.get(id);
        if (spell == null) {
            LOGGER.warn("{} type=spell id={} status=REGISTRY_VALUE_UNAVAILABLE", PREFIX, id);
            return;
        }

        try {
            ResourceLocation schoolId = spell.getSchoolType().getId();
            LOGGER.info(
                "{} type=spell id={} status=OBSERVED school={} enabled={} allow_crafting={}",
                PREFIX,
                id,
                schoolId,
                spell.isEnabled(),
                spell.allowCrafting()
            );
        } catch (RuntimeException unavailable) {
            LOGGER.warn(
                "{} type=spell id={} status=HOST_VALUE_UNAVAILABLE error={}",
                PREFIX,
                id,
                unavailable.getClass().getSimpleName()
            );
        }
    }
}
