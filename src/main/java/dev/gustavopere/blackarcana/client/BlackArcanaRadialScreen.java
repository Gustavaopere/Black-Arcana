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
    private static final int CARD_TEXT_PADDING = 2;

    private final List<ArcanaSpellId> loadout;
    private final Map<ArcanaSpellId, SpellPresentationPayload.Entry> presentation;
    private final Map<ArcanaSpellId, HazardPreflightPayload.Entry> hazards;
    private int page;
    private int hoveredSlot = -1;
    private int focusedSlot;
    private KeyboardFocusNavigation.InputModality inputModality = KeyboardFocusNavigation.InputModality.KEYBOARD;
    private boolean pointerSeeded;
    private int lastMouseX;
    private int lastMouseY;

    private BlackArcanaRadialScreen() {
        super(Component.translatable("screen.black_arcana.radial"));
        this.loadout = ClientArcanaSyncState.loadoutSnapshot();
        this.presentation = ClientArcanaSyncState.presentationSnapshot();
        this.hazards = ClientArcanaSyncState.hazardPreflightSnapshot();
        int selectedSlot = ClientInputController.selection().selectedSlot();
        this.page = RadialLayout.clampPage(loadout.size(), selectedSlot / RadialLayout.SLOTS_PER_PAGE);
        this.focusedSlot = KeyboardFocusNavigation.radialInitialFocus(loadout.size(), page, selectedSlot);
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
        updatePointerModality(mouseX, mouseY, hoveredSlot >= 0);

        for (int visibleIndex = 0; visibleIndex < visible.size(); visibleIndex++) {
            int slot = visible.get(visibleIndex);
            ArcanaSpellId spell = loadout.get(slot);
            RadialLayout.Point point = RadialLayout.slotCenter(
                    visibleIndex, visible.size(), centerX, centerY, radius);
            int x = (int) Math.round(point.x());
            int y = (int) Math.round(point.y());
            boolean selected = slot == ClientInputController.selection().selectedSlot();
            boolean hovered = slot == hoveredSlot;
            boolean focused = slot == focusedSlot;
            CastingUxSemantics.FocusState focus = CastingUxSemantics.focus(selected, hovered, focused);
            int background = switch (focus) {
                case NONE -> 0xB815101A;
                case SELECTED -> 0xCC3D2748;
                case HOVERED, SELECTED_HOVERED -> 0xDD6B376D;
                case FOCUSED -> 0xCC273448;
                case SELECTED_FOCUSED -> 0xDD4A3452;
                case HOVERED_FOCUSED, SELECTED_HOVERED_FOCUSED -> 0xEE714578;
            };
            int border = switch (focus) {
                case NONE -> 0xFF5A4A60;
                case SELECTED -> 0xFFB991C0;
                case HOVERED -> 0xFFF2D0F2;
                case SELECTED_HOVERED -> 0xFFFFE8FF;
                case FOCUSED -> 0xFF9DD9FF;
                case SELECTED_FOCUSED -> 0xFFC4DEFF;
                case HOVERED_FOCUSED, SELECTED_HOVERED_FOCUSED -> 0xFFFFFFFF;
            };
            graphics.fill(x - card.halfWidth() - 1, y - card.halfHeight() - 1,
                    x + card.halfWidth() + 1, y + card.halfHeight() + 1, border);
            graphics.fill(x - card.halfWidth(), y - card.halfHeight(),
                    x + card.halfWidth(), y + card.halfHeight(), background);

            int maxLabelWidth = Math.max(1, card.halfWidth() * 2 - CARD_TEXT_PADDING * 2);
            String label;
            if (card.compact()) {
                String compactLabel = compactFocusPrefix(focus) + (slot + 1);
                label = font.plainSubstrByWidth(compactLabel, maxLabelWidth);
            } else {
                String fixedPrefix = focusPrefix(focus) + (slot + 1) + " · ";
                int nameBudget = spellNameWidthBudget(maxLabelWidth, font.width(fixedPrefix));
                String name = nameBudget > 0 ? displayName(spell, nameBudget) : "";
                label = font.plainSubstrByWidth(fixedPrefix + name, maxLabelWidth);
            }
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
        int temporarySlot = activeTemporarySlot();
        if (card.compact() && temporarySlot >= 0) {
            int tooltipX = mouseX;
            int tooltipY = mouseY;
            if (inputModality == KeyboardFocusNavigation.InputModality.KEYBOARD) {
                int visibleIndex = visible.indexOf(temporarySlot);
                if (visibleIndex >= 0) {
                    RadialLayout.Point point = RadialLayout.slotCenter(
                            visibleIndex, visible.size(), centerX, centerY, radius);
                    tooltipX = (int) Math.round(point.x());
                    tooltipY = (int) Math.round(point.y()) + card.halfHeight() + 4;
                }
            }
            int finalTooltipX = tooltipX;
            int finalTooltipY = tooltipY;
            focusedSpellName().ifPresent(line -> graphics.renderTooltip(font, line, finalTooltipX, finalTooltipY));
        }
    }

    @Override
    public boolean mouseClicked(double mouseX, double mouseY, int button) {
        if (button == GLFW.GLFW_MOUSE_BUTTON_LEFT && hoveredSlot >= 0) {
            inputModality = KeyboardFocusNavigation.InputModality.POINTER;
            if (selectFocusedSlot(hoveredSlot, loadout, ClientInputController.selection())) {
                ClientUxState.markSelectionChanged();
                onClose();
            }
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
        if (keyCode == GLFW.GLFW_KEY_TAB) {
            inputModality = KeyboardFocusNavigation.InputModality.KEYBOARD;
            int direction = (modifiers & GLFW.GLFW_MOD_SHIFT) != 0 ? -1 : 1;
            focusedSlot = KeyboardFocusNavigation.radialTraverse(loadout.size(), page, focusedSlot, direction);
            return focusedSlot >= 0 || !RadialLayout.visibleSlots(loadout.size(), page).isEmpty();
        }
        if (keyCode == GLFW.GLFW_KEY_ENTER || keyCode == GLFW.GLFW_KEY_KP_ENTER || keyCode == GLFW.GLFW_KEY_SPACE) {
            inputModality = KeyboardFocusNavigation.InputModality.KEYBOARD;
            if (selectFocusedSlot(focusedSlot, loadout, ClientInputController.selection())) {
                ClientUxState.markSelectionChanged();
                onClose();
                return true;
            }
            return super.keyPressed(keyCode, scanCode, modifiers);
        }
        if (keyCode == GLFW.GLFW_KEY_PAGE_UP || keyCode == GLFW.GLFW_KEY_LEFT) {
            changePage(-1);
            return true;
        }
        if (keyCode == GLFW.GLFW_KEY_PAGE_DOWN || keyCode == GLFW.GLFW_KEY_RIGHT) {
            changePage(1);
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

    static boolean selectFocusedSlot(
            int focusedSlot,
            List<ArcanaSpellId> loadout,
            ClientLoadoutSelection selection
    ) {
        return selection.select(focusedSlot, loadout);
    }

    static String focusPrefix(CastingUxSemantics.FocusState focus) {
        return switch (focus) {
            case NONE -> "";
            case SELECTED -> "[S] ";
            case HOVERED -> "> ";
            case FOCUSED -> "[F] ";
            case SELECTED_HOVERED -> ">[S] ";
            case SELECTED_FOCUSED -> "[F][S] ";
            case HOVERED_FOCUSED -> ">[F] ";
            case SELECTED_HOVERED_FOCUSED -> ">[F][S] ";
        };
    }

    static String compactFocusPrefix(CastingUxSemantics.FocusState focus) {
        return switch (focus) {
            case NONE -> "";
            case SELECTED -> "S";
            case HOVERED -> ">";
            case FOCUSED -> "F";
            case SELECTED_HOVERED -> ">S";
            case SELECTED_FOCUSED -> "FS";
            case HOVERED_FOCUSED -> ">F";
            case SELECTED_HOVERED_FOCUSED -> ">FS";
        };
    }

    static int spellNameWidthBudget(int labelWidth, int fixedPrefixWidth) {
        if (labelWidth < 0 || fixedPrefixWidth < 0) {
            throw new IllegalArgumentException("radial label widths cannot be negative");
        }
        return Math.max(0, labelWidth - fixedPrefixWidth);
    }

    @Override
    public boolean isPauseScreen() {
        return false;
    }

    private void changePage(int direction) {
        inputModality = KeyboardFocusNavigation.InputModality.KEYBOARD;
        int destination = RadialLayout.clampPage(loadout.size(), page + direction);
        if (destination == page) return;
        focusedSlot = KeyboardFocusNavigation.radialFocusAfterPageChange(
                loadout.size(), page, destination,
                ClientInputController.selection().selectedSlot(), focusedSlot);
        page = destination;
    }

    private void updatePointerModality(int mouseX, int mouseY, boolean overInteractiveSlot) {
        if (!pointerSeeded) {
            pointerSeeded = true;
        } else if (overInteractiveSlot && (mouseX != lastMouseX || mouseY != lastMouseY)) {
            inputModality = KeyboardFocusNavigation.InputModality.POINTER;
        }
        lastMouseX = mouseX;
        lastMouseY = mouseY;
    }

    private int activeTemporarySlot() {
        if (inputModality == KeyboardFocusNavigation.InputModality.POINTER) {
            return hoveredSlot >= 0 && hoveredSlot < loadout.size() ? hoveredSlot : -1;
        }
        return focusedSlot >= 0 && focusedSlot < loadout.size() ? focusedSlot : -1;
    }

    private Optional<ArcanaSpellId> focusedSpell() {
        int temporary = activeTemporarySlot();
        if (temporary >= 0) return Optional.of(loadout.get(temporary));
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
