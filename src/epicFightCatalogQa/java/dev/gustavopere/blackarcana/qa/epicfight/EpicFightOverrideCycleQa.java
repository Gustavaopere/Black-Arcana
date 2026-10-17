package dev.gustavopere.blackarcana.qa.epicfight;

import com.mojang.logging.LogUtils;
import com.google.gson.JsonArray;
import com.google.gson.JsonObject;
import net.minecraft.core.Registry;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.MinecraftServer;
import net.minecraft.world.level.storage.LevelResource;
import net.neoforged.neoforge.server.ServerLifecycleHooks;
import org.slf4j.Logger;

import java.io.IOException;
import java.lang.reflect.Field;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Map;
import java.util.LinkedHashMap;
import java.util.Set;

/**
 * Explicitly opt-in, disposable QA-only datapack lifecycle probe.
 * Uses a new Black Arcana-owned JSON fixture; never distributes or rewrites
 * any publisher resource. Does not equip skills or touch player attributes.
 */
final class EpicFightOverrideCycleQa {
    private static final Logger LOG = LogUtils.getLogger();
    private static final String PREFIX = "[BLACK_ARCANA_EPICFIGHT_OVERRIDE_QA]";
    private static final String PACK_FOLDER = "black_arcana_epicfight_override_qa";
    private static final String OVERRIDE_JSON = """
        {
          "attribute_modifiers": [
            {
              "attribute": "minecraft:generic.max_health",
              "id": "black_arcana_epicfight_qa:adaptive_skin_control",
              "operation": "add_value",
              "amount": 6.0
            }
          ]
        }
        """;
    private static final Map<String, Integer> BASELINE_COUNTS = Map.of(
        "adaptive_skin", 0,
        "adrenaline_fiend", 0,
        "catharsis", 0,
        "bonebreaker", 0,
        "vengeance", 0,
        "swordmaster", 2,
        "forbidden_strength", 2,
        "technician", 1
    );

    private static final boolean ALL_LEGACY = "1".equals(System.getenv("BLACK_ARCANA_EPICFIGHT_QA_ALL_LEGACY"));

    // Original QA fixtures built from physically audited attribute types and
    // values; no publisher JSON or third-party class source is embedded.
    private record ModifierSpec(String attribute, String operation, double amount) {}
    private static final Map<String, List<ModifierSpec>> FULL_LEGACY_REPLACEMENTS = Map.of(
        "adaptive_skin", List.of(new ModifierSpec("minecraft:generic.max_health", "add_value", 6.0D)),
        "adrenaline_fiend", List.of(
            new ModifierSpec("minecraft:generic.attack_speed", "add_multiplied_total", 0.1D),
            new ModifierSpec("minecraft:generic.attack_damage", "add_multiplied_total", 0.075D)),
        "catharsis", List.of(
            new ModifierSpec("epicfight:stamina_regen", "add_value", 0.15D),
            new ModifierSpec("minecraft:generic.attack_damage", "add_multiplied_total", 0.1D)),
        "bonebreaker", List.of(new ModifierSpec("minecraft:generic.attack_speed", "add_multiplied_total", 0.15D)),
        "vengeance", List.of(
            new ModifierSpec("minecraft:generic.max_health", "add_value", 3.0D),
            new ModifierSpec("minecraft:generic.attack_damage", "add_multiplied_total", 0.075D))
    );

    private static String fixtureJson(String skill) {
        JsonObject document = new JsonObject();
        JsonArray modifiers = new JsonArray();
        int i = 0;
        for (ModifierSpec spec : FULL_LEGACY_REPLACEMENTS.get(skill)) {
            JsonObject modifier = new JsonObject();
            modifier.addProperty("attribute", spec.attribute());
            modifier.addProperty("id", "black_arcana_epicfight_qa:" + skill + "_modifier_" + i++);
            modifier.addProperty("operation", spec.operation());
            modifier.addProperty("amount", spec.amount());
            modifiers.add(modifier);
        }
        document.add("attribute_modifiers", modifiers);
        return document.toString();
    }

