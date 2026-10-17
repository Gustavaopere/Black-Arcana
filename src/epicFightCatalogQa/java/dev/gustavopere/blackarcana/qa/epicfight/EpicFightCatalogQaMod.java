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

    public EpicFightCatalogQaMod() {
        NeoForge.EVENT_BUS.addListener(EpicFightCatalogQaMod::onServerStarted);
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

            LOG.info("{} type=end status={} observed={} expected={}",
                PREFIX, observed == LEGACY_SKILLS.size() ? "OBSERVED" : "INCOMPLETE",
                observed, LEGACY_SKILLS.size());
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
}
