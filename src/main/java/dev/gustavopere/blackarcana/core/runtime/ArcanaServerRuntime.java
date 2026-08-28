package dev.gustavopere.blackarcana.core.runtime;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.api.ArcanaCastContext;
import dev.gustavopere.blackarcana.api.ArcanaCastEngine;
import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaCastResult;
import dev.gustavopere.blackarcana.api.ArcanaChannelSpec;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.core.cast.ArcanaCastIngressService;
import dev.gustavopere.blackarcana.core.cast.ArcanaChannelCastCoordinator;
import dev.gustavopere.blackarcana.core.cast.ArcanaChannelManager;
import dev.gustavopere.blackarcana.core.cast.LoadoutRegistry;
import dev.gustavopere.blackarcana.core.cooldown.ArcanaCooldownPolicyRegistry;
import dev.gustavopere.blackarcana.core.cooldown.ChargePoolCooldownService;
import dev.gustavopere.blackarcana.core.cooldown.PersistentCooldownService;
import dev.gustavopere.blackarcana.core.cooldown.RuntimeGroupMigrations;
import dev.gustavopere.blackarcana.core.registry.ArcanaSpellRegistry;
import dev.gustavopere.blackarcana.core.registry.SpellDataCatalog;
import dev.gustavopere.blackarcana.network.CastIntentPayload;
import dev.gustavopere.blackarcana.network.CastResultPayload;
import dev.gustavopere.blackarcana.network.IngressRateLimiter;

import java.util.HashSet;
import java.util.Map;
import java.util.Objects;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;

/**
 * Runtime state owned by one Minecraft server instance. Optional-mod adapters
 * install engines into this object; no mutable gameplay state is shared across servers.
 */
public final class ArcanaServerRuntime {
    public static final int DEFAULT_MAX_CAST_INTENTS_PER_SECOND = 12;
    public static final int DEFAULT_MAX_TRACKED_CASTERS = 4096;
    public static final int DEFAULT_MAX_CHANNEL_SESSIONS = 4096;
    public static final int DEFAULT_MAX_SCHEDULED_EFFECTS = 2048;
    public static final int DEFAULT_EFFECT_WORK_BUDGET_PER_TICK = 128;

    private final ArcanaSpellRegistry spells = new ArcanaSpellRegistry();
    private final SpellDataCatalog spellData = new SpellDataCatalog();
    private final LoadoutRegistry loadouts = new LoadoutRegistry();
    private final ArcanaCooldownPolicyRegistry cooldownPolicies = new ArcanaCooldownPolicyRegistry();
    private final PersistentCooldownService cooldowns = new PersistentCooldownService(cooldownPolicies::cooldownFor);
    private final ChargePoolCooldownService charges = new ChargePoolCooldownService(cooldownPolicies::requireCharge);
    private final Map<ArcanaSpellId, ArcanaCastEngine> engines = new ConcurrentHashMap<>();
    private final ArcanaCastIngressService ingress;
    private final ArcanaChannelManager channels;
    private final ArcanaChannelCastCoordinator channelCasts;
    private final BoundedWorkScheduler effectScheduler;
    private RuntimeGroupMigrations groupMigrations = RuntimeGroupMigrations.none();

    public ArcanaServerRuntime(int maxCastIntentsPerSecond, int maxTrackedCasters) {
        this(
                maxCastIntentsPerSecond,
                maxTrackedCasters,
                DEFAULT_MAX_CHANNEL_SESSIONS,
                DEFAULT_MAX_SCHEDULED_EFFECTS,
                DEFAULT_EFFECT_WORK_BUDGET_PER_TICK);
    }

    public ArcanaServerRuntime(int maxCastIntentsPerSecond, int maxTrackedCasters, int maxChannelSessions) {
        this(
                maxCastIntentsPerSecond,
                maxTrackedCasters,
                maxChannelSessions,
                DEFAULT_MAX_SCHEDULED_EFFECTS,
                DEFAULT_EFFECT_WORK_BUDGET_PER_TICK);
    }

    public ArcanaServerRuntime(
            int maxCastIntentsPerSecond,
            int maxTrackedCasters,
            int maxChannelSessions,
            int maxScheduledEffects,
            int effectWorkBudgetPerTick
    ) {
        IngressRateLimiter limiter = new IngressRateLimiter(maxCastIntentsPerSecond, 20L, maxTrackedCasters);
        this.ingress = new ArcanaCastIngressService(spells, limiter, engines::get);
        this.channels = new ArcanaChannelManager(maxChannelSessions);
        this.channelCasts = new ArcanaChannelCastCoordinator(spells, loadouts, channels, engines::get);
        this.effectScheduler = new BoundedWorkScheduler(
                maxScheduledEffects,
                effectWorkBudgetPerTick,
                failure -> BlackArcanaMod.LOGGER.error("Scheduled Black Arcana effect failed and was dropped", failure));
    }

