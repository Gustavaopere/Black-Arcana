package dev.gustavopere.blackarcana.client;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import net.minecraft.client.DeltaTracker;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.util.FormattedCharSequence;
import net.neoforged.neoforge.client.event.RegisterGuiLayersEvent;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

/** Non-blocking, bounded Stage 05.16 first-use cue. */
public final class DiscoverabilityHintLayer {
    private static final ResourceLocation ID = ResourceLocation.fromNamespaceAndPath(
            BlackArcanaMod.MOD_ID, "discoverability_hint");
    private static final int PADDING = 6;
    private static final int BACKGROUND = 0xD8120E18;
    private static final int BORDER = 0xFF8F7797;
    private static final int TEXT = 0xFFF0E4F0;

    private DiscoverabilityHintLayer() { }

    public static void register(RegisterGuiLayersEvent event) {
        Objects.requireNonNull(event, "event").registerAboveAll(ID, DiscoverabilityHintLayer::render);
    }

    private static void render(GuiGraphics graphics, DeltaTracker deltaTracker) {
        Minecraft minecraft = Minecraft.getInstance();
        if (minecraft.player == null || minecraft.getConnection() == null || minecraft.screen != null) return;

        DiscoverabilityModel.Hint hint = DiscoverabilityClientRuntime.active(minecraft.player).orElse(null);
        if (hint == null) return;

        DiscoverabilityHintLayout layout = DiscoverabilityHintLayout.forViewport(
                graphics.guiWidth(), graphics.guiHeight());
        int textWidth = Math.max(1, layout.width() - PADDING * 2);
        List<FormattedCharSequence> wrapped = new ArrayList<>();
        for (Component line : DiscoverabilityHelpPresentation.hintLines(hint)) {
            wrapped.addAll(minecraft.font.split(line, textWidth));
        }

        int lineHeight = minecraft.font.lineHeight + 1;
        int maxLines = Math.max(1, (layout.maxHeight() - PADDING * 2) / lineHeight);
        int visibleLines = Math.min(maxLines, wrapped.size());
        int height = Math.min(
                layout.maxHeight(),
                PADDING * 2 + Math.max(minecraft.font.lineHeight, visibleLines * lineHeight));
        int right = layout.x() + layout.width();
        int bottom = layout.y() + height;

        graphics.fill(layout.x(), layout.y(), right, bottom, BACKGROUND);
        graphics.fill(layout.x(), layout.y(), right, layout.y() + 1, BORDER);
        graphics.fill(layout.x(), bottom - 1, right, bottom, BORDER);
        graphics.fill(layout.x(), layout.y(), layout.x() + 1, bottom, BORDER);
        graphics.fill(right - 1, layout.y(), right, bottom, BORDER);

        for (int index = 0; index < visibleLines; index++) {
            graphics.drawString(
                    minecraft.font,
                    wrapped.get(index),
                    layout.x() + PADDING,
                    layout.y() + PADDING + index * lineHeight,
                    TEXT,
                    false);
        }
    }
}
