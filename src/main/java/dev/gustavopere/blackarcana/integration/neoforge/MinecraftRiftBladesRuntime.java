package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.content.projection.ProjectionBudgetTracker;
import dev.gustavopere.blackarcana.content.projection.ProjectionSafetyCeilings;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntimeManager;
import dev.gustavopere.blackarcana.core.world.ChunkRef;
import dev.gustavopere.blackarcana.core.world.EntityEffectLimits;
import dev.gustavopere.blackarcana.core.world.EntityInteractionAuthorization;
import dev.gustavopere.blackarcana.core.world.EntityInteractionType;
import dev.gustavopere.blackarcana.core.world.EntityProtectionFacts;
import dev.gustavopere.blackarcana.core.world.ProtectionQuery;
import net.minecraft.core.BlockPos;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.RelativeMovement;
import net.minecraft.world.phys.AABB;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.common.Tags;
import net.neoforged.neoforge.event.entity.player.PlayerEvent;
import net.neoforged.neoforge.event.server.ServerStoppedEvent;
import net.neoforged.neoforge.event.tick.ServerTickEvent;

import java.util.ArrayList;
import java.util.Collections;
import java.util.IdentityHashMap;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Set;
import java.util.UUID;

/**
 * Server-authoritative Rift Blades boundary.
 *
 * Marked-hit damage and optional caster displacement are admitted independently. Projectile
 * manifestations are server-owned ephemeral handles with bounded lifetime/accounting; the Iron's
 * host remains responsible for rendering/materializing any projectile entity and must bind it to
 * these handles rather than creating persistent Black Arcana items.
 */
public final class MinecraftRiftBladesRuntime {
    /** Technical ceilings only; Stage 08/config owns final spell balance below them. */
    public static final long ABSOLUTE_MAX_PROJECTILE_LIFETIME_TICKS = 20L * 60L * 60L;
    public static final double ABSOLUTE_MAX_PROJECTILE_RANGE_BLOCKS = 128.0D;

    private static final Map<MinecraftServer, ProjectileState> PROJECTILE_STATES =
        Collections.synchronizedMap(new IdentityHashMap<>());

    private MinecraftRiftBladesRuntime() { }

    public static void register(IEventBus gameBus) {
        Objects.requireNonNull(gameBus, "gameBus");
        gameBus.addListener(MinecraftRiftBladesRuntime::onServerTick);
        gameBus.addListener(MinecraftRiftBladesRuntime::onPlayerLoggedOut);
        gameBus.addListener(MinecraftRiftBladesRuntime::onServerStopped);
    }

    /**
     * Compatibility overload for callers that have not yet supplied spell-specific range balance.
     * It still receives the absolute technical ceiling; Stage 08/host wiring should use the bounded
     * overload below with its configured range.
     */
    public static VolleyResult launchProjectileVolley(
            MinecraftServer server,
            UUID ownerId,
            long nowTick,
            int projectileCount,
            long lifetimeTicks
    ) {
        return launchProjectileVolley(
            server,
            ownerId,
            nowTick,
            projectileCount,
            lifetimeTicks,
            ABSOLUTE_MAX_PROJECTILE_RANGE_BLOCKS);
    }

    public static VolleyResult launchProjectileVolley(
            MinecraftServer server,
            UUID ownerId,
            long nowTick,
            int projectileCount,
            long lifetimeTicks,
            double maxRangeBlocks
    ) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(ownerId, "ownerId");
        if (nowTick < 0L) {
            return VolleyResult.denied("rift_blades_invalid_time", "Projectile creation tick must be non-negative");
        }
        try {
            ProjectionBudgetTracker.validateVolleySize(projectileCount);
        } catch (IllegalArgumentException invalidCount) {
            return VolleyResult.denied("rift_blades_projectile_count", "Projectile count exceeds the hard volley ceiling");
        }
        if (lifetimeTicks <= 0L || lifetimeTicks > ABSOLUTE_MAX_PROJECTILE_LIFETIME_TICKS) {
            return VolleyResult.denied(
                "rift_blades_projectile_lifetime",
                "Projectile lifetime is outside the technical safety ceiling");
        }
        if (!Double.isFinite(maxRangeBlocks)
                || maxRangeBlocks <= 0.0D
                || maxRangeBlocks > ABSOLUTE_MAX_PROJECTILE_RANGE_BLOCKS) {
            return VolleyResult.denied(
                "rift_blades_projectile_range",
                "Projectile range is outside the technical safety ceiling");
        }

