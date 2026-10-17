package dev.gustavopere.blackarcana.qa.epicfight;

import com.mojang.logging.LogUtils;
import net.minecraft.core.Registry;
import net.minecraft.resources.ResourceLocation;
import net.neoforged.fml.ModList;
import net.neoforged.fml.common.Mod;
import net.neoforged.neoforge.common.NeoForge;
import net.neoforged.neoforge.event.server.ServerStartedEvent;
import org.slf4j.Logger;

import java.lang.reflect.Method;
import java.util.Collection;
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

        try {
            Class<?> registriesClass = Class.forName("yesman.epicfight.registry.EpicFightRegistries");
            Object registryObject = registriesClass.getField("SKILL").get(null);
            if (!(registryObject instanceof Registry<?> skills)) {
                LOG.warn("{} type=end status=REGISTRY_TYPE_UNAVAILABLE", PREFIX);
                return;
            }

            Class<?> skillClass = Class.forName("yesman.epicfight.skill.Skill");
            Method modifierEntries = skillClass.getMethod("getModfierEntry");
            int observed = 0;

            for (String skillId : LEGACY_SKILLS) {
                String qualified = "epicfight:" + skillId;
                Object skill = skills.get(ResourceLocation.fromNamespaceAndPath("epicfight", skillId));
                if (skill == null || !skillClass.isInstance(skill)) {
                    LOG.warn("{} type=skill id={} status=REGISTRY_VALUE_UNAVAILABLE", PREFIX, qualified);
                    continue;
                }
                Object entries = modifierEntries.invoke(skill);
                if (!(entries instanceof Collection<?> modifiers)) {
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
            LOG.warn("{} type=end status=PROVIDER_ABI_UNAVAILABLE exception={}",
                PREFIX, failure.getClass().getSimpleName());
        }
    }
}
