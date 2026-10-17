package dev.gustavopere.blackarcana.qa.catalog;

import com.mojang.logging.LogUtils;
import io.redspace.ironsspellbooks.api.events.SpellDamageEvent;
import io.redspace.ironsspellbooks.api.events.SpellOnCastEvent;
import io.redspace.ironsspellbooks.api.magic.MagicData;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.LivingEntity;
import net.neoforged.neoforge.common.NeoForge;
import net.neoforged.neoforge.event.entity.living.LivingDamageEvent;
import net.neoforged.neoforge.event.server.ServerStoppedEvent;
import net.neoforged.neoforge.event.tick.ServerTickEvent;
import org.slf4j.Logger;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

/**
 * READ-ONLY optional companion probe. No casts, rewards, effects, entity edits,
 * reflection, chunk loads or scans. A QA session slot is not an Iron's session ID.
 *
 * Activate on isolated modpack test server only:
 * -Dblack_arcana.catalog_qa.irons_event_phase=true
 *
 * The event canceled flag is a snapshot at observer notification time, NOT
 * evidence of the final value after all other listeners have returned.
 */
final class IronsEventPhaseRuntimeEvidence {
    private static final Logger LOG = LogUtils.getLogger();
    private static final String PREFIX = "[BLACK_ARCANA_PHASE_QA]";
    private static final String ELDRITCH = "irons_spellbooks:eldritch_blast";
    private static final String DASH = "irons_spellbooks:burning_dash";
    private static final int MAX_ACTORS = 8;
    private static final int MAX_TARGETS = 64;
    private static final int MAX_CASTS = 64;
    private static final int MAX_ATTEMPTS = 192;
    private static final int MAX_PENDING = 16;
    private static final int MAX_SESSIONS = 16;
    private static final long MAX_RECAST_OBSERVATION_GAP = 100L;

    private static final Map<UUID, Integer> ACTORS = new LinkedHashMap<>();
    private static final Map<UUID, Integer> TARGETS = new LinkedHashMap<>();
    private static final Map<UUID, CandidateSession> SESSIONS = new HashMap<>();
    private static final List<CastSample> CAST_PENDING = new ArrayList<>();
    private static final List<DamageSample> DAMAGE_PENDING = new ArrayList<>();
    private static int castEvents;
    private static int damageEvents;
    private static int sessionCounter;
    private static boolean budgetWarned;
    private static boolean providerInterfaceWarned;

    private IronsEventPhaseRuntimeEvidence() {}

    // Only for removable QA and only against the exact, source-verified
    // 3.16.3 provider JAR. This is NOT a public API contract for gameplay.
    // The compileOnly :api classifier intentionally omits PlayerRecasts and
    // SpellDamageSource, so neither type is statically linked.
    private static void providerUnavailable(String reason) {
        if (!providerInterfaceWarned) {
            providerInterfaceWarned = true;
            LOG.warn("{} type=probe_unavailable reason={} state=FAIL_CLOSED",
                    PREFIX, reason);
        }
    }

    private static Boolean recastActiveSnapshot(MagicData data) {
        try {
            Object recasts = data.getClass().getMethod("getPlayerRecasts")
                    .invoke(data);
            Object result = recasts.getClass()
                    .getMethod("hasRecastForSpell", String.class)
                    .invoke(recasts, ELDRITCH);
            if (result instanceof Boolean flag) {
                return flag;
            }
        } catch (ReflectiveOperationException | RuntimeException | LinkageError failure) {
            providerUnavailable("PROVIDER_RECAST_METHOD_UNAVAILABLE");
            return null;
        }
        providerUnavailable("PROVIDER_RECAST_RESULT_INVALID");
        return null;
    }

    private static String readSourceSpellId(Object source) {
        if (source == null || !source.getClass().getName().equals(
                "io.redspace.ironsspellbooks.damage.SpellDamageSource")) {
            return null;
        }
        try {
            Object spell = source.getClass().getMethod("spell").invoke(source);
            Object result = spell.getClass().getMethod("getSpellId").invoke(spell);
            if (result instanceof String id) {
                return id;
            }
        } catch (ReflectiveOperationException | RuntimeException | LinkageError failure) {
            providerUnavailable("PROVIDER_DAMAGE_SPELL_METHOD_UNAVAILABLE");
            return null;
        }
        providerUnavailable("PROVIDER_DAMAGE_SPELL_RESULT_INVALID");
        return null;
    }

    private static DamageSource damageSourceSnapshot(SpellDamageEvent event) {
        try {
            Object source = event.getClass().getMethod("getSpellDamageSource")
                    .invoke(event);
            if (source instanceof DamageSource damage) {
                return damage;
            }
        } catch (ReflectiveOperationException | RuntimeException | LinkageError failure) {
            providerUnavailable("PROVIDER_DAMAGE_SOURCE_METHOD_UNAVAILABLE");
            return null;
        }
        providerUnavailable("PROVIDER_DAMAGE_SOURCE_RESULT_INVALID");
        return null;
    }

