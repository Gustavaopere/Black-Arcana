package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.content.noetic.FamiliarOwnershipProvider;
import dev.gustavopere.blackarcana.content.noetic.FamiliarOwnershipRegistry;
import dev.gustavopere.blackarcana.content.noetic.NoeticSafetyCeilings;
import dev.gustavopere.blackarcana.content.noetic.PactSanctuarySpec;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntimeManager;
import dev.gustavopere.blackarcana.core.world.EntityInteractionAuthorization;
import dev.gustavopere.blackarcana.core.world.EntityInteractionType;
import dev.gustavopere.blackarcana.core.world.EntityProtectionFacts;
import dev.gustavopere.blackarcana.core.world.ProtectionQuery;
import net.minecraft.core.BlockPos;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.level.entity.EntityTypeTest;
import net.minecraft.world.phys.AABB;

import java.util.ArrayList;
import java.util.IdentityHashMap;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Set;
import java.util.UUID;

/**
 * Loaded-only, server-authoritative runtime for the Stage 07.07 Pact Sanctuary familiar aura.
 *
 * <p>The aura follows an explicitly owned familiar. It never acquires chunk tickets, never rewrites
 * teams/factions/brains and only clears the current hostile target of an ordinary mob when that target
 * is an explicitly supplied member currently inside the bounded familiar-centered aura.</p>
 */
public final class MinecraftPactSanctuaryRuntime {
    private final FamiliarOwnershipRegistry familiarOwnership;
    private final Map<MinecraftServer, ServerState> states = new IdentityHashMap<>();

    public MinecraftPactSanctuaryRuntime(FamiliarOwnershipRegistry familiarOwnership) {
        this.familiarOwnership = Objects.requireNonNull(familiarOwnership, "familiarOwnership");
    }

    public synchronized ArcanaDecision activate(
            MinecraftServer server,
            UUID ownerId,
            UUID familiarId,
            PactSanctuarySpec spec,
            Set<UUID> members
    ) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(ownerId, "ownerId");
        Objects.requireNonNull(familiarId, "familiarId");
        Objects.requireNonNull(spec, "spec");
        Objects.requireNonNull(members, "members");

        if (ownerId.equals(familiarId)) {
            return deny("pact_sanctuary_self_familiar", "Pact Sanctuary requires a distinct owned familiar");
        }

        LinkedHashSet<UUID> sanitizedMembers = new LinkedHashSet<>();
        for (UUID member : members) {
            if (member == null) {
                return deny("pact_sanctuary_member_null", "Sanctuary members must be concrete entity UUIDs");
            }
            sanitizedMembers.add(member);
            if (sanitizedMembers.size() > spec.memberBudget()
                    || sanitizedMembers.size() > NoeticSafetyCeilings.MAX_SANCTUARY_MEMBERS) {
                return deny("pact_sanctuary_member_limit", "Sanctuary member budget exceeds the hard ceiling");
            }
        }

        LivingEntity owner = findLoadedLivingEntity(server, ownerId);
        LivingEntity familiar = findLoadedLivingEntity(server, familiarId);
        if (owner == null || !owner.isAlive()) {
            return deny("pact_sanctuary_owner_unavailable", "Sanctuary owner must be a loaded living entity");
        }
        if (familiar == null || !familiar.isAlive()) {
            return deny("pact_sanctuary_familiar_unavailable", "Sanctuary familiar must be a loaded living entity");
        }
        if (!(familiar.level() instanceof ServerLevel level) || owner.level() != level) {
            return deny("pact_sanctuary_dimension", "Owner and familiar must share one loaded server dimension");
        }

        FamiliarOwnershipProvider.Result ownership = familiarOwnership.ownership(ownerId, familiar);
        if (ownership != FamiliarOwnershipProvider.Result.OWNED) {
            return deny(
                    ownership == FamiliarOwnershipProvider.Result.NOT_OWNED
                            ? "pact_sanctuary_foreign_familiar"
                            : "pact_sanctuary_ownership_unsupported",
                    "Pact Sanctuary requires explicit familiar ownership confirmation");
        }

        if (!allAuraChunksLoaded(level, familiar.blockPosition(), spec.radiusBlocks())) {
            return deny("pact_sanctuary_chunk_unloaded", "Every aura-covering chunk must already be loaded");
        }