        LivingEntity owner = findLoadedLivingEntity(server, ownerId);
        if (owner == null || !owner.isAlive()) {
            return VolleyResult.denied("rift_blades_owner_unavailable", "Projectile owner must be loaded and alive");
        }

        final long expiresAtTick;
        try {
            expiresAtTick = Math.addExact(nowTick, lifetimeTicks);
        } catch (ArithmeticException overflow) {
            return VolleyResult.denied("rift_blades_projectile_lifetime", "Projectile expiry overflowed server tick range");
        }

        ProjectileState state = projectileState(server);
        synchronized (state) {
            if (!state.budget.tryAcquireEchoes(ownerId, projectileCount)) {
                return VolleyResult.denied(
                    "rift_blades_active_projectile_capacity",
                    "Active Rift Blades projection budget is full for owner");
            }

            List<RiftBladeProjectileHandle> launched = new ArrayList<>(projectileCount);
            for (int index = 0; index < projectileCount; index++) {
                RiftBladeProjectileHandle handle = new RiftBladeProjectileHandle(
                    UUID.randomUUID(), ownerId, nowTick, expiresAtTick);
                TrackedProjectile tracked = new TrackedProjectile(
                    handle,
                    owner.getX(),
                    owner.getY(),
                    owner.getZ(),
                    maxRangeBlocks);
                state.projectiles.put(handle.projectileId(), tracked);
                launched.add(handle);
            }
            return VolleyResult.allowed(launched);
        }
    }

    /**
     * Accepts an observation from the host-owned projectile entity. The core never force-loads
     * chunks or owns projectile physics; it only enforces its registered lifetime/range/collision
     * contract and releases the matching budget slot exactly once when the handle terminates.
     */
    public static ProjectileStepResult updateProjectile(
            MinecraftServer server,
            UUID projectileId,
            double x,
            double y,
            double z,
            boolean collided
    ) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(projectileId, "projectileId");
        if (!Double.isFinite(x) || !Double.isFinite(y) || !Double.isFinite(z)) {
            return ProjectileStepResult.terminated("invalid_position");
        }

        ProjectileState state = PROJECTILE_STATES.get(server);
        if (state == null) return ProjectileStepResult.terminated("missing");
        synchronized (state) {
            TrackedProjectile tracked = state.projectiles.get(projectileId);
            if (tracked == null) return ProjectileStepResult.terminated("missing");

            if (collided) {
                terminateProjectile(server, state, tracked);
                return ProjectileStepResult.terminated("collision");
            }

            double dx = x - tracked.originX();
            double dy = y - tracked.originY();
            double dz = z - tracked.originZ();
            double distanceSquared = dx * dx + dy * dy + dz * dz;
            double maxRangeSquared = tracked.maxRangeBlocks() * tracked.maxRangeBlocks();
            if (!Double.isFinite(distanceSquared) || distanceSquared > maxRangeSquared) {
                terminateProjectile(server, state, tracked);
                return ProjectileStepResult.terminated("range_exceeded");
            }

            LivingEntity owner = findLoadedLivingEntity(server, tracked.handle().ownerId());
            if (owner == null || !owner.isAlive()) {
                terminateProjectile(server, state, tracked);
                return ProjectileStepResult.terminated("owner_unavailable");
            }
            return ProjectileStepResult.activeResult();
        }
    }

    public static int activeProjectiles(MinecraftServer server, UUID ownerId) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(ownerId, "ownerId");
        ProjectileState state = PROJECTILE_STATES.get(server);
        if (state == null) return 0;
        synchronized (state) {
            return state.budget.activeEchoes(ownerId);
        }
    }

    /** Public for deterministic GameTests; normal production invocation is ServerTickEvent.Post. */
    public static void tickProjectiles(MinecraftServer server, long nowTick) {
        Objects.requireNonNull(server, "server");
        ProjectileState state = PROJECTILE_STATES.get(server);
        if (state == null) return;
        synchronized (state) {
            Iterator<Map.Entry<UUID, TrackedProjectile>> iterator = state.projectiles.entrySet().iterator();
            while (iterator.hasNext()) {
                TrackedProjectile tracked = iterator.next().getValue();
                RiftBladeProjectileHandle handle = tracked.handle();
                boolean expired = handle.expiresAtTick() <= nowTick;
                LivingEntity owner = findLoadedLivingEntity(server, handle.ownerId());
                boolean ownerUnavailable = owner == null || !owner.isAlive();
                if (expired || ownerUnavailable) {
                    iterator.remove();
                    state.budget.releaseEchoes(handle.ownerId(), 1);
                }
            }
            if (state.projectiles.isEmpty()) PROJECTILE_STATES.remove(server);
        }
    }

    public static StrikeResult resolveMarkedStrike(
            MinecraftServer server,
            UUID casterId,
            UUID targetId,
            double requestedDamage,
            double landingX,
            double landingY,
            double landingZ,
            double maxGapCloseBlocks
    ) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(casterId, "casterId");
        Objects.requireNonNull(targetId, "targetId");

        if (!Double.isFinite(requestedDamage) || requestedDamage <= 0.0D) {
            return StrikeResult.denied("rift_blades_invalid_damage", "Requested Rift Blades damage must be finite and positive");
        }
        if (!Double.isFinite(maxGapCloseBlocks) || maxGapCloseBlocks < 0.0D
                || maxGapCloseBlocks > EntityEffectLimits.ABSOLUTE_MAX_DISPLACEMENT_BLOCKS) {
            return StrikeResult.denied("rift_blades_invalid_gap_close", "Requested gap-close limit is outside displacement safety bounds");
        }
        if (!Double.isFinite(landingX) || !Double.isFinite(landingY) || !Double.isFinite(landingZ)) {
            return StrikeResult.denied("rift_blades_invalid_landing", "Landing candidate must use finite coordinates");
        }

        LivingEntity caster = findLoadedLivingEntity(server, casterId);
        LivingEntity target = findLoadedLivingEntity(server, targetId);
        if (caster == null || target == null || !caster.isAlive() || !target.isAlive()) {
            return StrikeResult.denied("rift_blades_endpoint_unavailable", "Caster and marked target must be loaded living entities");
        }
        if (!(caster.level() instanceof ServerLevel level) || target.level() != level) {
            return StrikeResult.denied("rift_blades_dimension_mismatch", "Marked strike endpoints must share one loaded server level");
        }

        ArcanaServerRuntime runtime = ArcanaServerRuntimeManager.get(server).orElse(null);
        if (runtime == null) {
            return StrikeResult.denied("rift_blades_runtime_unavailable", "Black Arcana server runtime is unavailable");
        }

        EntityInteractionAuthorization damageAuthorization = authorizeDamage(server, runtime, caster, target, level);
        if (!damageAuthorization.decision().allowed()) {
            return new StrikeResult(damageAuthorization.decision(), 0.0D, false, "not_attempted");
        }

        // Hard technical ceiling only. Stage 08 owns final spell balance below this boundary.
        double boundedDamage = Math.min(requestedDamage, ProjectionSafetyCeilings.MAX_RAW_ATTACK_DAMAGE);

        LivingEntity liveCaster = findLoadedLivingEntity(server, casterId);
        LivingEntity liveTarget = findLoadedLivingEntity(server, targetId);
        if (liveCaster != caster || liveTarget != target || !caster.isAlive() || !target.isAlive()) {
            return StrikeResult.denied("rift_blades_endpoint_changed", "Marked strike endpoint changed before damage settlement");
        }
        EntityInteractionAuthorization settlementAuthorization = authorizeDamage(server, runtime, caster, target, level);
        if (!settlementAuthorization.decision().allowed()) {
            return new StrikeResult(settlementAuthorization.decision(), 0.0D, false, "not_attempted");
        }

        float healthBefore = target.getHealth();
        target.hurt(target.damageSources().indirectMagic(caster, caster), (float) boundedDamage);
        double damageDealt = Math.max(0.0D, (double) healthBefore - target.getHealth());
        if (damageDealt <= 0.0D || !caster.isAlive()) {
            return new StrikeResult(ArcanaDecision.allow(), damageDealt, false, "no_damage");
        }

        double policyGapLimit = Math.min(
            maxGapCloseBlocks,
            settlementAuthorization.limits().maxDisplacementBlocks());
        if (policyGapLimit <= 0.0D || !withinGapLimit(caster, landingX, landingY, landingZ, policyGapLimit)) {
            return new StrikeResult(ArcanaDecision.allow(), damageDealt, false, "range_denied");
        }

        LandingEvaluation landing = evaluateLanding(server, runtime, caster, level, landingX, landingY, landingZ);
        if (!landing.allowed()) {
            return new StrikeResult(ArcanaDecision.allow(), damageDealt, false, landing.code());
        }

        LivingEntity settlementCaster = findLoadedLivingEntity(server, casterId);
        if (settlementCaster != caster || !caster.isAlive()) {
            return new StrikeResult(ArcanaDecision.allow(), damageDealt, false, "caster_changed");
        }
        LandingEvaluation settlementLanding = evaluateLanding(server, runtime, caster, level, landingX, landingY, landingZ);
        if (!settlementLanding.allowed()) {
            return new StrikeResult(ArcanaDecision.allow(), damageDealt, false, settlementLanding.code());
        }

        boolean teleported = caster.teleportTo(
            level,
            landingX,
            landingY,
            landingZ,
            Set.<RelativeMovement>of(),
            caster.getYRot(),
            caster.getXRot());
        return new StrikeResult(
            ArcanaDecision.allow(),
            damageDealt,
            teleported,
            teleported ? "" : "teleport_failed");
    }

    private static EntityInteractionAuthorization authorizeDamage(
            MinecraftServer server,
            ArcanaServerRuntime runtime,
            LivingEntity caster,
            LivingEntity target,
            ServerLevel level
    ) {
        EntityProtectionFacts facts = MinecraftEntityProtectionResolver.resolve(server, caster, target);
        return runtime.entityInteractionAdmission().authorize(
            EntityInteractionType.DAMAGE,
            facts,
            new ProtectionQuery(
                caster.getUUID(),
                level.dimension().location().toString(),
                target.getUUID().toString(),
                EntityInteractionType.DAMAGE));
    }

    private static boolean withinGapLimit(
            LivingEntity caster,
            double landingX,
            double landingY,
            double landingZ,
            double limit
    ) {
        double dx = landingX - caster.getX();
        double dy = landingY - caster.getY();
        double dz = landingZ - caster.getZ();
        return dx * dx + dy * dy + dz * dz <= limit * limit;
    }

    private static LandingEvaluation evaluateLanding(
            MinecraftServer server,
            ArcanaServerRuntime runtime,
            LivingEntity caster,
            ServerLevel level,
            double landingX,
            double landingY,
            double landingZ
    ) {
        if (caster.getType().is(Tags.EntityTypes.TELEPORTING_NOT_SUPPORTED)) {
            return LandingEvaluation.deny("teleport_unsupported");
        }

        BlockPos landing = BlockPos.containing(landingX, landingY, landingZ);
        boolean loaded = level.getChunkSource().getChunkNow(landing.getX() >> 4, landing.getZ() >> 4) != null;
        AABB landingBox = caster.getBoundingBox().move(
            landingX - caster.getX(),
            landingY - caster.getY(),
            landingZ - caster.getZ());
        boolean border = level.getWorldBorder().isWithinBounds(landingBox);
        boolean collisionFree = loaded && level.noCollision(caster, landingBox);
        boolean fluidAllowed = loaded
            && level.getFluidState(landing).isEmpty()
            && level.getFluidState(landing.above()).isEmpty();
        boolean vehicleUnsafe = caster.isPassenger() || caster.isVehicle();

        boolean protectionAllowed = false;
        if (loaded) {
            var guard = runtime.protectedDestinationGuard().orElse(null);
            if (guard != null) {
                ArcanaDecision protectedDecision = guard.authorize(
                    new ChunkRef(level.dimension().location().toString(), landing.getX() >> 4, landing.getZ() >> 4),
                    new ProtectionQuery(
                        caster.getUUID(),
                        level.dimension().location().toString(),
                        caster.getUUID().toString(),
                        EntityInteractionType.DISPLACEMENT));
                protectionAllowed = protectedDecision.allowed();
            }
        }

        // Preserve the historical SafeDestinationPolicy ordering without importing the 07.04
        // content/space package into this 07.03 PR. All facts here come from canonical world-safety.
        if (!loaded) return LandingEvaluation.deny("destination_unloaded");
        if (!border) return LandingEvaluation.deny("world_border");
        if (!collisionFree) return LandingEvaluation.deny("collision_blocked");
        if (!fluidAllowed) return LandingEvaluation.deny("fluid_denied");
        if (!protectionAllowed) return LandingEvaluation.deny("protection_denied");
        if (vehicleUnsafe) return LandingEvaluation.deny("vehicle_unsafe");
        return LandingEvaluation.allow();
    }

    private static ProjectileState projectileState(MinecraftServer server) {
        synchronized (PROJECTILE_STATES) {
            return PROJECTILE_STATES.computeIfAbsent(server, ignored -> new ProjectileState());
        }
    }

    private static void terminateProjectile(
            MinecraftServer server,
            ProjectileState state,
            TrackedProjectile tracked
    ) {
        RiftBladeProjectileHandle removed = null;
        TrackedProjectile removedTracked = state.projectiles.remove(tracked.handle().projectileId());
        if (removedTracked != null) removed = removedTracked.handle();
        if (removed == null) return;
        state.budget.releaseEchoes(removed.ownerId(), 1);
        if (state.projectiles.isEmpty()) PROJECTILE_STATES.remove(server);
    }

    private static void clearOwner(MinecraftServer server, UUID ownerId) {
        ProjectileState state = PROJECTILE_STATES.get(server);
        if (state == null) return;
        synchronized (state) {
            int removed = 0;
            Iterator<Map.Entry<UUID, TrackedProjectile>> iterator = state.projectiles.entrySet().iterator();
            while (iterator.hasNext()) {
                if (iterator.next().getValue().handle().ownerId().equals(ownerId)) {
                    iterator.remove();
                    removed++;
                }
            }
            if (removed > 0) state.budget.releaseEchoes(ownerId, removed);
            if (state.projectiles.isEmpty()) PROJECTILE_STATES.remove(server);
        }
    }

    private static void onServerTick(ServerTickEvent.Post event) {
        tickProjectiles(event.getServer(), event.getServer().getTickCount());
    }

    static void onPlayerLoggedOut(PlayerEvent.PlayerLoggedOutEvent event) {
        MinecraftServer server = event.getEntity().level().getServer();
        if (server == null) return;
        clearOwner(server, event.getEntity().getUUID());
    }

    private static void onServerStopped(ServerStoppedEvent event) {
        PROJECTILE_STATES.remove(event.getServer());
    }

    private static LivingEntity findLoadedLivingEntity(MinecraftServer server, UUID entityId) {
        for (ServerLevel level : server.getAllLevels()) {
            Entity entity = level.getEntity(entityId);
            if (entity instanceof LivingEntity living) return living;
        }
        return null;
    }

    private record LandingEvaluation(boolean allowed, String code) {
        private LandingEvaluation {
            Objects.requireNonNull(code, "code");
        }
        private static LandingEvaluation allow() { return new LandingEvaluation(true, ""); }
        private static LandingEvaluation deny(String code) { return new LandingEvaluation(false, code); }
    }

    private record TrackedProjectile(
        RiftBladeProjectileHandle handle,
        double originX,
        double originY,
        double originZ,
        double maxRangeBlocks
    ) {
        private TrackedProjectile {
            Objects.requireNonNull(handle, "handle");
            if (!Double.isFinite(originX) || !Double.isFinite(originY) || !Double.isFinite(originZ)) {
                throw new IllegalArgumentException("Rift Blades projectile origin must be finite");
            }
            if (!Double.isFinite(maxRangeBlocks)
                    || maxRangeBlocks <= 0.0D
                    || maxRangeBlocks > ABSOLUTE_MAX_PROJECTILE_RANGE_BLOCKS) {
                throw new IllegalArgumentException("Rift Blades projectile range outside technical ceiling");
            }
        }
    }

    public record RiftBladeProjectileHandle(
        UUID projectileId,
        UUID ownerId,
        long createdTick,
        long expiresAtTick
    ) {
        public RiftBladeProjectileHandle {
            Objects.requireNonNull(projectileId, "projectileId");
            Objects.requireNonNull(ownerId, "ownerId");
            if (createdTick < 0L || expiresAtTick <= createdTick) {
                throw new IllegalArgumentException("invalid Rift Blades projectile lifetime");
            }
        }
    }

    public record ProjectileStepResult(boolean active, String code) {
        public ProjectileStepResult {
            Objects.requireNonNull(code, "code");
            if (active && !code.isEmpty()) {
                throw new IllegalArgumentException("active Rift Blades projectile cannot carry termination reason");
            }
            if (!active && code.isEmpty()) {
                throw new IllegalArgumentException("terminated Rift Blades projectile must carry a reason");
            }
        }

        private static ProjectileStepResult activeResult() {
            return new ProjectileStepResult(true, "");
        }

        private static ProjectileStepResult terminated(String code) {
            return new ProjectileStepResult(false, Objects.requireNonNull(code, "code"));
        }
    }

    public record VolleyResult(ArcanaDecision decision, List<RiftBladeProjectileHandle> projectiles) {
        public VolleyResult {
            Objects.requireNonNull(decision, "decision");
            projectiles = List.copyOf(Objects.requireNonNull(projectiles, "projectiles"));
            if (!decision.allowed() && !projectiles.isEmpty()) {
                throw new IllegalArgumentException("denied Rift Blades volley cannot carry projectile handles");
            }
            if (projectiles.size() > ProjectionSafetyCeilings.MAX_PROJECTILES_PER_VOLLEY) {
                throw new IllegalArgumentException("Rift Blades volley exceeds hard projectile ceiling");
            }
        }

        public int launchedCount() { return projectiles.size(); }

        private static VolleyResult allowed(List<RiftBladeProjectileHandle> projectiles) {
            return new VolleyResult(ArcanaDecision.allow(), projectiles);
        }

        private static VolleyResult denied(String code, String detail) {
            return new VolleyResult(ArcanaDecision.deny(code, detail), List.of());
        }
    }

    public record StrikeResult(ArcanaDecision decision, double damageDealt, boolean gapClosed, String gapCloseCode) {
        public StrikeResult {
            Objects.requireNonNull(decision, "decision");
            Objects.requireNonNull(gapCloseCode, "gapCloseCode");
            if (!Double.isFinite(damageDealt) || damageDealt < 0.0D) {
                throw new IllegalArgumentException("damageDealt must be finite and non-negative");
            }
            if (!decision.allowed() && (damageDealt != 0.0D || gapClosed)) {
                throw new IllegalArgumentException("denied Rift Blades result cannot carry settlement effects");
            }
            if (gapClosed && damageDealt <= 0.0D) {
                throw new IllegalArgumentException("Rift Blades cannot gap-close without real damage settlement");
            }
            if (gapClosed && !gapCloseCode.isEmpty()) {
                throw new IllegalArgumentException("successful gap-close cannot carry a denial diagnostic");
            }
            if (!gapClosed && gapCloseCode.isEmpty()) {
                throw new IllegalArgumentException("skipped gap-close must carry a diagnostic code");
            }
        }

        public static StrikeResult denied(String code, String detail) {
            return new StrikeResult(ArcanaDecision.deny(code, detail), 0.0D, false, "not_attempted");
        }
    }

    private static final class ProjectileState {
        private final ProjectionBudgetTracker budget =
            new ProjectionBudgetTracker(ProjectionSafetyCeilings.MAX_ACTIVE_ECHOES);
        private final Map<UUID, TrackedProjectile> projectiles = new LinkedHashMap<>();
    }
}