    static void install() {
        NeoForge.EVENT_BUS.addListener(IronsEventPhaseRuntimeEvidence::onCast);
        NeoForge.EVENT_BUS.addListener(IronsEventPhaseRuntimeEvidence::onSpellDamage);
        NeoForge.EVENT_BUS.addListener(IronsEventPhaseRuntimeEvidence::onPostDamage);
        NeoForge.EVENT_BUS.addListener(IronsEventPhaseRuntimeEvidence::onServerTick);
        NeoForge.EVENT_BUS.addListener(IronsEventPhaseRuntimeEvidence::onServerStopped);
        LOG.info("{} type=armed state=OBSERVING_ONLY actors={} targets={} casts={} attempts={} pending={} sessions={}",
                PREFIX, MAX_ACTORS, MAX_TARGETS, MAX_CASTS, MAX_ATTEMPTS,
                MAX_PENDING, MAX_SESSIONS);
    }

    private static Integer allocateSlot(Map<UUID, Integer> registry, UUID id, int cap) {
        Integer current = registry.get(id);
        if (current != null) {
            return current;
        }
        if (registry.size() >= cap) {
            budgetExceeded();
            return null;
        }
        int next = registry.size() + 1;
        registry.put(id, next);
        return next;
    }

    private static void budgetExceeded() {
        if (!budgetWarned) {
            budgetWarned = true;
            LOG.warn("{} type=budget_exhausted state=FAIL_CLOSED", PREFIX);
        }
    }

    private static void onCast(SpellOnCastEvent event) {
        if (!ELDRITCH.equals(event.getSpellId())
                || !(event.getEntity() instanceof ServerPlayer actor)
                || !(actor.level() instanceof ServerLevel level)) {
            return;
        }
        if (castEvents >= MAX_CASTS || CAST_PENDING.size() >= MAX_PENDING) {
            budgetExceeded();
            return;
        }
        Integer actorSlot = allocateSlot(ACTORS, actor.getUUID(), MAX_ACTORS);
        if (actorSlot == null) {
            return;
        }

        MagicData data = MagicData.getPlayerMagicData(actor);
        // This is read at the SpellOnCastEvent listener; the provider checked
        // recast earlier. Another listener may still mutate event level/cost.
        Boolean priorSnapshot = recastActiveSnapshot(data);
        if (priorSnapshot == null) {
            return;
        }
        boolean prior = priorSnapshot;
        long tick = level.getGameTime();
        CandidateSession previous = SESSIONS.get(actor.getUUID());
        String kind;
        int sessionSlot;
        if (!prior) {
            if (sessionCounter >= MAX_SESSIONS) {
                budgetExceeded();
                return;
            }
            sessionSlot = ++sessionCounter;
            SESSIONS.put(actor.getUUID(), new CandidateSession(sessionSlot, tick));
            kind = "ROOT_CANDIDATE";
        } else if (previous != null && tick >= previous.lastTick
                && tick - previous.lastTick <= MAX_RECAST_OBSERVATION_GAP) {
            sessionSlot = previous.slot;
            previous.lastTick = tick;
            kind = "RECAST_CANDIDATE";
        } else {
            sessionSlot = 0;
            kind = "UNLINKED_RECAST";
        }

        castEvents++;
        LOG.info("{} type=cast actor_slot={} session_slot={} classification={} prior_recast={} tick={} original_level={} event_level_snapshot={} mana_at_event_snapshot={} cast_source={}",
                PREFIX, actorSlot, sessionSlot, kind, prior, tick,
                event.getOriginalSpellLevel(), event.getSpellLevel(), data.getMana(),
                event.getCastSource());
        CAST_PENDING.add(new CastSample(actor, level, actorSlot, sessionSlot, tick));
    }

    private static void onSpellDamage(SpellDamageEvent event) {
        DamageSource damage = damageSourceSnapshot(event);
        if (damage == null || !DASH.equals(readSourceSpellId(damage))) {
            return;
        }
        Entity attacker = damage.getEntity();
        LivingEntity target = event.getEntity();
        if (!(attacker instanceof ServerPlayer actor)
                || !(target.level() instanceof ServerLevel level)
                || actor.level() != level) {
            return;
        }
        if (damageEvents >= MAX_ATTEMPTS || DAMAGE_PENDING.size() >= MAX_PENDING) {
            budgetExceeded();
            return;
        }
        Integer actorSlot = allocateSlot(ACTORS, actor.getUUID(), MAX_ACTORS);
        Integer targetSlot = allocateSlot(TARGETS, target.getUUID(), MAX_TARGETS);
        if (actorSlot == null || targetSlot == null) {
            return;
        }
        int attemptSlot = ++damageEvents;
        long tick = level.getGameTime();
        DamageSample sample = new DamageSample(attemptSlot, actorSlot, targetSlot,
                actor.getUUID(), target.getUUID(), target, level, tick,
                event.isCanceled(), target.invulnerableTime);
        for (DamageSample previous : DAMAGE_PENDING) {
            if (previous.tick == tick && previous.targetId.equals(target.getUUID())
                    && previous.actorId.equals(actor.getUUID())) {
                previous.ambiguous = true;
                sample.ambiguous = true;
            }
        }
        DAMAGE_PENDING.add(sample);
    }

