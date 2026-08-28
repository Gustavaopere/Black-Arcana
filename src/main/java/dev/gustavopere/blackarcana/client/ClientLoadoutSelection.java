package dev.gustavopere.blackarcana.client;

import dev.gustavopere.blackarcana.api.ArcanaSpellId;

import java.util.List;
import java.util.Objects;
import java.util.Optional;

/** Presentation/input state only. The server-owned loadout remains authoritative. */
public final class ClientLoadoutSelection {
    private int selectedSlot;

    public synchronized int selectedSlot() {
        return selectedSlot;
    }

    public synchronized boolean select(int slot, List<ArcanaSpellId> loadout) {
        Objects.requireNonNull(loadout, "loadout");
        if (slot < 0 || slot >= loadout.size()) return false;
        selectedSlot = slot;
        return true;
    }

    public synchronized Optional<ArcanaSpellId> selected(List<ArcanaSpellId> loadout) {
        Objects.requireNonNull(loadout, "loadout");
        reconcile(loadout);
        if (loadout.isEmpty()) return Optional.empty();
        return Optional.of(loadout.get(selectedSlot));
    }

    public synchronized void reconcile(List<ArcanaSpellId> loadout) {
        Objects.requireNonNull(loadout, "loadout");
        if (loadout.isEmpty()) selectedSlot = 0;
        else if (selectedSlot >= loadout.size()) selectedSlot = loadout.size() - 1;
    }
}
