package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.api.ArcanaCastContext;
import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaCost;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaServices;
import dev.gustavopere.blackarcana.api.ArcanaSpellDefinition;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.content.forbidden.ForbiddenDomainAdmission;
import dev.gustavopere.blackarcana.content.forbidden.ForbiddenDomainRuntime;
import dev.gustavopere.blackarcana.content.forbidden.ForbiddenDomainSafetyCeilings;
import dev.gustavopere.blackarcana.content.forbidden.ForbiddenDomainSession;
import dev.gustavopere.blackarcana.content.forbidden.ForbiddenDomainSpec;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntimeManager;
import dev.gustavopere.blackarcana.core.world.ChunkRef;
import dev.gustavopere.blackarcana.core.world.EntityInteractionAuthorization;
import dev.gustavopere.blackarcana.core.world.EntityInteractionType;
import dev.gustavopere.blackarcana.core.world.EntityProtectionFacts;
import dev.gustavopere.blackarcana.core.world.ProtectionQuery;
import dev.gustavopere.blackarcana.core.world.ProtectedDestinationGuard;
import dev.gustavopere.blackarcana.core.world.WorldEffectProfile;
import dev.gustavopere.blackarcana.core.world.WorldMutationClass;
import dev.gustavopere.blackarcana.core.world.WorldMutationType;
import net.minecraft.core.BlockPos;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.phys.AABB;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.event.entity.player.PlayerEvent;
import net.neoforged.neoforge.event.server.ServerStartedEvent;
import net.neoforged.neoforge.event.server.ServerStoppedEvent;
import net.neoforged.neoforge.event.tick.ServerTickEvent;

import java.util.ArrayList;
import java.util.Collections;
import java.util.IdentityHashMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.UUID;

/**
 * NeoForge/Minecraft boundary for Stage 07.06 localized Forbidden Domains.
 *
 * This adapter intentionally owns only bounded ephemeral session state. It does not create dimensions,
 * acquire chunk tickets, copy inventories or mutate terrain. Concrete domain variants may consume this
 * admission/session boundary later, but their gameplay semantics remain separate and fail closed until
 * explicitly specified.
 */
public final class MinecraftForbiddenDomainRuntime {
    private static final ArcanaSpellId WORLD_SAFETY_ID =
        new ArcanaSpellId("black_arcana", "forbidden_domain_field");
    private static final ArcanaSpellDefinition WORLD_SAFETY_SPELL = new ArcanaSpellDefinition(
        WORLD_SAFETY_ID,
        "spell.black_arcana.forbidden_domain_field",
        "black_arcana:forbidden_domain_field",
        ArcanaCost.none(),
        true);

    private static final Map<MinecraftServer, ServerState> STATES =
        Collections.synchronizedMap(new IdentityHashMap<>());

    private MinecraftForbiddenDomainRuntime() { }

    public static void register(IEventBus gameBus) {
        Objects.requireNonNull(gameBus, "gameBus");
        ArcanaServerRuntimeManager.addInitializer(MinecraftForbiddenDomainRuntime::installWorldProfile);
        gameBus.addListener(MinecraftForbiddenDomainRuntime::onServerStarted);
        gameBus.addListener(MinecraftForbiddenDomainRuntime::onServerTick);
        gameBus.addListener(MinecraftForbiddenDomainRuntime::onPlayerLoggedOut);
        gameBus.addListener(MinecraftForbiddenDomainRuntime::onServerStopped);
    }

    /**
     * Starts one bounded field centered on the loaded living owner. No entity is moved by this operation.
     */
    public static ArcanaDecision start(
            MinecraftServer server,
            UUID ownerId,
            ForbiddenDomainSpec spec
    ) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(ownerId, "ownerId");
        Objects.requireNonNull(spec, "spec");