    private final MinecraftServer server;
    private final Path packDir;
    private final Registry<?> skills;
    private final Class<?> skillClass;
    private final Field attributesField;
    private String packId;
    private boolean created;

    private EpicFightOverrideCycleQa(MinecraftServer server) throws ReflectiveOperationException {
        this.server = server;
        this.packDir = server.getWorldPath(LevelResource.DATAPACK_DIR).resolve(PACK_FOLDER);
        Class<?> registryClass = Class.forName("yesman.epicfight.registry.EpicFightRegistries");
        Object registry = registryClass.getField("SKILL").get(null);
        if (!(registry instanceof Registry<?> result)) {
            throw new IllegalStateException("Epic Fight skill registry unavailable");
        }
        skills = result;
        skillClass = Class.forName("yesman.epicfight.skill.Skill");
        attributesField = skillClass.getDeclaredField("attributes");
        attributesField.setAccessible(true);
    }

    static void start(MinecraftServer server) {
        try {
            if (!server.isSameThread()) {
                throw new IllegalStateException("QA may only start on the server thread");
            }
            EpicFightOverrideCycleQa probe = new EpicFightOverrideCycleQa(server);
            probe.begin();
        } catch (ReflectiveOperationException | RuntimeException | LinkageError error) {
            LOG.warn("{} type=end status=SETUP_FAILED exception={}", PREFIX, error.getClass().getName());
        }
    }

    private void begin() {
        try {
            if (Files.exists(packDir)) {
                finishFailure("PACK_PATH_ALREADY_EXISTS");
                return;
            }
            if (!readCounts("baseline", BASELINE_COUNTS)) {
                finishFailure("BASELINE_MISMATCH");
                return;
            }
            // The temporary datapack is 100% original QA data. It replaces the
            // resource path via normal server pack priority, not via API patches.
            Path parameters = packDir.resolve("data/epicfight/skill_parameters");
            Files.createDirectories(parameters);
            created = true;
            Files.writeString(packDir.resolve("pack.mcmeta"),
                "{\"pack\":{\"pack_format\":48,\"description\":\"Black Arcana temporary Epic Fight codec QA\"}}\n",
                StandardCharsets.UTF_8);
            if (ALL_LEGACY) {
                for (String skill : List.of("adaptive_skin", "adrenaline_fiend", "catharsis", "bonebreaker", "vengeance")) {
                    Files.writeString(parameters.resolve(skill + ".json"),
                        fixtureJson(skill), StandardCharsets.UTF_8);
                }
            } else {
                Files.writeString(parameters.resolve("adaptive_skin.json"),
                    OVERRIDE_JSON, StandardCharsets.UTF_8);
            }

            var repo = server.getPackRepository();
            repo.reload();
            List<String> found = repo.getAvailableIds().stream()
                .filter(id -> id.equals("file/" + PACK_FOLDER))
                .toList();
            if (found.size() != 1) {
                finishFailure("QA_DATAPACK_NOT_DISCOVERED");
                return;
            }
            packId = found.getFirst();
            List<String> selected = new ArrayList<>(repo.getSelectedIds());
            if (selected.contains(packId)) {
                finishFailure("QA_PACK_UNEXPECTEDLY_PRESELECTED");
                return;
            }
            selected.add(packId);
            LOG.info("{} type=override_begin status=REQUESTED pack_id={} pack_format=48 scope={}",
                PREFIX, packId, ALL_LEGACY ? "ALL_FIVE_LEGACY" : "SINGLE_ADAPTIVE_SKIN");
            repo.setSelected(selected);
            server.reloadResources(selected).whenComplete((none, error) ->
                server.execute(() -> {
                    if (error != null) {
                        finishFailure("OVERRIDE_RELOAD_FAILED");
                    } else {
                        onOverrideLoaded();
                    }
                })
            );
        } catch (IOException | RuntimeException error) {
            finishFailure("OVERRIDE_SETUP_FAILED_" + error.getClass().getSimpleName());
        }
    }

