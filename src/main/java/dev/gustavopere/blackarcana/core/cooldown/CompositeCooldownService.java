package dev.gustavopere.blackarcana.core.cooldown;

import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaServices.CooldownService;

import java.util.List;
import java.util.Objects;

public final class CompositeCooldownService implements CooldownService {
    private final List<CooldownService> services;

    public CompositeCooldownService(List<? extends CooldownService> services) {
        Objects.requireNonNull(services, "services");
        this.services = List.copyOf(services);
    }

    @Override
    public ArcanaDecision check(ArcanaCastRequest request) {
        for (CooldownService service : services) {
            ArcanaDecision decision = Objects.requireNonNull(service.check(request), "cooldown decision");
            if (!decision.allowed()) return decision;
        }
        return ArcanaDecision.allow();
    }

    @Override
    public void start(ArcanaCastRequest request) {
        for (CooldownService service : services) service.start(request);
    }
}
