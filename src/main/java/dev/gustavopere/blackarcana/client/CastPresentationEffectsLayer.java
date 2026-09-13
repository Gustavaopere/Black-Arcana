package dev.gustavopere.blackarcana.client;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import net.minecraft.client.DeltaTracker;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.resources.sounds.SimpleSoundInstance;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.sounds.SoundEvent;
import net.neoforged.neoforge.client.event.RegisterGuiLayersEvent;

import java.util.Objects;

/**
 * Physical-client generic cast audiovisual sink for Stage 05.15.
 *
 * <p>This layer presents only the already-arbitrated directive supplied by
 * {@link CastPresentationClientRuntime}. It never samples aim/target/world geometry and never owns
 * cast authority. Audio is optional; the transient shape remains available when sound is muted or
 * its resource is absent.</p>
 */
public final class CastPresentationEffectsLayer {
    private static final ResourceLocation ID = ResourceLocation.fromNamespaceAndPath(
            BlackArcanaMod.MOD_ID, "cast_presentation");
    private static final CastPresentationPulseState PULSES = new CastPresentationPulseState(4L, 8L);

    private CastPresentationEffectsLayer() { }

    public static void register(RegisterGuiLayersEvent event) {
        Objects.requireNonNull(event, "event").registerAboveAll(ID, CastPresentationEffectsLayer::render);
    }

    public static void accept(CastAudiovisualOrchestration.Directive directive) {
        Objects.requireNonNull(directive, "directive");
        Minecraft minecraft = Minecraft.getInstance();
        if (minecraft.player == null || minecraft.getConnection() == null) return;

        PULSES.accept(directive, minecraft.player.tickCount);
        playOptionalSound(minecraft, directive);
    }

    public static void clear() {
        PULSES.clear();
    }

    private static void playOptionalSound(
            Minecraft minecraft,
            CastAudiovisualOrchestration.Directive directive
    ) {
        CastPresentationResources.resolveSoundEvent(
                directive.kind(),
                asset -> minecraft.getResourceManager().getResource(asset).isPresent())
                .ifPresent(eventId -> minecraft.getSoundManager().play(SimpleSoundInstance.forUI(
                        SoundEvent.createVariableRangeEvent(eventId),
                        pitch(directive.kind()),
                        volume(directive.kind()))));
    }

    private static void render(GuiGraphics graphics, DeltaTracker deltaTracker) {
        Minecraft minecraft = Minecraft.getInstance();
        if (minecraft.player == null || minecraft.getConnection() == null || minecraft.screen != null) return;

        CastPresentationPulseState.Pulse pulse = PULSES.current(minecraft.player.tickCount).orElse(null);
        if (pulse == null) return;

        long age = Math.max(0L, minecraft.player.tickCount - pulse.startedTick());
        int motionExpansion = pulse.optionalMotionAllowed() ? (int) Math.min(3L, age) : 0;
        int radius = baseRadius(pulse.kind()) + motionExpansion;
        int color = pulseColor(pulse);
        int centerX = graphics.guiWidth() / 2;
        int centerY = graphics.guiHeight() / 2;

        drawCornerBrackets(graphics, centerX, centerY, radius, color);
        switch (pulse.kind()) {
            case ANTICIPATION -> { }
            case RESULT_SUCCESS -> drawSuccessMark(graphics, centerX, centerY, radius, color);
            case RESULT_DENIED -> drawDenialMark(graphics, centerX, centerY, color);
            case RESULT_FAILED -> drawFailureMark(graphics, centerX, centerY, radius, color);
        }
    }

    private static void drawCornerBrackets(GuiGraphics graphics, int x, int y, int r, int color) {
        int arm = 4;
        graphics.fill(x - r, y - r, x - r + arm, y - r + 1, color);
        graphics.fill(x - r, y - r, x - r + 1, y - r + arm, color);
        graphics.fill(x + r - arm, y - r, x + r, y - r + 1, color);
        graphics.fill(x + r - 1, y - r, x + r, y - r + arm, color);
        graphics.fill(x - r, y + r - 1, x - r + arm, y + r, color);
        graphics.fill(x - r, y + r - arm, x - r + 1, y + r, color);
        graphics.fill(x + r - arm, y + r - 1, x + r, y + r, color);
        graphics.fill(x + r - 1, y + r - arm, x + r, y + r, color);
    }

    private static void drawSuccessMark(GuiGraphics graphics, int x, int y, int r, int color) {
        graphics.fill(x - 2, y + r + 2, x + 3, y + r + 3, color);
    }

    private static void drawDenialMark(GuiGraphics graphics, int x, int y, int color) {
        graphics.fill(x - 4, y, x + 5, y + 1, color);
        graphics.fill(x, y - 4, x + 1, y + 5, color);
    }

    private static void drawFailureMark(GuiGraphics graphics, int x, int y, int r, int color) {
        int inner = Math.max(3, r - 4);
        graphics.fill(x - inner, y - inner, x + inner, y - inner + 1, color);
        graphics.fill(x - inner, y + inner - 1, x + inner, y + inner, color);
        graphics.fill(x - inner, y - inner, x - inner + 1, y + inner, color);
        graphics.fill(x + inner - 1, y - inner, x + inner, y + inner, color);
    }

    private static int baseRadius(CastAudiovisualOrchestration.Kind kind) {
        return switch (kind) {
            case ANTICIPATION -> 7;
            case RESULT_SUCCESS -> 9;
            case RESULT_DENIED, RESULT_FAILED -> 10;
        };
    }

    private static int pulseColor(CastPresentationPulseState.Pulse pulse) {
        int rgb = switch (pulse.kind()) {
            case ANTICIPATION -> 0x9A839F;
            case RESULT_SUCCESS -> 0x93B39A;
            case RESULT_DENIED -> 0xC0787E;
            case RESULT_FAILED -> 0xA47AAE;
        };
        int alpha = pulse.flashHeavyEffectsAllowed() ? 0xB0 : 0x70;
        return (alpha << 24) | rgb;
    }

    private static float pitch(CastAudiovisualOrchestration.Kind kind) {
        return switch (kind) {
            case ANTICIPATION -> 0.92F;
            case RESULT_SUCCESS -> 1.08F;
            case RESULT_DENIED -> 0.82F;
            case RESULT_FAILED -> 0.74F;
        };
    }

    private static float volume(CastAudiovisualOrchestration.Kind kind) {
        return kind == CastAudiovisualOrchestration.Kind.ANTICIPATION ? 0.25F : 0.45F;
    }
}
