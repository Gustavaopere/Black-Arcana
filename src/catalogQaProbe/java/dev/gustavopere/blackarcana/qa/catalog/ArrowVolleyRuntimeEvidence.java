package dev.gustavopere.blackarcana.qa.catalog;

import com.mojang.logging.LogUtils;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.projectile.Projectile;
import net.neoforged.neoforge.common.NeoForge;
import net.neoforged.neoforge.event.entity.EntityJoinLevelEvent;
import net.neoforged.neoforge.event.entity.EntityLeaveLevelEvent;
import net.neoforged.neoforge.event.tick.ServerTickEvent;
import org.slf4j.Logger;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

/**
 * Optional, strictly passive QA-only observer for the exact assembled Iron's server.
 *
 * The source set is packaged as a separate companion JAR, not as production
 * Black Arcana content. It never creates, removes, teleports, mutates or scans
 * entities. Its owner/proximity attribution is a CANDIDATE, not cast provenance.
 *
 * Enable only in an isolated QA run with:
 * -Dblack_arcana.catalog_qa.arrow_volley=true
 */
final class ArrowVolleyRuntimeEvidence {
    private static final Logger LOG = LogUtils.getLogger();
    private static final String PREFIX = "[BLACK_ARCANA_ARROW_VOLLEY_QA]";
    private static final ResourceLocation CONTROLLER =
        ResourceLocation.fromNamespaceAndPath("irons_spellbooks", "arrow_volley");
    private static final ResourceLocation ARROW =
        ResourceLocation.fromNamespaceAndPath("irons_spellbooks", "small_magic_arrow");

    private static final int MAX_TOTAL_SESSIONS = 16;
    private static final int MAX_ACTIVE_SESSIONS = 4;
    private static final int MAX_OBSERVATION_TICKS = 100;
    private static final int MAX_CANDIDATES_PER_SESSION = 256;
    private static final double MAX_MATCH_DISTANCE_SQUARED = 64.0;

    private static final Map<UUID, Trace> ACTIVE = new LinkedHashMap<>();
    private static int begun;
    private static int unmatchedArrowJoins;
    private static int ambiguousArrowJoins;

    private ArrowVolleyRuntimeEvidence() {
    }

    static void install() {
        NeoForge.EVENT_BUS.addListener(ArrowVolleyRuntimeEvidence::onJoin);
        NeoForge.EVENT_BUS.addListener(ArrowVolleyRuntimeEvidence::onLeave);
        NeoForge.EVENT_BUS.addListener(ArrowVolleyRuntimeEvidence::onServerTick);
        LOG.info("{} type=armed status=OBSERVING_ONLY max_sessions={} max_active={} max_ticks={} max_candidates={}",
            PREFIX, MAX_TOTAL_SESSIONS, MAX_ACTIVE_SESSIONS, MAX_OBSERVATION_TICKS,
            MAX_CANDIDATES_PER_SESSION);
    }

    private static void onJoin(EntityJoinLevelEvent event) {
        if (!(event.getLevel() instanceof ServerLevel level)) {
            return;
        }
        Entity entity = event.getEntity();
        ResourceLocation id = BuiltInRegistries.ENTITY_TYPE.getKey(entity.getType());

        if (CONTROLLER.equals(id)) {
            if (begun >= MAX_TOTAL_SESSIONS || ACTIVE.size() >= MAX_ACTIVE_SESSIONS) {
                LOG.warn("{} type=controller_ignored status=BUDGET_EXHAUSTED", PREFIX);
                return;
            }
            if (!(entity instanceof Projectile projectile) || projectile.getOwner() == null) {
                LOG.warn("{} type=controller_ignored status=OWNER_UNAVAILABLE", PREFIX);
                return;
            }
            UUID controllerId = entity.getUUID();
            Trace trace = new Trace(level, controllerId, projectile.getOwner().getUUID(),
                level.getGameTime());
            ACTIVE.put(controllerId, trace);
            begun++;
            LOG.info("{} type=begin controller={} dimension={} join_game_tick={} status=JOIN_CANDIDATE",
                PREFIX, controllerId, level.dimension().location(), trace.joinGameTick);
            return;
        }
        if (!ARROW.equals(id) || ACTIVE.isEmpty()) {
            return;
        }
        if (!(entity instanceof Projectile projectile) || projectile.getOwner() == null) {
            unmatchedArrowJoins++;
            return;
        }

        UUID owner = projectile.getOwner().getUUID();
        List<Trace> matches = new ArrayList<>(2);
        for (Trace trace : ACTIVE.values()) {
            if (trace.level == level && trace.owner.equals(owner)) {
                Entity controller = level.getEntity(trace.controller);
                if (controller != null
                    && controller.distanceToSqr(entity) <= MAX_MATCH_DISTANCE_SQUARED) {
                    matches.add(trace);
                }
            }
        }
        if (matches.size() != 1) {
            if (matches.size() > 1) {
                ambiguousArrowJoins++;
                for (Trace trace : matches) {
                    trace.ambiguousJoins++;
                }
            } else {
                unmatchedArrowJoins++;
            }
            return;
        }

        Trace trace = matches.get(0);
        trace.candidateJoins++;
        if (trace.candidates.size() >= MAX_CANDIDATES_PER_SESSION) {
            trace.budgetExceeded = true;
            return;
        }
        trace.candidates.putIfAbsent(entity.getUUID(), false);
        long tick = level.getGameTime();
        trace.byTick.merge(tick, 1, Integer::sum);
    }

