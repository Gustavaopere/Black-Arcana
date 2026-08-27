package dev.gustavopere.blackarcana.core.targeting;

import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaServices;
import dev.gustavopere.blackarcana.api.ArcanaTargetSpec;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.Entity;

import java.util.List;
import java.util.Objects;
import java.util.UUID;
import java.util.function.Function;

/**
 * Initial Minecraft target adapter. Only SELF and explicit loaded ENTITY targets
 * are supported here. More complex geometry gets dedicated adapters later.
 */
public final class ServerEntityTargetSelector implements ArcanaServices.TargetSelector {
    private final MinecraftServer server;
    private final Function<ArcanaCastRequest, ArcanaTargetSpec> specResolver;

    public ServerEntityTargetSelector(
            MinecraftServer server,
            Function<ArcanaCastRequest, ArcanaTargetSpec> specResolver
    ) {
        this.server = Objects.requireNonNull(server, "server");
        this.specResolver = Objects.requireNonNull(specResolver, "specResolver");
    }

    @Override
    public ArcanaServices.TargetResolution resolve(ArcanaCastRequest request) {
        ArcanaTargetSpec spec = Objects.requireNonNull(specResolver.apply(request), "target spec");
        ServerPlayer caster = server.getPlayerList().getPlayer(request.context().casterId());
        if (caster == null || !caster.isAlive()) {
            return ArcanaServices.TargetResolution.denied("caster is not a live server player");
        }

        if (!caster.level().dimension().location().toString().equals(request.context().dimensionId())) {
            return ArcanaServices.TargetResolution.denied("caster dimension changed before target resolution");
        }

        if (spec.kind() == ArcanaTargetSpec.Kind.SELF) {
            return ArcanaServices.TargetResolution.resolved(caster.getUUID().toString());
        }
        if (spec.kind() != ArcanaTargetSpec.Kind.ENTITY) {
            return ArcanaServices.TargetResolution.denied("target kind requires a dedicated server adapter: " + spec.kind());
        }
        if (request.targetHint().isBlank()) {
            return ArcanaServices.TargetResolution.denied("entity target hint is missing");
        }

        final UUID targetUuid;
        try {
            targetUuid = UUID.fromString(request.targetHint());
        } catch (IllegalArgumentException ex) {
            return ArcanaServices.TargetResolution.denied("entity target hint is not a UUID");
        }

        ServerLevel level = caster.serverLevel();
        Entity target = level.getEntity(targetUuid);
        if (target == null) {
            return ArcanaServices.TargetResolution.denied("target is not naturally loaded in caster dimension");
        }

        TargetCandidate candidate = new TargetCandidate(
                target.getUUID().toString(),
                caster.distanceToSqr(target),
                true,
                target.isAlive(),
                caster.hasLineOfSight(target),
                target instanceof ServerPlayer,
                caster.isAlliedTo(target));

        List<TargetCandidate> selected = BoundedTargeting.select(spec, List.of(candidate));
        if (selected.isEmpty()) {
            return ArcanaServices.TargetResolution.denied("target rejected by range/LOS/player/friendly policy");
        }
        return ArcanaServices.TargetResolution.resolved(selected.getFirst().targetId());
    }
}
