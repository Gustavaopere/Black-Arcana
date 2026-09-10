package dev.gustavopere.blackarcana.client;

import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

/** Unsaved client draft. It has no gameplay authority until the server accepts an update packet. */
public final class LoadoutDraft {
    private final List<ArcanaSpellId> baseline;
    private final List<ArcanaSpellId> spells = new ArrayList<>();

    public LoadoutDraft(List<ArcanaSpellId> initial) {
        Objects.requireNonNull(initial, "initial");
        if (initial.size() > ArcanaCastRequest.MAX_LOADOUT_SLOTS) {
            throw new IllegalArgumentException("initial loadout exceeds slot bound");
        }
        if (initial.stream().distinct().count() != initial.size()) {
            throw new IllegalArgumentException("initial loadout contains duplicate spells");
        }
        baseline = List.copyOf(initial);
        spells.addAll(baseline);
    }

    public boolean toggle(ArcanaSpellId spell) {
        Objects.requireNonNull(spell, "spell");
        if (spells.remove(spell)) return true;
        if (spells.size() >= ArcanaCastRequest.MAX_LOADOUT_SLOTS) return false;
        spells.add(spell);
        return true;
    }

    public boolean move(int fromIndex, int toIndex) {
        if (fromIndex < 0 || toIndex < 0 || fromIndex >= spells.size() || toIndex >= spells.size()) {
            return false;
        }
        if (fromIndex == toIndex) return true;
        ArcanaSpellId spell = spells.remove(fromIndex);
        spells.add(toIndex, spell);
        return true;
    }

    public boolean contains(ArcanaSpellId spell) {
        return spells.contains(Objects.requireNonNull(spell, "spell"));
    }

    public boolean isDirty() {
        return !spells.equals(baseline);
    }

    public void reset() {
        spells.clear();
        spells.addAll(baseline);
    }

    public void clear() {
        spells.clear();
    }

    public List<ArcanaSpellId> snapshot() {
        return List.copyOf(spells);
    }
}
