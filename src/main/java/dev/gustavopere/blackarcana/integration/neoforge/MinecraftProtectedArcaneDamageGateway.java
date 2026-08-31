package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.hazard.ArcanaDamageProvenance;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntimeManager;
import dev.gustavopere.blackarcana.core.world.EntityInteractionType;
import dev.gustavopere.blackarcana.core.world.ProtectionQuery;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.LivingEntity;

import java.util.Objects;
import java.util.UUID;

/**
 * Canonical NeoForge entrypoint for attributed hostile spell damage.
 *
 * Stage 05A attribution never bypasses the frozen Stage 04 entity-admission route: PvP,
 * allied targets, boss semantics and optional protection adapters are resolved before the
 * lower-level damage/provenance pipeline is invoked. A denied interaction therefore cannot
 * become confirmed eligible damage and cannot create Arcane Backlash settlement.
 */
public final class MinecraftProtectedArcaneDamageGateway {
    private MinecraftProtectedArcaneDamageGateway() { }

    public static MinecraftArcaneDamagePipeline.DamageAttempt hurtAttributed(
        ServerPlayer caster,
        LivingEntity target,
        DamageSource source,
        float requestedDamage,
        ArcanaDamageProvenance provenance
    ) {
        Objects.requireNonNull(caster, "caster");
        Objects.requireNonNull(target, "target");
        Objects.requireNonNull(source, "source");
        Objects.requireNonNull(provenance, "provenance");

        ArcanaDecision identity = validateCasterIdentity(caster.getUUID(), provenance);
        if (!identity.allowed()) {
            return MinecraftArcaneDamagePipeline.DamageAttempt.denied(identity.code());
        }
        if (!(target.level() instanceof ServerLevel targetLevel)) {
            return MinecraftArcaneDamagePipeline.DamageAttempt.denied("server_level_required");
        }

        MinecraftServer server = targetLevel.getServer();
        if (caster.serverLevel().getServer() != server) {
            return MinecraftArcaneDamagePipeline.DamageAttempt.denied("damage_server_mismatch");
        }

        var runtime = ArcanaServerRuntimeManager.get(server).orElse(null);
        if (runtime == null) {
            return MinecraftArcaneDamagePipeline.DamageAttempt.denied("server_runtime_unavailable");
        }

        var facts = MinecraftEntityProtectionResolver.resolve(server, caster, target);
        var query = new ProtectionQuery(
            caster.getUUID(),
            targetLevel.dimension().location().toString(),
            "entity:" + target.getUUID(),
            EntityInteractionType.DAMAGE);
        var authorization = runtime.entityInteractionAdmission().authorize(
            EntityInteractionType.DAMAGE,
            facts,
            query);
        if (!authorization.decision().allowed()) {
            return MinecraftArcaneDamagePipeline.DamageAttempt.denied(authorization.decision().code());
        }

        return MinecraftArcaneDamagePipeline.hurtAttributed(target, source, requestedDamage, provenance);
    }

    static ArcanaDecision validateCasterIdentity(UUID casterId, ArcanaDamageProvenance provenance) {
        Objects.requireNonNull(casterId, "casterId");
        Objects.requireNonNull(provenance, "provenance");
        if (!provenance.casterId().equals(casterId)) {
            return ArcanaDecision.deny(
                "damage_caster_mismatch",
                "Attributed damage provenance does not belong to the authoritative caster");
        }
        return ArcanaDecision.allow();
    }
}
