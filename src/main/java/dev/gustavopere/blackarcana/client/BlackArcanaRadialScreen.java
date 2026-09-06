package dev.gustavopere.blackarcana.client;

import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.network.ClientArcanaSyncState;
import dev.gustavopere.blackarcana.network.HazardPreflightPayload;
import dev.gustavopere.blackarcana.network.SpellPresentationPayload;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.network.chat.Component;
import org.lwjgl.glfw.GLFW;

import java.util.List;
import java.util.Map;
import java.util.Optional;

/** Compact selector only: choosing a wedge changes selection but never executes a cast. */
public final class BlackArcanaRadialScreen extends Screen {
    private static final double PREFERRED_RADIUS = 78.0D;
    private static final double PREFERRED_INNER_HIT_RADIUS = 28.0D;
    private static final double HIT_RADIUS_PADDING = 34.0D;
    private static final int VIEWPORT_MARGIN = 4;

    private final List<ArcanaSpellId> loadout;
    private final Map<ArcanaSpellId, SpellPresentationPayload.Entry> presentation;
    private final Map<ArcanaSpellId, HazardPreflightPayload.Entry> hazards;
    private int page;
    private int hoveredSlot = -1;

    private BlackArcanaRadialScreen() {
        super(Component.translatable("screen.black_arcana.radial"));
        this.loadout = ClientArcanaSyncState.loadoutSnapshot();
        this.presentation = ClientArcanaSyncState.presentationSnapshot();
        this.hazards = ClientArcanaSyncState.hazardPreflightSnapshot();
        this.page = RadialLayout.clampPage(
                loadout.size(),
                ClientInputController.selection().selectedSlot() / RadialLayout.SLOTS_PER_PAGE);
    }

    public static void open() {
        Minecraft minecraft = Minecraft.getInstance();
        if (minecraft.screen == null && minecraft.player != null && !ClientArcanaSyncState.loadoutSnapshot().isEmpty()) {
            minecraft.setScreen(new BlackArcanaRadialScreen());
        }
    }

    @Override
    public void tick() {
        super.tick();
        if (BlackArcanaClientConfig.RADIAL_BEHAVIOR.get() == BlackArcanaClientConfig.RadialBehavior.HOLD
                && !BlackArcanaKeyMappings.OPEN_RADIAL.isDown()) {
            onClose();
        }
    }

    @Override
    public void render(GuiGraphics graphics, int mouseX, int mouseY, float partialTick) {
        graphics.fill(0, 0, width, height, 0x55000000);
        int centerX = width / 2;
        int centerY = height / 2;
        RadialLayout.CardMetrics card = RadialLayout.cardMetricsForViewport(width, height);
        double radius = RadialLayout.radiusForViewport(
                width, height, card.halfWidth() + 1, card.halfHeight() + 1,
                PREFERRED_RADIUS, VIEWPORT_MARGIN);
        double innerHitRadius = Math.min(PREFERRED_INNER_HIT_RADIUS, Math.max(8.0D, radius * 0.36D));
        double outerHitRadius = Math.max(innerHitRadius + 1.0D, radius + HIT_RADIUS_PADDING);

        List<Integer> visible = RadialLayout.visibleSlots(loadout.size(), page);
        hoveredSlot = RadialLayout.hoveredSlot(
                loadout.size(), page, mouseX, mouseY, centerX, centerY,
                innerHitRadius, outerHitRadius);

        for (int visibleIndex = 0; visibleIndex < visible.size(); visibleIndex++) {
            int slot = visible.get(visibleIndex);
            ArcanaSpellId spell = loadout.get(slot);
            RadialLayout.Point point = RadialLayout.slotCenter(
                    visibleIndex, visible.size(), centerX, centerY, radius);
            int x = (int) Math.round(point.x());
            int y = (int) Math.round(point.y());
            boolean selected = slot == ClientInputController.selection().selectedSlot();
            boolean hovered = slot == hoveredSlot;
            int background = hovered ? 0xDD6B376D : selected ? 0xCC3D2748 : 0xB815101A;
            int border = hovered ? 0xFFF2D0F2 : selected ? 0xFFB991C0 : 0xFF5A4A60;
            graphics.fill(x - card.halfWidth() - 1, y - card.halfHeight() - 1,
                    x + card.halfWidth() + 1, y + card.halfHeight() + 1, border);
            graphics.fill(x - card.halfWidth(), y - card.halfHeight(),
                    x + card.halfWidth(), y + card.halfHeight(), background);

            String label = card.compact()
                    ? Integer.toString(slot + 1)
                    : (slot + 1) + " · " + displayName(spell, card.halfWidth() * 2 - 18);
            graphics.drawCenteredString(font, label, x, y - 4, 0xFFFFFFFF);
        }

        int centerTextWidth = Math.max(1, width - 16);
        if (!card.compact()) {
            graphics.drawCenteredString(font, title, centerX, centerY - 4, 0xFFEADCEA);
            focusedHazard().ifPresent(line -> graphics.drawCenteredString(
                    font, boundedCenterLine(line, centerTextWidth), centerX, centerY + 12, 0xFFF2D0F2));
            if (RadialLayout.pageCount(loadout.size()) > 1) {
                Component pages = Component.translatable(
                        "screen.black_arcana.radial.page", page + 1, RadialLayout.pageCount(loadout.size()));
                graphics.drawCenteredString(font, pages, centerX, centerY + 26, 0xFFB9ABB9);
            }
            graphics.drawCenteredString(
                    font,
                    boundedCenterLine(Component.translatable("screen.black_arcana.radial.hint"), centerTextWidth),
                    centerX,
                    Math.max(4, height - 24),
                    0xFFD0C6D0);
        }
        super.render(graphics, mouseX, mouseY, partialTick);
        if (card.compact() && hoveredSlot >= 0) {
            focusedSpellName().ifPresent(line -> graphics.renderTooltip(font, line, mouseX, mouseY));
        }
    }

