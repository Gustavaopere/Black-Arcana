package dev.gustavopere.blackarcana.config;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParseException;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.packs.resources.ResourceManager;
import net.minecraft.server.packs.resources.SimpleJsonResourceReloadListener;
import net.minecraft.util.profiling.ProfilerFiller;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.event.AddReloadListenerEvent;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Objects;
import java.util.Set;

/**
 * Strict non-executable loader for the optional server-owned Astral movement control profile.
 *
 * <p>Files live under {@code data/<namespace>/black_arcana/astral_control/*.json}. No profile is bundled by
 * default; an empty reload clears the authority and keeps MOVE gameplay fail-closed.</p>
 */
public final class AstralControlDataReloadListener extends SimpleJsonResourceReloadListener {
    public static final String DIRECTORY = "black_arcana/astral_control";
    private static final Gson GSON = new GsonBuilder().disableHtmlEscaping().create();
    private static final Set<String> ALLOWED_KEYS = Set.of(
            "schemaVersion", "id", "scope", "maxStepBlocks", "maxLookDeltaDegrees");

    public AstralControlDataReloadListener() {
        super(GSON, DIRECTORY);
    }

    public static void register(IEventBus gameBus) {
        Objects.requireNonNull(gameBus, "gameBus");
        gameBus.addListener(AstralControlDataReloadListener::onAddReloadListeners);
    }

    private static void onAddReloadListeners(AddReloadListenerEvent event) {
        event.addListener(new AstralControlDataReloadListener());
    }

    @Override
    protected void apply(
            Map<ResourceLocation, JsonElement> resources,
            ResourceManager resourceManager,
            ProfilerFiller profiler
    ) {
        if (resources.size() > 1) {
            throw new JsonParseException("at most one Black Arcana Astral control profile may be active");
        }

        List<AstralControlDataDefinition> parsed = new ArrayList<>(resources.size());
        resources.entrySet().stream()
                .sorted(Map.Entry.comparingByKey(Comparator.comparing(ResourceLocation::toString)))
                .forEach(entry -> parsed.add(parseDefinition(entry.getKey(), entry.getValue())));

        // Publication occurs only after the complete reload snapshot has parsed and validated.
        AstralControlConfigAuthority.reload(parsed);
    }

    static AstralControlDataDefinition parseDefinition(ResourceLocation resourceId, JsonElement element) {
        Objects.requireNonNull(resourceId, "resourceId");
        Objects.requireNonNull(element, "element");
        if (!element.isJsonObject()) {
            throw new JsonParseException("Astral control profile must be a JSON object: " + resourceId);
        }

        JsonObject object = element.getAsJsonObject();
        for (String key : object.keySet()) {
            if (!ALLOWED_KEYS.contains(key)) {
                throw new JsonParseException("unknown field '" + key + "' in Astral control profile " + resourceId);
            }
        }

        String canonicalId = resourceId.getNamespace() + ':' + resourceId.getPath();
        AstralControlDataDefinition definition;
        try {
            definition = new AstralControlDataDefinition(
                    requiredInt(object, "schemaVersion", resourceId),
                    requiredString(object, "id", resourceId),
                    ConfigScope.valueOf(requiredString(object, "scope", resourceId).toUpperCase(Locale.ROOT)),
                    requiredDouble(object, "maxStepBlocks", resourceId),
                    requiredFloat(object, "maxLookDeltaDegrees", resourceId));
        } catch (IllegalArgumentException invalid) {
            throw new JsonParseException("invalid Astral control profile " + resourceId + ": " + invalid.getMessage(), invalid);
        }

        if (!canonicalId.equals(definition.id())) {
            throw new JsonParseException(
                    "Astral control profile id must match resource id: expected "
                            + canonicalId + " but got " + definition.id());
        }
        List<String> errors = definition.validate();
        if (!errors.isEmpty()) {
            throw new JsonParseException(
                    "invalid Astral control profile " + resourceId + ": " + String.join("; ", errors));
        }
        return definition;
    }

    private static JsonElement required(JsonObject object, String key, ResourceLocation resourceId) {
        JsonElement value = object.get(key);
        if (value == null || !value.isJsonPrimitive()) {
            throw new JsonParseException("required field '" + key + "' missing/invalid in " + resourceId);
        }
        return value;
    }

    private static String requiredString(JsonObject object, String key, ResourceLocation resourceId) {
        JsonElement value = required(object, key, resourceId);
        if (!value.getAsJsonPrimitive().isString()) {
            throw new JsonParseException("required string '" + key + "' missing/invalid in " + resourceId);
        }
        return value.getAsString();
    }

    private static int requiredInt(JsonObject object, String key, ResourceLocation resourceId) {
        JsonElement value = required(object, key, resourceId);
        if (!value.getAsJsonPrimitive().isNumber()) {
            throw new JsonParseException("required integer '" + key + "' missing/invalid in " + resourceId);
        }
        try {
            return new BigDecimal(value.getAsString()).intValueExact();
        } catch (ArithmeticException | NumberFormatException invalid) {
            throw new JsonParseException("required integer '" + key + "' missing/invalid in " + resourceId, invalid);
        }
    }

    private static double requiredDouble(JsonObject object, String key, ResourceLocation resourceId) {
        JsonElement value = required(object, key, resourceId);
        if (!value.getAsJsonPrimitive().isNumber()) {
            throw new JsonParseException("required number '" + key + "' missing/invalid in " + resourceId);
        }
        return value.getAsDouble();
    }

    private static float requiredFloat(JsonObject object, String key, ResourceLocation resourceId) {
        JsonElement value = required(object, key, resourceId);
        if (!value.getAsJsonPrimitive().isNumber()) {
            throw new JsonParseException("required number '" + key + "' missing/invalid in " + resourceId);
        }
        return value.getAsFloat();
    }
}
