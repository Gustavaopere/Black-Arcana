package dev.gustavopere.blackarcana.network.neoforge;

import dev.gustavopere.blackarcana.api.ArcanaCastContext;
import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaGatePreflight;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDangerProfile;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceQuery;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceSnapshot;
import dev.gustavopere.blackarcana.core.hazard.ArcaneDangerProfileRuntimeStore;
import dev.gustavopere.blackarcana.core.hazard.ArcaneResistancePreviewRuntimeStore;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntimeManager;
import dev.gustavopere.blackarcana.network.ArcanaProtocol;
import dev.gustavopere.blackarcana.network.HazardResistanceForecastPayload;
import dev.gustavopere.blackarcana.network.HazardResistanceForecastRequestPayload;
import dev.gustavopere.blackarcana.network.IngressRateLimiter;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerPlayer;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.event.server.ServerStoppedEvent;

import java.util.Collections;
import java.util.IdentityHashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;

/** Server-side read-only projection. It never opens a hazard session or reserves gameplay state. */
public final class HazardResistanceForecastService {
    private static final int MAX_REQUESTS_PER_SECOND = 4;
    private static final int MAX_TRACKED_PLAYERS = 4_096;
    private static final Map<MinecraftServer, IngressRateLimiter> LIMITERS =
        Collections.synchronizedMap(new IdentityHashMap<>());

    private HazardResistanceForecastService() { }

    public static void register(IEventBus gameBus) {
        Objects.requireNonNull(gameBus, "gameBus").addListener(HazardResistanceForecastService::onServerStopped);
    }

    public static HazardResistanceForecastPayload handle(
        ServerPlayer player,
        HazardResistanceForecastRequestPayload request
    ) {
        Objects.requireNonNull(player, "player");
        Objects.requireNonNull(request, "request");
        MinecraftServer server = player.serverLevel().getServer();
        long now = player.level().getGameTime();
        ArcanaDecision admitted = limiter(server).claim(player.getUUID(), now);
        if (!admitted.allowed()) return unavailable(request, ArcaneDangerProfile.normal());

        Optional<ArcanaServerRuntime> runtimeOptional = ArcanaServerRuntimeManager.get(server);
        if (runtimeOptional.isEmpty()) return unavailable(request, ArcaneDangerProfile.normal());
        ArcanaServerRuntime runtime = runtimeOptional.orElseThrow();
        ArcanaSpellId spellId = request.parsedSpellId();
        ArcaneDangerProfile profile = ArcaneDangerProfileRuntimeStore.forRuntime(runtime)
            .resolve(spellId)
            .orElse(ArcaneDangerProfile.normal());

        try {
            ArcanaCastContext castContext = ServerPlayerArcanaContext.from(player);
            Optional<ArcanaCastRequest> gateRequest = previewRequest(runtime, spellId, castContext);
            if (gateRequest.isEmpty()) return unavailable(request, profile);
            Optional<ArcanaGatePreflight> gatePreview = runtime.previewReadOnlyGates(gateRequest.orElseThrow());
            if (gatePreview.isEmpty()) return unavailable(request, profile);

            ArcaneResistanceQuery query = new ArcaneResistanceQuery(
                ArcanaCastId.random(),
                spellId,
                player.getUUID(),
                player.level().dimension().location().toString(),
                now,
                profile);
            Optional<ArcaneResistanceSnapshot> preview =
                ArcaneResistancePreviewRuntimeStore.snapshotIfComplete(runtime, query);
            if (preview.isEmpty()) return unavailable(request, profile);
            double effective = preview.orElseThrow().effectiveResistance();
            return available(request, profile, effective, gateStatus(gatePreview.orElseThrow()));
        } catch (RuntimeException | LinkageError failure) {
            return unavailable(request, profile);
        }
    }