    @Override
    public boolean mouseClicked(double mouseX, double mouseY, int button) {
        if (button == GLFW.GLFW_MOUSE_BUTTON_LEFT && hoveredSlot >= 0) {
            ClientInputController.selection().select(hoveredSlot, loadout);
            ClientUxState.markSelectionChanged();
            onClose();
            return true;
        }
        return super.mouseClicked(mouseX, mouseY, button);
    }

    @Override
    public boolean keyPressed(int keyCode, int scanCode, int modifiers) {
        if (shouldCloseFromOpenKey(
                BlackArcanaClientConfig.RADIAL_BEHAVIOR.get(),
                BlackArcanaKeyMappings.OPEN_RADIAL.matches(keyCode, scanCode))) {
            onClose();
            return true;
        }
        if (keyCode == GLFW.GLFW_KEY_PAGE_UP || keyCode == GLFW.GLFW_KEY_LEFT) {
            page = RadialLayout.clampPage(loadout.size(), page - 1);
            return true;
        }
        if (keyCode == GLFW.GLFW_KEY_PAGE_DOWN || keyCode == GLFW.GLFW_KEY_RIGHT) {
            page = RadialLayout.clampPage(loadout.size(), page + 1);
            return true;
        }
        return super.keyPressed(keyCode, scanCode, modifiers);
    }

    static boolean shouldCloseFromOpenKey(
            BlackArcanaClientConfig.RadialBehavior behavior,
            boolean openKeyPressed
    ) {
        return behavior == BlackArcanaClientConfig.RadialBehavior.TOGGLE && openKeyPressed;
    }

    @Override
    public boolean isPauseScreen() {
        return false;
    }

    private Optional<ArcanaSpellId> focusedSpell() {
        if (hoveredSlot >= 0 && hoveredSlot < loadout.size()) {
            return Optional.of(loadout.get(hoveredSlot));
        }
        return ClientInputController.selection().selected(loadout);
    }

    private Optional<Component> focusedSpellName() {
        return focusedSpell().map(spell -> {
            SpellPresentationPayload.Entry entry = presentation.get(spell);
            return entry == null
                    ? Component.literal(spell.path().replace('_', ' '))
                    : Component.translatable(entry.translationKey());
        });
    }

    private Optional<Component> focusedHazard() {
        ArcanaSpellId spell = focusedSpell().orElse(null);
        if (spell == null) return Optional.empty();
        HazardPreflightPayload.Entry entry = hazards.get(spell);
        return entry == null ? Optional.empty() : Optional.of(BlackArcanaHudLayer.preflightLine(entry));
    }

    private Component boundedCenterLine(Component line, int maxWidth) {
        return BlackArcanaHudLayer.boundLine(font, line, maxWidth);
    }

    private String displayName(ArcanaSpellId spell, int maxWidth) {
        SpellPresentationPayload.Entry entry = presentation.get(spell);
        String raw = entry == null
                ? spell.path().replace('_', ' ')
                : Component.translatable(entry.translationKey()).getString();
        return font.plainSubstrByWidth(raw, Math.max(1, maxWidth));
    }
}
