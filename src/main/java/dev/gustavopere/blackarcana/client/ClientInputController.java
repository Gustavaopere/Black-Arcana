package dev.gustavopere.blackarcana.client;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.api.ArcanaTargetReference;
import dev.gustavopere.blackarcana.network.ArcanaProtocol;
import dev.gustavopere.blackarcana.network.CastIntentPayload;
import dev.gustavopere.blackarcana.network.ChannelBeginIntentPayload;
import dev.gustavopere.blackarcana.network.ChannelReleaseIntentPayload;
import dev.gustavopere.blackarcana.network.ClientArcanaSyncState;
import dev.gustavopere.blackarcana.network.neoforge.ArcanaNetworkBridge;
import dev.gustavopere.blackarcana.network.neoforge.ChannelNetworkBridge;
import net.minecraft.client.Minecraft;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.EntityHitResult;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.client.event.ClientTickEvent;

import java.util.List;
import java.util.Objects;

/** Physical-client input adapter. It emits intent only; all gameplay validation remains server-side. */
public final class ClientInputController {
    private static final int CAST_SELECTED_INPUT_ID = 0;
    private static final int QUICK_CAST_INPUT_ID_BASE = 1;
    private static final ClientLoadoutSelection SELECTION = new ClientLoadoutSelection();
    private static final ClientChannelInvocationState CHANNELS = new ClientChannelInvocationState();
    private static volatile Runnable radialOpener = () -> { };
    private static volatile Runnable loadoutEditorOpener = () -> { };
    private static ResourceKey<Level> presentationDimension;

    private ClientInputController() { }

    public static void register(IEventBus gameBus) {
        Objects.requireNonNull(gameBus, "gameBus").addListener(ClientInputController::onClientTick);
    }

    public static void installRadialOpener(Runnable opener) {
        radialOpener = Objects.requireNonNull(opener, "opener");
    }

    public static void installLoadoutEditorOpener(Runnable opener) {
        loadoutEditorOpener = Objects.requireNonNull(opener, "opener");
    }

    public static ClientLoadoutSelection selection() {
        return SELECTION;
    }

    /**
     * Executes an immediate cast from a non-held caller. Server-advertised channel spells require
     * a physical input source so their exact BEGIN can later be paired with RELEASE.
     */
    public static boolean castSlot(int slot) {
        Minecraft minecraft = Minecraft.getInstance();
        if (minecraft.player == null || minecraft.getConnection() == null || minecraft.screen != null) return false;
        List<ArcanaSpellId> loadout = ClientArcanaSyncState.loadoutSnapshot();
        if (!SELECTION.select(slot, loadout)) return false;
        ClientUxState.markSelectionChanged();
        ArcanaSpellId spell = loadout.get(slot);
        if (ClientArcanaSyncState.channelCapability(spell).isPresent()) return false;
        sendImmediateCast(minecraft, slot, spell);
        return true;
    }

    private static void sendImmediateCast(Minecraft minecraft, int slot, ArcanaSpellId spell) {
        ArcanaCastId castId = ArcanaCastId.random();
        CastPresentationClientRuntime.recordLocalIntent(castId, spell, minecraft.player.tickCount);
        ArcanaNetworkBridge.sendCastIntent(new CastIntentPayload(
                ArcanaProtocol.VERSION,
                castId.canonical(),
                spell.canonical(),
                slot,
                currentTargetHint(minecraft)));
    }

    private static boolean castSlotFromInput(int slot, int inputId) {
        Minecraft minecraft = Minecraft.getInstance();
        if (minecraft.player == null || minecraft.getConnection() == null || minecraft.screen != null) return false;
        List<ArcanaSpellId> loadout = ClientArcanaSyncState.loadoutSnapshot();
        if (!SELECTION.select(slot, loadout)) return false;
        ClientUxState.markSelectionChanged();
        ArcanaSpellId spell = loadout.get(slot);

        if (ClientArcanaSyncState.channelCapability(spell).isPresent()) {
            ArcanaCastId castId = ArcanaCastId.random();
            if (!CHANNELS.begin(inputId, slot, spell, castId)) return false;
            ChannelNetworkBridge.requestBegin(new ChannelBeginIntentPayload(
                    ArcanaProtocol.VERSION,
                    castId.canonical(),
                    spell.canonical(),
                    slot));
            return true;
        }

        sendImmediateCast(minecraft, slot, spell);
        return true;
    }

