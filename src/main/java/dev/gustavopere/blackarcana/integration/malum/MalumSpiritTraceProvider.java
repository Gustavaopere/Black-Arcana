package dev.gustavopere.blackarcana.integration.malum;

import dev.gustavopere.blackarcana.content.souls.SpiritSightPolicy;
import dev.gustavopere.blackarcana.content.souls.SpiritTraceProvider;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.level.entity.EntityTypeTest;
import net.minecraft.world.phys.AABB;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.Optional;

/**
 * Malum-backed Spirit Sight provider using only stable registry ids.
 *
 * <p>This class intentionally does not link against Malum classes. If Malum changes or removes
 * the supported entity ids, the provider returns no trace for the unknown entity and therefore
 * fails closed instead of reflecting private host state.</p>
 */
public final class MalumSpiritTraceProvider implements SpiritTraceProvider {
    public static final int ABSOLUTE_MAX_TRACES = 256;
    private static final String PROVIDER_ID = "black_arcana:malum_spirit_traces";
    private static final ResourceLocation NATURAL_SPIRIT =
        ResourceLocation.fromNamespaceAndPath(MalumIntegrationIds.MOD_ID, "natural_spirit");
    private static final ResourceLocation SOUL_TAG_ENTITY =
        ResourceLocation.fromNamespaceAndPath(MalumIntegrationIds.MOD_ID, "soul_tag_entity");

    private final MinecraftServer server;

    public MalumSpiritTraceProvider(MinecraftServer server) {
        this.server = Objects.requireNonNull(server, "server");
    }

    @Override
    public String providerId() {
        return PROVIDER_ID;
    }

    @Override
    public List<Trace> query(Query query) {
        Objects.requireNonNull(query, "query");
        ServerLevel level = findLevel(query.dimensionId());
        if (level == null) return List.of();

        double radius = query.radius();
        AABB bounds = new AABB(
            query.x() - radius,
            query.y() - radius,
            query.z() - radius,
            query.x() + radius,
            query.y() + radius,
            query.z() + radius);

        EntityTypeTest<Entity, Entity> allEntities = EntityTypeTest.forClass(Entity.class);
        List<Entity> candidates = new ArrayList<>();
        level.getEntities(
            allEntities,
            bounds,
            entity -> classifyEntityType(BuiltInRegistries.ENTITY_TYPE.getKey(entity.getType())).isPresent(),
            candidates,
            ABSOLUTE_MAX_TRACES);

        if (candidates.isEmpty()) return List.of();
        List<Trace> traces = new ArrayList<>(candidates.size());
        for (Entity entity : candidates) {
            Optional<Classification> classification = classifyEntityType(
                BuiltInRegistries.ENTITY_TYPE.getKey(entity.getType()));
            if (classification.isEmpty()) continue;
            Classification value = classification.get();
            traces.add(new Trace(
                entity.getUUID(),
                entity.getX(),
                entity.getY(),
                entity.getZ(),
                value.kind(),
                value.privateData()));
        }
        return List.copyOf(traces);
    }

    static Optional<Classification> classifyEntityType(ResourceLocation entityTypeId) {
        if (entityTypeId == null) return Optional.empty();
        if (NATURAL_SPIRIT.equals(entityTypeId)) {
            return Optional.of(new Classification(SpiritSightPolicy.TraceKind.MALUM_SPIRIT, false));
        }
        if (SOUL_TAG_ENTITY.equals(entityTypeId)) {
            // SoulTagEntity contains target UUID/name in host state. Never copy that identity into our Trace.
            return Optional.of(new Classification(SpiritSightPolicy.TraceKind.MALUM_SPIRIT, true));
        }
        return Optional.empty();
    }

    private ServerLevel findLevel(String dimensionId) {
        for (ServerLevel level : server.getAllLevels()) {
            if (level.dimension().location().toString().equals(dimensionId)) return level;
        }
        return null;
    }

    record Classification(SpiritSightPolicy.TraceKind kind, boolean privateData) {
        Classification {
            Objects.requireNonNull(kind, "kind");
        }
    }
}
