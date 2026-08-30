package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.content.projection.ProjectedWeaponProfile;
import dev.gustavopere.blackarcana.content.projection.ProjectedWeaponProfileRegistry;
import dev.gustavopere.blackarcana.content.projection.ProjectionSafetyCeilings;
import net.minecraft.core.Holder;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.ai.attributes.Attribute;
import net.minecraft.world.entity.ai.attributes.AttributeModifier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.ProjectileWeaponItem;
import net.minecraft.world.item.ShieldItem;
import net.minecraft.world.item.component.ItemAttributeModifiers;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.event.server.ServerStoppedEvent;

import java.util.Collections;
import java.util.IdentityHashMap;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;
import java.util.UUID;

/**
 * Server-owned Echo Armament memory. Only explicit scalar gameplay observations cross the
 * ItemStack boundary; the source stack, components, enchantments and capabilities are never stored.
 */
public final class MinecraftEchoArmamentRuntime {
    private static final int MAX_OWNERS = 4096;
    private static final int MAX_PROFILES_PER_OWNER = ProjectionSafetyCeilings.MAX_STORED_PROFILES;
    private static final double PLAYER_BASE_ATTACK_DAMAGE = 1.0D;
    private static final double PLAYER_BASE_ATTACK_SPEED = 4.0D;
    private static final Map<MinecraftServer, ProjectedWeaponProfileRegistry> REGISTRIES =
        Collections.synchronizedMap(new IdentityHashMap<>());

    private MinecraftEchoArmamentRuntime() { }

    public static void register(IEventBus gameBus) {
        Objects.requireNonNull(gameBus, "gameBus");
        gameBus.addListener(MinecraftEchoArmamentRuntime::onServerStopped);
    }

    public static RememberResult rememberHeldWeapon(MinecraftServer server, UUID ownerId, String profileId) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(ownerId, "ownerId");
        Objects.requireNonNull(profileId, "profileId");

        ServerPlayer owner = server.getPlayerList().getPlayer(ownerId);
        if (owner == null || !owner.isAlive()) {
            return RememberResult.denied("echo_armament_owner_unavailable", "Echo Armament owner must be loaded and alive");
        }

        ItemStack source = owner.getMainHandItem();
        if (source.isEmpty()) {
            return RememberResult.denied("echo_armament_empty_hand", "Echo Armament requires an eligible held item");
        }

        Optional<ProjectedWeaponProfile> sanitized;
        try {
            sanitized = sanitize(profileId, source);
        } catch (IllegalArgumentException invalid) {
            return RememberResult.denied("echo_armament_profile_invalid", invalid.getMessage());
        }
        if (sanitized.isEmpty()) {
            return RememberResult.denied(
                "echo_armament_unsupported_item",
                "Held item does not expose an eligible bounded projection profile");
        }

        ProjectedWeaponProfile profile = sanitized.get();
        try {
            registry(server).remember(ownerId, profile);
        } catch (IllegalStateException capacity) {
            return RememberResult.denied("echo_armament_memory_capacity", capacity.getMessage());
        }
        return RememberResult.allowed(profile);
    }

    public static Optional<ProjectedWeaponProfile> findProfile(MinecraftServer server, UUID ownerId, String profileId) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(ownerId, "ownerId");
        Objects.requireNonNull(profileId, "profileId");
        ProjectedWeaponProfileRegistry registry = REGISTRIES.get(server);
        return registry == null ? Optional.empty() : registry.find(ownerId, profileId);
    }

    static Optional<ProjectedWeaponProfile> sanitize(String profileId, ItemStack source) {
        Objects.requireNonNull(profileId, "profileId");
        Objects.requireNonNull(source, "source");
        if (source.isEmpty()) return Optional.empty();

        Item item = source.getItem();
        AttributeObservation attributes = observeMainHandAttributes(source);
        ProjectedWeaponProfile.Archetype archetype;
        if (item instanceof ShieldItem) {
            archetype = ProjectedWeaponProfile.Archetype.SHIELD;
        } else if (item instanceof ProjectileWeaponItem) {
            archetype = ProjectedWeaponProfile.Archetype.PROJECTILE;
        } else if (attributes.hasAttackDamageModifier()) {
            archetype = ProjectedWeaponProfile.Archetype.MELEE;
        } else {
            return Optional.empty();
        }

        String sourceItemId = BuiltInRegistries.ITEM.getKey(item).toString();
        return Optional.of(ProjectedWeaponProfile.sanitized(
            profileId,
            sourceItemId,
            archetype,
            attributes.attackDamage(),
            attributes.attackSpeed(),
            0.0D));
    }

    private static AttributeObservation observeMainHandAttributes(ItemStack source) {
        MutableAttribute attackDamage = new MutableAttribute(PLAYER_BASE_ATTACK_DAMAGE);
        MutableAttribute attackSpeed = new MutableAttribute(PLAYER_BASE_ATTACK_SPEED);
        ItemAttributeModifiers modifiers = source.getAttributeModifiers();
        modifiers.forEach(EquipmentSlot.MAINHAND, (attribute, modifier) -> {
            if (attribute.equals(Attributes.ATTACK_DAMAGE)) attackDamage.accept(modifier);
            if (attribute.equals(Attributes.ATTACK_SPEED)) attackSpeed.accept(modifier);
        });
        return new AttributeObservation(
            attackDamage.value(),
            attackSpeed.value(),
            attackDamage.seenModifier);
    }

    private static ProjectedWeaponProfileRegistry registry(MinecraftServer server) {
        synchronized (REGISTRIES) {
            return REGISTRIES.computeIfAbsent(
                server,
                ignored -> new ProjectedWeaponProfileRegistry(MAX_OWNERS, MAX_PROFILES_PER_OWNER));
        }
    }

    private static void onServerStopped(ServerStoppedEvent event) {
        REGISTRIES.remove(event.getServer());
    }

    public record RememberResult(ArcanaDecision decision, Optional<ProjectedWeaponProfile> profile) {
        public RememberResult {
            Objects.requireNonNull(decision, "decision");
            profile = Objects.requireNonNull(profile, "profile");
            if (!decision.allowed() && profile.isPresent()) {
                throw new IllegalArgumentException("denied Echo Armament result cannot carry a profile");
            }
        }

        private static RememberResult allowed(ProjectedWeaponProfile profile) {
            return new RememberResult(ArcanaDecision.allow(), Optional.of(Objects.requireNonNull(profile, "profile")));
        }

        private static RememberResult denied(String code, String detail) {
            return new RememberResult(ArcanaDecision.deny(code, detail == null ? "" : detail), Optional.empty());
        }
    }

    private record AttributeObservation(double attackDamage, double attackSpeed, boolean hasAttackDamageModifier) { }

    private static final class MutableAttribute {
        private final double base;
        private double additive;
        private double multipliedBase;
        private double multipliedTotal = 1.0D;
        private boolean seenModifier;

        private MutableAttribute(double base) {
            this.base = base;
        }

        private void accept(AttributeModifier modifier) {
            seenModifier = true;
            double amount = modifier.amount();
            switch (modifier.operation()) {
                case ADD_VALUE -> additive += amount;
                case ADD_MULTIPLIED_BASE -> multipliedBase += amount;
                case ADD_MULTIPLIED_TOTAL -> multipliedTotal *= 1.0D + amount;
            }
        }

        private double value() {
            double value = (base + additive + base * multipliedBase) * multipliedTotal;
            return Double.isFinite(value) ? Math.max(0.0D, value) : 0.0D;
        }
    }
}
