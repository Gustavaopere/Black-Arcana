package dev.gustavopere.blackarcana.config;

import dev.gustavopere.blackarcana.api.ArcanaChannelSpec;
import dev.gustavopere.blackarcana.api.ArcanaCooldownSpec;
import dev.gustavopere.blackarcana.api.ArcanaCost;
import dev.gustavopere.blackarcana.content.noetic.NoeticSafetyCeilings;
import dev.gustavopere.blackarcana.core.cost.ResourceCostProvider;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

/**
 * Strict server-owned Astral invocation parameters.
 *
 * <p>This is a configuration surface only. It intentionally provides no production defaults and does not
 * install Astral Severance into a runtime. Hard safety ceilings only reject unsafe configured values.</p>
 */
public record AstralInvocationDataDefinition(
        int schemaVersion,
        String id,
        ConfigScope scope,
        String resourceId,
        double resourceAmount,
        ArcanaCost.Unit resourceUnit,
        String cooldownGroup,
        long cooldownDurationTicks,
        boolean cooldownPersistent,
        long channelMinimumTicks,
        long channelMaximumTicks,
        int projectionDurationTicks,
        double maxRangeBlocks
) {
    public static final int CURRENT_SCHEMA_VERSION = 1;
    public static final String ASTRAL_SEVERANCE_ID = "black_arcana:astral_severance";

    public AstralInvocationDataDefinition {
        Objects.requireNonNull(id, "id");
        Objects.requireNonNull(scope, "scope");
        Objects.requireNonNull(resourceId, "resourceId");
        Objects.requireNonNull(resourceUnit, "resourceUnit");
        Objects.requireNonNull(cooldownGroup, "cooldownGroup");
    }

    public List<String> validate() {
        List<String> errors = new ArrayList<>();
        if (schemaVersion != CURRENT_SCHEMA_VERSION) {
            errors.add("unsupported schemaVersion: " + schemaVersion);
        }
        if (!ASTRAL_SEVERANCE_ID.equals(id)) {
            errors.add("id must be " + ASTRAL_SEVERANCE_ID);
        }
        if (scope != ConfigScope.SERVER || !scope.isGameplayAuthority()) {
            errors.add("Astral invocation config must use SERVER gameplay authority");
        }
        try {
            ResourceCostProvider.requireResourceId(resourceId);
        } catch (IllegalArgumentException invalid) {
            errors.add("invalid resource id: " + invalid.getMessage());
        }
        try {
            new ArcanaCost(resourceId, resourceAmount, resourceUnit);
        } catch (IllegalArgumentException invalid) {
            errors.add("invalid resource cost: " + invalid.getMessage());
        }
        try {
            new ArcanaCooldownSpec(cooldownGroup, cooldownDurationTicks, cooldownPersistent);
        } catch (IllegalArgumentException invalid) {
            errors.add("invalid cooldown: " + invalid.getMessage());
        }
        try {
            new ArcanaChannelSpec(channelMinimumTicks, channelMaximumTicks);
        } catch (IllegalArgumentException invalid) {
            errors.add("invalid channel: " + invalid.getMessage());
        }
        if (projectionDurationTicks <= 0 || projectionDurationTicks > NoeticSafetyCeilings.MAX_DURATION_TICKS) {
            errors.add("projectionDurationTicks outside hard Noetic bounds");
        }
        if (!Double.isFinite(maxRangeBlocks)
                || maxRangeBlocks <= 0.0D
                || maxRangeBlocks > NoeticSafetyCeilings.MAX_RANGE_BLOCKS) {
            errors.add("maxRangeBlocks outside hard Noetic bounds");
        }
        return List.copyOf(errors);
    }

    public Invocation toInvocation() {
        List<String> errors = validate();
        if (!errors.isEmpty()) {
            throw new IllegalArgumentException("invalid Astral invocation config: " + String.join("; ", errors));
        }
        return new Invocation(
                new ArcanaCost(resourceId, resourceAmount, resourceUnit),
                new ArcanaCooldownSpec(cooldownGroup, cooldownDurationTicks, cooldownPersistent),
                new ArcanaChannelSpec(channelMinimumTicks, channelMaximumTicks),
                projectionDurationTicks,
                maxRangeBlocks);
    }

    public record Invocation(
            ArcanaCost cost,
            ArcanaCooldownSpec cooldown,
            ArcanaChannelSpec channelSpec,
            int projectionDurationTicks,
            double maxRangeBlocks
    ) {
        public Invocation {
            Objects.requireNonNull(cost, "cost");
            Objects.requireNonNull(cooldown, "cooldown");
            Objects.requireNonNull(channelSpec, "channelSpec");
        }
    }
}
