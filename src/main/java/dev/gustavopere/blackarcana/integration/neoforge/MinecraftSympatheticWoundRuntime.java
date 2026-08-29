package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.content.blood.SympatheticWoundService;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.LivingEntity;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.event.entity.living.LivingDamageEvent;
import net.neoforged.neoforge.event.server.ServerStartedEvent;
import net.neoforged.neoforge.event.server.ServerStoppedEvent;
import net.neoforged.neoforge.event.tick.ServerTickEvent;

import java.util.Collections;
import java.util.IdentityHashMap;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;
import java.util.UUID;

/**
 * Server-authoritative NeoForge bridge for Sympathetic Wound.
 *
 * The dedicated damage type is the recursion marker. Mirrored damage is attributed
 * to the originally wounded entity as the causing entity and never feeds another
 * Sympathetic Wound link, including deliberately crossed links.
 */
public final class MinecraftSympatheticWoundRuntime {
    public static final int DEFAULT_MAX_LINKS = SympatheticWoundService.ABSOLUTE_MAX_LINKS;

    private static final Map<MinecraftServer, SympatheticWoundService> STATES =
        Collections.synchronizedMap(new IdentityHashMap<>());

    private MinecraftSympatheticWoundRuntime() { }

    public static void register(IEventBus gameBus) {
        Objects.requireNonNull(gameBus, "gameBus");
        gameBus.addListener(MinecraftSympatheticWoundRuntime::onServerStarted);
        gameBus.addListener(MinecraftSympatheticWoundRuntime::onServerTick);
        gameBus.addListener(MinecraftSympatheticWoundRuntime::onLivingDamagePost);
        gameBus.addListener(MinecraftSympatheticWoundRuntime::onServerStopped);
    }

    public static ArcanaDecision bind(MinecraftServer server, SympatheticWoundService.LinkSpec spec) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(spec, "spec");
        SympatheticWoundService service = STATES.get(server);
        if (service == null) {
            return ArcanaDecision.deny(
                "sympathetic_wound_runtime_unavailable",
                "Sympathetic Wound runtime is unavailable on this server");
        }

        long nowTick = server.overworld().getGameTime();
        service.pruneExpired(nowTick);
        if (spec.expiresAtTick() <= nowTick) {
            return ArcanaDecision.deny(
                "sympathetic_wound_link_expired",
                "Sympathetic Wound link must expire in the future");
        }

        try {
            service.bind(spec);
            return ArcanaDecision.allow();
        } catch (IllegalStateException full) {
            return ArcanaDecision.deny(
                "sympathetic_wound_link_capacity",
                "Sympathetic Wound link registry reached its bounded capacity");
        }
    }

    public static boolean breakLink(MinecraftServer server, UUID casterId) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(casterId, "casterId");
        SympatheticWoundService service = STATES.get(server);
        return service != null && service.breakLink(casterId);
    }

    public static int activeLinks(MinecraftServer server) {
        Objects.requireNonNull(server, "server");
        SympatheticWoundService service = STATES.get(server);
        return service == null ? 0 : service.size();
    }

    private static void onServerStarted(ServerStartedEvent event) {
        STATES.put(event.getServer(), new SympatheticWoundService(DEFAULT_MAX_LINKS));
    }

    private static void onServerTick(ServerTickEvent.Post event) {
        SympatheticWoundService service = STATES.get(event.getServer());
        if (service != null) {
            service.pruneExpired(event.getServer().overworld().getGameTime());
        }
    }

    private static void onLivingDamagePost(LivingDamageEvent.Post event) {
        if (!(event.getEntity().level() instanceof ServerLevel level)) return;
        MinecraftServer server = level.getServer();
        SympatheticWoundService service = STATES.get(server);
        if (service == null) return;

        float confirmedDamage = event.getNewDamage();
        if (!Float.isFinite(confirmedDamage) || confirmedDamage <= 0.0F) return;

        SympatheticWoundService.DamageProvenance provenance = classify(event.getSource());
        Optional<SympatheticWoundService.DamageEvent> mirrored = service.mirror(
            new SympatheticWoundService.DamageEvent(
                UUID.randomUUID(),
                event.getEntity().getUUID(),
                confirmedDamage,
                provenance),
            server.overworld().getGameTime());
        if (mirrored.isEmpty()) return;

        SympatheticWoundService.DamageEvent outgoing = mirrored.orElseThrow();
        LivingEntity target = findLivingEntity(server, outgoing.victimId());
        if (target == null || !target.isAlive()) {
            service.breakLink(event.getEntity().getUUID());
            return;
        }

        float boundedDamage = (float) Math.min(outgoing.amount(), Float.MAX_VALUE);
        if (!Float.isFinite(boundedDamage) || boundedDamage <= 0.0F) return;
        DamageSource source = target.damageSources().source(
            SympatheticWoundDamageTypes.SYMPATHETIC_WOUND,
            event.getEntity());
        target.hurt(source, boundedDamage);
    }

    private static SympatheticWoundService.DamageProvenance classify(DamageSource source) {
        if (source.is(SympatheticWoundDamageTypes.SYMPATHETIC_WOUND)) {
            return SympatheticWoundService.DamageProvenance.SYMPATHETIC_WOUND;
        }
        if (source.is(ArcaneBacklashDamageTypes.ARCANE_BACKLASH)) {
            return SympatheticWoundService.DamageProvenance.OTHER_PROPAGATED;
        }
        return SympatheticWoundService.DamageProvenance.DIRECT;
    }

    private static LivingEntity findLivingEntity(MinecraftServer server, UUID entityId) {
        for (ServerLevel candidate : server.getAllLevels()) {
            Entity entity = candidate.getEntity(entityId);
            if (entity instanceof LivingEntity living) return living;
        }
        return null;
    }

    private static void onServerStopped(ServerStoppedEvent event) {
        STATES.remove(event.getServer());
    }
}
