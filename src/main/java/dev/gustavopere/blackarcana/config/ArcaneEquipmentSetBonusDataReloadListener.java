package dev.gustavopere.blackarcana.config;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParseException;
import dev.gustavopere.blackarcana.api.hazard.ArcaneEquipmentSetBonus;
import dev.gustavopere.blackarcana.core.hazard.ArcaneEquipmentSetBonusRegistry;
import dev.gustavopere.blackarcana.core.hazard.ArcaneEquipmentSetBonusRuntimeStore;
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

/** Strict non-executable datapack loader for cumulative containment equipment set thresholds. */
public final class ArcaneEquipmentSetBonusDataReloadListener extends SimpleJsonResourceReloadListener {
    public static final String DIRECTORY = "black_arcana/equipment_set_bonuses";
    private static final Gson GSON = new GsonBuilder().disableHtmlEscaping().create();
    private static final Set<String> ALLOWED_KEYS = Set.of(
        "schemaVersion", "id", "setId", "requiredPieces", "arcaneResistance",
        "corruptionResistance", "strainCapacityBonus", "strainRecoveryPerTick", "containmentTags");

    public ArcaneEquipmentSetBonusDataReloadListener() { super(GSON, DIRECTORY); }

    public static void register(IEventBus gameBus) {
        Objects.requireNonNull(gameBus, "gameBus");
        gameBus.addListener(ArcaneEquipmentSetBonusDataReloadListener::onAddReloadListeners);
    }

    private static void onAddReloadListeners(AddReloadListenerEvent event) {
        event.addListener(new ArcaneEquipmentSetBonusDataReloadListener());
    }

    @Override
    protected void apply(Map<ResourceLocation, JsonElement> resources, ResourceManager manager, ProfilerFiller profiler) {
        if (resources.size() > ArcaneEquipmentSetBonusRegistry.MAX_BONUSES) {
            throw new JsonParseException("too many Black Arcana equipment set bonuses: " + resources.size());
        }
        LinkedHashMap<String, ArcaneEquipmentSetBonus> parsed = new LinkedHashMap<>();
        resources.entrySet().stream()
            .sorted(Map.Entry.comparingByKey(Comparator.comparing(ResourceLocation::toString)))
            .forEach(entry -> {
                ArcaneEquipmentSetBonusDataDefinition definition = parseDefinition(entry.getKey(), entry.getValue());
                if (parsed.putIfAbsent(definition.id(), definition.bonus()) != null) {
                    throw new JsonParseException("duplicate containment set bonus: " + definition.id());
                }
            });
        ArcaneEquipmentSetBonusRuntimeStore.reload(parsed);
    }

    static ArcaneEquipmentSetBonusDataDefinition parseDefinition(ResourceLocation resourceId, JsonElement element) {
        Objects.requireNonNull(resourceId, "resourceId");
        if (element == null || !element.isJsonObject()) {
            throw new JsonParseException("equipment set bonus must be an object: " + resourceId);
        }
        JsonObject object = element.getAsJsonObject();
        for (String key : object.keySet()) {
            if (!ALLOWED_KEYS.contains(key)) {
                throw new JsonParseException("unknown field '" + key + "' in equipment set bonus " + resourceId);
            }
        }

        String canonicalId = resourceId.getNamespace() + ':' + resourceId.getPath();
        String declaredId = requiredString(object, "id", resourceId);
        if (!canonicalId.equals(declaredId)) {
            throw new JsonParseException(
                "equipment set bonus id must match resource id: expected " + canonicalId + " but got " + declaredId);
        }

        try {
            ArcaneEquipmentSetBonus bonus = new ArcaneEquipmentSetBonus(
                declaredId,
                requiredString(object, "setId", resourceId),
                requiredInt(object, "requiredPieces", resourceId),
                requiredDouble(object, "arcaneResistance", resourceId),
                requiredDouble(object, "corruptionResistance", resourceId),
                requiredDouble(object, "strainCapacityBonus", resourceId),
                requiredDouble(object, "strainRecoveryPerTick", resourceId),
                requiredStringSet(object, "containmentTags", resourceId));
            return new ArcaneEquipmentSetBonusDataDefinition(
                requiredInt(object, "schemaVersion", resourceId), declaredId, bonus);
        } catch (IllegalArgumentException invalid) {
            throw new JsonParseException("invalid equipment set bonus " + resourceId + ": " + invalid.getMessage(), invalid);
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
        double raw = value.getAsDouble();
        if (!Double.isFinite(raw) || raw != Math.rint(raw) || raw < Integer.MIN_VALUE || raw > Integer.MAX_VALUE) {
            throw new JsonParseException("required integer '" + key + "' missing/invalid in " + id);
        }
        return (int) raw;
    }

    private static double requiredDouble(JsonObject object, String key, ResourceLocation id) {
        JsonElement value = required(object, key, id);
        if (!value.getAsJsonPrimitive().isNumber()) {
            throw new JsonParseException("required number '" + key + "' missing/invalid in " + id);
        }
        double result = value.getAsDouble();
        if (!Double.isFinite(result)) throw new JsonParseException("required number '" + key + "' invalid in " + id);
        return result;
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
