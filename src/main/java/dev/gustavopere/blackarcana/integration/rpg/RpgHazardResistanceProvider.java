package dev.gustavopere.blackarcana.integration.rpg;

import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceContribution;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceProvider;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceQuery;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceSourceCategory;
import dev.gustavopere.blackarcana.api.hazard.CorruptionResistanceContribution;
import dev.gustavopere.blackarcana.api.hazard.CorruptionResistanceProvider;
import dev.gustavopere.blackarcana.api.hazard.CorruptionResistanceQuery;
import dev.gustavopere.blackarcana.api.hazard.CorruptionResistanceSourceCategory;

import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.UUID;

/** Read-only RPG adapter. It never awards mastery and therefore cannot create backlash feedback loops. */
public final class RpgHazardResistanceProvider implements ArcaneResistanceProvider, CorruptionResistanceProvider {
    public static final String PROVIDER_ID = "black_arcana:rpg_hazard";
    private final RpgSkillTreeBridge bridge;
    private final RpgHazardResistanceConfig config;

    public RpgHazardResistanceProvider(RpgSkillTreeBridge bridge, RpgHazardResistanceConfig config) {
        this.bridge = Objects.requireNonNull(bridge, "bridge");
        this.config = Objects.requireNonNull(config, "config");
    }

    @Override public String providerId() { return PROVIDER_ID; }

    @Override
    public List<ArcaneResistanceContribution> contributions(ArcaneResistanceQuery query) {
        double amount = mapped(query.casterId(), config.arcaneResistancePerRank(), config.maxArcaneContribution());
        if (amount <= 0.0D) return List.of();
        return List.of(new ArcaneResistanceContribution(
            "rpg:attributes", ArcaneResistanceSourceCategory.RPG, amount));
    }

    @Override
    public List<CorruptionResistanceContribution> contributions(CorruptionResistanceQuery query) {
        double amount = mapped(query.subjectId(), config.corruptionResistancePerRank(), config.maxCorruptionContribution());
        if (amount <= 0.0D) return List.of();
        return List.of(new CorruptionResistanceContribution(
            "rpg:attributes", CorruptionResistanceSourceCategory.RPG, amount));
    }

    private double mapped(UUID playerId, Map<String, Double> coefficients, double cap) {
        if (!bridge.available()) return 0.0D;
        RpgProgressionQuery query = bridge.query(playerId);
        if (!query.decision().allowed() || query.snapshot().isEmpty()) return 0.0D;
        double total = 0.0D;
        Map<String, Long> ranks = query.snapshot().orElseThrow().attributeRanks();
        for (Map.Entry<String, Double> mapping : coefficients.entrySet()) {
            long rank = Math.max(0L, ranks.getOrDefault(mapping.getKey(), 0L));
            double contribution = rank * mapping.getValue();
            if (!Double.isFinite(contribution)) return cap;
            total = Math.min(cap, total + contribution);
        }
        return total;
    }
}
