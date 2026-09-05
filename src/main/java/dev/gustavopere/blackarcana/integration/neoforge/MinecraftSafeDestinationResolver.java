package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.content.space.SafeDestinationPolicy;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntimeManager;
import dev.gustavopere.blackarcana.core.world.ChunkRef;
import dev.gustavopere.blackarcana.core.world.EntityInteractionType;
import dev.gustavopere.blackarcana.core.world.ProtectionQuery;
import net.minecraft.core.BlockPos;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.phys.AABB;
import net.neoforged.neoforge.common.Tags;

import java.util.Objects;

public final class MinecraftSafeDestinationResolver {
    private static final SafeDestinationPolicy POLICY = new SafeDestinationPolicy();

    private MinecraftSafeDestinationResolver() { }

    public static Result evaluate(
            MinecraftServer server,
            LivingEntity entity,
            ServerLevel destinationLevel,
            double x,
            double y,
            double z
    ) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(entity, "entity");
        Objects.requireNonNull(destinationLevel, "destinationLevel");
        if (!Double.isFinite(x) || !Double.isFinite(y) || !Double.isFinite(z)) {
            return denied("invalid_position");
        }
        if (entity.getType().is(Tags.EntityTypes.TELEPORTING_NOT_SUPPORTED)) {
            return denied("teleport_unsupported");
        }

        ArcanaServerRuntime runtime = ArcanaServerRuntimeManager.get(server).orElse(null);
        if (runtime == null) return denied("runtime_unavailable");

        boolean sameDimension = entity.level() == destinationLevel;
        BlockPos landing = BlockPos.containing(x, y, z);
        boolean loaded = destinationLevel.getChunkSource().getChunkNow(
            landing.getX() >> 4,
            landing.getZ() >> 4) != null;
        AABB landingBox = entity.getBoundingBox().move(
            x - entity.getX(),
            y - entity.getY(),
            z - entity.getZ());
        boolean border = destinationLevel.getWorldBorder().isWithinBounds(landingBox);
        boolean collisionFree = sameDimension && loaded && destinationLevel.noCollision(entity, landingBox);
        boolean fluidAllowed = sameDimension
            && loaded
            && destinationLevel.getFluidState(landing).isEmpty()
            && destinationLevel.getFluidState(landing.above()).isEmpty();
        boolean vehicleUnsafe = entity.isPassenger() || entity.isVehicle();

        boolean protectionAllowed = false;
        if (sameDimension && loaded) {
            var guard = runtime.protectedDestinationGuard().orElse(null);
            if (guard != null) {
                String dimensionId = destinationLevel.dimension().location().toString();
                ArcanaDecision decision = guard.authorize(
                    new ChunkRef(dimensionId, landing.getX() >> 4, landing.getZ() >> 4),
                    new ProtectionQuery(
                        entity.getUUID(),
                        dimensionId,
                        entity.getUUID().toString(),
                        EntityInteractionType.DISPLACEMENT));
                protectionAllowed = decision.allowed();
            }
        }

        SafeDestinationPolicy.Facts facts = new SafeDestinationPolicy.Facts(
            loaded,
            border,
            collisionFree,
            collisionFree,
            fluidAllowed,
            sameDimension,
            protectionAllowed,
            vehicleUnsafe);
        SafeDestinationPolicy.Decision decision = POLICY.validate(facts);
        return new Result(decision.allowed(), decision.code(), facts);
    }

    private static Result denied(String code) {
        return new Result(false, code, new SafeDestinationPolicy.Facts(
            false, false, false, false, false, false, false, false));
    }

    public record Result(boolean allowed, String code, SafeDestinationPolicy.Facts facts) {
        public Result {
            Objects.requireNonNull(code, "code");
            Objects.requireNonNull(facts, "facts");
            if (allowed && !code.isEmpty()) throw new IllegalArgumentException("allowed result has denial code");
            if (!allowed && code.isEmpty()) throw new IllegalArgumentException("denied result lacks code");
        }
    }
}
