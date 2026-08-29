package dev.gustavopere.blackarcana.config;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParseException;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDangerTier;
import dev.gustavopere.blackarcana.core.hazard.ArcaneDangerProfileRegistry;
import dev.gustavopere.blackarcana.network.neoforge.HazardPreflightSyncService;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.packs.resources.ResourceManager;
import net.minecraft.server.packs.resources.SimpleJsonResourceReloadListener;
import net.minecraft.util.profiling.ProfilerFiller;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.event.AddReloadListenerEvent;

import java.util.Comparator;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Objects;
import java.util.Set;

/** Strict, non-executable datapack loader for Stage 05A danger profiles. */
public final class ArcaneDangerDataReloadListener extends SimpleJsonResourceReloadListener {
    public static final String DIRECTORY = "black_arcana/hazards";
    private static final Gson GSON = new GsonBuilder().disableHtmlEscaping().create();
    private static final Set<String> ALLOWED_KEYS = Set.of(
        "schemaVersion", "profileVersion", "id", "tier", "backlashMultiplier",
        "corruptionCoefficient", "strainCoefficient", "damageLeaseTicks", "maxDamageInstances",
        "minimumArcaneResistance", "recommendedArcaneResistance", "emergencyProtectionAllowed");

    public ArcaneDangerDataReloadListener() { super(GSON, DIRECTORY); }

    public static void register(IEventBus gameBus) {
        Objects.requireNonNull(gameBus, "gameBus");
        gameBus.addListener(ArcaneDangerDataReloadListener::onAddReloadListeners);
    }

    private static void onAddReloadListeners(AddReloadListenerEvent event) {
        event.addListener(new ArcaneDangerDataReloadListener());
    }

    @Override
    protected void apply(Map<ResourceLocation, JsonElement> resources, ResourceManager manager, ProfilerFiller profiler) {
        if (resources.size() > ArcaneDangerProfileRegistry.MAX_PROFILES) {
            throw new JsonParseException("too many Black Arcana danger profiles: " + resources.size());
        }
        LinkedHashMap<ArcanaSpellId, ArcaneDangerDataDefinition> parsed = new LinkedHashMap<>();
        resources.entrySet().stream()
            .sorted(Map.Entry.comparingByKey(Comparator.comparing(ResourceLocation::toString)))
            .forEach(entry -> {
                ArcaneDangerDataDefinition definition = parseDefinition(entry.getKey(), entry.getValue());
                ArcanaSpellId id = ArcanaSpellId.parse(definition.id());
                if (parsed.putIfAbsent(id, definition) != null) {
                    throw new JsonParseException("duplicate danger profile: " + id.canonical());
                }
            });
        HazardPreflightSyncService.reload(parsed);
    }

    static ArcaneDangerDataDefinition parseDefinition(ResourceLocation resourceId, JsonElement element) {
        Objects.requireNonNull(resourceId, "resourceId");
        if (element == null || !element.isJsonObject()) throw new JsonParseException("danger profile must be an object: " + resourceId);
        JsonObject object = element.getAsJsonObject();
        for (String key : object.keySet()) {
            if (!ALLOWED_KEYS.contains(key)) throw new JsonParseException("unknown field '" + key + "' in danger profile " + resourceId);
        }
        String canonical = resourceId.getNamespace() + ':' + resourceId.getPath();
        ArcaneDangerDataDefinition definition;
        try {
            definition = new ArcaneDangerDataDefinition(
                requiredInt(object, "schemaVersion", resourceId),
                requiredInt(object, "profileVersion", resourceId),
                requiredString(object, "id", resourceId),
                ArcaneDangerTier.valueOf(requiredString(object, "tier", resourceId).toUpperCase(java.util.Locale.ROOT)),
                requiredDouble(object, "backlashMultiplier", resourceId),
                requiredDouble(object, "corruptionCoefficient", resourceId),
                requiredDouble(object, "strainCoefficient", resourceId),
                requiredLong(object, "damageLeaseTicks", resourceId),
                requiredInt(object, "maxDamageInstances", resourceId),
                requiredDouble(object, "minimumArcaneResistance", resourceId),
                requiredDouble(object, "recommendedArcaneResistance", resourceId),
                requiredBoolean(object, "emergencyProtectionAllowed", resourceId));
        } catch (IllegalArgumentException invalid) {
            throw new JsonParseException("invalid danger profile " + resourceId + ": " + invalid.getMessage(), invalid);
        }
        if (!canonical.equals(definition.id())) {
            throw new JsonParseException("danger profile id must match resource id: expected " + canonical + " but got " + definition.id());
        }
        var errors = definition.validate();
        if (!errors.isEmpty()) throw new JsonParseException("invalid danger profile " + resourceId + ": " + String.join("; ", errors));
        return definition;
    }

    private static JsonElement required(JsonObject object, String key, ResourceLocation id) {
        JsonElement value = object.get(key);
        if (value == null || !value.isJsonPrimitive()) throw new JsonParseException("required field '" + key + "' missing/invalid in " + id);
        return value;
    }
    private static String requiredString(JsonObject o, String k, ResourceLocation id) { return required(o,k,id).getAsString(); }
    private static int requiredInt(JsonObject o, String k, ResourceLocation id) { return required(o,k,id).getAsInt(); }
    private static long requiredLong(JsonObject o, String k, ResourceLocation id) { return required(o,k,id).getAsLong(); }
    private static double requiredDouble(JsonObject o, String k, ResourceLocation id) { return required(o,k,id).getAsDouble(); }
    private static boolean requiredBoolean(JsonObject o, String k, ResourceLocation id) { return required(o,k,id).getAsBoolean(); }
}
