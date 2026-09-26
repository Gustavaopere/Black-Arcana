package dev.gustavopere.blackarcana.qa.catalog;

import com.mojang.logging.LogUtils;
import io.redspace.ironsspellbooks.api.registry.SpellRegistry;
import io.redspace.ironsspellbooks.api.spells.AbstractSpell;
import net.minecraft.resources.ResourceLocation;
import net.neoforged.fml.ModList;
import net.neoforged.neoforge.registries.NeoForgeRegistries;
import org.slf4j.Logger;

import java.util.Comparator;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;

/**
 * Emits a bounded, read-only runtime snapshot from public host APIs.
 *
 * <p>The output deliberately contains only target mod presence, Iron's spell
 * registry identity/effective host values, the bounded Not Enough Glyphs
 * effective Ars glyph state, and the two Traveloptics global loot-modifier
 * serializer registrations required by its historical closure checklist.
 * It never inspects provider implementation classes or reconstructs behavior.</p>
 */
final class CatalogRuntimeEvidence {
    static final String PREFIX = "[BLACK_ARCANA_CATALOG_PROBE]";
    static final int SCHEMA_VERSION = 3;

    private static final Logger LOGGER = LogUtils.getLogger();

    private static final List<String> TARGET_SPELL_NAMESPACES = List.of(
        "asterismarcanum",
        "gaze",
        "somakespells",
        "traveloptics"
    );

    private static final List<String> TARGET_MOD_IDS = List.of(
        "ars_nouveau",
        "asterismarcanum",
        "gaze",
        "irons_spellbooks",
        "not_enough_glyphs",
        "somakespells",
        "traveloptics"
    );

    private static final ResourceLocation TRAVELOPTICS_KEY_LOOT =
        ResourceLocation.fromNamespaceAndPath("traveloptics", "key_loot");
    private static final ResourceLocation TRAVELOPTICS_UNIVERSAL_LOOT =
        ResourceLocation.fromNamespaceAndPath("traveloptics", "universal_loot");

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

        if (ModList.get().isLoaded("ars_nouveau") && ModList.get().isLoaded("not_enough_glyphs")) {
            NegGlyphRuntimeEvidence.emit();
        }

        emitTravelopticsLootModifierRegistry();

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

    private static void emitTravelopticsLootModifierRegistry() {
        try {
            Object keyLootCodec = NeoForgeRegistries.GLOBAL_LOOT_MODIFIER_SERIALIZERS
                .getOptional(TRAVELOPTICS_KEY_LOOT)
                .orElse(null);
            Object universalLootCodec = NeoForgeRegistries.GLOBAL_LOOT_MODIFIER_SERIALIZERS
                .getOptional(TRAVELOPTICS_UNIVERSAL_LOOT)
                .orElse(null);

            emitLootModifierSerializer(TRAVELOPTICS_KEY_LOOT, keyLootCodec != null);
            emitLootModifierSerializer(TRAVELOPTICS_UNIVERSAL_LOOT, universalLootCodec != null);

            if (keyLootCodec != null && universalLootCodec != null) {
                LOGGER.info(
                    "{} type=loot_modifier_pair namespace=traveloptics status=OBSERVED distinct_codec_instances={}",
                    PREFIX,
                    keyLootCodec != universalLootCodec
                );
            } else {
                LOGGER.warn(
                    "{} type=loot_modifier_pair namespace=traveloptics status=INCOMPLETE key_loot_present={} universal_loot_present={}",
                    PREFIX,
                    keyLootCodec != null,
                    universalLootCodec != null
                );
            }
        } catch (RuntimeException unavailable) {
            LOGGER.warn(
                "{} type=loot_modifier_pair namespace=traveloptics status=REGISTRY_VALUE_UNAVAILABLE error={}",
                PREFIX,
                unavailable.getClass().getSimpleName()
            );
        }
    }

    private static void emitLootModifierSerializer(ResourceLocation id, boolean present) {
        LOGGER.info(
            "{} type=loot_modifier_serializer id={} status={}",
            PREFIX,
            id,
            present ? "OBSERVED" : "NOT_PRESENT"
        );
    }
}
