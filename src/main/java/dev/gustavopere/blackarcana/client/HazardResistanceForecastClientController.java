package dev.gustavopere.blackarcana.client;

import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.network.ArcanaProtocol;
import dev.gustavopere.blackarcana.network.ClientArcanaSyncState;
import dev.gustavopere.blackarcana.network.HazardResistanceForecastRequestPayload;
import dev.gustavopere.blackarcana.network.neoforge.HazardResistanceForecastNetworkBridge;
import net.minecraft.client.Minecraft;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.client.event.ClientTickEvent;

import java.util.List;
import java.util.Objects;

/** Refreshes the selected-spell forecast only while the contextual HUD can actually display it. */
public final class HazardResistanceForecastClientController {
    private static final long REFRESH_INTERVAL_TICKS = 20L;
    private static ArcanaSpellId lastRequestedSpell;
    private static long lastRequestTick = Long.MIN_VALUE;
    private static long nextRequestId;

    private HazardResistanceForecastClientController() { }

    public static void register(IEventBus gameBus) {
        Objects.requireNonNull(gameBus, "gameBus").addListener(HazardResistanceForecastClientController::onClientTick);
    }

    private static void onClientTick(ClientTickEvent.Post event) {
        Minecraft minecraft = Minecraft.getInstance();
        if (minecraft.player == null || minecraft.getConnection() == null) {
            reset();
            return;
        }
        long now = minecraft.player.tickCount;
        if (!HudLayout.isRecent(
            now,
            ClientUxState.selectionChangedTick(),
            BlackArcanaClientConfig.SELECTION_DURATION_TICKS.get())) {
            return;
        }
        List<ArcanaSpellId> loadout = ClientArcanaSyncState.loadoutSnapshot();
        ArcanaSpellId selected = ClientInputController.selection().selected(loadout).orElse(null);
        if (selected == null) return;

        boolean changed = !selected.equals(lastRequestedSpell);
        boolean refreshDue = lastRequestTick == Long.MIN_VALUE || now - lastRequestTick >= REFRESH_INTERVAL_TICKS;
        if (!changed && !refreshDue) return;

        long requestId = nextRequestId++;
        HazardResistanceForecastNetworkBridge.request(new HazardResistanceForecastRequestPayload(
            ArcanaProtocol.VERSION,
            requestId,
            selected.canonical()));
        lastRequestedSpell = selected;
        lastRequestTick = now;
    }

    private static void reset() {
        lastRequestedSpell = null;
        lastRequestTick = Long.MIN_VALUE;
        nextRequestId = 0L;
    }
}