    private static void onPostDamage(LivingDamageEvent.Post event) {
        if (!DASH.equals(readSourceSpellId(event.getSource()))) {
            return;
        }
        Entity attacker = event.getSource().getEntity();
        LivingEntity target = event.getEntity();
        if (!(attacker instanceof ServerPlayer actor)
                || !(target.level() instanceof ServerLevel level)) {
            return;
        }
        long tick = level.getGameTime();
        List<DamageSample> matches = new ArrayList<>(2);
        for (DamageSample sample : DAMAGE_PENDING) {
            if (sample.level == level && sample.tick == tick
                    && sample.actorId.equals(actor.getUUID())
                    && sample.targetId.equals(target.getUUID())) {
                matches.add(sample);
            }
        }
        if (matches.size() == 1 && !matches.get(0).ambiguous) {
            matches.get(0).postHits++;
        } else {
            // An uncorrelated or multi-hit sample MUST never be promoted.
            for (DamageSample sample : matches) {
                sample.ambiguous = true;
            }
            if (matches.isEmpty()) {
                budgetExceeded();
            }
        }
    }

    private static void onServerTick(ServerTickEvent.Post event) {
        Iterator<CastSample> casts = CAST_PENDING.iterator();
        while (casts.hasNext()) {
            CastSample sample = casts.next();
            if (sample.level.getGameTime() >= sample.tick) {
                MagicData data = MagicData.getPlayerMagicData(sample.actor);
                Boolean active = recastActiveSnapshot(data);
                if (active != null) {
                    LOG.info("{} type=cast_followup actor_slot={} session_slot={} tick={} recast_after={} mana_after_snapshot={}",
                            PREFIX, sample.actorSlot, sample.sessionSlot, sample.tick,
                            active, data.getMana());
                }
                casts.remove();
            }
        }
        Iterator<DamageSample> attempts = DAMAGE_PENDING.iterator();
        while (attempts.hasNext()) {
            DamageSample sample = attempts.next();
            if (sample.level.getGameTime() >= sample.tick) {
                LOG.info("{} type=damage_followup attempt_slot={} actor_slot={} target_slot={} tick={} cancelled_event_snapshot={} post_hits={} ambiguous={} iframe_at_event={} iframe_at_post_tick={}",
                        PREFIX, sample.attemptSlot, sample.actorSlot,
                        sample.targetSlot, sample.tick, sample.cancelSnapshot,
                        sample.postHits, sample.ambiguous, sample.iframesAtEvent,
                        sample.target.invulnerableTime);
                attempts.remove();
            }
        }
    }

    private static void onServerStopped(ServerStoppedEvent event) {
        ACTORS.clear();
        TARGETS.clear();
        SESSIONS.clear();
        CAST_PENDING.clear();
        DAMAGE_PENDING.clear();
        castEvents = 0;
        damageEvents = 0;
        sessionCounter = 0;
        budgetWarned = false;
        providerInterfaceWarned = false;
    }

    private static final class CandidateSession {
        final int slot;
        long lastTick;
        CandidateSession(int slot, long tick) {
            this.slot = slot;
            this.lastTick = tick;
        }
    }

    private record CastSample(ServerPlayer actor, ServerLevel level,
                              int actorSlot, int sessionSlot, long tick) {}

    private static final class DamageSample {
        final int attemptSlot;
        final int actorSlot;
        final int targetSlot;
        final UUID actorId;
        final UUID targetId;
        final LivingEntity target;
        final ServerLevel level;
        final long tick;
        final boolean cancelSnapshot;
        final int iframesAtEvent;
        boolean ambiguous;
        int postHits;

        DamageSample(int attemptSlot, int actorSlot, int targetSlot,
                     UUID actorId, UUID targetId, LivingEntity target,
                     ServerLevel level, long tick, boolean cancelSnapshot,
                     int iframesAtEvent) {
            this.attemptSlot = attemptSlot;
            this.actorSlot = actorSlot;
            this.targetSlot = targetSlot;
            this.actorId = actorId;
            this.targetId = targetId;
            this.target = target;
            this.level = level;
            this.tick = tick;
            this.cancelSnapshot = cancelSnapshot;
            this.iframesAtEvent = iframesAtEvent;
        }
    }
}
