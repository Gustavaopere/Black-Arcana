package dev.gustavopere.blackarcana.qa.epicfight;

import com.mojang.logging.LogUtils;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.ai.attributes.AttributeInstance;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.neoforged.neoforge.attachment.AttachmentType;
import net.neoforged.neoforge.common.util.FakePlayer;
import net.neoforged.neoforge.event.entity.player.PlayerEvent;
import net.neoforged.neoforge.event.tick.ServerTickEvent;
import org.slf4j.Logger;

import java.lang.reflect.Field;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.UUID;
import java.util.function.Supplier;

/**
 * Opt-in Stage 09 manual QA for a genuinely connected ServerPlayer.
 *
 * Observational only: no fake player, manual ServerPlayerPatch construction,
 * onJoinWorld invocation, SkillContainer assignment or attribute mutation.
 * Never logs player names or identifiers. An unconnected CI server MUST NOT
 * claim that connected-player lifecycle was validated.
 */
final class EpicFightConnectedPlayerLifecycleQa {
    private static final Logger LOG = LogUtils.getLogger();
    private static final String PREFIX = "[BLACK_ARCANA_EPICFIGHT_CONNECTED_PLAYER_QA]";
    private static final int MAX_TICKS = 80;
    private final Map<UUID, Pending> pending = new LinkedHashMap<>();

    private record Pending(ServerPlayer player, String source, int ticks) {
        Pending nextTick() {
            return new Pending(player, source, ticks + 1);
        }
    }

    void onServerStarted(MinecraftServer server) {
        LOG.info("{} type=armed status=AWAIT_CONNECTED_PLAYER connected_count={} equip_invoked=false attribute_mutated=false",
            PREFIX, server.getPlayerList().getPlayers().size());
    }

    void onLogin(PlayerEvent.PlayerLoggedInEvent event) {
        enqueue(event.getEntity(), "login");
    }

    void onRespawn(PlayerEvent.PlayerRespawnEvent event) {
        enqueue(event.getEntity(), "respawn");
    }

    void onLogout(PlayerEvent.PlayerLoggedOutEvent event) {
        if (event.getEntity() instanceof ServerPlayer serverPlayer) {
            pending.remove(serverPlayer.getUUID());
        }
    }

    private void enqueue(net.minecraft.world.entity.player.Player player, String source) {
        if (!(player instanceof ServerPlayer serverPlayer) || player instanceof FakePlayer) {
            LOG.warn("{} type=rejected source={} status=NOT_CONNECTED_REAL_SERVER_PLAYER", PREFIX, source);
            return;
        }
        pending.put(serverPlayer.getUUID(), new Pending(serverPlayer, source, 0));
        LOG.info("{} type=queued source={} status=WAIT_NATIVE_PATCH", PREFIX, source);
    }

    void onTick(ServerTickEvent.Post event) {
        if (pending.isEmpty()) return;
        MinecraftServer server = event.getServer();
        Iterator<Map.Entry<UUID, Pending>> iterator = pending.entrySet().iterator();
        while (iterator.hasNext()) {
            var entry = iterator.next();
            Pending p = entry.getValue();
            // Eligibility only applies while the original ServerPlayer is
            // still connected; replacements after respawn must be re-queued.
            if (!server.getPlayerList().getPlayers().contains(p.player())) {
                LOG.warn("{} type=result source={} status=NOT_CONNECTED_AT_OBSERVATION", PREFIX, p.source());
                iterator.remove();
                continue;
            }
            String status = inspectNativePatch(p.player());
            if ("ATTACHED_AND_INITIALIZED".equals(status)) {
                LOG.info("{} type=result source={} status=CONNECTED_PATCH_INITIALIZED equip_invoked=false attribute_mutated=false",
                    PREFIX, p.source());
                iterator.remove();
            } else if ("ATTACHED_BUT_UNINITIALIZED".equals(status) && p.ticks() < MAX_TICKS) {
                entry.setValue(p.nextTick());
            } else if ("ATTACHED_BUT_UNINITIALIZED".equals(status)) {
                LOG.warn("{} type=result source={} status=PATCH_UNINITIALIZED_AFTER_TIMEOUT equip_invoked=false attribute_mutated=false",
                    PREFIX, p.source());
                iterator.remove();
            } else {
                LOG.warn("{} type=result source={} status={} equip_invoked=false attribute_mutated=false",
                    PREFIX, p.source(), status);
                iterator.remove();
            }
        }
    }

    private static String inspectNativePatch(ServerPlayer player) {
        try {
            AttributeInstance maxHealth = player.getAttribute(Attributes.MAX_HEALTH);
            if (maxHealth == null) return "MAX_HEALTH_ABSENT";
            Class<?> registry = Class.forName("yesman.epicfight.registry.entries.EpicFightAttachmentTypes");
            Object deferredHolder = registry.getField("ENTITY_PATCH").get(null);
            if (!(deferredHolder instanceof Supplier<?> supplier)) return "ATTACHMENT_HOLDER_UNAVAILABLE";
            Object registered = supplier.get();
            if (!(registered instanceof AttachmentType<?> type)) return "ATTACHMENT_TYPE_UNAVAILABLE";
            Object provider = player.getData(type);
            if (provider == null) return "PROVIDER_NULL";

            Field patchField = provider.getClass().getDeclaredField("entitypatch");
            patchField.setAccessible(true);
            Object patch = patchField.get(provider);
            if (patch == null) return "PATCH_NULL";
            if (!patch.getClass().getName().equals(
                "yesman.epicfight.world.capabilities.entitypatch.player.ServerPlayerPatch"
            )) return "PATCH_TYPE_MISMATCH";
            Class<?> base = Class.forName("yesman.epicfight.world.capabilities.entitypatch.EntityPatch");
            Field originalField = base.getDeclaredField("original");
            originalField.setAccessible(true);
            if (originalField.get(patch) != player) return "PATCH_ORIGINAL_MISMATCH";
            Field initializedField = base.getDeclaredField("initialized");
            initializedField.setAccessible(true);
            return initializedField.getBoolean(patch) ? "ATTACHED_AND_INITIALIZED" :
                "ATTACHED_BUT_UNINITIALIZED";
        } catch (ReflectiveOperationException | RuntimeException | LinkageError failure) {
            LOG.warn("{} type=inspection status=ABI_OR_RUNTIME_UNAVAILABLE exception={}",
                PREFIX, failure.getClass().getName());
            return "ABI_OR_RUNTIME_UNAVAILABLE";
        }
    }
}