        LivingEntity owner = findLoadedLivingEntity(server, ownerId);
        if (owner == null || !owner.isAlive() || !(owner.level() instanceof ServerLevel level)) {
            return ArcanaDecision.deny(
                "forbidden_domain_owner_unavailable",
                "Forbidden Domain owner must be a loaded living server entity");
        }

        ArcanaServerRuntime runtime = ArcanaServerRuntimeManager.get(server).orElse(null);
        if (runtime == null) {
            return ArcanaDecision.deny(
                "forbidden_domain_runtime_unavailable",
                "Black Arcana server runtime is unavailable");
        }

        BlockPos center = owner.blockPosition();
        AdmissionEvaluation evaluation = evaluateAdmission(server, runtime, owner, level, center, spec);
        if (!evaluation.facts().admitted()) return evaluation.decision();

        ServerState state = stateFor(server);
        ForbiddenDomainRuntime.StartResult startResult;
        synchronized (state) {
            startResult = state.domains.start(ownerId, spec, level.getGameTime());
            if (startResult == ForbiddenDomainRuntime.StartResult.STARTED) {
                state.fields.put(ownerId, new FieldContext(
                    level.dimension().location().toString(),
                    new BlockPos(center.getX(), center.getY(), center.getZ()),
                    spec));
            }
        }

