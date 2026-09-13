package dev.gustavopere.blackarcana.client;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.EnumSet;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;

/**
 * Pure, session-local discoverability state for Stage 05.16.
 *
 * This model owns presentation state only. It has no network, progression,
 * casting, loadout mutation, cooldown, hazard, provider, or persistence authority.
 */
final class DiscoverabilityModel {
    enum Topic {
        CORE_CASTING,
        UNBOUND_EDITOR
    }

    enum Priority {
        OPTIONAL(0),
        REQUIRED(1);

        private final int rank;

        Priority(int rank) {
            this.rank = rank;
        }

        int rank() {
            return rank;
        }
    }

    record BindingPresentation(
            String actionTranslationKey,
            Optional<String> currentLabel,
            boolean unbound
    ) {
        BindingPresentation {
            Objects.requireNonNull(actionTranslationKey, "actionTranslationKey");
            Objects.requireNonNull(currentLabel, "currentLabel");
            if (actionTranslationKey.isBlank()) {
                throw new IllegalArgumentException("actionTranslationKey cannot be blank");
            }
            if (unbound && currentLabel.isPresent()) {
                throw new IllegalArgumentException("unbound mapping cannot carry a current label");
            }
            if (!unbound && (currentLabel.isEmpty() || currentLabel.orElseThrow().isBlank())) {
                throw new IllegalArgumentException("bound mapping requires a current label");
            }
        }

        static BindingPresentation bound(String actionTranslationKey, String currentLabel) {
            Objects.requireNonNull(currentLabel, "currentLabel");
            return new BindingPresentation(actionTranslationKey, Optional.of(currentLabel), false);
        }

        static BindingPresentation unbound(String actionTranslationKey) {
            return new BindingPresentation(actionTranslationKey, Optional.empty(), true);
        }
    }

    record BindingSnapshot(
            BindingPresentation radial,
            BindingPresentation castSelected,
            BindingPresentation editLoadout,
            List<BindingPresentation> quickCasts
    ) {
        BindingSnapshot {
            Objects.requireNonNull(radial, "radial");
            Objects.requireNonNull(castSelected, "castSelected");
            Objects.requireNonNull(editLoadout, "editLoadout");
            quickCasts = List.copyOf(Objects.requireNonNull(quickCasts, "quickCasts"));
            if (quickCasts.size() != 8) {
                throw new IllegalArgumentException("exactly eight quick-cast mappings are required");
            }
            if (quickCasts.stream().anyMatch(Objects::isNull)) {
                throw new IllegalArgumentException("quick-cast mappings cannot contain null");
            }
        }
    }

    record Hint(
            Topic topic,
            Priority priority,
            long startedTick,
            long expiresAtTick,
            BindingSnapshot bindings
    ) {
        Hint {
            Objects.requireNonNull(topic, "topic");
            Objects.requireNonNull(priority, "priority");
            Objects.requireNonNull(bindings, "bindings");
            if (expiresAtTick <= startedTick) {
                throw new IllegalArgumentException("hint expiry must be after its start tick");
            }
        }
    }

    private static final Comparator<Hint> DISPLAY_ORDER = Comparator
            .comparingInt((Hint hint) -> hint.priority().rank())
            .thenComparingLong(Hint::startedTick)
            .thenComparing(hint -> hint.topic().ordinal());

    private final int maxActiveHints;
    private final long hintLifetimeTicks;
    private final Map<Topic, Hint> active = new LinkedHashMap<>();
    private final EnumSet<Topic> seen = EnumSet.noneOf(Topic.class);
    private final EnumSet<Topic> dismissed = EnumSet.noneOf(Topic.class);

    DiscoverabilityModel(int maxActiveHints, long hintLifetimeTicks) {
        if (maxActiveHints <= 0) {
            throw new IllegalArgumentException("maxActiveHints must be positive");
        }
        if (hintLifetimeTicks <= 0) {
            throw new IllegalArgumentException("hintLifetimeTicks must be positive");
        }
        this.maxActiveHints = maxActiveHints;
        this.hintLifetimeTicks = hintLifetimeTicks;
    }

    Optional<Hint> offer(
            Topic topic,
            Priority priority,
            long nowTick,
            boolean hintsEnabled,
            BindingSnapshot bindings
    ) {
        Objects.requireNonNull(topic, "topic");
        Objects.requireNonNull(priority, "priority");
        Objects.requireNonNull(bindings, "bindings");
        expire(nowTick);

        if (!hintsEnabled && priority == Priority.OPTIONAL) return Optional.empty();
        if (seen.contains(topic) || dismissed.contains(topic)) return Optional.empty();

        Hint candidate = new Hint(topic, priority, nowTick, expiry(nowTick), bindings);
        if (!makeRoom(candidate, false)) return Optional.empty();

        active.put(topic, candidate);
        seen.add(topic);
        return Optional.of(candidate);
    }

    Optional<Hint> reopen(
            Topic topic,
            Priority priority,
            long nowTick,
            BindingSnapshot bindings
    ) {
        Objects.requireNonNull(topic, "topic");
        Objects.requireNonNull(priority, "priority");
        Objects.requireNonNull(bindings, "bindings");
        expire(nowTick);

        active.remove(topic);
        dismissed.remove(topic);
        Hint candidate = new Hint(topic, priority, nowTick, expiry(nowTick), bindings);
        makeRoom(candidate, true);
        active.put(topic, candidate);
        seen.add(topic);
        return Optional.of(candidate);
    }

    void dismiss(Topic topic) {
        Objects.requireNonNull(topic, "topic");
        active.remove(topic);
        seen.add(topic);
        dismissed.add(topic);
    }

    Optional<Hint> active(long nowTick) {
        expire(nowTick);
        return active.values().stream().max(DISPLAY_ORDER);
    }

    int activeCount(long nowTick) {
        expire(nowTick);
        return active.size();
    }

    boolean hasSeen(Topic topic) {
        return seen.contains(Objects.requireNonNull(topic, "topic"));
    }

    boolean isDismissed(Topic topic) {
        return dismissed.contains(Objects.requireNonNull(topic, "topic"));
    }

    void resetSession() {
        active.clear();
        seen.clear();
        dismissed.clear();
    }

    private boolean makeRoom(Hint candidate, boolean explicitReentry) {
        if (active.size() < maxActiveHints) return true;

        List<Hint> evictionOrder = new ArrayList<>(active.values());
        evictionOrder.sort(DISPLAY_ORDER);
        Hint weakest = evictionOrder.getFirst();
        if (!explicitReentry && candidate.priority().rank() <= weakest.priority().rank()) {
            return false;
        }
        active.remove(weakest.topic());
        return true;
    }

    private void expire(long nowTick) {
        active.values().removeIf(hint -> nowTick >= hint.expiresAtTick());
    }

    private long expiry(long nowTick) {
        try {
            return Math.addExact(nowTick, hintLifetimeTicks);
        } catch (ArithmeticException overflow) {
            return Long.MAX_VALUE;
        }
    }
}
