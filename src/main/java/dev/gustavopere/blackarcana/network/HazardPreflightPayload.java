package dev.gustavopere.blackarcana.network;

import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDangerTier;

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
            double minimumArcaneResistance,
            double recommendedArcaneResistance
    ) {
        public Entry {
            Objects.requireNonNull(spellId, "spellId");
            Objects.requireNonNull(dangerTier, "dangerTier");
            if (spellId.length() > ArcanaProtocol.MAX_RESOURCE_ID_LENGTH) {
                throw new IllegalArgumentException("spellId exceeds protocol bound");
            }
            ArcanaSpellId.parse(spellId);
            if (dangerTier.isBlank() || dangerTier.length() > ArcanaProtocol.MAX_DANGER_TIER_LENGTH) {
                throw new IllegalArgumentException("dangerTier outside protocol bound");
            }
            ArcaneDangerTier.valueOf(dangerTier);
            validateResistance("minimumArcaneResistance", minimumArcaneResistance);
            validateResistance("recommendedArcaneResistance", recommendedArcaneResistance);
            if (minimumArcaneResistance > recommendedArcaneResistance) {
                throw new IllegalArgumentException("minimumArcaneResistance cannot exceed recommendedArcaneResistance");
            }
        }

        public ArcaneDangerTier parsedTier() {
            return ArcaneDangerTier.valueOf(dangerTier);
        }

        private static void validateResistance(String name, double value) {
            if (!Double.isFinite(value) || value < 0.0D || value > ArcanaProtocol.MAX_HAZARD_RESISTANCE_HINT) {
                throw new IllegalArgumentException(name + " outside protocol bound");
            }
        }
    }
}
