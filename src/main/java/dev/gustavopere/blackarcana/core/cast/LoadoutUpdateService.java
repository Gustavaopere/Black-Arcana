package dev.gustavopere.blackarcana.core.cast;

import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.core.registry.ArcanaSpellRegistry;

import java.util.List;
import java.util.Objects;
import java.util.UUID;
import java.util.function.Predicate;

/** Validates a complete client-proposed loadout before mutating server-owned state. */
public final class LoadoutUpdateService {
    private final ArcanaSpellRegistry spells;
    private final LoadoutRegistry loadouts;
    private final Predicate<ArcanaSpellId> executable;

    public LoadoutUpdateService(
            ArcanaSpellRegistry spells,
            LoadoutRegistry loadouts,
            Predicate<ArcanaSpellId> executable
    ) {
        this.spells = Objects.requireNonNull(spells, "spells");
        this.loadouts = Objects.requireNonNull(loadouts, "loadouts");
        this.executable = Objects.requireNonNull(executable, "executable");
    }

    public Result apply(UUID casterId, List<ArcanaSpellId> requested) {
        Objects.requireNonNull(casterId, "casterId");
        Objects.requireNonNull(requested, "requested");
        List<ArcanaSpellId> candidate = List.copyOf(requested);
        if (candidate.size() > dev.gustavopere.blackarcana.api.ArcanaCastRequest.MAX_LOADOUT_SLOTS) {
            return new Result(
                    ArcanaDecision.deny("loadout_too_large", "requested loadout exceeds server slot bound"),
                    loadouts.getLoadout(casterId));
        }
        if (candidate.stream().distinct().count() != candidate.size()) {
            return new Result(
                    ArcanaDecision.deny("loadout_duplicate_spell", "a spell may appear only once in a loadout"),
                    loadouts.getLoadout(casterId));
        }
        for (ArcanaSpellId spellId : candidate) {
            if (spells.resolve(spellId).isEmpty()) {
                return new Result(
                        ArcanaDecision.deny("loadout_unknown_spell", "spell is not registered on the server: " + spellId.canonical()),
                        loadouts.getLoadout(casterId));
            }
            if (!executable.test(spellId)) {
                return new Result(
                        ArcanaDecision.deny("loadout_spell_unavailable", "spell has no installed execution runtime: " + spellId.canonical()),
                        loadouts.getLoadout(casterId));
            }
        }
        loadouts.setLoadout(casterId, candidate);
        return new Result(ArcanaDecision.allow(), candidate);
    }

    public record Result(ArcanaDecision decision, List<ArcanaSpellId> loadout) {
        public Result {
            Objects.requireNonNull(decision, "decision");
            Objects.requireNonNull(loadout, "loadout");
            loadout = List.copyOf(loadout);
        }
    }
}
