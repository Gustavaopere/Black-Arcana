package dev.gustavopere.blackarcana.core.cast;

import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaServices.CastRequestValidator;

import java.util.List;
import java.util.Objects;

public final class CompositeCastRequestValidator implements CastRequestValidator {
    private final List<CastRequestValidator> validators;

    public CompositeCastRequestValidator(List<? extends CastRequestValidator> validators) {
        Objects.requireNonNull(validators, "validators");
        this.validators = List.copyOf(validators);
    }

    @Override
    public ArcanaDecision check(ArcanaCastRequest request) {
        for (CastRequestValidator validator : validators) {
            ArcanaDecision decision = Objects.requireNonNull(validator.check(request), "request validation decision");
            if (!decision.allowed()) return decision;
        }
        return ArcanaDecision.allow();
    }
}
