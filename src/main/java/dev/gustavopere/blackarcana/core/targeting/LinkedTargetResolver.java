package dev.gustavopere.blackarcana.core.targeting;

import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import net.minecraft.server.level.ServerPlayer;

import java.util.List;
import java.util.UUID;

/**
 * Resolves spell-specific linked entities from server-owned state. Implementations
 * may consult contracts, marks, familiars or other Black Arcana state, but must
 * never trust a client-supplied list of entity ids.
 */
@FunctionalInterface
public interface LinkedTargetResolver {
    List<UUID> resolve(ArcanaCastRequest request, ServerPlayer caster);

    static LinkedTargetResolver none() {
        return (request, caster) -> List.of();
    }
}
