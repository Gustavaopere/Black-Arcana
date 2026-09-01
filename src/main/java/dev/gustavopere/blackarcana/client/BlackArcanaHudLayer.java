package dev.gustavopere.blackarcana.client;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDangerTier;
import dev.gustavopere.blackarcana.network.CastResultPayload;
import dev.gustavopere.blackarcana.network.ClientArcanaSyncState;
import dev.gustavopere.blackarcana.network.HazardPreflightPayload;
import dev.gustavopere.blackarcana.network.HazardResistanceForecastPayload;
import dev.gustavopere.blackarcana.network.SpellPresentationPayload;
import net.minecraft.client.DeltaTracker;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.neoforged.neoforge.client.event.RegisterGuiLayersEvent;

import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
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

        List<Component> lines = new ArrayList<>(4);
        if (level != BlackArcanaClientConfig.FeedbackLevel.MINIMAL) {
            selectedSpellLine().ifPresent(lines::add);
            if (selectionRecent) {
                selectedHazardLine().ifPresent(lines::add);
                selectedGateLine().ifPresent(lines::add);
            }
        }
        if (resultRecent) {
            CastResultPayload payload = result.orElseThrow();
            if (!"SUCCESS".equals(payload.status())) {
                // The detail is the bounded server result; the client never invents a gate reason.
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
        Optional<ArcanaSpellId> selected = selectedSpell();
        if (selected.isEmpty()) return Optional.empty();
        ArcanaSpellId spell = selected.orElseThrow();
        Map<ArcanaSpellId, SpellPresentationPayload.Entry> presentation = ClientArcanaSyncState.presentationSnapshot();
        SpellPresentationPayload.Entry entry = presentation.get(spell);
        Component name = entry == null
                ? Component.literal(spell.path().replace('_', ' '))
                : Component.translatable(entry.translationKey());
        return Optional.of(Component.translatable("hud.black_arcana.selected", name));
    }

    private static Optional<Component> selectedHazardLine() {
        Optional<ArcanaSpellId> selected = selectedSpell();
        if (selected.isEmpty()) return Optional.empty();
        ArcanaSpellId spell = selected.orElseThrow();
        HazardPreflightPayload.Entry entry = ClientArcanaSyncState.hazardPreflightSnapshot().get(spell);
        if (entry == null || entry.parsedTier() == ArcaneDangerTier.NORMAL) return Optional.empty();

        Optional<HazardResistanceForecastPayload> forecast = ClientArcanaSyncState.hazardResistanceForecast(spell);
        if (forecast.isPresent()) {
            HazardResistanceForecastPayload payload = forecast.orElseThrow();
            if (forecastMatchesPreflight(entry, payload)) {
                return Optional.of(resistanceForecastLine(payload));
            }
        }
        return Optional.of(preflightLine(entry));
    }

    private static Optional<Component> selectedGateLine() {
        Optional<ArcanaSpellId> selected = selectedSpell();
        if (selected.isEmpty()) return Optional.empty();
        ArcanaSpellId spell = selected.orElseThrow();
        HazardPreflightPayload.Entry entry = ClientArcanaSyncState.hazardPreflightSnapshot().get(spell);
        if (entry == null || entry.parsedTier() == ArcaneDangerTier.NORMAL) return Optional.empty();

        Optional<HazardResistanceForecastPayload> forecast = ClientArcanaSyncState.hazardResistanceForecast(spell);
        if (forecast.isEmpty()) return Optional.empty();
        HazardResistanceForecastPayload payload = forecast.orElseThrow();
        if (!forecastMatchesPreflight(entry, payload)) return Optional.empty();
        HazardResistanceForecastPayload.GateStatus status = payload.gateForecastAvailable()
                ? payload.parsedGateStatus()
                : HazardResistanceForecastPayload.GateStatus.UNAVAILABLE;
        return Optional.of(Component.translatable(gateStatusTranslationKey(status)));
    }

    static boolean forecastMatchesPreflight(
        HazardPreflightPayload.Entry preflight,
        HazardResistanceForecastPayload forecast
    ) {
        return preflight.parsedTier() == forecast.parsedTier()
            && Double.compare(preflight.minimumArcaneResistance(), forecast.minimumArcaneResistance()) == 0
            && Double.compare(preflight.recommendedArcaneResistance(), forecast.recommendedArcaneResistance()) == 0;
    }

    static Component resistanceForecastLine(HazardResistanceForecastPayload forecast) {
        Component tier = Component.translatable(
            "hazard.black_arcana.tier." + forecast.parsedTier().name().toLowerCase(Locale.ROOT));
        if (!forecast.available()) {
            return Component.translatable(
                "hazard.black_arcana.forecast.unavailable",
                tier,
                Component.literal(formatResistance(forecast.minimumArcaneResistance())),
                Component.literal(formatResistance(forecast.recommendedArcaneResistance())));
        }
        Component status = Component.translatable(switch (forecast.parsedStatus()) {
            case BELOW_MINIMUM -> "hazard.black_arcana.forecast.status.blocked";
            case BELOW_RECOMMENDED -> "hazard.black_arcana.forecast.status.below_recommended";
            case RECOMMENDED -> "hazard.black_arcana.forecast.status.recommended";
            case NORMAL -> "hazard.black_arcana.forecast.status.normal";
            case UNAVAILABLE -> "hazard.black_arcana.forecast.status.unavailable";
        });
        return Component.translatable(
            "hazard.black_arcana.forecast",
            tier,
            Component.literal(formatResistance(forecast.effectiveArcaneResistance())),
            Component.literal(formatResistance(forecast.minimumArcaneResistance())),
            Component.literal(formatResistance(forecast.recommendedArcaneResistance())),
            status);
    }

    static String gateStatusTranslationKey(HazardResistanceForecastPayload.GateStatus status) {
        return switch (status) {
            case CLEAR -> "hazard.black_arcana.gate.clear";
            case IDENTITY -> "hazard.black_arcana.gate.identity";
            case PROGRESSION -> "hazard.black_arcana.gate.progression";
            case COOLDOWN -> "hazard.black_arcana.gate.cooldown";
            case COST -> "hazard.black_arcana.gate.cost";
            case UNAVAILABLE -> "hazard.black_arcana.gate.unavailable";
        };
    }

    static Component preflightLine(HazardPreflightPayload.Entry entry) {
        Component tier = Component.translatable(
                "hazard.black_arcana.tier." + entry.parsedTier().name().toLowerCase(Locale.ROOT));
        if (entry.parsedTier() == ArcaneDangerTier.NORMAL) {
            return Component.translatable("hazard.black_arcana.preflight.normal", tier);
        }
        return Component.translatable(
                "hazard.black_arcana.preflight",
                tier,
                Component.literal(formatResistance(entry.minimumArcaneResistance())),
                Component.literal(formatResistance(entry.recommendedArcaneResistance())));
    }

    private static Optional<ArcanaSpellId> selectedSpell() {
        List<ArcanaSpellId> loadout = ClientArcanaSyncState.loadoutSnapshot();
        return ClientInputController.selection().selected(loadout);
    }

    private static String formatResistance(double value) {
        return String.format(Locale.ROOT, "%.1f", value);
    }
}
