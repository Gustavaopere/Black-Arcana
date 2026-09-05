package dev.gustavopere.blackarcana.content.projection;

import java.util.Locale;
import java.util.Objects;
import java.util.regex.Pattern;

/**
 * Sanitized immutable projection input. It deliberately has no ItemStack, NBT, data-component,
 * capability, UUID-owner token or callback field.
 */
public record ProjectedWeaponProfile(
    String profileId,
    String sourceItemId,
    Archetype archetype,
    double attackDamageContribution,
    double attackSpeed,
    double projectileSpeed
) {
    private static final Pattern ID = Pattern.compile("[a-z0-9_.-]+:[a-z0-9/._-]+");

    public ProjectedWeaponProfile {
        profileId = canonicalId(profileId, "profileId");
        sourceItemId = canonicalId(sourceItemId, "sourceItemId");
        Objects.requireNonNull(archetype, "archetype");
        if (!Double.isFinite(attackDamageContribution) || attackDamageContribution < 0.0D
            || attackDamageContribution > ProjectionSafetyCeilings.MAX_RAW_ATTACK_DAMAGE) {
            throw new IllegalArgumentException("attackDamageContribution outside hard ceiling");
        }
        if (!Double.isFinite(attackSpeed) || attackSpeed < 0.0D || attackSpeed > 20.0D) {
            throw new IllegalArgumentException("attackSpeed outside technical bounds");
        }
        if (!Double.isFinite(projectileSpeed) || projectileSpeed < 0.0D || projectileSpeed > 10.0D) {
            throw new IllegalArgumentException("projectileSpeed outside technical bounds");
        }
    }

    public static ProjectedWeaponProfile sanitized(
        String profileId,
        String sourceItemId,
        Archetype archetype,
        double observedAttackDamage,
        double observedAttackSpeed,
        double observedProjectileSpeed
    ) {
        if (!Double.isFinite(observedAttackDamage) || observedAttackDamage < 0.0D) {
            throw new IllegalArgumentException("observedAttackDamage invalid");
        }
        double damage = Math.min(observedAttackDamage, ProjectionSafetyCeilings.MAX_RAW_ATTACK_DAMAGE);
        double speed = clamp(observedAttackSpeed, 0.0D, 20.0D);
        double projectile = clamp(observedProjectileSpeed, 0.0D, 10.0D);
        return new ProjectedWeaponProfile(profileId, sourceItemId, archetype, damage, speed, projectile);
    }

    private static String canonicalId(String value, String field) {
        Objects.requireNonNull(value, field);
        String normalized = value.trim().toLowerCase(Locale.ROOT);
        if (normalized.length() > 128 || !ID.matcher(normalized).matches()) {
            throw new IllegalArgumentException(field + " must be a bounded namespaced id");
        }
        return normalized;
    }

    private static double clamp(double value, double min, double max) {
        if (!Double.isFinite(value)) return min;
        return Math.max(min, Math.min(max, value));
    }

    public enum Archetype {
        MELEE,
        PROJECTILE,
        SHIELD
    }
}
