package dev.gustavopere.blackarcana.qa.epicfight;

import com.mojang.logging.LogUtils;
import net.minecraft.core.Registry;
import net.minecraft.resources.ResourceLocation;
import net.neoforged.fml.ModList;
import net.neoforged.fml.common.Mod;
import net.neoforged.neoforge.common.NeoForge;
import net.neoforged.neoforge.event.server.ServerStartedEvent;
import org.slf4j.Logger;

import java.lang.reflect.Field;
import java.util.Map;
import java.util.List;

/**
 * Removable QA-only server probe, no Epic Fight source or compile dependency.
 * Reads five loaded registry skills without invoking casts, costs or damage.
 * Does not observe player/equipment attribute values or implement an adapter.
 */
@Mod(EpicFightCatalogQaMod.MOD_ID)
public final class EpicFightCatalogQaMod {
    public static final String MOD_ID = "black_arcana_epicfight_qa";
    static final String PREFIX = "[BLACK_ARCANA_EPICFIGHT_LOADED_QA]";
    private static final Logger LOG = LogUtils.getLogger();

    private static final List<String> LEGACY_SKILLS = List.of(
        "adaptive_skin",
        "adrenaline_fiend",
        "catharsis",
        "bonebreaker",
        "vengeance"
    );

    private static final Map<String, Integer> MODERN_CONTROLS = Map.of(
        "swordmaster", 2,
        "forbidden_strength", 2,
        "technician", 1
    );

    private static final boolean CONNECTED_PLAYER_PREFLIGHT =
        "1".equals(System.getenv("BLACK_ARCANA_EPICFIGHT_QA_CONNECTED_PLAYER_PREFLIGHT"));
    private static final EpicFightConnectedPlayerLifecycleQa CONNECTED_PLAYER_QA =
        new EpicFightConnectedPlayerLifecycleQa();

    public EpicFightCatalogQaMod() {
        NeoForge.EVENT_BUS.addListener(EpicFightCatalogQaMod::onServerStarted);
        if (CONNECTED_PLAYER_PREFLIGHT) {
            NeoForge.EVENT_BUS.addListener(CONNECTED_PLAYER_QA::onLogin);
            NeoForge.EVENT_BUS.addListener(CONNECTED_PLAYER_QA::onRespawn);
            NeoForge.EVENT_BUS.addListener(CONNECTED_PLAYER_QA::onLogout);
            NeoForge.EVENT_BUS.addListener(CONNECTED_PLAYER_QA::onTick);
        }
    }

