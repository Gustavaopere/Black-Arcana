package dev.gustavopere.blackarcana.client;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.network.ClientArcanaSyncState;
import net.minecraft.client.DeltaTracker;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.phys.HitResult;
import net.neoforged.neoforge.client.event.RegisterGuiLayersEvent;

/**
 * Physical-client-only, advisory aim cue.
 *
 * The cue reflects only the current vanilla client hit result. It never claims
 * server target validity, range, LOS, cast admission or world-effect permission.
 */
public final class TargetAimPresentationLayer {
    private static final ResourceLocation ID = ResourceLocation.fromNamespaceAndPath(
            BlackArcanaMod.MOD_ID, "target_local_observation");
    private static final int CROSSHAIR_OFFSET_Y = 12;
    private static final int VIEWPORT_MARGIN = 8;

    private TargetAimPresentationLayer() {
    }

    public static void register(RegisterGuiLayersEvent event) {
        event.registerAboveAll(ID, TargetAimPresentationLayer::render);
    }

    private static void render(GuiGraphics graphics, DeltaTracker deltaTracker) {
        if (!BlackArcanaClientConfig.CONTEXTUAL_HUD.get()) return;

        Minecraft minecraft = Minecraft.getInstance();
        boolean worldInputAvailable = minecraft.player != null
                && minecraft.getConnection() != null
                && minecraft.screen == null;
        boolean selectionRecent = worldInputAvailable && HudLayout.isRecent(
                minecraft.player.tickCount,
                ClientUxState.selectionChangedTick(),
                BlackArcanaClientConfig.SELECTION_DURATION_TICKS.get());
        boolean showSelectionContext = ContextualFeedbackOrchestration.decide(
                BlackArcanaClientConfig.FEEDBACK_LEVEL.get(),
                selectionRecent,
                false,
                null).showSelectionContext();
        var loadout = ClientArcanaSyncState.loadoutSnapshot();
        boolean hasSelectedSpell = worldInputAvailable
                && !loadout.isEmpty()
                && ClientInputController.selection().selected(loadout).isPresent();

        if (!TargetAimPresentationSemantics.shouldRender(
                BlackArcanaClientConfig.CONTEXTUAL_HUD.get(),
                worldInputAvailable,
                showSelectionContext,
                hasSelectedSpell)) {
            return;
        }

        TargetAimPresentationSemantics.Observation observation = observation(minecraft);
        Component cue = Component.translatable(
                TargetAimPresentationSemantics.translationKey(observation),
                TargetAimPresentationSemantics.marker(observation));
        Component bounded = BlackArcanaHudLayer.boundLine(
                minecraft.font,
                cue,
                Math.max(1, graphics.guiWidth() - VIEWPORT_MARGIN * 2));

        graphics.drawCenteredString(
                minecraft.font,
                bounded,
                graphics.guiWidth() / 2,
                graphics.guiHeight() / 2 + CROSSHAIR_OFFSET_Y,
                0xFFB9ABB9);
    }

    private static TargetAimPresentationSemantics.Observation observation(Minecraft minecraft) {
        HitResult.Type type = minecraft.hitResult == null
                ? HitResult.Type.MISS
                : minecraft.hitResult.getType();
        return TargetAimPresentationSemantics.fromHitType(type);
    }
}
