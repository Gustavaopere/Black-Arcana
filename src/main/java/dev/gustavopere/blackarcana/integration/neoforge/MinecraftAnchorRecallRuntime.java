package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.content.space.AnchorRecallValidator;
import dev.gustavopere.blackarcana.content.space.LiminalSafetyCeilings;
import dev.gustavopere.blackarcana.content.space.SafeDestinationPolicy;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.RelativeMovement;
import net.minecraft.world.entity.projectile.Projectile;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.event.entity.player.PlayerEvent;
import net.neoforged.neoforge.event.server.ServerStoppedEvent;

import java.util.Collections;
import java.util.IdentityHashMap;
import java.util.Map;
import java.util.Objects;
import java.util.Set;
import java.util.UUID;

public final class MinecraftAnchorRecallRuntime {
    private static final AnchorRecallValidator VALIDATOR =
        new AnchorRecallValidator(new SafeDestinationPolicy());
    private static final Map<MinecraftServer, Map<UUID, Mark>> MARKS =
        Collections.synchronizedMap(new IdentityHashMap<>());

    private MinecraftAnchorRecallRuntime() { }

    public static void register(IEventBus gameBus) {
        Objects.requireNonNull(gameBus, "gameBus");
        gameBus.addListener(MinecraftAnchorRecallRuntime::onPlayerLoggedOut);
        gameBus.addListener(MinecraftAnchorRecallRuntime::onServerStopped);
    }

    public static ArcanaDecision markProjectile(
            MinecraftServer server,
            UUID casterId,
            UUID projectileId,
            long nowTick,
            long maxAgeTicks,
            double maxRange
    ) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(casterId, "casterId");
        Objects.requireNonNull(projectileId, "projectileId");

        if (nowTick < 0L) {
            return ArcanaDecision.deny("anchor_recall_invalid_time", "Anchor Recall mark tick must be non-negative");
        }
        if (maxAgeTicks <= 0L || maxAgeTicks > LiminalSafetyCeilings.MAX_RECALL_PROJECTILE_AGE_TICKS) {
            return ArcanaDecision.deny(
                "anchor_recall_invalid_age",
                "Anchor Recall projectile age is outside the hard safety ceiling");
        }
        if (!Double.isFinite(maxRange) || maxRange <= 0.0D || maxRange > LiminalSafetyCeilings.MAX_RECALL_RANGE) {
            return ArcanaDecision.deny(
                "anchor_recall_invalid_range",
                "Anchor Recall range is outside the hard safety ceiling");
        }

        LivingEntity caster = findLoadedLivingEntity(server, casterId);
        if (caster == null || !caster.isAlive()) {
            return ArcanaDecision.deny(
                "anchor_recall_caster_unavailable",
                "Anchor Recall caster must be a loaded living entity");
        }

        Projectile projectile = findLoadedProjectile(server, projectileId);
        if (projectile == null || !projectile.isAlive()) {
            return ArcanaDecision.deny(
                "anchor_recall_projectile_unavailable",
                "Anchor Recall projectile must already be loaded");
        }
        Entity owner = projectile.getOwner();
        if (owner == null || !casterId.equals(owner.getUUID())) {
            return ArcanaDecision.deny(
                "anchor_recall_foreign_projectile",
                "Anchor Recall can mark only a projectile owned by the caster");
        }

