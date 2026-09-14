package dev.gustavopere.blackarcana.client;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;

import java.util.Objects;
import java.util.Optional;

/**
 * Minimal physical-client bookkeeping for one held channel input.
 * Gameplay authority remains entirely server-side; this state exists only to
 * pair one physical key-down edge with its exact release/cancel cast id.
 */
public final class ClientChannelInvocationState {
    private Active active;

    public synchronized boolean begin(int inputKey, int loadoutSlot, ArcanaSpellId spellId, ArcanaCastId castId) {
        if (inputKey < 0) throw new IllegalArgumentException("inputKey cannot be negative");
        if (loadoutSlot < 0 || loadoutSlot >= ArcanaCastRequest.MAX_LOADOUT_SLOTS) {
            throw new IllegalArgumentException("loadoutSlot outside cast request bounds");
        }
        ArcanaSpellId checkedSpell = Objects.requireNonNull(spellId, "spellId");
        ArcanaCastId checkedCast = Objects.requireNonNull(castId, "castId");
        if (active != null) return false;
        active = new Active(inputKey, loadoutSlot, checkedSpell, checkedCast);
        return true;
    }

    public synchronized Optional<ArcanaCastId> releaseWhenUp(int inputKey, boolean stillDown) {
        if (active == null || active.inputKey() != inputKey || stillDown) return Optional.empty();
        ArcanaCastId castId = active.castId();
        active = null;
        return Optional.of(castId);
    }

    public synchronized Optional<ArcanaCastId> cancel() {
        if (active == null) return Optional.empty();
        ArcanaCastId castId = active.castId();
        active = null;
        return Optional.of(castId);
    }

    public synchronized void rejectBegin(ArcanaCastId castId) {
        ArcanaCastId checked = Objects.requireNonNull(castId, "castId");
        if (active != null && active.castId().equals(checked)) active = null;
    }

    public synchronized Optional<Active> active() {
        return Optional.ofNullable(active);
    }

    public record Active(int inputKey, int loadoutSlot, ArcanaSpellId spellId, ArcanaCastId castId) {
        public Active {
            Objects.requireNonNull(spellId, "spellId");
            Objects.requireNonNull(castId, "castId");
        }
    }
}
