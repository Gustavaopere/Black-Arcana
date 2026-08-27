package dev.gustavopere.blackarcana.core.cooldown;

import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaChargeSpec;
import dev.gustavopere.blackarcana.api.ArcanaCooldownSpec;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;

import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;

/** Server-owned cooldown/charge policy table, atomically replaceable on data reload. */
public final class ArcanaCooldownPolicyRegistry {
    private volatile Map<ArcanaSpellId, ArcanaCooldownSpec> cooldowns = Map.of();
    private volatile Map<ArcanaSpellId, ArcanaChargeSpec> charges = Map.of();

    public synchronized void replaceAll(
            Map<ArcanaSpellId, ArcanaCooldownSpec> newCooldowns,
            Map<ArcanaSpellId, ArcanaChargeSpec> newCharges
    ) {
        Objects.requireNonNull(newCooldowns, "newCooldowns");
        Objects.requireNonNull(newCharges, "newCharges");

        Map<ArcanaSpellId, ArcanaCooldownSpec> validatedCooldowns = new LinkedHashMap<>();
        newCooldowns.forEach((id, spec) -> validatedCooldowns.put(
                Objects.requireNonNull(id, "cooldown spell id"),
                Objects.requireNonNull(spec, "cooldown spec")));

        Map<ArcanaSpellId, ArcanaChargeSpec> validatedCharges = new LinkedHashMap<>();
        newCharges.forEach((id, spec) -> validatedCharges.put(
                Objects.requireNonNull(id, "charge spell id"),
                Objects.requireNonNull(spec, "charge spec")));

        cooldowns = Map.copyOf(validatedCooldowns);
        charges = Map.copyOf(validatedCharges);
    }

    public ArcanaCooldownSpec cooldownFor(ArcanaCastRequest request) {
        Objects.requireNonNull(request, "request");
        return cooldowns.getOrDefault(
                request.spell().id(),
                ArcanaCooldownSpec.none(request.spell().id().canonical()));
    }

    public Optional<ArcanaChargeSpec> chargeFor(ArcanaCastRequest request) {
        Objects.requireNonNull(request, "request");
        return Optional.ofNullable(charges.get(request.spell().id()));
    }

    public ArcanaChargeSpec requireCharge(ArcanaCastRequest request) {
        return chargeFor(request).orElseThrow(() ->
                new IllegalStateException("no charge policy for spell: " + request.spell().id().canonical()));
    }

    public Map<ArcanaSpellId, ArcanaCooldownSpec> cooldownSnapshot() {
        return cooldowns;
    }

    public Map<ArcanaSpellId, ArcanaChargeSpec> chargeSnapshot() {
        return charges;
    }
}
