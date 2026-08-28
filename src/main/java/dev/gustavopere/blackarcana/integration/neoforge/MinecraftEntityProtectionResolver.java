package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.core.world.EntityProtectionFacts;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.MinecraftServer;
import net.minecraft.tags.TagKey;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.player.Player;

import java.util.Objects;

/** Computes protection facts exclusively from authoritative server/entity state. */
public final class MinecraftEntityProtectionResolver {
    private static final TagKey<EntityType<?>> BOSSES = TagKey.create(
        Registries.ENTITY_TYPE,
        ResourceLocation.fromNamespaceAndPath("c", "bosses"));

    private MinecraftEntityProtectionResolver() { }

    public static EntityProtectionFacts resolve(
        MinecraftServer server,
        Entity caster,
        Entity target
    ) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(caster, "caster");
        Objects.requireNonNull(target, "target");

        boolean player = target instanceof Player;
        boolean playerPrivilegeInvulnerable = target instanceof Player targetPlayer
            && (targetPlayer.isCreative() || targetPlayer.isSpectator());

        return new EntityProtectionFacts(
            player,
            caster.isAlliedTo(target),
            target.getType().is(BOSSES),
            target.isInvulnerable() || playerPrivilegeInvulnerable,
            server.isPvpAllowed());
    }
}
