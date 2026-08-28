package dev.gustavopere.blackarcana.core.progression;

import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaServices.ProgressionGate;

import java.util.Objects;

/** Fails closed for unknown spells. Disabling this gate must be an explicit server policy decision. */
public final class KnowledgeProgressionGate implements ProgressionGate {
    private final ArcanaKnowledgeLedger knowledge;

    public KnowledgeProgressionGate(ArcanaKnowledgeLedger knowledge) {
        this.knowledge = Objects.requireNonNull(knowledge, "knowledge");
    }

    @Override
    public ArcanaDecision check(ArcanaCastRequest request) {
        Objects.requireNonNull(request, "request");
        if (!knowledge.knows(request.context().casterId(), request.spell().id())) {
            return ArcanaDecision.deny("spell_unknown", "The caster has not learned this Black Arcana spell");
        }
        return ArcanaDecision.allow();
    }
}
