package dev.gustavopere.blackarcana.integration.irons;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import io.redspace.ironsspellbooks.api.registry.SpellRegistry;
import io.redspace.ironsspellbooks.api.spells.AbstractSpell;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.registries.DeferredRegister;

import java.util.function.Supplier;

/** Registers Black Arcana-hosted spells into Iron's supported spell registry. */
public final class IronsSpellRegistryBridge {
    private static final DeferredRegister<AbstractSpell> SPELLS =
        DeferredRegister.create(SpellRegistry.SPELL_REGISTRY_KEY, BlackArcanaMod.MOD_ID);

    public static final Supplier<AbstractSpell> INTEGRATION_PROBE =
        SPELLS.register("irons_integration_probe", IronsArcanaProbeSpell::new);

    private IronsSpellRegistryBridge() { }

    public static void register(IEventBus modEventBus) {
        SPELLS.register(modEventBus);
    }
}
