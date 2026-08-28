package dev.gustavopere.blackarcana.network;

import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import net.minecraft.world.entity.player.Player;

import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;
import java.util.UUID;

/**
 * Minimal client-view cache for network-confirmed Black Arcana state.
 *
 * This class deliberately uses no client-only Minecraft types, so it is safe to
 * package in the common jar. Server gameplay never reads this cache; Stage 05 UI
 * will consume immutable snapshots on the physical client.
 */
public final class ClientArcanaSyncState {
    private static UUID playerId;
    private static CastResultPayload lastResult;
    private static Map<String, Long> cooldowns = Map.of();
    private static Map<ArcanaSpellId, SpellPresentationPayload.Entry> presentation = Map.of();

    private ClientArcanaSyncState() { }

    public static synchronized void acceptResult(Player player, CastResultPayload payload) {
        ensurePlayer(player);
        lastResult = Objects.requireNonNull(payload, "payload");
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

    public static synchronized Optional<CastResultPayload> lastResult() {
        return Optional.ofNullable(lastResult);
    }

    public static synchronized Map<String, Long> cooldownSnapshot() {
        return cooldowns;
    }

    public static synchronized Map<ArcanaSpellId, SpellPresentationPayload.Entry> presentationSnapshot() {
        return presentation;
    }

    public static synchronized void clear() {
        playerId = null;
        lastResult = null;
        cooldowns = Map.of();
        presentation = Map.of();
    }

    private static void ensurePlayer(Player player) {
        Objects.requireNonNull(player, "player");
        UUID incoming = player.getUUID();
        if (playerId != null && !playerId.equals(incoming)) {
            lastResult = null;
            cooldowns = Map.of();
            presentation = Map.of();
        }
        playerId = incoming;
    }
}