    private void onOverrideLoaded() {
        Map<String, Integer> expected = new java.util.HashMap<>(BASELINE_COUNTS);
        if (ALL_LEGACY) {
            for (var row : FULL_LEGACY_REPLACEMENTS.entrySet()) {
                expected.put(row.getKey(), row.getValue().size());
            }
        } else {
            expected.put("adaptive_skin", 1);
        }
        if (!readCounts("override", expected)) {
            finishFailure("OVERRIDE_NOT_APPLIED");
            return;
        }
        try {
            removeOwnPack();
            var repo = server.getPackRepository();
            repo.reload();
            List<String> selected = new ArrayList<>(repo.getSelectedIds());
            selected.removeIf(id -> id.equals(packId));
            if (repo.getAvailableIds().contains(packId)) {
                finishFailure("QA_PACK_STILL_AVAILABLE");
                return;
            }
            LOG.info("{} type=restore_begin status=REQUESTED", PREFIX);
            repo.setSelected(selected);
            server.reloadResources(selected).whenComplete((none, error) ->
                server.execute(() -> {
                    if (error != null) {
                        finishFailure("RESTORE_RELOAD_FAILED");
                    } else if (readCounts("restored", BASELINE_COUNTS)) {
                        LOG.info("{} type=end status=OBSERVED phases=baseline,override,restored", PREFIX);
                    } else {
                        finishFailure("RESTORE_COUNTS_DRIFT");
                    }
                })
            );
        } catch (IOException | RuntimeException error) {
            finishFailure("RESTORE_SETUP_FAILED_" + error.getClass().getSimpleName());
        }
    }

    private boolean readCounts(String phase, Map<String, Integer> expected) {
        try {
            int observed = 0;
            boolean match = true;
            for (var entry : expected.entrySet()) {
                String skillName = entry.getKey();
                Object skill = skills.get(ResourceLocation.fromNamespaceAndPath("epicfight", skillName));
                if (skill == null || !skillClass.isInstance(skill)) {
                    LOG.warn("{} type=observation phase={} id=epicfight:{} status=SKILL_UNAVAILABLE",
                        PREFIX, phase, skillName);
                    return false;
                }
                Object modifiers = attributesField.get(skill);
                if (!(modifiers instanceof Map<?, ?> attributes)) {
                    LOG.warn("{} type=observation phase={} id=epicfight:{} status=ATTRIBUTES_UNAVAILABLE",
                        PREFIX, phase, skillName);
                    return false;
                }
                int actual = attributes.size();
                LOG.info("{} type=observation phase={} id=epicfight:{} count={} expected={}",
                    PREFIX, phase, skillName, actual, entry.getValue());
                match &= actual == entry.getValue();
                observed++;
            }
            LOG.info("{} type=phase_end phase={} status={} observed={}",
                PREFIX, phase, match ? "OBSERVED" : "COUNTS_DRIFT", observed);
            return match && observed == BASELINE_COUNTS.size();
        } catch (ReflectiveOperationException | RuntimeException | LinkageError error) {
            LOG.warn("{} type=phase_end phase={} status=READ_FAILED exception={}",
                PREFIX, phase, error.getClass().getName());
            return false;
        }
    }

    private void removeOwnPack() throws IOException {
        if (!created) return;
        if (Files.isDirectory(packDir)) {
            try (var paths = Files.walk(packDir)) {
                for (Path path : paths.sorted(Comparator.reverseOrder()).toList()) {
                    Files.delete(path);
                }
            }
        }
        created = false;
    }

    private void finishFailure(String status) {
        try {
            removeOwnPack();
        } catch (IOException cleanupFailed) {
            LOG.warn("{} type=cleanup status=FAILED exception={}",
                PREFIX, cleanupFailed.getClass().getName());
        }
        LOG.warn("{} type=end status={}", PREFIX, status);
    }
}
