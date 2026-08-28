package dev.gustavopere.blackarcana.integration.irons;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.api.ArcanaCastResult;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import io.redspace.ironsspellbooks.api.config.DefaultConfig;
import io.redspace.ironsspellbooks.api.magic.MagicData;
import io.redspace.ironsspellbooks.api.registry.SchoolRegistry;
import io.redspace.ironsspellbooks.api.spells.AbstractSpell;
import io.redspace.ironsspellbooks.api.spells.CastSource;
import io.redspace.ironsspellbooks.api.spells.CastType;
import io.redspace.ironsspellbooks.api.spells.SpellRarity;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.level.Level;

/**
 * Non-destructive Stage 03 integration probe. Iron's owns presentation and
 * invocation; Black Arcana owns validation, cost transaction and cooldown.
 */
public final class IronsArcanaProbeSpell extends AbstractSpell {
    public static final ArcanaSpellId ARCANA_ID = ArcanaSpellId.parse("black_arcana:irons_integration_probe");
    public static final ResourceLocation IRONS_ID = ResourceLocation.fromNamespaceAndPath(
        BlackArcanaMod.MOD_ID,
        "irons_integration_probe");
    public static final int MANA_COST = 20;

    private static final DefaultConfig CONFIG = new DefaultConfig()
        .setMinRarity(SpellRarity.COMMON)
        .setSchoolResource(SchoolRegistry.BLOOD_RESOURCE)
        .setMaxLevel(1)
        .setCooldownSeconds(0.0D)
        .setAllowCrafting(false)
        .build();

    public IronsArcanaProbeSpell() {
        this.baseManaCost = MANA_COST;
        this.manaCostPerLevel = 0;
        this.baseSpellPower = 0;
        this.spellPowerPerLevel = 0;
        this.castTime = 0;
    }

    @Override
    public ResourceLocation getSpellResource() {
        return IRONS_ID;
    }

    @Override
    public DefaultConfig getDefaultConfig() {
        return CONFIG;
    }

    @Override
    public CastType getCastType() {
        return CastType.INSTANT;
    }

    @Override
    public boolean requiresLearning() {
        return false;
    }

    @Override
    public boolean allowLooting() {
        return false;
    }

    @Override
    public void onCast(Level level, int spellLevel, LivingEntity entity, CastSource castSource, MagicData playerMagicData) {
        if (!(entity instanceof ServerPlayer player)) return;
        var result = IronsHostedCastDispatcher.cast(player, ARCANA_ID);
        if (ArcanaCastResult.Status.SUCCESS.name().equals(result.status())) {
            super.onCast(level, spellLevel, entity, castSource, playerMagicData);
        }
    }
}
