package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.damagesource.DamageType;

/** Dedicated recursion marker and attribution type for Sympathetic Wound damage. */
public final class SympatheticWoundDamageTypes {
    public static final ResourceKey<DamageType> SYMPATHETIC_WOUND = ResourceKey.create(
        Registries.DAMAGE_TYPE,
        ResourceLocation.fromNamespaceAndPath(BlackArcanaMod.MOD_ID, "sympathetic_wound"));

    private SympatheticWoundDamageTypes() { }
}
