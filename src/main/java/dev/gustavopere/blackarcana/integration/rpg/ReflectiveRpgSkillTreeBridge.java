package dev.gustavopere.blackarcana.integration.rpg;

import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaIntegrationAvailability;
import dev.gustavopere.blackarcana.api.ArcanaIntegrationCapability;
import java.lang.reflect.Constructor;
import java.lang.reflect.Method;
import java.util.Collection;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Set;
import java.util.UUID;
import java.util.function.Function;
import net.minecraft.server.level.ServerPlayer;

/**
 * Audited binary adapter for RPG Skill Tree 1.0.0-alpha.6-dev.
 *
 * <p>The RPG project is private/unpublished, so a direct Maven dependency would
 * make Black Arcana builds non-reproducible. Reflection is confined to this
 * adapter and probes the complete method surface before advertising a capability.</p>
 */
public final class ReflectiveRpgSkillTreeBridge implements RpgSkillTreeBridge {
    private static final String CORE_RUNTIME = "dev.gustavopere.rpgskilltree.runtime.CorePlayerProgressionRuntime";
    private static final String QUERY_SNAPSHOT = "dev.gustavopere.rpgskilltree.core.CoreProgressionQuerySnapshot";
    private static final String ATTRIBUTE_RANKS = "dev.gustavopere.rpgskilltree.core.AttributeRanks";
    private static final String ATTRIBUTE_ID = "dev.gustavopere.rpgskilltree.core.AttributeId";
    private static final String PLAYER_RUNTIME = "dev.gustavopere.rpgskilltree.runtime.PlayerProgressionRuntime";
    private static final String PROGRESSION_STATE = "dev.gustavopere.rpgskilltree.core.ProgressionState";
    private static final String MASTERY_STATE = "dev.gustavopere.rpgskilltree.core.MasteryState";
    private static final String MASTERY_AWARD = "dev.gustavopere.rpgskilltree.core.MasteryAward";

    private final ArcanaIntegrationAvailability availability;
    private final String version;
    private final String diagnostic;
    private final Function<UUID, ServerPlayer> playerResolver;
    private final Access access;

    private ReflectiveRpgSkillTreeBridge(
        ArcanaIntegrationAvailability availability,
        String version,
        String diagnostic,
        Function<UUID, ServerPlayer> playerResolver,
        Access access
    ) {
        this.availability = Objects.requireNonNull(availability, "availability");
        this.version = normalizeVersion(version);
        this.diagnostic = Objects.requireNonNull(diagnostic, "diagnostic");
        this.playerResolver = Objects.requireNonNull(playerResolver, "playerResolver");
        this.access = access;
    }

    public static ReflectiveRpgSkillTreeBridge probe(
        boolean modLoaded,
        String version,
        Function<UUID, ServerPlayer> playerResolver
    ) {
        Objects.requireNonNull(playerResolver, "playerResolver");
        if (!modLoaded) {
            return new ReflectiveRpgSkillTreeBridge(
                ArcanaIntegrationAvailability.MISSING_MOD,
                version,
                "RPG Skill Tree is not loaded",
                playerResolver,
                null);
        }

        try {
            ClassLoader loader = ReflectiveRpgSkillTreeBridge.class.getClassLoader();
            Class<?> coreRuntime = load(loader, CORE_RUNTIME);
            Class<?> querySnapshot = load(loader, QUERY_SNAPSHOT);
            Class<?> attributeRanks = load(loader, ATTRIBUTE_RANKS);
            Class<?> attributeId = load(loader, ATTRIBUTE_ID);
            Class<?> playerRuntime = load(loader, PLAYER_RUNTIME);
            Class<?> progressionState = load(loader, PROGRESSION_STATE);
            Class<?> masteryState = load(loader, MASTERY_STATE);
            Class<?> masteryAward = load(loader, MASTERY_AWARD);

            Access access = new Access(
                coreRuntime.getMethod("queryProgression", ServerPlayer.class),
                querySnapshot.getMethod("level"),
                querySnapshot.getMethod("attributeRanks"),
                attributeId,
                attributeId.getMethod("serializedId"),
                attributeRanks.getMethod("rank", attributeId),
                playerRuntime.getMethod("get", ServerPlayer.class),
                progressionState.getMethod("mastery"),
                masteryState.getMethod("experience"),
                masteryAward.getConstructor(String.class, int.class, String.class),
                playerRuntime.getMethod("awardMastery", ServerPlayer.class, Collection.class));

            return new ReflectiveRpgSkillTreeBridge(
                ArcanaIntegrationAvailability.AVAILABLE,
                version,
                "",
                playerResolver,
                access);
        } catch (ReflectiveOperationException | LinkageError failure) {
            return new ReflectiveRpgSkillTreeBridge(
                ArcanaIntegrationAvailability.API_INCOMPATIBLE,
                version,
                "RPG Skill Tree API probe failed: " + failure.getClass().getSimpleName(),
                playerResolver,
                null);
        }
    }

