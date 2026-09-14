package dev.gustavopere.blackarcana.network;

import dev.gustavopere.blackarcana.api.ArcanaChannelSpec;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import net.minecraft.world.entity.player.Player;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;
import java.util.OptionalLong;
import java.util.UUID;
import java.util.function.BiConsumer;

/**
 * Minimal client-view cache for network-confirmed Black Arcana state.
 *
 * This class deliberately uses no client-only Minecraft types, so it is safe to
 * package in the common jar. Server gameplay never reads this cache; Stage 05 UI
 * consumes immutable snapshots on the physical client.
 */
public final class ClientArcanaSyncState {
    private static UUID playerId;
    private static CastResultPayload lastResult;
    private static long lastResultTick = Long.MIN_VALUE;
    private static Map<String, Long> cooldowns = Map.of();
    private static Map<ArcanaSpellId, SpellPresentationPayload.Entry> presentation = Map.of();
    private static Map<ArcanaSpellId, HazardPreflightPayload.Entry> hazardPreflight = Map.of();
    private static Map<ArcanaSpellId, ArcanaChannelSpec> channelCapabilities = Map.of();
    private static HazardResistanceForecastPayload hazardResistanceForecast;
    private static List<ArcanaSpellId> loadout = List.of();
    private static volatile BiConsumer<Player, CastResultPayload> resultObserver = (player, payload) -> { };
    private static volatile BiConsumer<Player, List<ArcanaSpellId>> loadoutObserver = (player, acceptedLoadout) -> { };

    private ClientArcanaSyncState() { }

    /**
     * Installs a common-safe observer for physical-client presentation. The observer receives only
     * the already validated authoritative result after this cache has accepted it.
     */
    public static void installResultObserver(BiConsumer<Player, CastResultPayload> observer) {
        resultObserver = Objects.requireNonNull(observer, "observer");
    }

    /**
     * Installs a common-safe observer for accepted loadout presentation. The observer receives an
     * immutable copy only after this cache has accepted the server-authored snapshot.
     */
    public static void installLoadoutObserver(BiConsumer<Player, List<ArcanaSpellId>> observer) {
        loadoutObserver = Objects.requireNonNull(observer, "observer");
    }

    public static void acceptResult(Player player, CastResultPayload payload) {
        Objects.requireNonNull(payload, "payload");
        synchronized (ClientArcanaSyncState.class) {
            ensurePlayer(player);
            lastResult = payload;
            lastResultTick = player.tickCount;
        }
        resultObserver.accept(player, payload);
    }

    public static synchronized void acceptCooldowns(Player player, CooldownSnapshotPayload payload) {
        ensurePlayer(player);
        Objects.requireNonNull(payload, "payload");
        Map<String, Long> next = new LinkedHashMap<>();
        for (CooldownSnapshotPayload.Entry entry : payload.entries()) {
            if (next.putIfAbsent(entry.groupId(), entry.remainingTicks()) != null) {
                throw new IllegalArgumentException("duplicate cooldown group in client snapshot: " + entry.groupId());
            }
        }
        cooldowns = Map.copyOf(next);
    }

    public static synchronized void acceptPresentation(Player player, SpellPresentationPayload payload) {
        ensurePlayer(player);
        Objects.requireNonNull(payload, "payload");
        Map<ArcanaSpellId, SpellPresentationPayload.Entry> next = new LinkedHashMap<>();
        for (SpellPresentationPayload.Entry entry : payload.entries()) {
            ArcanaSpellId id = ArcanaSpellId.parse(entry.spellId());
            if (next.putIfAbsent(id, entry) != null) {
                throw new IllegalArgumentException("duplicate spell presentation entry: " + id.canonical());
            }
        }
        presentation = Map.copyOf(next);
    }

    public static synchronized void acceptHazardPreflight(Player player, HazardPreflightPayload payload) {
        ensurePlayer(player);
        replaceHazardPreflight(payload);
    }

