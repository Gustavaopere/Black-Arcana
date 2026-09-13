package dev.gustavopere.blackarcana.content.noetic;

import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.syncher.SynchedEntityData;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.level.Level;

/**
 * Ephemeral server-authored viewpoint entity for Astral Severance.
 *
 * <p>The entity is representation only: it has no gameplay inventory, combat ownership or interaction
 * authority. Lifecycle and movement authority remain in {@link AstralSeveranceRuntime}.</p>
 */
public final class AstralProjectionEntity extends Entity {
    public AstralProjectionEntity(EntityType<?> type, Level level) {
        super(type, level);
        this.noPhysics = true;
    }

    @Override
    protected void defineSynchedData(SynchedEntityData.Builder builder) {
    }

    @Override
    protected void readAdditionalSaveData(CompoundTag tag) {
    }

    @Override
    protected void addAdditionalSaveData(CompoundTag tag) {
    }

    @Override
    public boolean isPickable() {
        return false;
    }
}
