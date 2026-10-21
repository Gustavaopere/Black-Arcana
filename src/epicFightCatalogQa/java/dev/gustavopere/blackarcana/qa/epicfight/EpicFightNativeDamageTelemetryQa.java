package dev.gustavopere.blackarcana.qa.epicfight;

import com.mojang.logging.LogUtils;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.tags.DamageTypeTags;
import net.minecraft.world.damagesource.DamageSource;
import net.neoforged.neoforge.common.damagesource.DamageContainer;
import net.neoforged.neoforge.common.util.FakePlayer;
import net.neoforged.neoforge.event.entity.living.LivingDamageEvent;
import net.neoforged.neoforge.event.entity.living.LivingIncomingDamageEvent;
import org.slf4j.Logger;

/**
 * QA-only read-only telemetry for provider-native player attacks. Does not create
 * a DamageSource, trigger an attack, invoke the armor handler, mutate an event,
 * spend weapon charge, or implement Black Arcana/RPG Skill Tree perk adapters.
 *
 * Incoming and Post are independent observations; a shared cast/hit ID is NOT
 * claimed because NeoForge does not supply one in these two event contracts.
 * Logs contain no player name, UUID, position, entity ID or other identifier.
 */
final class EpicFightNativeDamageTelemetryQa {
    private static final Logger LOG = LogUtils.getLogger();
    private static final String PREFIX = "[BLACK_ARCANA_EPICFIGHT_NATIVE_DAMAGE_QA]";
    private static final String SOURCE_CLASS =
        "yesman.epicfight.world.damagesource.EpicFightDamageSource";
    private static final int SAMPLE_LIMIT_PER_PHASE = 12;

    private MinecraftServer server;
    private Class<?> epicDamageSource;
    private int incomingSamples;
    private int postSamples;

    void onServerStarted(MinecraftServer runningServer) {
        this.server = runningServer;
        try {
            this.epicDamageSource = Class.forName(SOURCE_CLASS);
            LOG.info("{} type=armed status=AWAIT_NATIVE_PLAYER_ATTACK "
                + "source_class_available=true connected_players={} "
                + "incoming_count=0 post_count=0 no_client_proof=false",
                PREFIX, runningServer.getPlayerList().getPlayers().size());
        } catch (ClassNotFoundException | LinkageError failure) {
            this.epicDamageSource = null;
            LOG.warn("{} type=armed status=PROVIDER_DAMAGE_CLASS_UNAVAILABLE exception={} "
                + "source_class_available=false incoming_count=0 post_count=0",
                PREFIX, failure.getClass().getName());
        }
    }

    private boolean eligible(DamageSource source) {
        if (server == null || epicDamageSource == null
            || !epicDamageSource.isInstance(source)
            || !(source.getEntity() instanceof ServerPlayer attacker)
            || attacker instanceof FakePlayer) {
            return false;
        }
        return server.getPlayerList().getPlayers().contains(attacker);
    }

    void onIncoming(LivingIncomingDamageEvent event) {
        if (incomingSamples >= SAMPLE_LIMIT_PER_PHASE || !eligible(event.getSource())) return;
        incomingSamples++;
        LOG.info("{} type=sample phase=incoming source=EPICFIGHT_CONNECTED_PLAYER "
            + "sample={} original_damage={} incoming_amount={} "
            + "bypasses_armor={} victim_is_player={} "
            + "correlated_with_post=false damage_modified=false",
            PREFIX, incomingSamples, event.getOriginalAmount(), event.getAmount(),
            event.getSource().is(DamageTypeTags.BYPASSES_ARMOR),
            event.getEntity() instanceof ServerPlayer);
    }

    void onDamagePost(LivingDamageEvent.Post event) {
        if (postSamples >= SAMPLE_LIMIT_PER_PHASE || !eligible(event.getSource())) return;
        postSamples++;
        LOG.info("{} type=sample phase=post source=EPICFIGHT_CONNECTED_PLAYER "
            + "sample={} original_damage={} health_damage={} armor_reduction={} "
            + "absorption_reduction={} bypasses_armor={} victim_is_player={} "
            + "correlated_with_incoming=false damage_modified=false",
            PREFIX, postSamples, event.getOriginalDamage(), event.getNewDamage(),
            event.getReduction(DamageContainer.Reduction.ARMOR),
            event.getReduction(DamageContainer.Reduction.ABSORPTION),
            event.getSource().is(DamageTypeTags.BYPASSES_ARMOR),
            event.getEntity() instanceof ServerPlayer);
    }
}
