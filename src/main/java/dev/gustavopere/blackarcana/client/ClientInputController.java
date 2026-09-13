package dev.gustavopere.blackarcana.client;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.api.ArcanaTargetReference;
import dev.gustavopere.blackarcana.network.ArcanaProtocol;
import dev.gustavopere.blackarcana.network.CastIntentPayload;
import dev.gustavopere.blackarcana.network.ClientArcanaSyncState;
import dev.gustavopere.blackarcana.network.neoforge.ArcanaNetworkBridge;
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
    private static final ClientLoadoutSelection SELECTION = new ClientLoadoutSelection();
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

    public static boolean castSlot(int slot) {
        Minecraft minecraft = Minecraft.getInstance();
        if (minecraft.player == null || minecraft.getConnection() == null || minecraft.screen != null) return false;
        List<ArcanaSpellId> loadout = ClientArcanaSyncState.loadoutSnapshot();
        if (!SELECTION.select(slot, loadout)) return false;
        ClientUxState.markSelectionChanged();
        ArcanaSpellId spell = loadout.get(slot);
        String targetHint = "";
        if (minecraft.hitResult instanceof EntityHitResult entityHit) {
            targetHint = new ArcanaTargetReference.EntityRef(entityHit.getEntity().getUUID()).canonical();
        }
        ArcanaCastId castId = ArcanaCastId.random();
        CastPresentationClientRuntime.recordLocalIntent(castId, spell, minecraft.player.tickCount);
        ArcanaNetworkBridge.sendCastIntent(new CastIntentPayload(
                ArcanaProtocol.VERSION,
                castId.canonical(),
                spell.canonical(),
                slot,
                targetHint));
        return true;
    }

    private static void onClientTick(ClientTickEvent.Post event) {
        Minecraft minecraft = Minecraft.getInstance();
        if (minecraft.player == null || minecraft.getConnection() == null) {
            presentationDimension = null;
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
            if (minecraft.screen == null) castSlot(SELECTION.selectedSlot());
        }
        for (int index = 0; index < BlackArcanaKeyMappings.QUICK_CAST.length; index++) {
            while (BlackArcanaKeyMappings.QUICK_CAST[index].consumeClick()) {
                if (minecraft.screen == null) castSlot(index);
            }
        }
    }
}
