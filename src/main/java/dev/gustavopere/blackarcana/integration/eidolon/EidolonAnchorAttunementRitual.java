package dev.gustavopere.blackarcana.integration.eidolon;

import alexthw.eidolon_repraised.api.ritual.Ritual;
import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.core.ritual.ArcanaRitualId;
import dev.gustavopere.blackarcana.core.ritual.RitualAnchor;
import dev.gustavopere.blackarcana.core.ritual.RitualCompletionKey;
import dev.gustavopere.blackarcana.core.ritual.RitualCompletionLedger;
import dev.gustavopere.blackarcana.persistence.RitualCompletionSavedData;
import net.minecraft.core.BlockPos;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.level.Level;

/**
 * Production bridge ritual hosted by Eidolon.
 *
 * Eidolon's 1.21.1 public start hook does not carry a caster identity, so the
 * durable result is deliberately scoped to the ritual anchor rather than a
 * guessed nearby player.
 */
public final class EidolonAnchorAttunementRitual extends Ritual {
    public static final ArcanaRitualId ARCANA_ID = ArcanaRitualId.parse("black_arcana:eidolon_anchor_attunement");
    private static final ResourceLocation SYMBOL = ResourceLocation.fromNamespaceAndPath(
        EidolonIntegrationIds.MOD_ID,
        "particle/crystal_ritual");
    private static final int COLOR = 0xFF6A1538;

    public EidolonAnchorAttunementRitual() {
        super(SYMBOL, COLOR);
    }

    @Override
    public Ritual cloneRitual() {
        return new EidolonAnchorAttunementRitual();
    }

    @Override
    public RitualResult start(Level world, BlockPos pos) {
        if (!(world instanceof ServerLevel level)) return RitualResult.TERMINATE;

        RitualAnchor anchor = new RitualAnchor(level.dimension().location().toString(), pos.asLong());
        RitualCompletionKey key = RitualCompletionKey.forAnchor(ARCANA_ID, anchor);
        RitualCompletionLedger.CompletionResult result = RitualCompletionSavedData
            .get(level.getServer())
            .complete(key, level.getServer().overworld().getGameTime());

        if (result == RitualCompletionLedger.CompletionResult.CAPACITY_EXCEEDED) {
            BlackArcanaMod.LOGGER.error(
                "Eidolon anchor attunement completed at {} but the ritual completion ledger is full; no durable reward was recorded",
                anchor);
        } else {
            BlackArcanaMod.LOGGER.info("Eidolon anchor attunement {} at {}", result, anchor);
        }
        return RitualResult.TERMINATE;
    }
}
