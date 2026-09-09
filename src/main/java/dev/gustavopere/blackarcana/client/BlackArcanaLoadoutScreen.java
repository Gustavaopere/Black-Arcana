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
    private int keyboardFocusedIndex = -1;
    private int lastRowsPerPage = -1;
    private ScreenFocusNavigation.InputModality modality = ScreenFocusNavigation.InputModality.KEYBOARD;
    private int lastMouseX = Integer.MIN_VALUE;
    private int lastMouseY = Integer.MIN_VALUE;

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
    public void render(GuiGraphics graphics, int mouseX, int mouseY, float partialTick) {
        graphics.fill(0, 0, width, height, 0x77000000);
        LoadoutLayout layout = LoadoutLayout.forViewport(width, height);
        ensureFocusForLayout(layout);
        int left = layout.left();
        int top = layout.top();
        int panelWidth = layout.panelWidth();
        int rowsPerPage = layout.rowsPerPage();
        int rowHeight = layout.rowHeight();

        graphics.fill(left - 8, top - 24, left + panelWidth + 8,
                top + rowsPerPage * rowHeight + 48, 0xE0100C14);
        graphics.drawCenteredString(font, title, width / 2, top - 16, 0xFFF0E4F0);

        boolean pointerMoved = lastMouseX != Integer.MIN_VALUE
                && (mouseX != lastMouseX || mouseY != lastMouseY);
        lastMouseX = mouseX;
        lastMouseY = mouseY;

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
            if (hovered) hoveredIndex = index;
            boolean keyboardFocused = modality == ScreenFocusNavigation.InputModality.KEYBOARD
                    && index == keyboardFocusedIndex;
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
            if (keyboardFocused) {
                graphics.fill(left + panelWidth - 2, y, left + panelWidth, y + rowHeight - 2, 0xFFFFE8FF);
            }
            String fixedPrefix = keyboardFocusPrefix(keyboardFocused) + membershipPrefix(membership);
            int maxTextWidth = Math.max(1, panelWidth - 16);
            int nameWidth = Math.max(1, maxTextWidth - font.width(fixedPrefix));
            String label = font.plainSubstrByWidth(fixedPrefix + displayName(spell, nameWidth), maxTextWidth);
            graphics.drawString(font, label, left + 8, y + textOffsetY, 0xFFFFFFFF, false);
        }

        if (pointerMoved && hoveredIndex >= 0) {
            modality = ScreenFocusNavigation.InputModality.POINTER;
        }

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

        int tooltipIndex = ScreenFocusNavigation.presentationFocus(
                modality,
                hoveredIndex,
                keyboardFocusedIndex,
                -1);
        if (tooltipIndex >= 0 && tooltipIndex < available.size()) {
            Component tooltip = hazardTooltip(hazards.get(available.get(tooltipIndex))).orElse(null);
            if (tooltip != null) {
                if (modality == ScreenFocusNavigation.InputModality.POINTER) {
                    graphics.renderTooltip(font, tooltip, mouseX, mouseY);
                } else {
                    int row = tooltipIndex - start;
                    int tooltipY = top + Math.max(0, row) * rowHeight;
                    graphics.renderTooltip(font, tooltip, left + panelWidth - 4, tooltipY);
                }
            }
        }
    }

    @Override
    public boolean mouseClicked(double mouseX, double mouseY, int button) {
        if (button == GLFW.GLFW_MOUSE_BUTTON_LEFT) {
            LoadoutLayout layout = LoadoutLayout.forViewport(width, height);
            ensureFocusForLayout(layout);
            int left = layout.left();
            int top = layout.top();
            int panelWidth = layout.panelWidth();
            int rowsPerPage = layout.rowsPerPage();
            int rowHeight = layout.rowHeight();
            if (mouseX >= left && mouseX <= left + panelWidth && mouseY >= top) {
                int row = (int) ((mouseY - top) / rowHeight);
                int index = page * rowsPerPage + row;
                if (row >= 0 && row < rowsPerPage && index < available.size()) {
                    modality = ScreenFocusNavigation.InputModality.POINTER;
                    draft.toggle(available.get(index));
                    return true;
                }
            }
        }
        return super.mouseClicked(mouseX, mouseY, button);
    }

    @Override
    public boolean keyPressed(int keyCode, int scanCode, int modifiers) {
        if (keyCode == GLFW.GLFW_KEY_ESCAPE) {
            onClose();
            return true;
        }
        if (keyCode == GLFW.GLFW_KEY_ENTER || keyCode == GLFW.GLFW_KEY_KP_ENTER) {
            apply();
            return true;
        }
        if (keyCode == GLFW.GLFW_KEY_BACKSPACE || keyCode == GLFW.GLFW_KEY_DELETE) {
            draft.clear();
            return true;
        }

        LoadoutLayout layout = LoadoutLayout.forViewport(width, height);
        ensureFocusForLayout(layout);
        List<Integer> visible = ScreenFocusNavigation.pageIndices(available.size(), page, layout.rowsPerPage());
        if (isDraftToggleKey(keyCode)) {
            if (keyboardFocusedIndex >= 0 && keyboardFocusedIndex < available.size()) {
                modality = ScreenFocusNavigation.InputModality.KEYBOARD;
                draft.toggle(available.get(keyboardFocusedIndex));
                return true;
            }
            return super.keyPressed(keyCode, scanCode, modifiers);
        }
        if (keyCode == GLFW.GLFW_KEY_UP) {
            keyboardFocusedIndex = ScreenFocusNavigation.moveClamped(visible, keyboardFocusedIndex, -1);
            modality = ScreenFocusNavigation.InputModality.KEYBOARD;
            return true;
        }
        if (keyCode == GLFW.GLFW_KEY_DOWN) {
            keyboardFocusedIndex = ScreenFocusNavigation.moveClamped(visible, keyboardFocusedIndex, 1);
            modality = ScreenFocusNavigation.InputModality.KEYBOARD;
            return true;
        }
        if (keyCode == GLFW.GLFW_KEY_LEFT || keyCode == GLFW.GLFW_KEY_PAGE_UP) {
            movePage(layout, -1);
            return true;
        }
        if (keyCode == GLFW.GLFW_KEY_RIGHT || keyCode == GLFW.GLFW_KEY_PAGE_DOWN) {
            movePage(layout, 1);
            return true;
        }
        return super.keyPressed(keyCode, scanCode, modifiers);
    }

    private void ensureFocusForLayout(LoadoutLayout layout) {
        int rowsPerPage = layout.rowsPerPage();
        if (lastRowsPerPage != rowsPerPage) {
            if (keyboardFocusedIndex >= 0 && keyboardFocusedIndex < available.size()) {
                page = layout.clampPage(available.size(), keyboardFocusedIndex / rowsPerPage);
            }
            lastRowsPerPage = rowsPerPage;
        }
        page = layout.clampPage(available.size(), page);
        List<Integer> visible = ScreenFocusNavigation.pageIndices(available.size(), page, rowsPerPage);
        if (!visible.contains(keyboardFocusedIndex)) {
            int firstAccepted = visible.stream()
                    .filter(index -> accepted.contains(available.get(index)))
                    .findFirst()
                    .orElse(-1);
            keyboardFocusedIndex = ScreenFocusNavigation.initialFocus(visible, firstAccepted);
        }
    }

    private void movePage(LoadoutLayout layout, int delta) {
        List<Integer> source = ScreenFocusNavigation.pageIndices(
                available.size(), page, layout.rowsPerPage());
        page = Math.max(0, Math.min(layout.pageCount(available.size()) - 1, page + delta));
        List<Integer> destination = ScreenFocusNavigation.pageIndices(
                available.size(), page, layout.rowsPerPage());
        keyboardFocusedIndex = ScreenFocusNavigation.transitionFocus(
                source,
                destination,
                keyboardFocusedIndex,
                -1);
        modality = ScreenFocusNavigation.InputModality.KEYBOARD;
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

    static Optional<Component> hazardTooltip(HazardPreflightPayload.Entry entry) {
        return entry == null ? Optional.empty() : Optional.of(BlackArcanaHudLayer.preflightLine(entry));
    }

    static boolean isDraftToggleKey(int keyCode) {
        return keyCode == GLFW.GLFW_KEY_SPACE;
    }

    static String keyboardFocusPrefix(boolean focused) {
        return focused ? "[F] " : "";
    }

    static String membershipPrefix(CastingUxSemantics.LoadoutMembership membership) {
        return switch (membership) {
            case NOT_INCLUDED -> "[ ] ";
            case ACCEPTED -> "[x] ";
            case DRAFT_ADDED -> "[+] ";
            case DRAFT_REMOVED -> "[-] ";
        };
    }

    private String displayName(ArcanaSpellId spell, int maxWidth) {
        SpellPresentationPayload.Entry entry = presentation.get(spell);
        String raw = entry == null
                ? spell.path().replace('_', ' ')
                : Component.translatable(entry.translationKey()).getString();
        return font.plainSubstrByWidth(raw, Math.max(1, maxWidth));
    }
}
