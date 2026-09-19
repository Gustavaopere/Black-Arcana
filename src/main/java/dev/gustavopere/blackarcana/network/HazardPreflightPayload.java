package dev.gustavopere.blackarcana.network;

import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDangerTier;
import dev.gustavopere.blackarcana.api.hazard.ArcaneInsufficientResistancePolicy;

import java.util.HashSet;
import java.util.List;
import java.util.Objects;
import java.util.Set;

/** Bounded, server-authored advisory data used only for client preflight presentation. */
public record HazardPreflightPayload(int protocolVersion, List<Entry> entries) {
    public HazardPreflightPayload {
        ArcanaProtocol.requireCompatible(protocolVersion);
        Objects.requireNonNull(entries, "entries");
        entries = List.copyOf(entries);
        if (entries.size() > ArcanaProtocol.MAX_HAZARD_PREFLIGHT_ENTRIES) {
            throw new IllegalArgumentException("too many hazard preflight entries");
        }

        Set<String> spellIds = new HashSet<>(entries.size());
        for (Entry entry : entries) {
            Objects.requireNonNull(entry, "hazard preflight entry");
            if (!spellIds.add(entry.spellId())) {
                throw new IllegalArgumentException("duplicate hazard preflight spell id: " + entry.spellId());
            }
        }
    }

    public record Entry(
            String spellId,
            String dangerTier,
            String belowMinimumPolicy,
            double minimumArcaneResistance,
            double recommendedArcaneResistance
    ) {
        /** Compatibility constructor for payload callers from before the policy became presentational metadata. */
        public Entry(
            String spellId,
            String dangerTier,
            double minimumArcaneResistance,
            double recommendedArcaneResistance
        ) {
            this(
                spellId,
                dangerTier,
                ArcaneInsufficientResistancePolicy.DENY_CAST.name(),
                minimumArcaneResistance,
                recommendedArcaneResistance);
        }

        public Entry {
            Objects.requireNonNull(spellId, "spellId");
            Objects.requireNonNull(dangerTier, "dangerTier");
            Objects.requireNonNull(belowMinimumPolicy, "belowMinimumPolicy");
            if (spellId.length() > ArcanaProtocol.MAX_RESOURCE_ID_LENGTH) {
                throw new IllegalArgumentException("spellId exceeds protocol bound");
            }
            ArcanaSpellId.parse(spellId);
            if (dangerTier.isBlank() || dangerTier.length() > ArcanaProtocol.MAX_DANGER_TIER_LENGTH) {
                throw new IllegalArgumentException("dangerTier outside protocol bound");
            }
            if (belowMinimumPolicy.isBlank()
                || belowMinimumPolicy.length() > ArcanaProtocol.MAX_HAZARD_POLICY_LENGTH) {
                throw new IllegalArgumentException("belowMinimumPolicy outside protocol bound");
            }
            ArcaneDangerTier parsedTier = ArcaneDangerTier.valueOf(dangerTier);
            ArcaneInsufficientResistancePolicy parsedPolicy =
                ArcaneInsufficientResistancePolicy.valueOf(belowMinimumPolicy);
            if (parsedTier == ArcaneDangerTier.NORMAL
                && parsedPolicy != ArcaneInsufficientResistancePolicy.DENY_CAST) {
                throw new IllegalArgumentException("NORMAL hazard metadata cannot carry allow-with-risk policy");
            }
            validateResistance("minimumArcaneResistance", minimumArcaneResistance);
            validateResistance("recommendedArcaneResistance", recommendedArcaneResistance);
            if (minimumArcaneResistance > recommendedArcaneResistance) {
                throw new IllegalArgumentException("minimumArcaneResistance cannot exceed recommendedArcaneResistance");
            }
        }

        public ArcaneDangerTier parsedTier() {
            return ArcaneDangerTier.valueOf(dangerTier);
        }

        public ArcaneInsufficientResistancePolicy parsedBelowMinimumPolicy() {
            return ArcaneInsufficientResistancePolicy.valueOf(belowMinimumPolicy);
        }

        private static void validateResistance(String name, double value) {
            if (!Double.isFinite(value) || value < 0.0D || value > ArcanaProtocol.MAX_HAZARD_RESISTANCE_HINT) {
                throw new IllegalArgumentException(name + " outside protocol bound");
            }
        }
    }
}
