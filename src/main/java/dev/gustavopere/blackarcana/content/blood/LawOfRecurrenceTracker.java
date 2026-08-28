package dev.gustavopere.blackarcana.content.blood;

import java.util.HashMap;
import java.util.Map;
import java.util.Objects;
import java.util.UUID;

/** Bounded state machine for the last recognized damage family. */
public final class LawOfRecurrenceTracker {
    public static final int ABSOLUTE_MAX_TRACKED_CASTERS = 4096;

    private final int maxTrackedCasters;
    private final Policy policy;
    private final Map<UUID, State> states = new HashMap<>();

    public LawOfRecurrenceTracker(int maxTrackedCasters, Policy policy) {
        if (maxTrackedCasters <= 0 || maxTrackedCasters > ABSOLUTE_MAX_TRACKED_CASTERS) {
            throw new IllegalArgumentException("maxTrackedCasters outside hard bounds");
        }
        this.maxTrackedCasters = maxTrackedCasters;
        this.policy = Objects.requireNonNull(policy, "policy");
    }

    public synchronized Outcome observe(UUID casterId, String damageFamily, long nowTick) {
        Objects.requireNonNull(casterId, "casterId");
        damageFamily = normalizeFamily(damageFamily);
        if (nowTick < 0L) throw new IllegalArgumentException("nowTick cannot be negative");

        State previous = states.get(casterId);
        boolean expired = previous == null || nowTick >= previous.expiresAtTick;
        boolean sameFamily = !expired && previous.damageFamily.equals(damageFamily);
        int stacks = sameFamily ? Math.min(policy.maxStacks(), previous.stacks + 1) : 1;
        int switches = sameFamily || expired ? 0 : Math.min(policy.maxSwitches(), previous.switches + 1);
        double resistance = Math.min(policy.maxResistance(), policy.resistancePerStack() * stacks);
        double vulnerability = Math.min(policy.maxVulnerability(), policy.vulnerabilityPerSwitch() * switches);
        long expiresAt = saturatingAdd(nowTick, policy.durationTicks());

        if (previous == null && states.size() >= maxTrackedCasters) {
            throw new IllegalStateException("Law of Recurrence state registry is full");
        }
        states.put(casterId, new State(damageFamily, stacks, switches, expiresAt));
        return new Outcome(damageFamily, resistance, vulnerability, stacks, switches, expiresAt);
    }

    public synchronized void clear(UUID casterId) {
        states.remove(Objects.requireNonNull(casterId, "casterId"));
    }

    private static String normalizeFamily(String family) {
        Objects.requireNonNull(family, "damageFamily");
        String normalized = family.trim().toLowerCase(java.util.Locale.ROOT);
        if (normalized.isEmpty() || normalized.length() > 64 || !normalized.matches("[a-z0-9_.:-]+")) {
            throw new IllegalArgumentException("damageFamily must be a bounded stable identifier");
        }
        return normalized;
    }

    private static long saturatingAdd(long value, long delta) {
        if (delta > Long.MAX_VALUE - value) return Long.MAX_VALUE;
        return value + delta;
    }

    public record Policy(
        double resistancePerStack,
        double maxResistance,
        double vulnerabilityPerSwitch,
        double maxVulnerability,
        int maxStacks,
        int maxSwitches,
        long durationTicks
    ) {
        public Policy {
            if (!Double.isFinite(resistancePerStack) || resistancePerStack < 0.0D) throw new IllegalArgumentException("resistancePerStack invalid");
            if (!Double.isFinite(maxResistance) || maxResistance < 0.0D || maxResistance >= 1.0D) throw new IllegalArgumentException("maxResistance must stay below immunity");
            if (!Double.isFinite(vulnerabilityPerSwitch) || vulnerabilityPerSwitch < 0.0D) throw new IllegalArgumentException("vulnerabilityPerSwitch invalid");
            if (!Double.isFinite(maxVulnerability) || maxVulnerability < 0.0D || maxVulnerability > 4.0D) throw new IllegalArgumentException("maxVulnerability invalid");
            if (maxStacks <= 0 || maxStacks > 64 || maxSwitches < 0 || maxSwitches > 64) throw new IllegalArgumentException("stack/switch bounds invalid");
            if (durationTicks <= 0L || durationTicks > 20L * 60L * 10L) throw new IllegalArgumentException("durationTicks outside technical bounds");
        }
    }

    public record Outcome(String damageFamily, double resistance, double vulnerability, int stacks, int switches, long expiresAtTick) { }

    private record State(String damageFamily, int stacks, int switches, long expiresAtTick) { }
}
