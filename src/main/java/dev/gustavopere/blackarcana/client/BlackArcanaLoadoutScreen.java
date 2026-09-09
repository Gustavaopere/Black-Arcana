package dev.gustavopere.blackarcana.client;

import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.network.ArcanaProtocol;
import dev.gustavopere.blackarcana.network.ClientArcanaSyncState;
import dev.gustavopere.blackarcana.network.HazardPreflightPayload;
import dev.gustavopere.blackarcana.network.LoadoutUpdatePayload;
import dev.gustavopere.blackarcana.network.SpellPresentationPayload;
import dev.gustavopere.blackarcana.network.neoforge.LoadoutNetworkBridge;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.network.chat.Component;
import org.lwjgl.glfw.GLFW;

import java.util.Comparator;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.Set;

/** Client-only draft editor. Apply sends intent; the server response remains canonical. */
public final class BlackArcanaLoadoutScreen extends Screen {
    private final Map<ArcanaSpellId, SpellPresentationPayload.Entry> presentation;
    private final Map<ArcanaSpellId, HazardPreflightPayload.Entry> hazards;
    private final List<ArcanaSpellId> available;
    private final Set<ArcanaSpellId> accepted;
    private final LoadoutDraft draft;
    private int page;
    private int focusedIndex = -1;
    private KeyboardFocusNavigation.InputModality inputModality = KeyboardFocusNavigation.InputModality.KEYBOARD;
    private boolean pointerSeeded;
    private int lastMouseX;
    private int lastMouseY;

    private BlackArcanaLoadoutScreen() {
        super(Component.translatable("screen.black_arcana.loadout"));
        presentation = ClientArcanaSyncState.presentationSnapshot();
        hazards = ClientArcanaSyncState.hazardPreflightSnapshot();
        available = presentation.keySet().stream()
                .sorted(Comparator.comparing(ArcanaSpellId::canonical))
                .toList();
        List<ArcanaSpellId> acceptedLoadout = ClientArcanaSyncState.loadoutSnapshot();
        accepted = Set.copyOf(acceptedLoadout);
        draft = new LoadoutDraft(acceptedLoadout);
    }

    public static void open() {
        Minecraft minecraft = Minecraft.getInstance();
        if (minecraft.screen == null && minecraft.player != null && minecraft.getConnection() != null) {
            minecraft.setScreen(new BlackArcanaLoadoutScreen());
        }
    }

    @Override
    protected void init() {
        super.init();
        LoadoutLayout layout = LoadoutLayout.forViewport(width, height);
        if (available.isEmpty()) {
            page = 0;
            focusedIndex = -1;
            return;
        }

        if (focusedIndex >= 0 && focusedIndex < available.size()) {
            page = layout.clampPage(available.size(), focusedIndex / layout.rowsPerPage());
            return;
        }

        page = layout.clampPage(available.size(), page);
        int preferred = firstVisibleAcceptedIndex(layout);
        focusedIndex = KeyboardFocusNavigation.loadoutInitialFocus(
                available.size(), page, layout.rowsPerPage(), preferred);
    }

