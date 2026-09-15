package dev.gustavopere.blackarcana.config;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParseException;
import dev.gustavopere.blackarcana.api.ArcanaCost;
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
 * Strict non-executable loader for optional server-owned Astral invocation parameters.
 *
 * <p>Files live under {@code data/<namespace>/black_arcana/astral_invocation/*.json}. No profile is bundled
 * by default. Empty reload clears the authority, and loading this data never installs Astral Severance.</p>
 */
public final class AstralInvocationDataReloadListener extends SimpleJsonResourceReloadListener {
    public static final String DIRECTORY = "black_arcana/astral_invocation";
    private static final Gson GSON = new GsonBuilder().disableHtmlEscaping().create();
    private static final Set<String> ALLOWED_KEYS = Set.of(
            "schemaVersion", "id", "scope",
            "resourceId", "resourceAmount", "resourceUnit",
            "cooldownGroup", "cooldownDurationTicks", "cooldownPersistent",
            "channelMinimumTicks", "channelMaximumTicks",
            "projectionDurationTicks", "maxRangeBlocks");

    public AstralInvocationDataReloadListener() {
        super(GSON, DIRECTORY);
    }

    public static void register(IEventBus gameBus) {
        Objects.requireNonNull(gameBus, "gameBus");
        gameBus.addListener(AstralInvocationDataReloadListener::onAddReloadListeners);
    }

    private static void onAddReloadListeners(AddReloadListenerEvent event) {
        event.addListener(new AstralInvocationDataReloadListener());
    }

    @Override
    protected void apply(
            Map<ResourceLocation, JsonElement> resources,
            ResourceManager resourceManager,
            ProfilerFiller profiler
    ) {
        if (resources.size() > 1) {
            throw new JsonParseException("at most one Black Arcana Astral invocation profile may be active");
        }

        List<AstralInvocationDataDefinition> parsed = new ArrayList<>(resources.size());
        resources.entrySet().stream()
                .sorted(Map.Entry.comparingByKey(Comparator.comparing(ResourceLocation::toString)))
                .forEach(entry -> parsed.add(parseDefinition(entry.getKey(), entry.getValue())));

        AstralInvocationConfigAuthority.reload(parsed);
    }

    static AstralInvocationDataDefinition parseDefinition(ResourceLocation resourceId, JsonElement element) {
        Objects.requireNonNull(resourceId, "resourceId");
        Objects.requireNonNull(element, "element");
        if (!element.isJsonObject()) {
            throw new JsonParseException("Astral invocation profile must be a JSON object: " + resourceId);
        }

        JsonObject object = element.getAsJsonObject();
        for (String key : object.keySet()) {
            if (!ALLOWED_KEYS.contains(key)) {
                throw new JsonParseException("unknown field '" + key + "' in Astral invocation profile " + resourceId);
            }
        }

        String canonicalId = resourceId.getNamespace() + ':' + resourceId.getPath();
        AstralInvocationDataDefinition definition;
        try {
            definition = new AstralInvocationDataDefinition(
                    requiredInt(object, "schemaVersion", resourceId),
                    requiredString(object, "id", resourceId),
                    ConfigScope.valueOf(requiredString(object, "scope", resourceId).toUpperCase(Locale.ROOT)),
                    requiredString(object, "resourceId", resourceId),
                    requiredDouble(object, "resourceAmount", resourceId),
                    ArcanaCost.Unit.valueOf(requiredString(object, "resourceUnit", resourceId).toUpperCase(Locale.ROOT)),
                    requiredString(object, "cooldownGroup", resourceId),
                    requiredLong(object, "cooldownDurationTicks", resourceId),
                    requiredBoolean(object, "cooldownPersistent", resourceId),
                    requiredLong(object, "channelMinimumTicks", resourceId),
                    requiredLong(object, "channelMaximumTicks", resourceId),
                    requiredInt(object, "projectionDurationTicks", resourceId),
                    requiredDouble(object, "maxRangeBlocks", resourceId));
        } catch (IllegalArgumentException invalid) {
            throw new JsonParseException("invalid Astral invocation profile " + resourceId + ": " + invalid.getMessage(), invalid);
        }

        if (!canonicalId.equals(definition.id())) {
            throw new JsonParseException(
                    "Astral invocation profile id must match resource id: expected "
                            + canonicalId + " but got " + definition.id());
        }
        List<String> errors = definition.validate();
        if (!errors.isEmpty()) {
            throw new JsonParseException(
                    "invalid Astral invocation profile " + resourceId + ": " + String.join("; ", errors));
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
        try {
            return requiredNumber(object, key, resourceId).intValueExact();
        } catch (ArithmeticException invalid) {
            throw new JsonParseException("required integer '" + key + "' missing/invalid in " + resourceId, invalid);
        }
    }

    private static long requiredLong(JsonObject object, String key, ResourceLocation resourceId) {
        try {
            return requiredNumber(object, key, resourceId).longValueExact();
        } catch (ArithmeticException invalid) {
            throw new JsonParseException("required integer '" + key + "' missing/invalid in " + resourceId, invalid);
        }
    }

    private static BigDecimal requiredNumber(JsonObject object, String key, ResourceLocation resourceId) {
        JsonElement value = required(object, key, resourceId);
        if (!value.getAsJsonPrimitive().isNumber()) {
            throw new JsonParseException("required number '" + key + "' missing/invalid in " + resourceId);
        }
        try {
            return new BigDecimal(value.getAsString());
        } catch (NumberFormatException invalid) {
            throw new JsonParseException("required number '" + key + "' missing/invalid in " + resourceId, invalid);
        }
    }

    private static double requiredDouble(JsonObject object, String key, ResourceLocation resourceId) {
        JsonElement value = required(object, key, resourceId);
        if (!value.getAsJsonPrimitive().isNumber()) {
            throw new JsonParseException("required number '" + key + "' missing/invalid in " + resourceId);
        }
        return value.getAsDouble();
    }

    private static boolean requiredBoolean(JsonObject object, String key, ResourceLocation resourceId) {
        JsonElement value = required(object, key, resourceId);
        if (!value.getAsJsonPrimitive().isBoolean()) {
            throw new JsonParseException("required boolean '" + key + "' missing/invalid in " + resourceId);
        }
        return value.getAsBoolean();
    }
}
