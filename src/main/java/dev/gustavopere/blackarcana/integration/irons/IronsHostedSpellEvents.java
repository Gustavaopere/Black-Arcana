package dev.gustavopere.blackarcana.integration.irons;

import io.redspace.ironsspellbooks.api.events.SpellOnCastEvent;
import net.neoforged.bus.api.EventPriority;
import net.neoforged.bus.api.SubscribeEvent;

/**
 * Prevents Iron's from charging hosted Black Arcana spells a second time.
 * Black Arcana's transactional CostProvider is the sole resource authority.
 */
public final class IronsHostedSpellEvents {
    private static final String OWNED_PREFIX = "black_arcana:";

    private IronsHostedSpellEvents() { }

    @SubscribeEvent(priority = EventPriority.HIGHEST)
    public static void neutralizeNativeManaEarly(SpellOnCastEvent event) {
        if (isBlackArcanaHosted(event)) event.setManaCost(0);
    }

    /** Reassert zero after intermediate provider modifiers so native deduction remains disabled. */
    @SubscribeEvent(priority = EventPriority.LOWEST)
    public static void neutralizeNativeManaLate(SpellOnCastEvent event) {
        if (isBlackArcanaHosted(event)) event.setManaCost(0);
    }

    static boolean isBlackArcanaHosted(SpellOnCastEvent event) {
        return event.getSpellId() != null && event.getSpellId().startsWith(OWNED_PREFIX);
    }
}