    static synchronized void replaceHazardPreflight(HazardPreflightPayload payload) {
        Objects.requireNonNull(payload, "payload");
        Map<ArcanaSpellId, HazardPreflightPayload.Entry> next = new LinkedHashMap<>();
        for (HazardPreflightPayload.Entry entry : payload.entries()) {
            ArcanaSpellId id = ArcanaSpellId.parse(entry.spellId());
            if (next.putIfAbsent(id, entry) != null) {
                throw new IllegalArgumentException("duplicate hazard preflight entry: " + id.canonical());
            }
        }
        hazardPreflight = Map.copyOf(next);
        // A datapack reload can change thresholds; never display a forecast from the previous revision.
        hazardResistanceForecast = null;
    }

    public static synchronized void acceptChannelCapabilities(Player player, ChannelCapabilityPayload payload) {
        ensurePlayer(player);
        replaceChannelCapabilities(payload);
    }

    static synchronized void replaceChannelCapabilities(ChannelCapabilityPayload payload) {
        Objects.requireNonNull(payload, "payload");
        Map<ArcanaSpellId, ArcanaChannelSpec> next = new LinkedHashMap<>();
        for (ChannelCapabilityPayload.Entry entry : payload.entries()) {
            ArcanaSpellId id = entry.parsedSpellId();
            if (next.putIfAbsent(id, entry.spec()) != null) {
                throw new IllegalArgumentException("duplicate channel capability entry: " + id.canonical());
            }
        }
        channelCapabilities = Map.copyOf(next);
    }

    public static synchronized void acceptHazardResistanceForecast(
        Player player,
        HazardResistanceForecastPayload payload
    ) {
        ensurePlayer(player);
        Objects.requireNonNull(payload, "payload");
        if (hazardResistanceForecast != null
            && payload.requestId() < hazardResistanceForecast.requestId()) {
            return;
        }
        hazardResistanceForecast = payload;
    }

    public static void acceptLoadout(Player player, LoadoutSnapshotPayload payload) {
        List<ArcanaSpellId> acceptedLoadout;
        synchronized (ClientArcanaSyncState.class) {
            ensurePlayer(player);
            acceptedLoadout = List.copyOf(Objects.requireNonNull(payload, "payload").parsedSpellIds());
            loadout = acceptedLoadout;
        }
        loadoutObserver.accept(player, acceptedLoadout);
    }

    public static synchronized Optional<CastResultPayload> lastResult() {
        return Optional.ofNullable(lastResult);
    }

    public static synchronized OptionalLong lastResultTick() {
        return lastResultTick == Long.MIN_VALUE ? OptionalLong.empty() : OptionalLong.of(lastResultTick);
    }

    public static synchronized Map<String, Long> cooldownSnapshot() {
        return cooldowns;
    }

    public static synchronized Map<ArcanaSpellId, SpellPresentationPayload.Entry> presentationSnapshot() {
        return presentation;
    }

    public static synchronized Map<ArcanaSpellId, HazardPreflightPayload.Entry> hazardPreflightSnapshot() {
        return hazardPreflight;
    }

    public static synchronized Optional<ArcanaChannelSpec> channelCapability(ArcanaSpellId spellId) {
        return Optional.ofNullable(channelCapabilities.get(Objects.requireNonNull(spellId, "spellId")));
    }

    public static synchronized Optional<HazardResistanceForecastPayload> hazardResistanceForecast(ArcanaSpellId spellId) {
        Objects.requireNonNull(spellId, "spellId");
        if (hazardResistanceForecast == null || !hazardResistanceForecast.parsedSpellId().equals(spellId)) {
            return Optional.empty();
        }
        return Optional.of(hazardResistanceForecast);
    }

    public static synchronized List<ArcanaSpellId> loadoutSnapshot() {
        return loadout;
    }

    public static synchronized void clear() {
        playerId = null;
        lastResult = null;
        lastResultTick = Long.MIN_VALUE;
        cooldowns = Map.of();
        presentation = Map.of();
        hazardPreflight = Map.of();
        channelCapabilities = Map.of();
        hazardResistanceForecast = null;
        loadout = List.of();
    }

    private static void ensurePlayer(Player player) {
        Objects.requireNonNull(player, "player");
        UUID incoming = player.getUUID();
        if (playerId != null && !playerId.equals(incoming)) {
            lastResult = null;
            lastResultTick = Long.MIN_VALUE;
            cooldowns = Map.of();
            presentation = Map.of();
            hazardPreflight = Map.of();
            channelCapabilities = Map.of();
            hazardResistanceForecast = null;
            loadout = List.of();
        }
        playerId = incoming;
    }
}
