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
import dev.gustavopere.blackarcana.core.hazard.ArcaneStrainStateService;
import dev.gustavopere.blackarcana.core.hazard.CorruptionStateService;
import dev.gustavopere.blackarcana.core.integration.ArcanaIntegrationRegistry;
import dev.gustavopere.blackarcana.core.registry.ArcanaSpellRegistry;
import dev.gustavopere.blackarcana.core.registry.SpellDataCatalog;
import dev.gustavopere.blackarcana.core.world.ConfigurableWorldEffectPolicy;
import dev.gustavopere.blackarcana.core.world.DefaultEntityInteractionPolicy;
import dev.gustavopere.blackarcana.core.world.EntityInteractionAdmissionService;
import dev.gustavopere.blackarcana.core.world.LoadedChunkGuard;
import dev.gustavopere.blackarcana.core.world.ProtectedDestinationGuard;
import dev.gustavopere.blackarcana.core.world.ProtectionAdapterRegistry;
import dev.gustavopere.blackarcana.core.world.TemporaryBlockBackend;
import dev.gustavopere.blackarcana.core.world.TemporaryBlockMutationGateway;
import dev.gustavopere.blackarcana.core.world.TemporaryMutationTracker;
import dev.gustavopere.blackarcana.core.world.TemporaryRestorationService;
import dev.gustavopere.blackarcana.core.world.WorldEffectAdmissionService;
import dev.gustavopere.blackarcana.core.world.WorldEffectBudgetLedger;
import dev.gustavopere.blackarcana.core.world.WorldEffectPolicyConfig;
import dev.gustavopere.blackarcana.core.world.WorldEffectProfileRegistry;
import dev.gustavopere.blackarcana.network.CastIntentPayload;
import dev.gustavopere.blackarcana.network.CastResultPayload;
import dev.gustavopere.blackarcana.network.IngressRateLimiter;

import java.util.HashSet;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;

/** Runtime state owned by one Minecraft server instance. */
public final class ArcanaServerRuntime {
    public static final int DEFAULT_MAX_CAST_INTENTS_PER_SECOND = 12;
    public static final int DEFAULT_MAX_TRACKED_CASTERS = 4096;
    public static final int DEFAULT_MAX_TRACKED_HAZARD_PLAYERS = 16_384;
    public static final int DEFAULT_MAX_CHANNEL_SESSIONS = 4096;
    public static final int DEFAULT_MAX_SCHEDULED_EFFECTS = 2048;
    public static final int DEFAULT_EFFECT_WORK_BUDGET_PER_TICK = 128;
    public static final int DEFAULT_MAX_TRACKED_WORLD_CASTS = 4096;
    public static final int DEFAULT_WORLD_UNITS_PER_CAST = 4096;
    public static final long DEFAULT_WORLD_CAST_IDLE_TICKS = 20L * 60L;
    public static final int DEFAULT_MAX_TEMPORARY_MUTATIONS = 16_384;
    public static final int DEFAULT_MAX_PROTECTION_ADAPTERS = 16;
    public static final int DEFAULT_MAX_WORLD_CHUNKS_PER_EFFECT = 64;
    public static final int DEFAULT_TEMPORARY_RESTORE_CHECKS_PER_TICK = 128;
    public static final long DEFAULT_MAX_TEMPORARY_MUTATION_LIFETIME_TICKS =
        TemporaryBlockMutationGateway.ABSOLUTE_MAX_LIFETIME_TICKS;

