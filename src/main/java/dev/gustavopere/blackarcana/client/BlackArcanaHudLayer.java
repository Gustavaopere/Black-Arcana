package dev.gustavopere.blackarcana.client;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.network.CastResultPayload;
import dev.gustavopere.blackarcana.network.ClientArcanaSyncState;
import dev.gustavopere.blackarcana.network.SpellPresentationPayload;
import net.minecraft.client.DeltaTracker;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.neoforged.neoforge.client.event.RegisterGuiLayersEvent;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.OptionalLong;

/** Small, event-driven HUD: it disappears when the player is idle. */
public final class BlackArcanaHudLayer {
    private static final ResourceLocation ID = ResourceLocation.fromNamespaceAndPath(BlackArcanaMod.MOD_ID, "contextual_hud");
    private static final int MARGIN = 10;
    private static final int PADDING = 6;

    private BlackArcanaHudLayer() { }

    public static void register(RegisterGuiLayersEvent event) {
        event.registerAboveAll(ID, BlackArcanaHudLayer::render);
    }

    private static void render(GuiGraphics graphics, DeltaTracker deltaTracker) {
        if (!BlackArcanaClientConfig.CONTEXTUAL_HUD.get()) return;
        Minecraft minecraft = Minecraft.getInstance();
        if (minecraft.player == null || minecraft.screen != null) return;

        long now = minecraft.player.tickCount;
        int selectionDuration = BlackArcanaClientConfig.SELECTION_DURATION_TICKS.get();
        int feedbackDuration = BlackArcanaClientConfig.FEEDBACK_DURATION_TICKS.get();
        boolean selectionRecent = HudLayout.isRecent(now, ClientUxState.selectionChangedTick(), selectionDuration);
        Optional<CastResultPayload> result = ClientArcanaSyncState.lastResult();
        OptionalLong resultTick = ClientArcanaSyncState.lastResultTick();
        boolean resultRecent = result.isPresent() && resultTick.isPresent()
                && HudLayout.isRecent(now, resultTick.getAsLong(), feedbackDuration);
        BlackArcanaClientConfig.FeedbackLevel level = BlackArcanaClientConfig.FEEDBACK_LEVEL.get();
        boolean denialRecent = resultRecent && !"SUCCESS".equals(result.orElseThrow().status());

        if (level == BlackArcanaClientConfig.FeedbackLevel.MINIMAL && !denialRecent) return;
        if (!selectionRecent && !resultRecent) return;

        List<Component> lines = new ArrayList<>(2);
        if (level != BlackArcanaClientConfig.FeedbackLevel.MINIMAL) {
            selectedSpellLine().ifPresent(lines::add);
        }
        if (resultRecent) {
            CastResultPayload payload = result.orElseThrow();
            if (!"SUCCESS".equals(payload.status())) {
                lines.add(Component.translatable("hud.black_arcana.denied", Component.literal(payload.detail())));
            } else if (level == BlackArcanaClientConfig.FeedbackLevel.VERBOSE) {
                lines.add(Component.translatable("hud.black_arcana.cast_success"));
            }
        }
        if (lines.isEmpty()) return;

        float scale = BlackArcanaClientConfig.HUD_SCALE.get().floatValue();
        int logicalWidth = Math.max(1, (int) Math.floor(graphics.guiWidth() / scale));
        int logicalHeight = Math.max(1, (int) Math.floor(graphics.guiHeight() / scale));
        int textWidth = lines.stream().mapToInt(minecraft.font::width).max().orElse(1);
        int panelWidth = textWidth + PADDING * 2;
        int panelHeight = lines.size() * (minecraft.font.lineHeight + 2) + PADDING * 2 - 2;
        HudLayout.Point origin = HudLayout.origin(
                BlackArcanaClientConfig.HUD_ANCHOR.get(),
                logicalWidth, logicalHeight, panelWidth, panelHeight, MARGIN);

        graphics.pose().pushPose();
        graphics.pose().scale(scale, scale, 1.0F);
        int x = origin.x();
        int y = origin.y();
        graphics.fill(x - 1, y - 1, x + panelWidth + 1, y + panelHeight + 1, 0xAA5A4A60);
        graphics.fill(x, y, x + panelWidth, y + panelHeight, 0xB815101A);
        int textY = y + PADDING;
        for (Component line : lines) {
            graphics.drawString(minecraft.font, line, x + PADDING, textY, 0xFFF2EAF2, false);
            textY += minecraft.font.lineHeight + 2;
        }
        graphics.pose().popPose();
    }

    private static Optional<Component> selectedSpellLine() {
        List<ArcanaSpellId> loadout = ClientArcanaSyncState.loadoutSnapshot();
        Optional<ArcanaSpellId> selected = ClientInputController.selection().selected(loadout);
        if (selected.isEmpty()) return Optional.empty();
        ArcanaSpellId spell = selected.orElseThrow();
        Map<ArcanaSpellId, SpellPresentationPayload.Entry> presentation = ClientArcanaSyncState.presentationSnapshot();
        SpellPresentationPayload.Entry entry = presentation.get(spell);
        Component name = entry == null
                ? Component.literal(spell.path().replace('_', ' '))
                : Component.translatable(entry.translationKey());
        return Optional.of(Component.translatable("hud.black_arcana.selected", name));
    }
}
