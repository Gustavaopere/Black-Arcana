package dev.gustavopere.blackarcana.core.world;

import java.util.Objects;

/** Default PvP/team/boss semantics before external claim/protection adapters are consulted. */
public final class DefaultEntityInteractionPolicy {
    private final EntityEffectLimits standardLimits;
    private final EntityEffectLimits bossLimits;

    public DefaultEntityInteractionPolicy(EntityEffectLimits standardLimits, EntityEffectLimits bossLimits) {
        this.standardLimits = Objects.requireNonNull(standardLimits, "standardLimits");
        this.bossLimits = Objects.requireNonNull(bossLimits, "bossLimits");
    }

    public static DefaultEntityInteractionPolicy safeDefaults() {
        return new DefaultEntityInteractionPolicy(
            EntityEffectLimits.standard(),
            EntityEffectLimits.bossSafeDefaults());
    }

    public EntityInteractionAuthorization authorize(EntityInteractionType type, EntityProtectionFacts facts) {
        Objects.requireNonNull(type, "type");
        Objects.requireNonNull(facts, "facts");
        EntityEffectLimits limits = facts.boss() ? bossLimits : standardLimits;

        if (facts.invulnerable()) {
            return EntityInteractionAuthorization.deny(
                "target_invulnerable", "Target is invulnerable to hostile Black Arcana effects", limits);
        }
        if (facts.player() && !facts.serverPvpEnabled()) {
            return EntityInteractionAuthorization.deny(
                "pvp_disabled", "Server PvP is disabled", limits);
        }
        if (facts.alliedWithCaster()) {
            return EntityInteractionAuthorization.deny(
                "target_allied", "Allied targets are protected from hostile Black Arcana effects", limits);
        }
        if (facts.boss()) {
            return switch (type) {
                case EXECUTION -> EntityInteractionAuthorization.deny(
                    "boss_execution_blocked", "Bosses cannot be executed by Black Arcana", limits);
                case RESURRECTION_DENIAL -> EntityInteractionAuthorization.deny(
                    "boss_resurrection_denial_blocked", "Boss resurrection lifecycle cannot be suppressed", limits);
                case DOMAIN_CAPTURE -> EntityInteractionAuthorization.deny(
                    "boss_domain_capture_blocked", "Bosses cannot be permanently captured by a domain", limits);
                case DAMAGE, CONTROL, DISPLACEMENT -> EntityInteractionAuthorization.allow(limits);
            };
        }
        return EntityInteractionAuthorization.allow(limits);
    }
}