        synchronized (MARKS) {
            MARKS.computeIfAbsent(server, ignored -> new java.util.LinkedHashMap<>())
                .put(casterId, new Mark(projectileId, casterId, nowTick, maxAgeTicks, maxRange));
        }
        return ArcanaDecision.allow();
    }

    public static RecallResult recall(MinecraftServer server, UUID casterId, long nowTick) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(casterId, "casterId");
        if (nowTick < 0L) {
            return RecallResult.denied("anchor_recall_invalid_time", "Anchor Recall tick must be non-negative");
        }

        Mark mark = mark(server, casterId);
        if (mark == null) {
            return RecallResult.denied("anchor_recall_missing_mark", "No Anchor Recall projectile is marked for caster");
        }

        LivingEntity caster = findLoadedLivingEntity(server, casterId);
        if (caster == null || !caster.isAlive()) {
            return RecallResult.denied(
                "anchor_recall_caster_unavailable",
                "Anchor Recall caster must remain loaded and alive");
        }

        Projectile projectile = findLoadedProjectile(server, mark.projectileId());
        if (projectile == null || !projectile.isAlive()) {
            return RecallResult.denied(
                "anchor_recall_projectile_unavailable",
                "Marked Anchor Recall projectile is no longer loaded");
        }
        if (!ownedBy(projectile, casterId)) {
            return RecallResult.denied(
                "anchor_recall_foreign_projectile",
                "Marked projectile is no longer owned by the caster");
        }
        if (!(projectile.level() instanceof ServerLevel destinationLevel)) {
            return RecallResult.denied(
                "anchor_recall_projectile_unavailable",
                "Marked projectile is not in a loaded server level");
        }

        MinecraftSafeDestinationResolver.Result destination = MinecraftSafeDestinationResolver.evaluate(
            server,
            caster,
            destinationLevel,
            projectile.getX(),
            projectile.getY(),
            projectile.getZ());
        AnchorRecallValidator.Result validation = validate(
            caster,
            projectile,
            mark,
            nowTick,
            destination.facts());
        if (!validation.allowed()) {
            return RecallResult.denied(validation.code(), "Anchor Recall validation denied the current projectile destination");
        }

        LivingEntity settlementCaster = findLoadedLivingEntity(server, casterId);
        Projectile settlementProjectile = findLoadedProjectile(server, mark.projectileId());
        if (settlementCaster != caster || settlementProjectile != projectile
                || !caster.isAlive() || !projectile.isAlive()) {
            return RecallResult.denied(
                "anchor_recall_endpoint_changed",
                "Anchor Recall endpoint changed before teleport settlement");
        }
        if (!ownedBy(projectile, casterId) || !(projectile.level() instanceof ServerLevel settlementLevel)) {
            return RecallResult.denied(
                "anchor_recall_endpoint_changed",
                "Anchor Recall projectile ownership or level changed before settlement");
        }

        double landingX = projectile.getX();
        double landingY = projectile.getY();
        double landingZ = projectile.getZ();
        MinecraftSafeDestinationResolver.Result settlementDestination = MinecraftSafeDestinationResolver.evaluate(
            server,
            caster,
            settlementLevel,
            landingX,
            landingY,
            landingZ);
        AnchorRecallValidator.Result settlementValidation = validate(
            caster,
            projectile,
            mark,
            nowTick,
            settlementDestination.facts());
        if (!settlementValidation.allowed()) {
            return RecallResult.denied(
                settlementValidation.code(),
                "Anchor Recall destination became unsafe before teleport settlement");
        }

        boolean teleported = caster.teleportTo(
            settlementLevel,
            landingX,
            landingY,
            landingZ,
            Set.<RelativeMovement>of(),
            caster.getYRot(),
            caster.getXRot());
        return teleported
            ? RecallResult.allowed()
            : RecallResult.denied("anchor_recall_teleport_failed", "Minecraft rejected Anchor Recall teleport settlement");
    }

    private static AnchorRecallValidator.Result validate(
            LivingEntity caster,
            Projectile projectile,
            Mark mark,
            long nowTick,
            SafeDestinationPolicy.Facts destinationFacts
    ) {
        double distance = Math.sqrt(caster.distanceToSqr(projectile));
        return VALIDATOR.validate(
            caster.getUUID(),
            nowTick,
            new AnchorRecallValidator.Anchor(
                mark.ownerId(),
                mark.createdAtTick(),
                mark.maxAgeTicks(),
                distance,
                mark.maxRange(),
                destinationFacts));
    }

    private static boolean ownedBy(Projectile projectile, UUID casterId) {
        Entity owner = projectile.getOwner();
        return owner != null && casterId.equals(owner.getUUID());
    }

    private static Mark mark(MinecraftServer server, UUID casterId) {
        synchronized (MARKS) {
            Map<UUID, Mark> serverMarks = MARKS.get(server);
            return serverMarks == null ? null : serverMarks.get(casterId);
        }
    }

    private static LivingEntity findLoadedLivingEntity(MinecraftServer server, UUID entityId) {
        for (ServerLevel level : server.getAllLevels()) {
            Entity entity = level.getEntity(entityId);
            if (entity instanceof LivingEntity living) return living;
        }
        return null;
    }

    private static Projectile findLoadedProjectile(MinecraftServer server, UUID projectileId) {
        for (ServerLevel level : server.getAllLevels()) {
            Entity entity = level.getEntity(projectileId);
            if (entity instanceof Projectile projectile) return projectile;
        }
        return null;
    }

    private static void onPlayerLoggedOut(PlayerEvent.PlayerLoggedOutEvent event) {
        MinecraftServer server = event.getEntity().level().getServer();
        if (server == null) return;
        synchronized (MARKS) {
            Map<UUID, Mark> serverMarks = MARKS.get(server);
            if (serverMarks == null) return;
            serverMarks.remove(event.getEntity().getUUID());
            if (serverMarks.isEmpty()) MARKS.remove(server);
        }
    }

    private static void onServerStopped(ServerStoppedEvent event) {
        MARKS.remove(event.getServer());
    }

    private record Mark(
        UUID projectileId,
        UUID ownerId,
        long createdAtTick,
        long maxAgeTicks,
        double maxRange
    ) {
        private Mark {
            Objects.requireNonNull(projectileId, "projectileId");
            Objects.requireNonNull(ownerId, "ownerId");
        }
    }

    public record RecallResult(ArcanaDecision decision, boolean teleported) {
        public RecallResult {
            Objects.requireNonNull(decision, "decision");
            if (!decision.allowed() && teleported) {
                throw new IllegalArgumentException("denied Anchor Recall result cannot report teleport settlement");
            }
            if (decision.allowed() != teleported) {
                throw new IllegalArgumentException("Anchor Recall allow result must correspond to successful teleport");
            }
        }

        private static RecallResult allowed() {
            return new RecallResult(ArcanaDecision.allow(), true);
        }

        private static RecallResult denied(String code, String detail) {
            return new RecallResult(ArcanaDecision.deny(code, detail), false);
        }
    }
}