    private final ArcanaSpellRegistry spells = new ArcanaSpellRegistry();
    private final SpellDataCatalog spellData = new SpellDataCatalog();
    private final LoadoutRegistry loadouts = new LoadoutRegistry();
    private final ArcanaCooldownPolicyRegistry cooldownPolicies = new ArcanaCooldownPolicyRegistry();
    private final PersistentCooldownService cooldowns = new PersistentCooldownService(cooldownPolicies::cooldownFor);
    private final ChargePoolCooldownService charges = new ChargePoolCooldownService(cooldownPolicies::requireCharge);
    private final ArcanaIntegrationRegistry integrations = new ArcanaIntegrationRegistry();
    private final CorruptionStateService corruption = CorruptionStateService.canonical(DEFAULT_MAX_TRACKED_HAZARD_PLAYERS);
    private final ArcaneStrainStateService strain = ArcaneStrainStateService.canonical(DEFAULT_MAX_TRACKED_HAZARD_PLAYERS);
    private final WorldEffectProfileRegistry worldEffectProfiles = new WorldEffectProfileRegistry();
    private final ConfigurableWorldEffectPolicy worldEffectPolicy =
        new ConfigurableWorldEffectPolicy(worldEffectProfiles, WorldEffectPolicyConfig.safeDefaults());
    private final WorldEffectBudgetLedger worldEffectBudgets = new WorldEffectBudgetLedger(
        DEFAULT_MAX_TRACKED_WORLD_CASTS, DEFAULT_WORLD_UNITS_PER_CAST, DEFAULT_WORLD_CAST_IDLE_TICKS);
    private final TemporaryMutationTracker temporaryMutations = new TemporaryMutationTracker(DEFAULT_MAX_TEMPORARY_MUTATIONS);
    private final DefaultEntityInteractionPolicy entityInteractionPolicy = DefaultEntityInteractionPolicy.safeDefaults();
    private final ProtectionAdapterRegistry protectionAdapters = new ProtectionAdapterRegistry(DEFAULT_MAX_PROTECTION_ADAPTERS);
    private final EntityInteractionAdmissionService entityInteractionAdmission =
        new EntityInteractionAdmissionService(entityInteractionPolicy, protectionAdapters);
    private final Map<ArcanaSpellId, ArcanaCastEngine> engines = new ConcurrentHashMap<>();
    private final ArcanaCastIngressService ingress;
    private final ArcanaChannelManager channels;
    private final ArcanaChannelCastCoordinator channelCasts;
    private final BoundedWorkScheduler effectScheduler;
    private volatile TemporaryBlockMutationGateway temporaryBlockGateway;
    private volatile TemporaryRestorationService temporaryRestorationService;
    private volatile ProtectedDestinationGuard protectedDestinationGuard;
    private volatile TemporaryRestorationService.TickResult lastTemporaryRestoration =
        new TemporaryRestorationService.TickResult(0, 0, 0, 0);
    private RuntimeGroupMigrations groupMigrations = RuntimeGroupMigrations.none();

    public ArcanaServerRuntime(int maxCastIntentsPerSecond, int maxTrackedCasters) {
        this(maxCastIntentsPerSecond, maxTrackedCasters, DEFAULT_MAX_CHANNEL_SESSIONS,
            DEFAULT_MAX_SCHEDULED_EFFECTS, DEFAULT_EFFECT_WORK_BUDGET_PER_TICK);
    }