    @Override
    public void render(GuiGraphics graphics, int mouseX, int mouseY, float partialTick) {
        graphics.fill(0, 0, width, height, 0x77000000);
        LoadoutLayout layout = LoadoutLayout.forViewport(width, height);
        page = layout.clampPage(available.size(), page);
        int left = layout.left();
        int top = layout.top();
        int panelWidth = layout.panelWidth();
        int rowsPerPage = layout.rowsPerPage();
        int rowHeight = layout.rowHeight();

        graphics.fill(left - 8, top - 24, left + panelWidth + 8,
                top + rowsPerPage * rowHeight + 48, 0xE0100C14);
        graphics.drawCenteredString(font, title, width / 2, top - 16, 0xFFF0E4F0);

        Component pointerTooltip = null;
        int hoveredIndex = -1;
        int start = page * rowsPerPage;
        int end = Math.min(available.size(), start + rowsPerPage);
        int textOffsetY = Math.max(2, (rowHeight - font.lineHeight) / 2);
        for (int index = start; index < end; index++) {
            ArcanaSpellId spell = available.get(index);
            int row = index - start;
            int y = top + row * rowHeight;
            boolean chosen = draft.contains(spell);
            CastingUxSemantics.LoadoutMembership membership = CastingUxSemantics.loadoutMembership(
                    accepted.contains(spell), chosen);
            boolean hovered = mouseX >= left && mouseX <= left + panelWidth
                    && mouseY >= y && mouseY < y + rowHeight - 2;
            boolean focused = index == focusedIndex;
            int background = switch (membership) {
                case NOT_INCLUDED -> 0xAA1A141E;
                case ACCEPTED -> 0xCC33223A;
                case DRAFT_ADDED -> 0xCC423049;
                case DRAFT_REMOVED -> 0xCC241A28;
            };
            graphics.fill(left, y, left + panelWidth, y + rowHeight - 2, background);
            if (hovered) {
                graphics.fill(left, y, left + 2, y + rowHeight - 2, 0xFFF2D0F2);
            }
            if (focused) {
                graphics.fill(left + 3, y, left + 5, y + rowHeight - 2, 0xFF9DD9FF);
            }
            String prefix = (focused ? "[F] " : "") + membershipPrefix(membership);
            graphics.drawString(font, prefix + displayName(spell, panelWidth),
                    left + 8, y + textOffsetY, 0xFFFFFFFF, false);
            if (hovered) {
                hoveredIndex = index;
                pointerTooltip = hazardTooltip(hazards.get(spell)).orElse(null);
            }
        }
        updatePointerModality(mouseX, mouseY, hoveredIndex >= 0);

        int pages = layout.pageCount(available.size());
        graphics.drawCenteredString(font,
                Component.translatable("screen.black_arcana.loadout.page", page + 1, pages),
                width / 2,
                top + rowsPerPage * rowHeight + 4,
                0xFFBFAFBF);
        graphics.drawCenteredString(font,
                Component.translatable("screen.black_arcana.loadout.hint", draft.snapshot().size()),
                width / 2,
                top + rowsPerPage * rowHeight + 20,
                0xFFD8CCD8);
        super.render(graphics, mouseX, mouseY, partialTick);

        Component tooltip = pointerTooltip;
        int tooltipX = mouseX;
        int tooltipY = mouseY;
        if (inputModality == KeyboardFocusNavigation.InputModality.KEYBOARD
                && focusedIndex >= start && focusedIndex < end) {
            tooltip = hazardTooltip(hazards.get(available.get(focusedIndex))).orElse(null);
            tooltipX = left + panelWidth;
            tooltipY = top + (focusedIndex - start) * rowHeight + rowHeight / 2;
        }
        if (tooltip != null) {
            graphics.renderTooltip(font, tooltip, tooltipX, tooltipY);
        }
    }

    @Override
    public boolean mouseClicked(double mouseX, double mouseY, int button) {
        if (button == GLFW.GLFW_MOUSE_BUTTON_LEFT) {
            LoadoutLayout layout = LoadoutLayout.forViewport(width, height);
            page = layout.clampPage(available.size(), page);
            int left = layout.left();
            int top = layout.top();
            int panelWidth = layout.panelWidth();
            int rowsPerPage = layout.rowsPerPage();
            int rowHeight = layout.rowHeight();
            if (mouseX >= left && mouseX <= left + panelWidth && mouseY >= top) {
                int row = (int) ((mouseY - top) / rowHeight);
                int index = page * rowsPerPage + row;
                if (row >= 0 && row < rowsPerPage && index < available.size()) {
                    inputModality = KeyboardFocusNavigation.InputModality.POINTER;
                    draft.toggle(available.get(index));
                    return true;
                }
            }
        }
        return super.mouseClicked(mouseX, mouseY, button);
    }

