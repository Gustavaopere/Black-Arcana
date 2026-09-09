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
    private int keyboardFocusedSlot = -1;
    private ScreenFocusNavigation.InputModality modality = ScreenFocusNavigation.InputModality.KEYBOARD;
    private int lastMouseX = Integer.MIN_VALUE;
    private int lastMouseY = Integer.MIN_VALUE;

    private BlackArcanaRadialScreen() {
        super(Component.translatable("screen.black_arcana.radial"));
        this.loadout = ClientArcanaSyncState.loadoutSnapshot();
        this.presentation = ClientArcanaSyncState.presentationSnapshot();
        this.hazards = ClientArcanaSyncState.hazardPreflightSnapshot();
        int selectedSlot = ClientInputController.selection().selectedSlot();
        this.page = RadialLayout.clampPage(
                loadout.size(),
                selectedSlot / RadialLayout.SLOTS_PER_PAGE);
        this.keyboardFocusedSlot = ScreenFocusNavigation.initialFocus(
                RadialLayout.visibleSlots(loadout.size(), page),
                selectedSlot);
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
        int newHoveredSlot = RadialLayout.hoveredSlot(
                loadout.size(), page, mouseX, mouseY, centerX, centerY,
                innerHitRadius, outerHitRadius);
        if (lastMouseX != Integer.MIN_VALUE
                && (mouseX != lastMouseX || mouseY != lastMouseY)
                && newHoveredSlot >= 0) {
            modality = ScreenFocusNavigation.InputModality.POINTER;
        }
        lastMouseX = mouseX;
        lastMouseY = mouseY;
        hoveredSlot = newHoveredSlot;

        for (int visibleIndex = 0; visibleIndex < visible.size(); visibleIndex++) {
            int slot = visible.get(visibleIndex);
            ArcanaSpellId spell = loadout.get(slot);
            RadialLayout.Point point = RadialLayout.slotCenter(
                    visibleIndex, visible.size(), centerX, centerY, radius);
            int x = (int) Math.round(point.x());
            int y = (int) Math.round(point.y());
            boolean selected = slot == ClientInputController.selection().selectedSlot();
            boolean hovered = slot == hoveredSlot;
            boolean keyboardFocused = modality == ScreenFocusNavigation.InputModality.KEYBOARD
                    && slot == keyboardFocusedSlot;
            CastingUxSemantics.FocusState focus = CastingUxSemantics.focus(selected, hovered);
            int background = switch (focus) {
                case NONE -> 0xB815101A;
                case SELECTED -> 0xCC3D2748;
                case HOVERED, SELECTED_HOVERED -> 0xDD6B376D;
            };
            int border = switch (focus) {
                case NONE -> 0xFF5A4A60;
                case SELECTED -> 0xFFB991C0;
                case HOVERED -> 0xFFF2D0F2;
                case SELECTED_HOVERED -> 0xFFFFE8FF;
            };
            graphics.fill(x - card.halfWidth() - 1, y - card.halfHeight() - 1,
                    x + card.halfWidth() + 1, y + card.halfHeight() + 1, border);
            graphics.fill(x - card.halfWidth(), y - card.halfHeight(),
                    x + card.halfWidth(), y + card.halfHeight(), background);
            if (keyboardFocused) {
                graphics.fill(x + card.halfWidth() - 2, y - card.halfHeight(),
                        x + card.halfWidth(), y + card.halfHeight(), 0xFFFFE8FF);
            }

            int maxLabelWidth = Math.max(1, card.halfWidth() * 2 - CARD_TEXT_PADDING * 2);
            String label;
            if (card.compact()) {
                String compactLabel = keyboardFocusPrefix(keyboardFocused, true)
                        + compactFocusPrefix(focus) + (slot + 1);
                label = font.plainSubstrByWidth(compactLabel, maxLabelWidth);
            } else {
                String fixedPrefix = keyboardFocusPrefix(keyboardFocused, false)
                        + focusPrefix(focus) + (slot + 1) + " · ";
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
        if (card.compact() && modality == ScreenFocusNavigation.InputModality.POINTER && hoveredSlot >= 0) {
            focusedSpellName().ifPresent(line -> graphics.renderTooltip(font, line, mouseX, mouseY));
        }
    }

    @Override
    public boolean mouseClicked(double mouseX, double mouseY, int button) {
        if (button == GLFW.GLFW_MOUSE_BUTTON_LEFT && hoveredSlot >= 0) {
            modality = ScreenFocusNavigation.InputModality.POINTER;
            selectSlotAndClose(hoveredSlot);
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
        if (keyCode == GLFW.GLFW_KEY_ESCAPE) {
            onClose();
            return true;
        }
        if (keyCode == GLFW.GLFW_KEY_TAB) {
            List<Integer> visible = RadialLayout.visibleSlots(loadout.size(), page);
            int direction = (modifiers & GLFW.GLFW_MOD_SHIFT) != 0 ? -1 : 1;
            keyboardFocusedSlot = ScreenFocusNavigation.moveWrapped(visible, keyboardFocusedSlot, direction);
            modality = ScreenFocusNavigation.InputModality.KEYBOARD;
            return true;
        }
        if (isKeyboardActivationKey(keyCode)) {
            if (keyboardFocusedSlot >= 0 && keyboardFocusedSlot < loadout.size()) {
                modality = ScreenFocusNavigation.InputModality.KEYBOARD;
                selectSlotAndClose(keyboardFocusedSlot);
                return true;
            }
            return super.keyPressed(keyCode, scanCode, modifiers);
        }
        if (keyCode == GLFW.GLFW_KEY_PAGE_UP || keyCode == GLFW.GLFW_KEY_LEFT) {
            movePage(-1);
            return true;
        }
        if (keyCode == GLFW.GLFW_KEY_PAGE_DOWN || keyCode == GLFW.GLFW_KEY_RIGHT) {
            movePage(1);
            return true;
        }
        return super.keyPressed(keyCode, scanCode, modifiers);
    }

    private void movePage(int delta) {
        List<Integer> source = RadialLayout.visibleSlots(loadout.size(), page);
        int destinationPage = RadialLayout.clampPage(loadout.size(), page + delta);
        page = destinationPage;
        List<Integer> destination = RadialLayout.visibleSlots(loadout.size(), page);
        keyboardFocusedSlot = ScreenFocusNavigation.transitionFocus(
                source,
                destination,
                keyboardFocusedSlot,
                ClientInputController.selection().selectedSlot());
        modality = ScreenFocusNavigation.InputModality.KEYBOARD;
    }

    private void selectSlotAndClose(int slot) {
        ClientInputController.selection().select(slot, loadout);
        ClientUxState.markSelectionChanged();
        onClose();
    }

    static boolean shouldCloseFromOpenKey(
            BlackArcanaClientConfig.RadialBehavior behavior,
            boolean openKeyPressed
    ) {
        return behavior == BlackArcanaClientConfig.RadialBehavior.TOGGLE && openKeyPressed;
    }

    static boolean isKeyboardActivationKey(int keyCode) {
        return keyCode == GLFW.GLFW_KEY_ENTER
                || keyCode == GLFW.GLFW_KEY_KP_ENTER
                || keyCode == GLFW.GLFW_KEY_SPACE;
    }

    static String keyboardFocusPrefix(boolean focused, boolean compact) {
        if (!focused) return "";
        return compact ? "F" : "[F] ";
    }

    static String focusPrefix(CastingUxSemantics.FocusState focus) {
        return switch (focus) {
            case NONE -> "";
            case SELECTED -> "[S] ";
            case HOVERED -> "> ";
            case SELECTED_HOVERED -> ">[S] ";
        };
    }

    static String compactFocusPrefix(CastingUxSemantics.FocusState focus) {
        return switch (focus) {
            case NONE -> "";
            case SELECTED -> "S";
            case HOVERED -> ">";
            case SELECTED_HOVERED -> ">S";
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

    private Optional<ArcanaSpellId> focusedSpell() {
        int fallback = ClientInputController.selection().selectedSlot();
        int focused = ScreenFocusNavigation.presentationFocus(
                modality,
                hoveredSlot,
                keyboardFocusedSlot,
                fallback);
        if (focused >= 0 && focused < loadout.size()) {
            return Optional.of(loadout.get(focused));
        }
        return Optional.empty();
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