    public static ArcanaServerRuntime createDefault() {
        return new ArcanaServerRuntime(
                DEFAULT_MAX_CAST_INTENTS_PER_SECOND,
                DEFAULT_MAX_TRACKED_CASTERS,
                DEFAULT_MAX_CHANNEL_SESSIONS,
                DEFAULT_MAX_SCHEDULED_EFFECTS,
                DEFAULT_EFFECT_WORK_BUDGET_PER_TICK);
    }

    public CastResultPayload handle(ArcanaCastContext context, CastIntentPayload intent) {
        return ingress.handle(context, intent);
    }

    public ArcanaDecision beginChannel(
            ArcanaCastContext context,
            CastIntentPayload intent,
            ArcanaChannelSpec spec
    ) {
        return channelCasts.begin(context, intent, spec);
    }

    public ArcanaCastResult releaseChannel(
            ArcanaCastContext context,
            ArcanaCastId castId,
            String targetHint
    ) {
        return channelCasts.release(context, castId, targetHint);
    }

    public boolean cancelChannel(ArcanaCastContext context, ArcanaCastId castId) {
        return channelCasts.cancel(context, castId);
    }

    /** Runs bounded follow-up effect work and removes abandoned expired channels. */
    public RuntimeTickResult tick(long serverTick) {
        int expiredChannels = channels.pruneExpired(serverTick);
        BoundedWorkScheduler.TickResult work = effectScheduler.tick();
        return new RuntimeTickResult(expiredChannels, work);
    }

    public void installEngine(ArcanaSpellId spellId, ArcanaCastEngine engine) {
        engines.put(Objects.requireNonNull(spellId, "spellId"), Objects.requireNonNull(engine, "engine"));
    }

    public void removeEngine(ArcanaSpellId spellId) {
        engines.remove(Objects.requireNonNull(spellId, "spellId"));
    }

    /** Initializers register rename tables before SavedData restoration. */
    public void setRuntimeGroupMigrations(RuntimeGroupMigrations migrations) {
        this.groupMigrations = Objects.requireNonNull(migrations, "migrations");
    }

    /** Applies configured renames to restored state before removed-group pruning. */
    public MigrationResult migrateRestoredPersistentState() {
        int cooldownsRenamed = cooldowns.migrateGroups(groupMigrations);
        int chargesRenamed = charges.migrateGroups(groupMigrations);
        return new MigrationResult(cooldownsRenamed, chargesRenamed);
    }

    /**
     * Prunes restored cooldown/charge state after all server initializers have
     * installed the canonical policies for this runtime and migrations ran.
     */
    public PruneResult pruneOrphanedPersistentState() {
        Set<String> activeCooldownGroups = new HashSet<>();
        cooldownPolicies.cooldownSnapshot().values().forEach(spec -> {
            if (spec.durationTicks() > 0L && spec.persistent()) activeCooldownGroups.add(spec.groupId());
        });

        Set<String> activeChargeGroups = new HashSet<>();
        cooldownPolicies.chargeSnapshot().values().forEach(spec -> {
            if (spec.persistent()) activeChargeGroups.add(spec.groupId());
        });

        int cooldownsRemoved = cooldowns.pruneGroups(activeCooldownGroups);
        int chargesRemoved = charges.pruneGroups(activeChargeGroups);
        return new PruneResult(cooldownsRemoved, chargesRemoved);
    }

    public ArcanaSpellRegistry spells() {
        return spells;
    }

    public SpellDataCatalog spellData() {
        return spellData;
    }

    public LoadoutRegistry loadouts() {
        return loadouts;
    }

    public ArcanaCooldownPolicyRegistry cooldownPolicies() {
        return cooldownPolicies;
    }

    public PersistentCooldownService cooldowns() {
        return cooldowns;
    }

    public ChargePoolCooldownService charges() {
        return charges;
    }

    public ArcanaChannelManager channels() {
        return channels;
    }

    public BoundedWorkScheduler effectScheduler() {
        return effectScheduler;
    }

    public int installedEngineCount() {
        return engines.size();
    }

    public record RuntimeTickResult(int expiredChannels, BoundedWorkScheduler.TickResult scheduledWork) {
        public RuntimeTickResult {
            if (expiredChannels < 0) throw new IllegalArgumentException("expiredChannels cannot be negative");
            Objects.requireNonNull(scheduledWork, "scheduledWork");
        }
    }

    public record MigrationResult(int cooldownsRenamed, int chargePoolsRenamed) {
        public MigrationResult {
            if (cooldownsRenamed < 0 || chargePoolsRenamed < 0) {
                throw new IllegalArgumentException("migration counts cannot be negative");
            }
        }
    }

    public record PruneResult(int cooldownsRemoved, int chargePoolsRemoved) {
        public PruneResult {
            if (cooldownsRemoved < 0 || chargePoolsRemoved < 0) {
                throw new IllegalArgumentException("prune counts cannot be negative");
            }
        }
    }
}