        ServerState state = states.computeIfAbsent(server, ignored -> new ServerState());
        if (state.familiarByOwner.containsKey(ownerId)) {
            return deny("pact_sanctuary_owner_active", "Owner already has an active Pact Sanctuary");
        }
        if (state.byFamiliar.containsKey(familiarId)) {
            return deny("pact_sanctuary_familiar_active", "Familiar already anchors an active Pact Sanctuary");
        }
        if (state.byFamiliar.size() >= NoeticSafetyCeilings.MAX_ACTIVE_SANCTUARIES) {
            return deny("pact_sanctuary_capacity", "Active Pact Sanctuary registry reached its hard ceiling");
        }

        long nowTick = level.getGameTime();
        ActiveSanctuary active = new ActiveSanctuary(
                ownerId,
                familiarId,
                spec,
                sanitizedMembers,
                Math.addExact(nowTick, spec.durationTicks()));
        state.byFamiliar.put(familiarId, active);
        state.familiarByOwner.put(ownerId, familiarId);
        return ArcanaDecision.allow();
    }

    /**
     * Revalidates every active aura and clears at most the bounded candidate budget per sanctuary.
     * The returned value is the number of hostile mob targets suppressed during this tick.
     */
    public synchronized int tick(MinecraftServer server) {
        Objects.requireNonNull(server, "server");
        ServerState state = states.get(server);
        if (state == null) return 0;

        ArcanaServerRuntime runtime = ArcanaServerRuntimeManager.get(server).orElse(null);
        long nowTick = server.overworld().getGameTime();
        List<UUID> closeFamiliars = new ArrayList<>();
        int suppressed = 0;

        for (ActiveSanctuary active : state.byFamiliar.values()) {
            if (runtime == null || nowTick >= active.expiresAtTick) {
                closeFamiliars.add(active.familiarId);
                continue;
            }

            LivingEntity owner = findLoadedLivingEntity(server, active.ownerId);
            LivingEntity familiar = findLoadedLivingEntity(server, active.familiarId);
            if (owner == null || familiar == null || !owner.isAlive() || !familiar.isAlive()
                    || !(familiar.level() instanceof ServerLevel level) || owner.level() != level) {
                closeFamiliars.add(active.familiarId);
                continue;
            }

            if (familiarOwnership.ownership(active.ownerId, familiar) != FamiliarOwnershipProvider.Result.OWNED) {
                closeFamiliars.add(active.familiarId);
                continue;
            }
            if (!allAuraChunksLoaded(level, familiar.blockPosition(), active.spec.radiusBlocks())) {
                closeFamiliars.add(active.familiarId);
                continue;
            }

            suppressed += suppressEligibleTargets(server, runtime, level, owner, familiar, active);
        }

        for (UUID familiarId : closeFamiliars) {
            closeByFamiliar(state, familiarId);
        }
        if (state.byFamiliar.isEmpty()) states.remove(server);
        return suppressed;
    }

    public synchronized int activeSanctuaries(MinecraftServer server) {
        Objects.requireNonNull(server, "server");
        ServerState state = states.get(server);
        return state == null ? 0 : state.byFamiliar.size();
    }

    /**
     * Clears any aura owned or anchored by the entity and removes it from member allowlists.
     * Repeated calls are idempotent and therefore return zero once no state remains.
     */
    public synchronized int clearEntity(MinecraftServer server, UUID entityId) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(entityId, "entityId");
        ServerState state = states.get(server);
        if (state == null) return 0;

        int changed = 0;
        UUID familiarByOwner = state.familiarByOwner.get(entityId);
        if (familiarByOwner != null && closeByFamiliar(state, familiarByOwner)) changed++;
        if (state.byFamiliar.containsKey(entityId) && closeByFamiliar(state, entityId)) changed++;

        for (ActiveSanctuary active : state.byFamiliar.values()) {
            if (active.members.remove(entityId)) changed++;
        }

        if (state.byFamiliar.isEmpty()) states.remove(server);
        return changed;
    }

    public synchronized int clearForServerStop(MinecraftServer server) {
        Objects.requireNonNull(server, "server");
        ServerState state = states.remove(server);
        if (state == null) return 0;
        int closed = state.byFamiliar.size();
        state.byFamiliar.clear();
        state.familiarByOwner.clear();
        return closed;
    }

    private static int suppressEligibleTargets(
            MinecraftServer server,
            ArcanaServerRuntime runtime,
            ServerLevel level,
            LivingEntity owner,
            LivingEntity familiar,
            ActiveSanctuary active
    ) {
        int radius = active.spec.radiusBlocks();
        double r = radius;
        AABB bounds = new AABB(
                familiar.getX() - r,
                familiar.getY() - r,
                familiar.getZ() - r,
                familiar.getX() + r,
                familiar.getY() + r,
                familiar.getZ() + r);

        List<Mob> candidates = new ArrayList<>(NoeticSafetyCeilings.MAX_SANCTUARY_MOBS_PER_TICK);
        level.getEntities(
                EntityTypeTest.forClass(Mob.class),
                bounds,
                mob -> mob.isAlive() && mob != familiar,
                candidates,
                NoeticSafetyCeilings.MAX_SANCTUARY_MOBS_PER_TICK);

        double radiusSquared = r * r;
        int suppressed = 0;
        for (Mob mob : candidates) {
            if (familiar.distanceToSqr(mob) > radiusSquared) continue;

            LivingEntity hostileTarget = mob.getTarget();
            if (hostileTarget == null || hostileTarget.level() != level) continue;
            if (!active.members.contains(hostileTarget.getUUID())) continue;
            if (!hostileTarget.isAlive() || familiar.distanceToSqr(hostileTarget) > radiusSquared) continue;

            EntityProtectionFacts facts = MinecraftEntityProtectionResolver.resolve(server, owner, mob);
            if (facts.boss() || facts.invulnerable()) continue;

            EntityInteractionAuthorization authorization = runtime.entityInteractionAdmission().authorize(
                    EntityInteractionType.CONTROL,
                    facts,
                    new ProtectionQuery(
                            active.ownerId,
                            level.dimension().location().toString(),
                            mob.getUUID().toString(),
                            EntityInteractionType.CONTROL));
            if (!authorization.decision().allowed()) continue;

            mob.setTarget(null);
            suppressed++;
        }
        return suppressed;
    }

    private static boolean allAuraChunksLoaded(ServerLevel level, BlockPos center, int radius) {
        int minChunkX = Math.floorDiv(center.getX() - radius, 16);
        int maxChunkX = Math.floorDiv(center.getX() + radius, 16);
        int minChunkZ = Math.floorDiv(center.getZ() - radius, 16);
        int maxChunkZ = Math.floorDiv(center.getZ() + radius, 16);
        for (int chunkX = minChunkX; chunkX <= maxChunkX; chunkX++) {
            for (int chunkZ = minChunkZ; chunkZ <= maxChunkZ; chunkZ++) {
                if (level.getChunkSource().getChunkNow(chunkX, chunkZ) == null) return false;
            }
        }
        return true;
    }

    private static LivingEntity findLoadedLivingEntity(MinecraftServer server, UUID entityId) {
        for (ServerLevel level : server.getAllLevels()) {
            Entity candidate = level.getEntity(entityId);
            if (candidate instanceof LivingEntity living) return living;
        }
        return null;
    }

    private static boolean closeByFamiliar(ServerState state, UUID familiarId) {
        ActiveSanctuary removed = state.byFamiliar.remove(familiarId);
        if (removed == null) return false;
        state.familiarByOwner.remove(removed.ownerId, familiarId);
        removed.members.clear();
        return true;
    }

    private static ArcanaDecision deny(String code, String detail) {
        return ArcanaDecision.deny(code, detail);
    }

    private static final class ServerState {
        private final Map<UUID, ActiveSanctuary> byFamiliar = new LinkedHashMap<>();
        private final Map<UUID, UUID> familiarByOwner = new LinkedHashMap<>();
    }

    private static final class ActiveSanctuary {
        private final UUID ownerId;
        private final UUID familiarId;
        private final PactSanctuarySpec spec;
        private final LinkedHashSet<UUID> members;
        private final long expiresAtTick;

        private ActiveSanctuary(
                UUID ownerId,
                UUID familiarId,
                PactSanctuarySpec spec,
                Set<UUID> members,
                long expiresAtTick
        ) {
            this.ownerId = Objects.requireNonNull(ownerId, "ownerId");
            this.familiarId = Objects.requireNonNull(familiarId, "familiarId");
            this.spec = Objects.requireNonNull(spec, "spec");
            this.members = new LinkedHashSet<>(Objects.requireNonNull(members, "members"));
            this.expiresAtTick = expiresAtTick;
        }
    }
}
