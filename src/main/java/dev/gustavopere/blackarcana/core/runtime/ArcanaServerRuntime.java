package dev.gustavopere.blackarcana.core.runtime;

import dev.gustavopere.blackarcana.api.ArcanaCastContext;
import dev.gustavopere.blackarcana.api.ArcanaCastEngine;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.core.cast.ArcanaCastIngressService;
import dev.gustavopere.blackarcana.core.cast.LoadoutRegistry;
import dev.gustavopere.blackarcana.core.cooldown.ArcanaCooldownPolicyRegistry;
import dev.gustavopere.blackarcana.core.cooldown.ChargePoolCooldownService;
import dev.gustavopere.blackarcana.core.cooldown.PersistentCooldownService;
import dev.gustavopere.blackarcana.core.registry.ArcanaSpellRegistry;
import dev.gustavopere.blackarcana.network.CastIntentPayload;
import dev.gustavopere.blackarcana.network.CastResultPayload;
import dev.gustavopere.blackarcana.network.IngressRateLimiter;

import java.util.Map;
import java.util.Objects;
import java.util.concurrent.ConcurrentHashMap;

/**
 * Runtime state owned by one Minecraft server instance. Optional-mod adapters
 * install engines into this object; no runtime state is shared across servers.
 */
public final class ArcanaServerRuntime {
    public static final int DEFAULT_MAX_CAST_INTENTS_PER_SECOND = 12;
    public static final int DEFAULT_MAX_TRACKED_CASTERS = 4096;

    private final ArcanaSpellRegistry spells = new ArcanaSpellRegistry();
    private final LoadoutRegistry loadouts = new LoadoutRegistry();
    private final ArcanaCooldownPolicyRegistry cooldownPolicies = new ArcanaCooldownPolicyRegistry();
    private final PersistentCooldownService cooldowns = new PersistentCooldownService(cooldownPolicies::cooldownFor);
    private final ChargePoolCooldownService charges = new ChargePoolCooldownService(cooldownPolicies::requireCharge);
    private final Map<ArcanaSpellId, ArcanaCastEngine> engines = new ConcurrentHashMap<>();
    private final ArcanaCastIngressService ingress;

    public ArcanaServerRuntime(int maxCastIntentsPerSecond, int maxTrackedCasters) {
        IngressRateLimiter limiter = new IngressRateLimiter(maxCastIntentsPerSecond, 20L, maxTrackedCasters);
        this.ingress = new ArcanaCastIngressService(spells, limiter, engines::get);
    }

    public static ArcanaServerRuntime createDefault() {
        return new ArcanaServerRuntime(DEFAULT_MAX_CAST_INTENTS_PER_SECOND, DEFAULT_MAX_TRACKED_CASTERS);
    }

    public CastResultPayload handle(ArcanaCastContext context, CastIntentPayload intent) {
        return ingress.handle(context, intent);
    }

    public void installEngine(ArcanaSpellId spellId, ArcanaCastEngine engine) {
        engines.put(Objects.requireNonNull(spellId, "spellId"), Objects.requireNonNull(engine, "engine"));
    }

    public void removeEngine(ArcanaSpellId spellId) {
        engines.remove(Objects.requireNonNull(spellId, "spellId"));
    }

    public ArcanaSpellRegistry spells() {
        return spells;
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

    public int installedEngineCount() {
        return engines.size();
    }
}
