package dev.gustavopere.blackarcana.client;

import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;

import java.util.List;
import java.util.Objects;
import java.util.Optional;

/** Pure client-local semantics for Stage 05.10 loadout-editor presentation. */
public final class LoadoutEditorSemantics {
    private LoadoutEditorSemantics() { }

    public static Optional<SlotPosition> slotPosition(List<ArcanaSpellId> draft, ArcanaSpellId spell) {
        Objects.requireNonNull(draft, "draft");
        Objects.requireNonNull(spell, "spell");
        int index = draft.indexOf(spell);
        if (index < 0 || index >= ArcanaCastRequest.MAX_LOADOUT_SLOTS) return Optional.empty();
        int slotNumber = index + 1;
        boolean quickCastEligible = slotNumber <= 8;
        return Optional.of(new SlotPosition(
                slotNumber,
                quickCastEligible,
                quickCastEligible ? slotNumber : -1));
    }

    public record SlotPosition(int slotNumber, boolean quickCastEligible, int quickCastSlot) {
        public SlotPosition {
            if (slotNumber < 1 || slotNumber > ArcanaCastRequest.MAX_LOADOUT_SLOTS) {
                throw new IllegalArgumentException("slotNumber outside loadout bound");
            }
            int expectedQuickCastSlot = slotNumber <= 8 ? slotNumber : -1;
            if (quickCastEligible != (slotNumber <= 8) || quickCastSlot != expectedQuickCastSlot) {
                throw new IllegalArgumentException("quick-cast eligibility must follow slots 1-8");
            }
        }
    }
}