    public ArcanaServerRuntime(int maxCastIntentsPerSecond, int maxTrackedCasters, int maxChannelSessions) {
        this(maxCastIntentsPerSecond, maxTrackedCasters, maxChannelSessions,
            DEFAULT_MAX_SCHEDULED_EFFECTS, DEFAULT_EFFECT_WORK_BUDGET_PER_TICK);
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

    public CastResultPayload handle(ArcanaCastContext context, CastIntentPayload intent) { return ingress.handle(context, intent); }
    public ArcanaDecision beginChannel(ArcanaCastContext context, CastIntentPayload intent, ArcanaChannelSpec spec) {
        return channelCasts.begin(context, intent, spec);
    }
    public ArcanaCastResult releaseChannel(ArcanaCastContext context, ArcanaCastId castId, String targetHint) {
        return channelCasts.release(context, castId, targetHint);
    }
    public boolean cancelChannel(ArcanaCastContext context, ArcanaCastId castId) { return channelCasts.cancel(context, castId); }

    public RuntimeTickResult tick(long serverTick) {
        int expiredChannels = channels.pruneExpired(serverTick);
        BoundedWorkScheduler.TickResult work = effectScheduler.tick();
        worldEffectBudgets.pruneIdle(serverTick);
        TemporaryRestorationService restoration = temporaryRestorationService;
        if (restoration != null) {
            lastTemporaryRestoration = restoration.tick(serverTick, DEFAULT_TEMPORARY_RESTORE_CHECKS_PER_TICK);
        }
        return new RuntimeTickResult(expiredChannels, work);
    }

    public synchronized void installWorldBackend(TemporaryBlockBackend backend, LoadedChunkGuard.LoadedChunkProbe loadedChunkProbe) {
        Objects.requireNonNull(backend, "backend");
        Objects.requireNonNull(loadedChunkProbe, "loadedChunkProbe");
        if (temporaryBlockGateway != null || temporaryRestorationService != null || protectedDestinationGuard != null) {
            throw new IllegalStateException("world backend already installed");
        }
        LoadedChunkGuard chunkGuard = new LoadedChunkGuard(DEFAULT_MAX_WORLD_CHUNKS_PER_EFFECT, loadedChunkProbe);
        WorldEffectAdmissionService admission = new WorldEffectAdmissionService(worldEffectPolicy, chunkGuard, worldEffectBudgets);
        temporaryBlockGateway = new TemporaryBlockMutationGateway(
            admission, temporaryMutations, backend, DEFAULT_MAX_TEMPORARY_MUTATION_LIFETIME_TICKS);
        temporaryRestorationService = new TemporaryRestorationService(temporaryMutations, backend);
        protectedDestinationGuard = new ProtectedDestinationGuard(chunkGuard, protectionAdapters);
    }

    public void installEngine(ArcanaSpellId spellId, ArcanaCastEngine engine) {
        engines.put(Objects.requireNonNull(spellId, "spellId"), Objects.requireNonNull(engine, "engine"));
    }
    public void removeEngine(ArcanaSpellId spellId) { engines.remove(Objects.requireNonNull(spellId, "spellId")); }
    public void configureWorldEffects(WorldEffectPolicyConfig config) { worldEffectPolicy.updateConfig(Objects.requireNonNull(config, "config")); }
    public void setRuntimeGroupMigrations(RuntimeGroupMigrations migrations) { this.groupMigrations = Objects.requireNonNull(migrations, "migrations"); }

    public MigrationResult migrateRestoredPersistentState() {
        return new MigrationResult(cooldowns.migrateGroups(groupMigrations), charges.migrateGroups(groupMigrations));
    }

    public PruneResult pruneOrphanedPersistentState() {
        Set<String> activeCooldownGroups = new HashSet<>();
        cooldownPolicies.cooldownSnapshot().values().forEach(spec -> {
            if (spec.durationTicks() > 0L && spec.persistent()) activeCooldownGroups.add(spec.groupId());
        });
        Set<String> activeChargeGroups = new HashSet<>();
        cooldownPolicies.chargeSnapshot().values().forEach(spec -> {
            if (spec.persistent()) activeChargeGroups.add(spec.groupId());
        });
        return new PruneResult(cooldowns.pruneGroups(activeCooldownGroups), charges.pruneGroups(activeChargeGroups));
    }

    public ArcanaSpellRegistry spells() { return spells; }
    public SpellDataCatalog spellData() { return spellData; }
    public LoadoutRegistry loadouts() { return loadouts; }
    public ArcanaCooldownPolicyRegistry cooldownPolicies() { return cooldownPolicies; }
    public PersistentCooldownService cooldowns() { return cooldowns; }
    public ChargePoolCooldownService charges() { return charges; }
    public ArcanaChannelManager channels() { return channels; }
    public BoundedWorkScheduler effectScheduler() { return effectScheduler; }
    public ArcanaIntegrationRegistry integrations() { return integrations; }
    public CorruptionStateService corruption() { return corruption; }
    public ArcaneStrainStateService strain() { return strain; }
    public WorldEffectProfileRegistry worldEffectProfiles() { return worldEffectProfiles; }
    public ConfigurableWorldEffectPolicy worldEffectPolicy() { return worldEffectPolicy; }
    public WorldEffectBudgetLedger worldEffectBudgets() { return worldEffectBudgets; }
    public TemporaryMutationTracker temporaryMutations() { return temporaryMutations; }
    public Optional<TemporaryBlockMutationGateway> temporaryBlockGateway() { return Optional.ofNullable(temporaryBlockGateway); }
    public Optional<ProtectedDestinationGuard> protectedDestinationGuard() { return Optional.ofNullable(protectedDestinationGuard); }
    public TemporaryRestorationService.TickResult lastTemporaryRestoration() { return lastTemporaryRestoration; }
    public DefaultEntityInteractionPolicy entityInteractionPolicy() { return entityInteractionPolicy; }
    public EntityInteractionAdmissionService entityInteractionAdmission() { return entityInteractionAdmission; }
    public ProtectionAdapterRegistry protectionAdapters() { return protectionAdapters; }
    public int installedEngineCount() { return engines.size(); }

    public record RuntimeTickResult(int expiredChannels, BoundedWorkScheduler.TickResult scheduledWork) {
        public RuntimeTickResult {
            if (expiredChannels < 0) throw new IllegalArgumentException("expiredChannels cannot be negative");
            Objects.requireNonNull(scheduledWork, "scheduledWork");
        }
    }
    public record MigrationResult(int cooldownsRenamed, int chargePoolsRenamed) {
        public MigrationResult {
            if (cooldownsRenamed < 0 || chargePoolsRenamed < 0) throw new IllegalArgumentException("migration counts cannot be negative");
        }
    }
    public record PruneResult(int cooldownsRemoved, int chargePoolsRemoved) {
        public PruneResult {
            if (cooldownsRemoved < 0 || chargePoolsRemoved < 0) throw new IllegalArgumentException("prune counts cannot be negative");
        }
    }
}
