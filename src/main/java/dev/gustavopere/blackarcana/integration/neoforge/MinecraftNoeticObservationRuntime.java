package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.content.noetic.FamiliarOwnershipRegistry;
import dev.gustavopere.blackarcana.content.noetic.NoeticObservationRuntime;

import java.util.Objects;

/**
 * Minecraft-facing Stage 07.07 boundary.
 *
 * <p>Observation-session ownership and familiar-ownership authority stay in their bounded core registries.
 * World/entity admission and whitelisted snapshot construction are added behind this adapter, never by
 * exposing arbitrary entity serialization.</p>
 */
public final class MinecraftNoeticObservationRuntime {
    private final NoeticObservationRuntime observations;
    private final FamiliarOwnershipRegistry familiarOwnership;

    public MinecraftNoeticObservationRuntime(
            NoeticObservationRuntime observations,
            FamiliarOwnershipRegistry familiarOwnership
    ) {
        this.observations = Objects.requireNonNull(observations, "observations");
        this.familiarOwnership = Objects.requireNonNull(familiarOwnership, "familiarOwnership");
    }

    NoeticObservationRuntime observations() {
        return observations;
    }

    FamiliarOwnershipRegistry familiarOwnership() {
        return familiarOwnership;
    }
}