    private static void processChannelBeginAcknowledgement() {
        ClientArcanaSyncState.lastChannelBeginResult().ifPresent(beginResult -> {
            if (!beginResult.accepted()) CHANNELS.rejectBegin(beginResult.parsedCastId());
        });
    }

    private static void processChannelRelease(Minecraft minecraft) {
        ClientChannelInvocationState.Active active = CHANNELS.active().orElse(null);
        if (active == null) return;
        if (inputStillDown(active.inputKey())) return;

        CHANNELS.releaseWhenUp(active.inputKey(), false).ifPresent(castId -> {
            CastPresentationClientRuntime.recordLocalIntent(castId, active.spellId(), minecraft.player.tickCount);
            ChannelNetworkBridge.requestRelease(new ChannelReleaseIntentPayload(
                    ArcanaProtocol.VERSION,
                    castId.canonical(),
                    currentTargetHint(minecraft)));
        });
    }

    private static boolean inputStillDown(int inputId) {
        if (inputId == CAST_SELECTED_INPUT_ID) return BlackArcanaKeyMappings.CAST_SELECTED.isDown();
        int quickIndex = inputId - QUICK_CAST_INPUT_ID_BASE;
        return quickIndex >= 0
                && quickIndex < BlackArcanaKeyMappings.QUICK_CAST.length
                && BlackArcanaKeyMappings.QUICK_CAST[quickIndex].isDown();
    }

    private static String currentTargetHint(Minecraft minecraft) {
        if (minecraft.hitResult instanceof EntityHitResult entityHit) {
            return new ArcanaTargetReference.EntityRef(entityHit.getEntity().getUUID()).canonical();
        }
        return "";
    }

    private static void onClientTick(ClientTickEvent.Post event) {
        Minecraft minecraft = Minecraft.getInstance();
        if (minecraft.player == null || minecraft.getConnection() == null) {
            presentationDimension = null;
            CHANNELS.cancel();
            ClientArcanaSyncState.clear();
            ClientUxState.clear();
            CastPresentationClientRuntime.clear();
            CastPresentationEffectsLayer.clear();
            DiscoverabilityClientRuntime.clearSession();
            return;
        }

        ResourceKey<Level> currentDimension = minecraft.player.level().dimension();
        boolean dimensionChanged = presentationDimension != null
                && !presentationDimension.equals(currentDimension);
        presentationDimension = currentDimension;
        if (!minecraft.player.isAlive() || dimensionChanged) {
            CastPresentationClientRuntime.clear();
            CastPresentationEffectsLayer.clear();
        } else if (minecraft.screen != null) {
            CastPresentationEffectsLayer.clear();
        }

        processChannelBeginAcknowledgement();
        processChannelRelease(minecraft);
        CastPresentationClientRuntime.tick(minecraft.player);
        List<ArcanaSpellId> loadout = ClientArcanaSyncState.loadoutSnapshot();
        SELECTION.reconcile(loadout);

        while (BlackArcanaKeyMappings.OPEN_RADIAL.consumeClick()) {
            if (minecraft.screen == null && !loadout.isEmpty()) {
                radialOpener.run();
            }
        }
        while (BlackArcanaKeyMappings.EDIT_LOADOUT.consumeClick()) {
            if (minecraft.screen == null) {
                loadoutEditorOpener.run();
            }
        }
        while (BlackArcanaKeyMappings.CAST_SELECTED.consumeClick()) {
            if (minecraft.screen == null) {
                castSlotFromInput(SELECTION.selectedSlot(), CAST_SELECTED_INPUT_ID);
            }
        }
        for (int index = 0; index < BlackArcanaKeyMappings.QUICK_CAST.length; index++) {
            while (BlackArcanaKeyMappings.QUICK_CAST[index].consumeClick()) {
                if (minecraft.screen == null) {
                    castSlotFromInput(index, QUICK_CAST_INPUT_ID_BASE + index);
                }
            }
        }
    }
}
