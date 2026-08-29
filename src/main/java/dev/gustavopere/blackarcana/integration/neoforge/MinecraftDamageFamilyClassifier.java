package dev.gustavopere.blackarcana.integration.neoforge;

import net.minecraft.tags.DamageTypeTags;
import net.minecraft.world.damagesource.DamageSource;
import net.neoforged.neoforge.common.Tags;

import java.nio.charset.StandardCharsets;
import java.util.Objects;
import java.util.UUID;

/**
 * Stable server-side damage-family classifier for Law of Recurrence.
 *
 * Semantic tags are preferred over concrete damage-type ids so vanilla and modded
 * sources that opt into the same NeoForge/vanilla contract adapt as one family.
 * Unknown registered types retain their exact registry key when it fits the bounded
 * family contract; exceptionally long or direct/unregistered types receive a stable
 * bounded fallback instead of using display names or attacker heuristics.
 */
public final class MinecraftDamageFamilyClassifier {
    private static final int MAX_FAMILY_LENGTH = 64;

    private MinecraftDamageFamilyClassifier() { }

    public static String classify(DamageSource source) {
        Objects.requireNonNull(source, "source");

        if (source.is(DamageTypeTags.IS_FIRE)) return "black_arcana:fire";
        if (source.is(DamageTypeTags.IS_EXPLOSION)) return "black_arcana:explosion";
        if (source.is(DamageTypeTags.IS_PROJECTILE)) return "black_arcana:projectile";
        if (source.is(DamageTypeTags.IS_FALL)) return "black_arcana:fall";
        if (source.is(DamageTypeTags.IS_DROWNING)) return "black_arcana:drowning";
        if (source.is(DamageTypeTags.IS_FREEZING)) return "black_arcana:freezing";
        if (source.is(DamageTypeTags.IS_LIGHTNING)) return "black_arcana:lightning";

        if (source.is(Tags.DamageTypes.IS_POISON)) return "black_arcana:poison";
        if (source.is(Tags.DamageTypes.IS_WITHER)) return "black_arcana:wither";
        if (source.is(Tags.DamageTypes.IS_MAGIC)) return "black_arcana:magic";
        if (source.is(Tags.DamageTypes.IS_TECHNICAL)) return "black_arcana:technical";
        if (source.is(Tags.DamageTypes.IS_ENVIRONMENT)) return "black_arcana:environment";
        if (source.is(Tags.DamageTypes.IS_PHYSICAL)) return "black_arcana:physical";

        return source.typeHolder().unwrapKey()
            .map(key -> boundedRegisteredFamily(key.location().toString()))
            .orElse("black_arcana:unknown");
    }

    private static String boundedRegisteredFamily(String registeredId) {
        if (registeredId.length() <= MAX_FAMILY_LENGTH) return registeredId;
        UUID stable = UUID.nameUUIDFromBytes(registeredId.getBytes(StandardCharsets.UTF_8));
        return "black_arcana:unknown/" + stable;
    }
}