    private static void onLeave(EntityLeaveLevelEvent event) {
        Entity entity = event.getEntity();
        Trace trace = ACTIVE.get(entity.getUUID());
        if (trace != null && event.getLevel() == trace.level) {
            trace.leaveSeen = true;
            trace.removal = entity.getRemovalReason() == null
                ? "NULL_REASON" : entity.getRemovalReason().name();
        }
    }

    private static void onServerTick(ServerTickEvent.Post event) {
        if (ACTIVE.isEmpty()) {
            return;
        }
        List<UUID> completed = new ArrayList<>();
        for (Trace trace : ACTIVE.values()) {
            long now = trace.level.getGameTime();
            Entity controller = trace.level.getEntity(trace.controller);
            if (controller != null) {
                int age = controller.tickCount;
                if (trace.previousAge != Integer.MIN_VALUE
                    && now > trace.previousGameTick
                    && age <= trace.previousAge) {
                    trace.monotonic = false;
                }
                if (trace.firstAge == Integer.MIN_VALUE) {
                    trace.firstAge = age;
                }
                trace.lastAge = age;
                trace.previousAge = age;
                trace.previousGameTick = now;
                trace.observedTicks++;
            }

            // Confirm candidates still exist in the level by UUID at server-tick end.
            // No chunk loads and no broad entity search. Fast despawns can be missed.
            for (Map.Entry<UUID, Boolean> entry : trace.candidates.entrySet()) {
                if (!entry.getValue() && trace.level.getEntity(entry.getKey()) != null) {
                    entry.setValue(true);
                    trace.confirmedPresent++;
                }
            }

            if (now - trace.joinGameTick >= MAX_OBSERVATION_TICKS
                || trace.leaveSeen
                || (controller == null && trace.observedTicks > 0)) {
                LOG.info("{} type=end controller={} join_game_tick={} status={} observed_ticks={} first_age={} last_age={} age_monotonic={} candidate_joins={} confirmed_present_at_post={} ambiguous_joins={} candidate_budget_exceeded={} leave_seen={} removal={} join_counts_per_tick={} unmatched_global={} ambiguous_global={}",
                    PREFIX, trace.controller, trace.joinGameTick,
                    trace.leaveSeen ? "LEFT_LEVEL" :
                        controller == null ? "ENTITY_NOT_FOUND" : "WINDOW_EXPIRED",
                    trace.observedTicks, trace.firstAge, trace.lastAge, trace.monotonic,
                    trace.candidateJoins, trace.confirmedPresent, trace.ambiguousJoins,
                    trace.budgetExceeded, trace.leaveSeen, trace.removal, trace.byTick,
                    unmatchedArrowJoins, ambiguousArrowJoins);
                completed.add(trace.controller);
            }
        }
        for (UUID id : completed) {
            ACTIVE.remove(id);
        }
    }

    private static final class Trace {
        final ServerLevel level;
        final UUID controller;
        final UUID owner;
        final long joinGameTick;
        final Map<UUID, Boolean> candidates = new LinkedHashMap<>();
        final Map<Long, Integer> byTick = new LinkedHashMap<>();
        int firstAge = Integer.MIN_VALUE;
        int lastAge = Integer.MIN_VALUE;
        int previousAge = Integer.MIN_VALUE;
        long previousGameTick = Long.MIN_VALUE;
        int observedTicks;
        int candidateJoins;
        int confirmedPresent;
        int ambiguousJoins;
        boolean monotonic = true;
        boolean budgetExceeded;
        boolean leaveSeen;
        String removal = "NOT_OBSERVED";

        Trace(ServerLevel level, UUID controller, UUID owner, long joinGameTick) {
            this.level = level;
            this.controller = controller;
            this.owner = owner;
            this.joinGameTick = joinGameTick;
        }
    }
}
