package dev.gustavopere.blackarcana.integration.eidolon;

import alexthw.eidolon_repraised.api.ritual.Ritual;
import dev.gustavopere.blackarcana.BlackArcanaMod;
import net.minecraft.core.BlockPos;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.level.Level;

/**
 * Non-destructive Stage 03 ritual-host probe. It proves Eidolon's public ritual
 * lifecycle without adding provisional gameplay effects before Stage 06.
 */
public final class EidolonArcanaProbeRitual extends Ritual {
    private static final ResourceLocation SYMBOL = ResourceLocation.fromNamespaceAndPath(
        EidolonIntegrationIds.MOD_ID,
        "particle/crystal_ritual");
    private static final int COLOR = 0xFF6A1538;

    public EidolonArcanaProbeRitual() {
        super(SYMBOL, COLOR);
    }

    @Override
    public Ritual cloneRitual() {
        return new EidolonArcanaProbeRitual();
    }

    @Override
    public RitualResult start(Level world, BlockPos pos) {
        if (!world.isClientSide) {
            BlackArcanaMod.LOGGER.info(
                "Black Arcana Eidolon ritual bridge activated at {} in {}",
                pos,
                world.dimension().location());
        }
        return RitualResult.TERMINATE;
    }
}
