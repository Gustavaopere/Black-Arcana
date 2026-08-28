package dev.gustavopere.blackarcana.config;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParseException;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntimeManager;
import dev.gustavopere.blackarcana.network.ArcanaProtocol;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.packs.resources.ResourceManager;
import net.minecraft.server.packs.resources.SimpleJsonResourceReloadListener;
import net.minecraft.util.profiling.ProfilerFiller;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.event.AddReloadListenerEvent;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Set;

/**
 * Strict datapack loader for presentation/identity metadata only.
 *
 * Files live under data/<namespace>/black_arcana/spells/*.json. The resource
 * location determines the canonical spell id; the JSON id must match it.
 * Execution logic, costs, targeting and world mutation are never supplied by this loader.
 */
public final class ArcanaSpellDataReloadListener extends SimpleJsonResourceReloadListener {
    public static final String DIRECTORY = "black_arcana/spells";
    private static final Gson GSON = new GsonBuilder().disableHtmlEscaping().create();
    private static final Set<String> ALLOWED_KEYS = Set.of("schemaVersion", "id", "translationKey", "iconId");

    public ArcanaSpellDataReloadListener() {
        super(GSON, DIRECTORY);
    }

    public static void register(IEventBus gameBus) {
        Objects.requireNonNull(gameBus, "gameBus");
        gameBus.addListener(ArcanaSpellDataReloadListener::onAddReloadListeners);
    }

    private static void onAddReloadListeners(AddReloadListenerEvent event) {
        event.addListener(new ArcanaSpellDataReloadListener());
    }

    @Override
    protected void apply(
            Map<ResourceLocation, JsonElement> resources,
            ResourceManager resourceManager,
            ProfilerFiller profiler
    ) {
        if (resources.size() > ArcanaProtocol.MAX_PRESENTATION_ENTRIES) {
            throw new JsonParseException("too many Black Arcana spell definitions: " + resources.size());
        }

        List<Map.Entry<ResourceLocation, JsonElement>> ordered = resources.entrySet().stream()
                .sorted(Map.Entry.comparingByKey(Comparator.comparing(ResourceLocation::toString)))
                .toList();
        List<SpellDataDefinition> definitions = new ArrayList<>(ordered.size());

        for (Map.Entry<ResourceLocation, JsonElement> entry : ordered) {
            ResourceLocation resourceId = entry.getKey();
            JsonElement element = entry.getValue();
            if (!element.isJsonObject()) {
                throw new JsonParseException("spell definition must be a JSON object: " + resourceId);
            }

            JsonObject object = element.getAsJsonObject();
            for (String key : object.keySet()) {
                if (!ALLOWED_KEYS.contains(key)) {
                    throw new JsonParseException("unknown field '" + key + "' in spell definition " + resourceId);
                }
            }

            String canonicalId = resourceId.getNamespace() + ":" + resourceId.getPath();
            SpellDataDefinition definition = new SpellDataDefinition(
                    requiredInt(object, "schemaVersion", resourceId),
                    requiredString(object, "id", resourceId),
                    requiredString(object, "translationKey", resourceId),
                    requiredString(object, "iconId", resourceId));

            if (!canonicalId.equals(definition.id())) {
                throw new JsonParseException(
                        "spell definition id must match resource id: expected " + canonicalId + " but got " + definition.id());
            }
            List<String> errors = definition.validate();
            if (!errors.isEmpty()) {
                throw new JsonParseException("invalid spell definition " + resourceId + ": " + String.join("; ", errors));
            }
            definitions.add(definition);
        }

        // Publication occurs only after the entire reload snapshot has parsed and validated.
        ArcanaServerRuntimeManager.reloadSpellData(definitions);
    }

    private static int requiredInt(JsonObject object, String key, ResourceLocation resourceId) {
        JsonElement value = object.get(key);
        if (value == null || !value.isJsonPrimitive() || !value.getAsJsonPrimitive().isNumber()) {
            throw new JsonParseException("required integer '" + key + "' missing/invalid in " + resourceId);
        }
        return value.getAsInt();
    }

    private static String requiredString(JsonObject object, String key, ResourceLocation resourceId) {
        JsonElement value = object.get(key);
        if (value == null || !value.isJsonPrimitive() || !value.getAsJsonPrimitive().isString()) {
            throw new JsonParseException("required string '" + key + "' missing/invalid in " + resourceId);
        }
        return value.getAsString();
    }
}