    static Optional<ArcanaCastRequest> previewRequest(
        ArcanaServerRuntime runtime,
        ArcanaSpellId spellId,
        ArcanaCastContext context
    ) {
        Objects.requireNonNull(runtime, "runtime");
        Objects.requireNonNull(spellId, "spellId");
        Objects.requireNonNull(context, "context");
        var definition = runtime.spells().resolve(spellId);
        if (definition.isEmpty()) return Optional.empty();

        List<ArcanaSpellId> loadout = runtime.loadouts().getLoadout(context.casterId());
        int loadoutSlot = loadout.indexOf(spellId);
        if (loadoutSlot < 0) {
            // Slot zero is a valid bounded request value. The canonical identity validator
            // remains responsible for the actual missing/mismatch denial.
            loadoutSlot = 0;
        }
        return Optional.of(new ArcanaCastRequest(
            ArcanaCastId.random(),
            definition.orElseThrow(),
            context,
            loadoutSlot,
            "",
            0L));
    }

    static HazardResistanceForecastPayload.GateStatus gateStatus(ArcanaGatePreflight preflight) {
        Objects.requireNonNull(preflight, "preflight");
        return switch (preflight.gate()) {
            case CLEAR -> HazardResistanceForecastPayload.GateStatus.CLEAR;
            case IDENTITY -> HazardResistanceForecastPayload.GateStatus.IDENTITY;
            case PROGRESSION -> HazardResistanceForecastPayload.GateStatus.PROGRESSION;
            case COOLDOWN -> HazardResistanceForecastPayload.GateStatus.COOLDOWN;
            case COST -> HazardResistanceForecastPayload.GateStatus.COST;
        };
    }

    private static HazardResistanceForecastPayload available(
        HazardResistanceForecastRequestPayload request,
        ArcaneDangerProfile profile,
        double effective,
        HazardResistanceForecastPayload.GateStatus gateStatus
    ) {
        HazardResistanceForecastPayload.Status status;
        if (!profile.requiresHazardSession()) {
            status = HazardResistanceForecastPayload.Status.NORMAL;
        } else if (effective < profile.minimumArcaneResistance()) {
            status = HazardResistanceForecastPayload.Status.BELOW_MINIMUM;
        } else if (effective < profile.recommendedArcaneResistance()) {
            status = HazardResistanceForecastPayload.Status.BELOW_RECOMMENDED;
        } else {
            status = HazardResistanceForecastPayload.Status.RECOMMENDED;
        }
        return new HazardResistanceForecastPayload(
            ArcanaProtocol.VERSION,
            request.requestId(),
            request.spellId(),
            true,
            status.name(),
            profile.tier().name(),
            effective,
            profile.minimumArcaneResistance(),
            profile.recommendedArcaneResistance(),
            true,
            Objects.requireNonNull(gateStatus, "gateStatus").name());
    }

    private static HazardResistanceForecastPayload unavailable(
        HazardResistanceForecastRequestPayload request,
        ArcaneDangerProfile profile
    ) {
        return new HazardResistanceForecastPayload(
            ArcanaProtocol.VERSION,
            request.requestId(),
            request.spellId(),
            false,
            HazardResistanceForecastPayload.Status.UNAVAILABLE.name(),
            profile.tier().name(),
            0.0D,
            profile.minimumArcaneResistance(),
            profile.recommendedArcaneResistance(),
            false,
            HazardResistanceForecastPayload.GateStatus.UNAVAILABLE.name());
    }

    private static IngressRateLimiter limiter(MinecraftServer server) {
        synchronized (LIMITERS) {
            return LIMITERS.computeIfAbsent(
                Objects.requireNonNull(server, "server"),
                ignored -> new IngressRateLimiter(MAX_REQUESTS_PER_SECOND, 20L, MAX_TRACKED_PLAYERS));
        }
    }

    private static void onServerStopped(ServerStoppedEvent event) {
        synchronized (LIMITERS) {
            LIMITERS.remove(event.getServer());
        }
    }
}
