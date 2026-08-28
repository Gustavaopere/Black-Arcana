package dev.gustavopere.blackarcana.integration.rpg;

import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaServices.ProgressionGate;
import java.util.Objects;

/** Uses the canonical RPG snapshot to gate one Black Arcana spell. */
public final class RpgSkillTreeProgressionGate implements ProgressionGate {
    private final RpgSkillTreeBridge bridge;
    private final RpgProgressionRequirement requirement;

    public RpgSkillTreeProgressionGate(RpgSkillTreeBridge bridge, RpgProgressionRequirement requirement) {
        this.bridge = Objects.requireNonNull(bridge, "bridge");
        this.requirement = Objects.requireNonNull(requirement, "requirement");
    }

    @Override
    public ArcanaDecision check(ArcanaCastRequest request) {
        Objects.requireNonNull(request, "request");
        if (!bridge.available()) {
            String detail = bridge.diagnostic().isBlank()
                ? "RPG Skill Tree integration is unavailable"
                : bridge.diagnostic();
            return ArcanaDecision.deny("rpg_integration_unavailable", detail);
        }

        RpgProgressionQuery query = bridge.query(request.context().casterId());
        if (!query.decision().allowed()) return query.decision();
        return requirement.evaluate(query.snapshot().orElseThrow());
    }
}
