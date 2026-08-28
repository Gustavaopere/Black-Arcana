package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.damagesource.DamageType;

public final class ArcaneBacklashDamageTypes {
    public static final ResourceKey<DamageType> ARCANE_BACKLASH = ResourceKey.create(
        Registries.DAMAGE_TYPE,
        ResourceLocation.fromNamespaceAndPath(BlackArcanaMod.MOD_ID, "arcane_backlash"));

    private ArcaneBacklashDamageTypes() { }
}
