package dev.gustavopere.blackarcana.qa.epicfight;

import com.mojang.logging.LogUtils;
import net.minecraft.server.MinecraftServer;
import net.minecraft.world.entity.ai.attributes.AttributeInstance;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.neoforged.neoforge.attachment.AttachmentType;
import net.neoforged.neoforge.common.util.FakePlayer;
import net.neoforged.neoforge.common.util.FakePlayerFactory;
import org.slf4j.Logger;

import java.lang.reflect.Field;
import java.util.function.Supplier;

/**
 * QA-only eligibility probe. A fake player must NEVER be treated as an
 * authenticated, joined Minecraft player, nor as a validated Epic Fight
 * SkillContainer executor merely because an attachment can be constructed.
 * No skills are assigned and no attributes are mutated.
 */
final class EpicFightFakePlayerEligibilityQa {
    private static final Logger LOG = LogUtils.getLogger();
    private static final String PREFIX = "[BLACK_ARCANA_EPICFIGHT_FAKE_PLAYER_PREFLIGHT]";

    private EpicFightFakePlayerEligibilityQa() {}

    static void check(MinecraftServer server) {
        if (!server.isSameThread()) {
            LOG.warn("{} type=end status=WRONG_THREAD", PREFIX);
            return;
        }
        try {
            FakePlayer fake = FakePlayerFactory.getMinecraft(server.overworld());
            AttributeInstance maxHealth = fake.getAttribute(Attributes.MAX_HEALTH);
            if (maxHealth == null) {
                LOG.warn("{} type=end status=FAKE_PLAYER_MAX_HEALTH_ABSENT", PREFIX);
                return;
            }

            // Read the actual registered Epic Fight attachment, not an
            // independently instantiated PlayerPatch. Field-only lookup
            // avoids resolving client-only method signatures on DEDICATED_SERVER.
            Class<?> attachmentTypes = Class.forName(
                "yesman.epicfight.registry.entries.EpicFightAttachmentTypes");
            Object holder = attachmentTypes.getField("ENTITY_PATCH").get(null);
            if (!(holder instanceof Supplier<?> supplier)) {
                LOG.warn("{} type=end status=ATTACHMENT_HOLDER_UNAVAILABLE", PREFIX);
                return;
            }
            Object registered = supplier.get();
            if (!(registered instanceof AttachmentType<?> attachmentType)) {
                LOG.warn("{} type=end status=ATTACHMENT_TYPE_UNAVAILABLE", PREFIX);
                return;
            }
            Object provider = fake.getData(attachmentType);
            if (provider == null) {
                LOG.warn("{} type=end status=ATTACHMENT_PROVIDER_NULL", PREFIX);
                return;
            }
            Field entitypatchField = provider.getClass().getDeclaredField("entitypatch");
            entitypatchField.setAccessible(true);
            Object patch = entitypatchField.get(provider);
            if (patch == null) {
                LOG.info("{} type=end status=NO_PATCH_CREATED_FOR_FAKE_PLAYER", PREFIX);
                return;
            }
            String patchName = patch.getClass().getName();
            if (!"yesman.epicfight.world.capabilities.entitypatch.player.ServerPlayerPatch".equals(patchName)) {
                LOG.info("{} type=end status=PATCH_TYPE_NOT_SERVER_PLAYER class={}", PREFIX, patchName);
                return;
            }
            Class<?> entityPatchClass = Class.forName(
                "yesman.epicfight.world.capabilities.entitypatch.EntityPatch");
            Field originalField = entityPatchClass.getDeclaredField("original");
            originalField.setAccessible(true);
            if (originalField.get(patch) != fake) {
                LOG.warn("{} type=end status=PATCH_ORIGINAL_MISMATCH", PREFIX);
                return;
            }
            Field initializedField = entityPatchClass.getDeclaredField("initialized");
            initializedField.setAccessible(true);
            boolean initialized = initializedField.getBoolean(patch);
            LOG.info("{} type=observation provider=epicfight fake_player=true patch=ServerPlayerPatch attached=true initialized={} max_health_base={}",
                PREFIX, initialized, maxHealth.getBaseValue());
            LOG.info("{} type=end status={} equip_invoked=false attribute_mutated=false",
                PREFIX, initialized ? "PATCH_ATTACHED_INITIALIZED_FAKE_PLAYER_NOT_CONNECTED"
                    : "PATCH_ATTACHED_UNINITIALIZED_REQUIRES_JOIN_LIFECYCLE");
        } catch (ReflectiveOperationException | RuntimeException | LinkageError e) {
            LOG.warn("{} type=end status=ABI_OR_RUNTIME_UNAVAILABLE exception={}", PREFIX,
                e.getClass().getName());
        }
    }
}
