package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.content.blood.EquilibriumTransferPlanner;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntimeManager;
import dev.gustavopere.blackarcana.core.world.EntityInteractionType;
import dev.gustavopere.blackarcana.core.world.EntityProtectionFacts;
import dev.gustavopere.blackarcana.core.world.ProtectionQuery;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;

import java.util.Objects;
import java.util.UUID;

/** Server-authoritative transaction boundary for Equilibrium Rite. */
public final class MinecraftEquilibriumRiteRuntime {
    private MinecraftEquilibriumRiteRuntime() { }

    public static TransferResult transfer(
        MinecraftServer server,
        UUID sourceId,
        UUID targetId,
        double requestedTransfer,
        double sourceHealthFloor
    ) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(sourceId, "sourceId");
        Objects.requireNonNull(targetId, "targetId");

        if (sourceId.equals(targetId)) {
            return TransferResult.denied(
                "equilibrium_same_endpoint",
                "Equilibrium Rite requires two distinct living endpoints");
        }

        LivingEntity source = findLoadedLivingEntity(server, sourceId);
        LivingEntity target = findLoadedLivingEntity(server, targetId);
        if (source == null || target == null) {
            return TransferResult.denied(
                "equilibrium_endpoint_unavailable",
                "Equilibrium Rite endpoints must already be loaded living entities");
        }
        if (!source.isAlive() || !target.isAlive()) {
            return TransferResult.denied(
                "equilibrium_endpoint_not_alive",
                "Equilibrium Rite cannot transfer health to or from a dead endpoint");
        }
        if (!(target.level() instanceof ServerLevel targetLevel)) {
            return TransferResult.denied(
                "equilibrium_server_level_required",
                "Equilibrium Rite target must exist on a server level");
        }

        ArcanaServerRuntime runtime = ArcanaServerRuntimeManager.get(server).orElse(null);
        if (runtime == null) {
            return TransferResult.denied(
                "equilibrium_runtime_unavailable",
                "Black Arcana server runtime is unavailable");
        }

        ArcanaDecision admission = authorizeTarget(server, runtime, source, target, targetLevel);
        if (!admission.allowed()) return new TransferResult(admission, 0.0D);

        final EquilibriumTransferPlanner.TransferPlan plan;
        try {
            plan = EquilibriumTransferPlanner.plan(
                source.getHealth(),
                source.getMaxHealth(),
                target.getHealth(),
                target.getMaxHealth(),
                requestedTransfer,
                sourceHealthFloor);
        } catch (IllegalArgumentException invalidRequest) {
            return TransferResult.denied(
                "equilibrium_request_invalid",
                "Equilibrium Rite transfer request violates bounded health-transfer rules");
        }
        if (!plan.applicable() || plan.transferred() <= 0.0D) {
            return TransferResult.denied(
                "equilibrium_no_transfer",
                "Equilibrium Rite has no eligible health to transfer");
        }

        LivingEntity liveSource = findLoadedLivingEntity(server, sourceId);
        LivingEntity liveTarget = findLoadedLivingEntity(server, targetId);
        if (liveSource != source || liveTarget != target || !source.isAlive() || !target.isAlive()) {
            return TransferResult.denied(
                "equilibrium_endpoint_changed",
                "Equilibrium Rite endpoint state changed before settlement");
        }
        ArcanaDecision settlementAdmission = authorizeTarget(server, runtime, source, target, targetLevel);
        if (!settlementAdmission.allowed()) return new TransferResult(settlementAdmission, 0.0D);

        source.setHealth((float) plan.sourceAfter());
        target.setHealth((float) plan.targetAfter());
        return new TransferResult(ArcanaDecision.allow(), plan.transferred());
    }

    private static ArcanaDecision authorizeTarget(
        MinecraftServer server,
        ArcanaServerRuntime runtime,
        LivingEntity source,
        LivingEntity target,
        ServerLevel targetLevel
    ) {
        EntityProtectionFacts facts = MinecraftEntityProtectionResolver.resolve(server, source, target);
        if (target instanceof Player) {
            return ArcanaDecision.deny(
                "equilibrium_player_target_disabled",
                "Hostile player health exchange is disabled by default");
        }
        if (facts.boss()) {
            return ArcanaDecision.deny(
                "equilibrium_boss_target_disabled",
                "Boss health exchange is disabled by default");
        }

        return runtime.entityInteractionAdmission().authorize(
            EntityInteractionType.DAMAGE,
            facts,
            new ProtectionQuery(
                source.getUUID(),
                targetLevel.dimension().location().toString(),
                target.getUUID().toString(),
                EntityInteractionType.DAMAGE))
            .decision();
    }

    private static LivingEntity findLoadedLivingEntity(MinecraftServer server, UUID entityId) {
        for (ServerLevel level : server.getAllLevels()) {
            Entity entity = level.getEntity(entityId);
            if (entity instanceof LivingEntity living) return living;
        }
        return null;
    }

    public record TransferResult(ArcanaDecision decision, double transferred) {
        public TransferResult {
            Objects.requireNonNull(decision, "decision");
            if (!Double.isFinite(transferred) || transferred < 0.0D) {
                throw new IllegalArgumentException("transferred must be finite and non-negative");
            }
            if (!decision.allowed() && transferred != 0.0D) {
                throw new IllegalArgumentException("denied Equilibrium Rite cannot report transferred health");
            }
        }

        public static TransferResult denied(String code, String detail) {
            return new TransferResult(ArcanaDecision.deny(code, detail), 0.0D);
        }
    }
}
