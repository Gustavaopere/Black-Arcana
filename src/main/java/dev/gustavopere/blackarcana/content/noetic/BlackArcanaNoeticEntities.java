package dev.gustavopere.blackarcana.content.noetic;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.MobCategory;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredRegister;

import java.util.Objects;

/** Common-side registration for bounded Noetic representation entities. */
public final class BlackArcanaNoeticEntities {
    private static final DeferredRegister<EntityType<?>> ENTITY_TYPES =
            DeferredRegister.create(BuiltInRegistries.ENTITY_TYPE, BlackArcanaMod.MOD_ID);

    public static final DeferredHolder<EntityType<?>, EntityType<AstralProjectionEntity>> ASTRAL_PROJECTION =
            ENTITY_TYPES.register("astral_projection", () ->
                    EntityType.Builder.of(AstralProjectionEntity::new, MobCategory.MISC)
                            .sized(0.25F, 0.25F)
                            .noSave()
                            .noSummon()
                            .clientTrackingRange(8)
                            .updateInterval(1)
                            .build(BlackArcanaMod.MOD_ID + ":astral_projection"));

    private BlackArcanaNoeticEntities() {
    }

    public static void register(IEventBus modEventBus) {
        ENTITY_TYPES.register(Objects.requireNonNull(modEventBus, "modEventBus"));
    }
}
