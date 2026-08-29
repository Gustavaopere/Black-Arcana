package dev.gustavopere.blackarcana.config;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParseException;
import dev.gustavopere.blackarcana.api.hazard.ArcaneEquipmentProfile;
import dev.gustavopere.blackarcana.core.hazard.ArcaneEquipmentProfileRegistry;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntimeManager;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.packs.resources.ResourceManager;
import net.minecraft.server.packs.resources.SimpleJsonResourceReloadListener;
import net.minecraft.util.profiling.ProfilerFiller;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.event.AddReloadListenerEvent;

import java.util.Comparator;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.Map;
import java.util.Objects;
import java.util.Set;

/** Strict non-executable datapack loader for explicit Stage 05A containment equipment profiles. */
public final class ArcaneEquipmentDataReloadListener extends SimpleJsonResourceReloadListener {
    public static final String DIRECTORY = "black_arcana/equipment_profiles";
    private static final Gson GSON = new GsonBuilder().disableHtmlEscaping().create();
    private static final Set<String> ALLOWED_KEYS = Set.of(
        "schemaVersion", "id", "itemId", "arcaneResistance", "corruptionResistance",
        "strainCapacityBonus", "strainRecoveryPerTick", "setId", "containmentTags");

    public ArcaneEquipmentDataReloadListener() {
        super(GSON, DIRECTORY);
    }

    public static void register(IEventBus gameBus) {
        Objects.requireNonNull(gameBus, "gameBus");
        gameBus.addListener(ArcaneEquipmentDataReloadListener::onAddReloadListeners);
    }

    private static void onAddReloadListeners(AddReloadListenerEvent event) {
        event.addListener(new ArcaneEquipmentDataReloadListener());
    }

    @Override
    protected void apply(Map<ResourceLocation, JsonElement> resources, ResourceManager manager, ProfilerFiller profiler) {
        if (resources.size() > ArcaneEquipmentProfileRegistry.MAX_PROFILES) {
            throw new JsonParseException("too many Black Arcana equipment profiles: " + resources.size());
        }
        LinkedHashMap<String, ArcaneEquipmentProfile> parsed = new LinkedHashMap<>();
        resources.entrySet().stream()
            .sorted(Map.Entry.comparingByKey(Comparator.comparing(ResourceLocation::toString)))
            .forEach(entry -> {
                ArcaneEquipmentDataDefinition definition = parseDefinition(entry.getKey(), entry.getValue());
                if (parsed.putIfAbsent(definition.itemId(), definition.profile()) != null) {
                    throw new JsonParseException("duplicate containment profile for item: " + definition.itemId());
                }
            });

        // Publish only after the complete snapshot has parsed and validated.
        ArcanaServerRuntimeManager.reloadEquipmentProfiles(parsed);
    }

    static ArcaneEquipmentDataDefinition parseDefinition(ResourceLocation resourceId, JsonElement element) {
        Objects.requireNonNull(resourceId, "resourceId");
        if (element == null || !element.isJsonObject()) {
            throw new JsonParseException("equipment profile must be an object: " + resourceId);
        }
        JsonObject object = element.getAsJsonObject();
        for (String key : object.keySet()) {
            if (!ALLOWED_KEYS.contains(key)) {
                throw new JsonParseException("unknown field '" + key + "' in equipment profile " + resourceId);
            }
        }

        String canonicalId = resourceId.getNamespace() + ':' + resourceId.getPath();
        String declaredId = requiredString(object, "id", resourceId);
        if (!canonicalId.equals(declaredId)) {
            throw new JsonParseException(
                "equipment profile id must match resource id: expected " + canonicalId + " but got " + declaredId);
        }

        String itemId = requiredString(object, "itemId", resourceId);
        Set<String> tags = requiredStringSet(object, "containmentTags", resourceId);
        String setId = optionalString(object, "setId", resourceId);
        try {
            ArcaneEquipmentProfile profile = new ArcaneEquipmentProfile(
                declaredId,
                requiredDouble(object, "arcaneResistance", resourceId),
                requiredDouble(object, "corruptionResistance", resourceId),
                requiredDouble(object, "strainCapacityBonus", resourceId),
                requiredDouble(object, "strainRecoveryPerTick", resourceId),
                setId,
                tags);
            ArcaneEquipmentProfileRegistry validator = new ArcaneEquipmentProfileRegistry();
            validator.register(itemId, profile);
            return new ArcaneEquipmentDataDefinition(
                requiredInt(object, "schemaVersion", resourceId),
                declaredId,
                itemId,
                profile);
        } catch (IllegalArgumentException | IllegalStateException invalid) {
            throw new JsonParseException("invalid equipment profile " + resourceId + ": " + invalid.getMessage(), invalid);
        }
    }

    private static JsonElement required(JsonObject object, String key, ResourceLocation id) {
        JsonElement value = object.get(key);
        if (value == null || !value.isJsonPrimitive()) {
            throw new JsonParseException("required field '" + key + "' missing/invalid in " + id);
        }
        return value;
    }

    private static String requiredString(JsonObject object, String key, ResourceLocation id) {
        JsonElement value = required(object, key, id);
        if (!value.getAsJsonPrimitive().isString()) {
            throw new JsonParseException("required string '" + key + "' missing/invalid in " + id);
        }
        return value.getAsString();
    }

    private static int requiredInt(JsonObject object, String key, ResourceLocation id) {
        JsonElement value = required(object, key, id);
        if (!value.getAsJsonPrimitive().isNumber()) {
            throw new JsonParseException("required integer '" + key + "' missing/invalid in " + id);
        }
        return value.getAsInt();
    }

    private static double requiredDouble(JsonObject object, String key, ResourceLocation id) {
        JsonElement value = required(object, key, id);
        if (!value.getAsJsonPrimitive().isNumber()) {
            throw new JsonParseException("required number '" + key + "' missing/invalid in " + id);
        }
        return value.getAsDouble();
    }

    private static String optionalString(JsonObject object, String key, ResourceLocation id) {
        JsonElement value = object.get(key);
        if (value == null || value.isJsonNull()) return null;
        if (!value.isJsonPrimitive() || !value.getAsJsonPrimitive().isString()) {
            throw new JsonParseException("optional string '" + key + "' invalid in " + id);
        }
        return value.getAsString();
    }

    private static Set<String> requiredStringSet(JsonObject object, String key, ResourceLocation id) {
        JsonElement value = object.get(key);
        if (value == null || !value.isJsonArray()) {
            throw new JsonParseException("required array '" + key + "' missing/invalid in " + id);
        }
        LinkedHashSet<String> result = new LinkedHashSet<>();
        value.getAsJsonArray().forEach(element -> {
            if (!element.isJsonPrimitive() || !element.getAsJsonPrimitive().isString()) {
                throw new JsonParseException("array '" + key + "' must contain strings in " + id);
            }
            if (!result.add(element.getAsString())) {
                throw new JsonParseException("array '" + key + "' contains duplicate values in " + id);
            }
        });
        return Set.copyOf(result);
    }
}