    private static void onServerStarted(ServerStartedEvent event) {
        boolean loaded = ModList.get().isLoaded("epicfight");
        LOG.info("{} type=begin provider=epicfight loaded={}", PREFIX, loaded);
        if (!loaded) {
            LOG.warn("{} type=end status=PROVIDER_NOT_LOADED", PREFIX);
            return;
        }

        String phase = "resolve_registry_class";
        try {
            Class<?> registriesClass = Class.forName("yesman.epicfight.registry.EpicFightRegistries");
            phase = "resolve_registry_field";
            Object registryObject = registriesClass.getField("SKILL").get(null);
            if (!(registryObject instanceof Registry<?> skills)) {
                LOG.warn("{} type=end status=REGISTRY_TYPE_UNAVAILABLE", PREFIX);
                return;
            }

            phase = "resolve_skill_class";
            Class<?> skillClass = Class.forName("yesman.epicfight.skill.Skill");
            // Avoid Class.getMethod(): it introspects client-only method
            // signatures and invokes RuntimeDistCleaner on a dedicated server.
            phase = "resolve_attributes_field";
            Field attributesField = skillClass.getDeclaredField("attributes");
            attributesField.setAccessible(true);
            int observed = 0;

            for (String skillId : LEGACY_SKILLS) {
                String qualified = "epicfight:" + skillId;
                phase = "lookup_skill_" + skillId;
                Object skill = skills.get(ResourceLocation.fromNamespaceAndPath("epicfight", skillId));
                if (skill == null || !skillClass.isInstance(skill)) {
                    LOG.warn("{} type=skill id={} status=REGISTRY_VALUE_UNAVAILABLE", PREFIX, qualified);
                    continue;
                }
                phase = "read_modifiers_" + skillId;
                Object entries = attributesField.get(skill);
                if (!(entries instanceof Map<?, ?> modifiers)) {
                    LOG.warn("{} type=skill id={} status=ATTRIBUTE_ENTRY_TYPE_UNAVAILABLE", PREFIX, qualified);
                    continue;
                }
                LOG.info("{} type=skill id={} status=OBSERVED_LOADED_REGISTRY modifier_entries={}",
                    PREFIX, qualified, modifiers.size());
                observed++;
            }

            int controls = 0;
            for (var control : MODERN_CONTROLS.entrySet()) {
                String skillId = control.getKey();
                String qualified = "epicfight:" + skillId;
                phase = "lookup_control_" + skillId;
                Object skill = skills.get(ResourceLocation.fromNamespaceAndPath("epicfight", skillId));
                if (skill == null || !skillClass.isInstance(skill)) {
                    LOG.warn("{} type=control id={} status=REGISTRY_VALUE_UNAVAILABLE", PREFIX, qualified);
                    continue;
                }
                phase = "read_control_" + skillId;
                Object entries = attributesField.get(skill);
                if (!(entries instanceof Map<?, ?> modifiers)) {
                    LOG.warn("{} type=control id={} status=ATTRIBUTE_ENTRY_TYPE_UNAVAILABLE", PREFIX, qualified);
                    continue;
                }
                LOG.info("{} type=control id={} status=OBSERVED_LOADED_REGISTRY modifier_entries={} raw_json_entries={}",
                    PREFIX, qualified, modifiers.size(), control.getValue());
                controls++;
            }
            LOG.info("{} type=end status={} observed={} expected={} controls={} expected_controls={}",
                PREFIX, observed == LEGACY_SKILLS.size() && controls == MODERN_CONTROLS.size() ?
                    "OBSERVED" : "INCOMPLETE",
                observed, LEGACY_SKILLS.size(), controls, MODERN_CONTROLS.size());
            // This companion exists only inside the ephemeral QA server. Ask
            // Minecraft's own resource pipeline to perform a genuine reload.
            // Never synthesize attributes or mutate any Epic Fight skill here.
            if (observed == LEGACY_SKILLS.size() && controls == MODERN_CONTROLS.size()) {
                var server = event.getServer();
                if (CONNECTED_PLAYER_PREFLIGHT) {
                    CONNECTED_PLAYER_QA.onServerStarted(server);
                } else if ("1".equals(System.getenv("BLACK_ARCANA_EPICFIGHT_QA_FAKE_PLAYER_PREFLIGHT"))) {
                    // Never equip a skill on a fake player: check whether its
                    // actual Epic Fight attachment has completed join lifecycle.
                    EpicFightFakePlayerEligibilityQa.check(server);
                } else if ("1".equals(System.getenv("BLACK_ARCANA_EPICFIGHT_QA_OVERRIDE_CYCLE"))) {
                    // Opt-in only in disposable CI; normal isolated registry QA
                    // never creates or mutates datapack resources.
                    EpicFightOverrideCycleQa.start(server);
                } else {
                    LOG.info("{} type=reload_begin status=REQUESTED", PREFIX);
                    server.reloadResources(server.getPackRepository().getSelectedIds())
                        .whenComplete((ignored, error) -> server.execute(() -> {
                            if (error != null) {
                                LOG.warn("{} type=reload_end status=RESOURCE_RELOAD_FAILED exception={}",
                                    PREFIX, error.getClass().getName());
                            } else {
                                emitAfterReload();
                            }
                        }));
                }
            } else {
                LOG.warn("{} type=reload_end status=INITIAL_REGISTRY_INCOMPLETE", PREFIX);
            }
        } catch (ReflectiveOperationException | LinkageError | RuntimeException failure) {
            Throwable cause = failure.getCause();
            String detail = failure.getMessage() == null ? "none" :
                failure.getMessage().replaceAll("[\\r\\n\\t]", " ");
            if (detail.length() > 180) {
                detail = detail.substring(0, 180);
            }
            StackTraceElement[] frames = failure.getStackTrace();
            String location = frames.length == 0 ? "none" :
                frames[0].getClassName() + "." + frames[0].getMethodName();
            LOG.warn("{} type=end status=PROVIDER_ABI_UNAVAILABLE phase={} exception={} cause={} location={} detail={}",
                PREFIX, phase, failure.getClass().getName(),
                cause == null ? "none" : cause.getClass().getName(), location, detail);
        }
    }
    /**
     * Runs only on the server executor after the actual resource reload future
     * has completed. This re-reads provider-owned fields without ever equipping
     * skills, instantiating players or interpreting publisher implementation.
     */
    private static void emitAfterReload() {
        String phase = "resolve_registry";
        try {
            Class<?> registriesClass = Class.forName("yesman.epicfight.registry.EpicFightRegistries");
            Object registryObject = registriesClass.getField("SKILL").get(null);
            if (!(registryObject instanceof Registry<?> skills)) {
                LOG.warn("{} type=reload_end status=REGISTRY_UNAVAILABLE", PREFIX);
                return;
            }
            phase = "resolve_attributes_field";
            Class<?> skillClass = Class.forName("yesman.epicfight.skill.Skill");
            Field attributesField = skillClass.getDeclaredField("attributes");
            attributesField.setAccessible(true);

            int observedLegacy = 0;
            int observedControls = 0;
            boolean matching = true;
            for (String skillId : LEGACY_SKILLS) {
                phase = "reload_legacy_" + skillId;
                Object skill = skills.get(ResourceLocation.fromNamespaceAndPath("epicfight", skillId));
                if (skill == null || !skillClass.isInstance(skill)) {
                    LOG.warn("{} type=reload_end status=SKILL_UNAVAILABLE id=epicfight:{}", PREFIX, skillId);
                    return;
                }
                Object raw = attributesField.get(skill);
                if (!(raw instanceof Map<?, ?> entries)) {
                    LOG.warn("{} type=reload_end status=ATTRIBUTES_UNAVAILABLE id=epicfight:{}", PREFIX, skillId);
                    return;
                }
                LOG.info("{} type=reload_skill id=epicfight:{} modifier_entries={}",
                    PREFIX, skillId, entries.size());
                matching &= entries.isEmpty();
                observedLegacy++;
            }
            for (var control : MODERN_CONTROLS.entrySet()) {
                String skillId = control.getKey();
                phase = "reload_control_" + skillId;
                Object skill = skills.get(ResourceLocation.fromNamespaceAndPath("epicfight", skillId));
                if (skill == null || !skillClass.isInstance(skill)) {
                    LOG.warn("{} type=reload_end status=CONTROL_UNAVAILABLE id=epicfight:{}", PREFIX, skillId);
                    return;
                }
                Object raw = attributesField.get(skill);
                if (!(raw instanceof Map<?, ?> entries)) {
                    LOG.warn("{} type=reload_end status=ATTRIBUTES_UNAVAILABLE id=epicfight:{}", PREFIX, skillId);
                    return;
                }
                LOG.info("{} type=reload_control id=epicfight:{} modifier_entries={} expected={}",
                    PREFIX, skillId, entries.size(), control.getValue());
                matching &= entries.size() == control.getValue();
                observedControls++;
            }
            LOG.info("{} type=reload_end status={} observed={} controls={}",
                PREFIX, matching ? "OBSERVED" : "COUNTS_DRIFT",
                observedLegacy, observedControls);
        } catch (ReflectiveOperationException | LinkageError | RuntimeException failure) {
            LOG.warn("{} type=reload_end status=PROVIDER_ABI_UNAVAILABLE phase={} exception={}",
                PREFIX, phase, failure.getClass().getName());
        }
    }

}