        return switch (startResult) {
            case STARTED -> ArcanaDecision.allow();
            case OWNER_ALREADY_ACTIVE -> ArcanaDecision.deny(
                "forbidden_domain_owner_active",
                "Owner already has an active Forbidden Domain");
            case GLOBAL_LIMIT -> ArcanaDecision.deny(
                "forbidden_domain_global_limit",
                "Server Forbidden Domain capacity is exhausted");
        };
    }

    /**
     * Adds an already-loaded participant to an existing localized field after canonical entity admission.
     * Capture records only UUID membership; it never owns inventory, capability or teleport state.
     */
    public static ArcanaDecision captureParticipant(
            MinecraftServer server,
            UUID ownerId,
            UUID participantId
    ) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(ownerId, "ownerId");
        Objects.requireNonNull(participantId, "participantId");
        if (ownerId.equals(participantId)) {
            return ArcanaDecision.deny(
                "forbidden_domain_owner_not_participant",
                "Domain owner is implicit and is not tracked as a captured participant");
        }

        ServerState state = STATES.get(server);
        if (state == null) {
            return ArcanaDecision.deny("forbidden_domain_missing", "No Forbidden Domain runtime state exists");
        }

        FieldContext field;
        synchronized (state) {
            field = state.fields.get(ownerId);
            if (field == null || state.domains.session(ownerId).isEmpty()) {
                return ArcanaDecision.deny("forbidden_domain_missing", "Owner has no active Forbidden Domain");
            }
        }

        ArcanaServerRuntime runtime = ArcanaServerRuntimeManager.get(server).orElse(null);
        if (runtime == null) {
            return ArcanaDecision.deny(
                "forbidden_domain_runtime_unavailable",
                "Black Arcana server runtime is unavailable");
        }

        LivingEntity owner = findLoadedLivingEntity(server, ownerId);
        LivingEntity participant = findLoadedLivingEntity(server, participantId);
        if (owner == null || participant == null || !owner.isAlive() || !participant.isAlive()) {
            return ArcanaDecision.deny(
                "forbidden_domain_participant_unavailable",
                "Owner and participant must remain loaded living entities");
        }
        if (!(participant.level() instanceof ServerLevel level)
                || participant.level() != owner.level()
                || !field.dimensionId().equals(level.dimension().location().toString())) {
            return ArcanaDecision.deny(
                "forbidden_domain_dimension_mismatch",
                "Participant must be in the active domain dimension");
        }
        if (!insideRadius(field.center(), participant.blockPosition(), field.spec().radius())) {
            return ArcanaDecision.deny(
                "forbidden_domain_outside_field",
                "Participant is outside the bounded Forbidden Domain radius");
        }

        BlockPos participantPos = participant.blockPosition();
        if (level.getChunkSource().getChunkNow(participantPos.getX() >> 4, participantPos.getZ() >> 4) == null) {
            return ArcanaDecision.deny(
                "forbidden_domain_chunk_unloaded",
                "Participant chunk is not already loaded");
        }

        EntityProtectionFacts facts = MinecraftEntityProtectionResolver.resolve(server, owner, participant);
        EntityInteractionAuthorization authorization = runtime.entityInteractionAdmission().authorize(
            EntityInteractionType.DOMAIN_CAPTURE,
            facts,
            new ProtectionQuery(
                ownerId,
                field.dimensionId(),
                participantId.toString(),
                EntityInteractionType.DOMAIN_CAPTURE));
        if (!authorization.decision().allowed()) return authorization.decision();

        MinecraftSafeDestinationResolver.Result recovery = MinecraftSafeDestinationResolver.evaluate(
            server,
            participant,
            level,
            participant.getX(),
            participant.getY(),
            participant.getZ());
        if (!recovery.allowed()) {
            return ArcanaDecision.deny(
                "forbidden_domain_recovery_unsafe",
                "Participant current position is not a validated recovery destination: " + recovery.code());
        }

        synchronized (state) {
            if (state.domains.session(ownerId).isEmpty()) {
                return ArcanaDecision.deny("forbidden_domain_missing", "Forbidden Domain ended during capture admission");
            }
            if (!state.domains.trackParticipant(ownerId, participantId)) {
                return ArcanaDecision.deny(
                    "forbidden_domain_participant_limit",
                    "Forbidden Domain participant budget is exhausted");
            }
        }
        return ArcanaDecision.allow();
    }

    public static boolean close(MinecraftServer server, UUID ownerId) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(ownerId, "ownerId");
        ServerState state = STATES.get(server);
        if (state == null) return false;
        synchronized (state) {
            boolean closed = state.domains.close(ownerId, ForbiddenDomainSession.CloseReason.EXPLICIT);
            state.fields.remove(ownerId);
            return closed;
        }
    }

    public static int activeCount(MinecraftServer server) {
        Objects.requireNonNull(server, "server");
        ServerState state = STATES.get(server);
        return state == null ? 0 : state.domains.activeCount();
    }

    static List<ChunkRef> coveredChunks(String dimensionId, BlockPos center, int radius) {
        Objects.requireNonNull(dimensionId, "dimensionId");
        Objects.requireNonNull(center, "center");
        if (dimensionId.isBlank()) throw new IllegalArgumentException("dimensionId cannot be blank");
        if (radius <= 0 || radius > ForbiddenDomainSafetyCeilings.MAX_RADIUS) {
            throw new IllegalArgumentException(
                "radius must be within 1.." + ForbiddenDomainSafetyCeilings.MAX_RADIUS);
        }

        int minChunkX = Math.floorDiv(center.getX() - radius, 16);
        int maxChunkX = Math.floorDiv(center.getX() + radius, 16);
        int minChunkZ = Math.floorDiv(center.getZ() - radius, 16);
        int maxChunkZ = Math.floorDiv(center.getZ() + radius, 16);
        List<ChunkRef> chunks = new ArrayList<>((maxChunkX - minChunkX + 1) * (maxChunkZ - minChunkZ + 1));
        for (int chunkX = minChunkX; chunkX <= maxChunkX; chunkX++) {
            for (int chunkZ = minChunkZ; chunkZ <= maxChunkZ; chunkZ++) {
                chunks.add(new ChunkRef(dimensionId, chunkX, chunkZ));
            }
        }
        return List.copyOf(chunks);
    }

    private static AdmissionEvaluation evaluateAdmission(
            MinecraftServer server,
            ArcanaServerRuntime runtime,
            LivingEntity owner,
            ServerLevel level,
            BlockPos center,
            ForbiddenDomainSpec spec
    ) {
        String dimensionId = level.dimension().location().toString();
        List<ChunkRef> chunks = coveredChunks(dimensionId, center, spec.radius());

        boolean chunksLoaded = true;
        for (ChunkRef chunk : chunks) {
            if (level.getChunkSource().getChunkNow(chunk.chunkX(), chunk.chunkZ()) == null) {
                chunksLoaded = false;
                break;
            }
        }

        double minX = (double) center.getX() - spec.radius();
        double minZ = (double) center.getZ() - spec.radius();
        double maxX = (double) center.getX() + spec.radius() + 1.0D;
        double maxZ = (double) center.getZ() + spec.radius() + 1.0D;
        boolean insideWorldBorder = level.getWorldBorder().isWithinBounds(
            new AABB(minX, center.getY(), minZ, maxX, center.getY() + 1.0D, maxZ));

        boolean protectionAllowed = false;
        ArcanaDecision protectionDecision = ArcanaDecision.deny(
            "forbidden_domain_protection_unavailable",
            "Protected destination guard is unavailable");
        ProtectedDestinationGuard guard = runtime.protectedDestinationGuard().orElse(null);
        if (guard != null && chunksLoaded) {
            protectionAllowed = true;
            protectionDecision = ArcanaDecision.allow();
            for (ChunkRef chunk : chunks) {
                ArcanaDecision chunkDecision = guard.authorize(
                    chunk,
                    new ProtectionQuery(
                        owner.getUUID(),
                        dimensionId,
                        "domain_chunk:" + chunk.chunkX() + "," + chunk.chunkZ(),
                        EntityInteractionType.DOMAIN_CAPTURE));
                if (!chunkDecision.allowed()) {
                    protectionAllowed = false;
                    protectionDecision = chunkDecision;
                    break;
                }
            }
        }

        String targetId = "domain@" + center.getX() + "," + center.getY() + "," + center.getZ();
        ArcanaCastRequest request = new ArcanaCastRequest(
            ArcanaCastId.random(),
            WORLD_SAFETY_SPELL,
            new ArcanaCastContext(owner.getUUID(), level.getGameTime(), dimensionId),
            0,
            targetId);
        ArcanaServices.TargetResolution target = ArcanaServices.TargetResolution.resolved(targetId);
        ArcanaDecision worldDecision = runtime.worldEffectPolicy().authorizeCast(request, target);
        if (worldDecision.allowed()) {
            worldDecision = runtime.worldEffectPolicy().authorize(request, target, WorldMutationClass.COSMETIC);
        }
        boolean worldEffectAllowed = worldDecision.allowed();

        MinecraftSafeDestinationResolver.Result recovery = MinecraftSafeDestinationResolver.evaluate(
            server,
            owner,
            level,
            owner.getX(),
            owner.getY(),
            owner.getZ());
        boolean safeRecoveryAvailable = recovery.allowed();

        ForbiddenDomainAdmission facts = new ForbiddenDomainAdmission(
            chunksLoaded,
            insideWorldBorder,
            protectionAllowed,
            worldEffectAllowed,
            safeRecoveryAvailable);
        if (facts.admitted()) return new AdmissionEvaluation(facts, ArcanaDecision.allow());
        if (!chunksLoaded) {
            return denied(facts, "forbidden_domain_chunk_unloaded", "Forbidden Domain intersects an unloaded chunk");
        }
        if (!insideWorldBorder) {
            return denied(facts, "forbidden_domain_world_border", "Forbidden Domain would cross the world border");
        }
        if (!protectionAllowed) return new AdmissionEvaluation(facts, protectionDecision);
        if (!worldEffectAllowed) return new AdmissionEvaluation(facts, worldDecision);
        return denied(
            facts,
            "forbidden_domain_recovery_unsafe",
            "Owner current position is not a validated recovery destination: " + recovery.code());
    }

    private static AdmissionEvaluation denied(ForbiddenDomainAdmission facts, String code, String detail) {
        return new AdmissionEvaluation(facts, ArcanaDecision.deny(code, detail));
    }

    private static boolean insideRadius(BlockPos center, BlockPos target, int radius) {
        long dx = (long) target.getX() - center.getX();
        long dy = (long) target.getY() - center.getY();
        long dz = (long) target.getZ() - center.getZ();
        long radiusSquared = (long) radius * radius;
        return dx * dx + dy * dy + dz * dz <= radiusSquared;
    }

    private static LivingEntity findLoadedLivingEntity(MinecraftServer server, UUID entityId) {
        for (ServerLevel level : server.getAllLevels()) {
            Entity entity = level.getEntity(entityId);
            if (entity instanceof LivingEntity living) return living;
        }
        return null;
    }

    private static void installWorldProfile(ArcanaServerRuntime runtime) {
        Objects.requireNonNull(runtime, "runtime");
        if (runtime.worldEffectProfiles().find(WORLD_SAFETY_ID).isPresent()) return;
        runtime.worldEffectProfiles().register(
            WORLD_SAFETY_ID,
            new WorldEffectProfile(
                WorldMutationType.VISUAL_FIELD,
                WorldMutationClass.COSMETIC,
                ForbiddenDomainSafetyCeilings.MAX_TRACKED_ENTITIES,
                false));
    }

    private static void onServerStarted(ServerStartedEvent event) {
        STATES.put(event.getServer(), new ServerState());
    }

    private static void onServerTick(ServerTickEvent.Post event) {
        MinecraftServer server = event.getServer();
        ServerState state = STATES.get(server);
        if (state == null) return;
        long nowTick = server.overworld().getGameTime();
        state.domains.expire(nowTick);
        synchronized (state) {
            state.fields.keySet().removeIf(ownerId -> state.domains.session(ownerId).isEmpty());
        }
    }

    private static void onPlayerLoggedOut(PlayerEvent.PlayerLoggedOutEvent event) {
        MinecraftServer server = event.getEntity().level().getServer();
        if (server == null) return;
        ServerState state = STATES.get(server);
        if (state == null) return;
        UUID playerId = event.getEntity().getUUID();
        synchronized (state) {
            state.domains.clearOwner(playerId);
            state.fields.remove(playerId);
        }
    }

    private static void onServerStopped(ServerStoppedEvent event) {
        ServerState state = STATES.remove(event.getServer());
        if (state == null) return;
        synchronized (state) {
            state.domains.clearForServerStop();
            state.fields.clear();
        }
    }

    private static ServerState stateFor(MinecraftServer server) {
        synchronized (STATES) {
            return STATES.computeIfAbsent(server, ignored -> new ServerState());
        }
    }

    private record AdmissionEvaluation(ForbiddenDomainAdmission facts, ArcanaDecision decision) {
        private AdmissionEvaluation {
            Objects.requireNonNull(facts, "facts");
            Objects.requireNonNull(decision, "decision");
            if (decision.allowed() != facts.admitted()) {
                throw new IllegalArgumentException("Forbidden Domain admission facts and decision disagree");
            }
        }
    }

    private record FieldContext(String dimensionId, BlockPos center, ForbiddenDomainSpec spec) {
        private FieldContext {
            Objects.requireNonNull(dimensionId, "dimensionId");
            Objects.requireNonNull(center, "center");
            Objects.requireNonNull(spec, "spec");
            if (dimensionId.isBlank()) throw new IllegalArgumentException("dimensionId cannot be blank");
        }
    }

    private static final class ServerState {
        final ForbiddenDomainRuntime domains =
            new ForbiddenDomainRuntime(ForbiddenDomainSafetyCeilings.MAX_ACTIVE_DOMAINS);
        final Map<UUID, FieldContext> fields = new LinkedHashMap<>();
    }
}