    @Override
    public String integrationId() {
        return MOD_ID;
    }

    @Override
    public boolean available() {
        return availability.usable();
    }

    @Override
    public String implementationVersion() {
        return version;
    }

    @Override
    public ArcanaIntegrationAvailability availability() {
        return availability;
    }

    @Override
    public Set<ArcanaIntegrationCapability> capabilities() {
        if (!available()) return Set.of();
        return Set.of(
            ArcanaIntegrationCapability.PROGRESSION_QUERY,
            ArcanaIntegrationCapability.MASTERY_AWARD);
    }

    @Override
    public String diagnostic() {
        return diagnostic;
    }

    @Override
    public RpgProgressionQuery query(UUID playerId) {
        Objects.requireNonNull(playerId, "playerId");
        if (!available() || access == null) {
            return RpgProgressionQuery.denied("rpg_integration_unavailable", diagnostic);
        }
        ServerPlayer player = playerResolver.apply(playerId);
        if (player == null) {
            return RpgProgressionQuery.denied("rpg_player_unavailable", "RPG player is not online on this server");
        }

        try {
            Object querySnapshot = access.queryProgression().invoke(null, player);
            long level = ((Number) access.level().invoke(querySnapshot)).longValue();
            Object ranks = access.attributeRanks().invoke(querySnapshot);

            Map<String, Long> attributes = new HashMap<>();
            Object[] attributeIds = access.attributeIdClass().getEnumConstants();
            if (attributeIds == null) throw new IllegalStateException("RPG AttributeId is no longer an enum");
            for (Object attributeId : attributeIds) {
                String id = (String) access.attributeSerializedId().invoke(attributeId);
                long rank = ((Number) access.attributeRank().invoke(ranks, attributeId)).longValue();
                if (rank != 0L) attributes.put(id, rank);
            }

            Object progression = access.playerProgressionGet().invoke(null, player);
            Object mastery = access.progressionMastery().invoke(progression);
            Object rawExperience = access.masteryExperience().invoke(mastery);
            if (!(rawExperience instanceof Map<?, ?> rawMap)) {
                throw new IllegalStateException("RPG mastery experience accessor no longer returns Map");
            }
            Map<String, Integer> masteryExperience = new HashMap<>();
            for (Map.Entry<?, ?> entry : rawMap.entrySet()) {
                if (!(entry.getKey() instanceof String lane) || !(entry.getValue() instanceof Number xp)) {
                    throw new IllegalStateException("RPG mastery map contains incompatible entries");
                }
                masteryExperience.put(lane, xp.intValue());
            }

            return RpgProgressionQuery.success(new RpgProgressionSnapshot(level, attributes, masteryExperience));
        } catch (ReflectiveOperationException | RuntimeException | LinkageError failure) {
            return RpgProgressionQuery.denied(
                "rpg_query_failed",
                "RPG progression query failed: " + failure.getClass().getSimpleName());
        }
    }

    @Override
    public ArcanaDecision awardMastery(UUID playerId, RpgMasteryAwardSpec award) {
        Objects.requireNonNull(playerId, "playerId");
        Objects.requireNonNull(award, "award");
        if (!available() || access == null) {
            return ArcanaDecision.deny("rpg_integration_unavailable", diagnostic);
        }
        ServerPlayer player = playerResolver.apply(playerId);
        if (player == null) {
            return ArcanaDecision.deny("rpg_player_unavailable", "RPG player is not online on this server");
        }

        try {
            Object nativeAward = access.masteryAwardConstructor().newInstance(
                award.laneId(), award.experience(), award.sourceId());
            access.awardMastery().invoke(null, player, List.of(nativeAward));
            return ArcanaDecision.allow();
        } catch (ReflectiveOperationException | RuntimeException | LinkageError failure) {
            return ArcanaDecision.deny(
                "rpg_mastery_award_failed",
                "RPG mastery award failed: " + failure.getClass().getSimpleName());
        }
    }

    private static Class<?> load(ClassLoader loader, String name) throws ClassNotFoundException {
        return Class.forName(name, false, loader);
    }

    private static String normalizeVersion(String version) {
        if (version == null || version.isBlank()) return "unknown";
        return version.length() > 96 ? version.substring(0, 96) : version;
    }

    private record Access(
        Method queryProgression,
        Method level,
        Method attributeRanks,
        Class<?> attributeIdClass,
        Method attributeSerializedId,
        Method attributeRank,
        Method playerProgressionGet,
        Method progressionMastery,
        Method masteryExperience,
        Constructor<?> masteryAwardConstructor,
        Method awardMastery
    ) { }
}
