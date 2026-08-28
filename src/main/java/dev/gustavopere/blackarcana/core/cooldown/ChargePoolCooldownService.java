package dev.gustavopere.blackarcana.core.cooldown;

import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaChargeSpec;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaServices.CooldownService;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;

import java.util.HashMap;
import java.util.Map;
import java.util.Objects;
import java.util.Set;
import java.util.UUID;
import java.util.function.Function;

public final class ChargePoolCooldownService implements CooldownService {
    private final Function<ArcanaCastRequest, ArcanaChargeSpec> policy;
    private final Map<ChargeKey, State> states = new HashMap<>();

    public ChargePoolCooldownService(Function<ArcanaCastRequest, ArcanaChargeSpec> policy) {
        this.policy = Objects.requireNonNull(policy, "policy");
    }

    @Override
    public synchronized ArcanaDecision check(ArcanaCastRequest request) {
        ArcanaChargeSpec spec = requireSpec(request);
        State state = stateFor(request, spec);
        refresh(state, request.context().serverTick(), spec);
        if (state.charges > 0) return ArcanaDecision.allow();
        long remaining = Math.max(0L, state.nextRechargeAt - request.context().serverTick());
        return ArcanaDecision.deny("no_charges", "remaining_ticks=" + remaining);
    }

    @Override
    public synchronized void start(ArcanaCastRequest request) {
        ArcanaChargeSpec spec = requireSpec(request);
        long now = request.context().serverTick();
        State state = stateFor(request, spec);
        refresh(state, now, spec);
        if (state.charges <= 0) throw new IllegalStateException("charge consumed after successful check but none remained");

        state.charges--;
        state.persistent = spec.persistent();
        if (state.charges < spec.maxCharges() && state.nextRechargeAt == 0L) {
            state.nextRechargeAt = safeAdd(now, spec.rechargeTicks());
        }
    }

    public synchronized int charges(ArcanaCastRequest request) {
        ArcanaChargeSpec spec = requireSpec(request);
        State state = stateFor(request, spec);
        refresh(state, request.context().serverTick(), spec);
        return state.charges;
    }

    public synchronized Map<ChargeKey, SnapshotEntry> persistentSnapshot() {
        Map<ChargeKey, SnapshotEntry> result = new HashMap<>();
        states.forEach((key, state) -> {
            if (state.persistent) result.put(key, new SnapshotEntry(state.charges, state.nextRechargeAt));
        });
        return Map.copyOf(result);
    }

    public synchronized void restorePersistentSnapshot(Map<ChargeKey, SnapshotEntry> snapshot) {
        Objects.requireNonNull(snapshot, "snapshot");
        snapshot.forEach((key, entry) -> {
            Objects.requireNonNull(key, "charge key");
            Objects.requireNonNull(entry, "charge snapshot entry");
            states.put(key, new State(entry.charges(), entry.nextRechargeAt(), true));
        });
    }

    /** Renames active/restored groups before pruning removed groups. */
    public synchronized int migrateGroups(RuntimeGroupMigrations migrations) {
        Objects.requireNonNull(migrations, "migrations");
        if (migrations.isEmpty() || states.isEmpty()) return 0;

        Map<ChargeKey, State> migrated = new HashMap<>();
        int renamed = 0;
        for (Map.Entry<ChargeKey, State> item : states.entrySet()) {
            ChargeKey oldKey = item.getKey();
            String resolvedGroup = migrations.resolve(oldKey.groupId());
            if (!resolvedGroup.equals(oldKey.groupId())) renamed++;

            ChargeKey newKey = new ChargeKey(oldKey.casterId(), resolvedGroup);
            State source = item.getValue();
            State copy = new State(source.charges, source.nextRechargeAt, source.persistent);
            migrated.merge(newKey, copy, ChargePoolCooldownService::mergeRestrictively);
        }
        states.clear();
        states.putAll(migrated);
        return renamed;
    }

    /** Removes charge groups that no longer have an active server policy. */
    public synchronized int pruneGroups(Set<String> activeGroupIds) {
        Set<String> active = validateGroups(activeGroupIds);
        int before = states.size();
        states.keySet().removeIf(key -> !active.contains(key.groupId()));
        return before - states.size();
    }

    public synchronized int size() {
        return states.size();
    }

    private State stateFor(ArcanaCastRequest request, ArcanaChargeSpec spec) {
        ChargeKey key = new ChargeKey(request.context().casterId(), spec.groupId());
        return states.computeIfAbsent(key, ignored -> new State(spec.maxCharges(), 0L, spec.persistent()));
    }

    private void refresh(State state, long now, ArcanaChargeSpec spec) {
        if (state.charges > spec.maxCharges()) state.charges = spec.maxCharges();
        state.persistent = spec.persistent();

        if (state.charges >= spec.maxCharges()) {
            state.nextRechargeAt = 0L;
            return;
        }

        if (state.nextRechargeAt == 0L) {
            state.nextRechargeAt = safeAdd(now, spec.rechargeTicks());
            return;
        }
        if (now < state.nextRechargeAt) return;

        long elapsedIntervals = 1L + (now - state.nextRechargeAt) / spec.rechargeTicks();
        int recoverable = (int) Math.min(elapsedIntervals, spec.maxCharges() - state.charges);
        state.charges += recoverable;
        if (state.charges >= spec.maxCharges()) {
            state.nextRechargeAt = 0L;
        } else {
            state.nextRechargeAt = safeAdd(state.nextRechargeAt, safeMultiply(elapsedIntervals, spec.rechargeTicks()));
        }
    }

    private ArcanaChargeSpec requireSpec(ArcanaCastRequest request) {
        return Objects.requireNonNull(policy.apply(request), "charge spec");
    }

    private static State mergeRestrictively(State left, State right) {
        return new State(
                Math.min(left.charges, right.charges),
                Math.max(left.nextRechargeAt, right.nextRechargeAt),
                left.persistent || right.persistent);
    }

    private static Set<String> validateGroups(Set<String> groupIds) {
        Objects.requireNonNull(groupIds, "groupIds");
        Set<String> copy = Set.copyOf(groupIds);
        copy.forEach(ArcanaSpellId::parse);
        return copy;
    }

    private static long safeAdd(long value, long delta) {
        if (delta > Long.MAX_VALUE - value) return Long.MAX_VALUE;
        return value + delta;
    }

    private static long safeMultiply(long left, long right) {
        if (left == 0L || right == 0L) return 0L;
        if (left > Long.MAX_VALUE / right) return Long.MAX_VALUE;
        return left * right;
    }

    public record ChargeKey(UUID casterId, String groupId) {
        public ChargeKey {
            Objects.requireNonNull(casterId, "casterId");
            Objects.requireNonNull(groupId, "groupId");
            ArcanaSpellId.parse(groupId);
        }
    }

    public record SnapshotEntry(int charges, long nextRechargeAt) {
        public SnapshotEntry {
            if (charges < 0 || charges > ArcanaChargeSpec.ABSOLUTE_MAX_CHARGES) {
                throw new IllegalArgumentException("charges outside absolute bounds");
            }
            if (nextRechargeAt < 0L) throw new IllegalArgumentException("nextRechargeAt cannot be negative");
        }
    }

    private static final class State {
        private int charges;
        private long nextRechargeAt;
        private boolean persistent;

        private State(int charges, long nextRechargeAt, boolean persistent) {
            this.charges = charges;
            this.nextRechargeAt = nextRechargeAt;
            this.persistent = persistent;
        }
    }
}