    @Override
    public boolean keyPressed(int keyCode, int scanCode, int modifiers) {
        if (keyCode == GLFW.GLFW_KEY_ENTER || keyCode == GLFW.GLFW_KEY_KP_ENTER) {
            inputModality = KeyboardFocusNavigation.InputModality.KEYBOARD;
            apply();
            return true;
        }
        if (keyCode == GLFW.GLFW_KEY_BACKSPACE || keyCode == GLFW.GLFW_KEY_DELETE) {
            inputModality = KeyboardFocusNavigation.InputModality.KEYBOARD;
            draft.clear();
            return true;
        }

        LoadoutLayout layout = LoadoutLayout.forViewport(width, height);
        page = layout.clampPage(available.size(), page);
        if (keyCode == GLFW.GLFW_KEY_UP) {
            inputModality = KeyboardFocusNavigation.InputModality.KEYBOARD;
            focusedIndex = KeyboardFocusNavigation.loadoutMoveRow(
                    available.size(), page, layout.rowsPerPage(), focusedIndex, -1);
            return focusedIndex >= 0 || !available.isEmpty();
        }
        if (keyCode == GLFW.GLFW_KEY_DOWN) {
            inputModality = KeyboardFocusNavigation.InputModality.KEYBOARD;
            focusedIndex = KeyboardFocusNavigation.loadoutMoveRow(
                    available.size(), page, layout.rowsPerPage(), focusedIndex, 1);
            return focusedIndex >= 0 || !available.isEmpty();
        }
        if (keyCode == GLFW.GLFW_KEY_SPACE) {
            inputModality = KeyboardFocusNavigation.InputModality.KEYBOARD;
            return toggleFocusedDraft(focusedIndex, available, draft);
        }
        if (keyCode == GLFW.GLFW_KEY_LEFT || keyCode == GLFW.GLFW_KEY_PAGE_UP) {
            changePage(layout, -1);
            return true;
        }
        if (keyCode == GLFW.GLFW_KEY_RIGHT || keyCode == GLFW.GLFW_KEY_PAGE_DOWN) {
            changePage(layout, 1);
            return true;
        }
        return super.keyPressed(keyCode, scanCode, modifiers);
    }

    @Override
    public boolean isPauseScreen() {
        return false;
    }

    private void apply() {
        LoadoutNetworkBridge.requestUpdate(new LoadoutUpdatePayload(
                ArcanaProtocol.VERSION,
                draft.snapshot().stream().map(ArcanaSpellId::canonical).toList()));
        onClose();
    }

    static boolean toggleFocusedDraft(
            int focusedIndex,
            List<ArcanaSpellId> available,
            LoadoutDraft draft
    ) {
        if (focusedIndex < 0 || focusedIndex >= available.size()) return false;
        return draft.toggle(available.get(focusedIndex));
    }

    static Optional<Component> hazardTooltip(HazardPreflightPayload.Entry entry) {
        return entry == null ? Optional.empty() : Optional.of(BlackArcanaHudLayer.preflightLine(entry));
    }

    static String membershipPrefix(CastingUxSemantics.LoadoutMembership membership) {
        return switch (membership) {
            case NOT_INCLUDED -> "[ ] ";
            case ACCEPTED -> "[x] ";
            case DRAFT_ADDED -> "[+] ";
            case DRAFT_REMOVED -> "[-] ";
        };
    }

    private void changePage(LoadoutLayout layout, int direction) {
        inputModality = KeyboardFocusNavigation.InputModality.KEYBOARD;
        int destination = layout.clampPage(available.size(), page + direction);
        if (destination == page) return;
        focusedIndex = KeyboardFocusNavigation.loadoutFocusAfterPageChange(
                available.size(), page, destination, layout.rowsPerPage(), focusedIndex);
        page = destination;
    }

    private int firstVisibleAcceptedIndex(LoadoutLayout layout) {
        int start = page * layout.rowsPerPage();
        int end = Math.min(available.size(), start + layout.rowsPerPage());
        for (int index = start; index < end; index++) {
            if (accepted.contains(available.get(index))) return index;
        }
        return -1;
    }

    private void updatePointerModality(int mouseX, int mouseY, boolean overInteractiveRow) {
        if (!pointerSeeded) {
            pointerSeeded = true;
        } else if (overInteractiveRow && (mouseX != lastMouseX || mouseY != lastMouseY)) {
            inputModality = KeyboardFocusNavigation.InputModality.POINTER;
        }
        lastMouseX = mouseX;
        lastMouseY = mouseY;
    }

    private String displayName(ArcanaSpellId spell, int panelWidth) {
        SpellPresentationPayload.Entry entry = presentation.get(spell);
        String raw = entry == null
                ? spell.path().replace('_', ' ')
                : Component.translatable(entry.translationKey()).getString();
        return font.plainSubstrByWidth(raw, Math.max(1, panelWidth - 50));
    }
}
