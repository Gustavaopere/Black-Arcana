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

/** Client-only draft editor. Apply sends intent; the server response remains canonical. */
public final class BlackArcanaLoadoutScreen extends Screen {
    private final Map<ArcanaSpellId, SpellPresentationPayload.Entry> presentation;
    private final Map<ArcanaSpellId, HazardPreflightPayload.Entry> hazards;
    private final List<ArcanaSpellId> available;
    private final LoadoutDraft draft;
    private int page;

    private BlackArcanaLoadoutScreen() {
        super(Component.translatable("screen.black_arcana.loadout"));
        presentation = ClientArcanaSyncState.presentationSnapshot();
        hazards = ClientArcanaSyncState.hazardPreflightSnapshot();
        available = presentation.keySet().stream()
                .sorted(Comparator.comparing(ArcanaSpellId::canonical))
                .toList();
        draft = new LoadoutDraft(ClientArcanaSyncState.loadoutSnapshot());
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
        page = layout.clampPage(available.size(), page);
        int left = layout.left();
        int top = layout.top();
        int panelWidth = layout.panelWidth();
        int rowsPerPage = layout.rowsPerPage();
        int rowHeight = layout.rowHeight();

        graphics.fill(left - 8, top - 24, left + panelWidth + 8,
                top + rowsPerPage * rowHeight + 48, 0xE0100C14);
        graphics.drawCenteredString(font, title, width / 2, top - 16, 0xFFF0E4F0);

        Component hoveredTooltip = null;
        int start = page * rowsPerPage;
        int end = Math.min(available.size(), start + rowsPerPage);
        int textOffsetY = Math.max(2, (rowHeight - font.lineHeight) / 2);
        for (int index = start; index < end; index++) {
            ArcanaSpellId spell = available.get(index);
            int row = index - start;
            int y = top + row * rowHeight;
            boolean chosen = draft.contains(spell);
            boolean hovered = mouseX >= left && mouseX <= left + panelWidth
                    && mouseY >= y && mouseY < y + rowHeight - 2;
            int background = hovered ? 0xDD4E3155 : chosen ? 0xCC33223A : 0xAA1A141E;
            graphics.fill(left, y, left + panelWidth, y + rowHeight - 2, background);
            String prefix = chosen ? "[x] " : "[ ] ";
            graphics.drawString(font, prefix + displayName(spell, panelWidth),
                    left + 8, y + textOffsetY, 0xFFFFFFFF, false);
            if (hovered) {
                hoveredTooltip = hazardTooltip(hazards.get(spell)).orElse(null);
            }
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
        if (hoveredTooltip != null) {
            graphics.renderTooltip(font, hoveredTooltip, mouseX, mouseY);
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
            apply();
            return true;
        }
        if (keyCode == GLFW.GLFW_KEY_BACKSPACE || keyCode == GLFW.GLFW_KEY_DELETE) {
            draft.clear();
            return true;
        }
        LoadoutLayout layout = LoadoutLayout.forViewport(width, height);
        page = layout.clampPage(available.size(), page);
        if (keyCode == GLFW.GLFW_KEY_LEFT || keyCode == GLFW.GLFW_KEY_PAGE_UP) {
            page = Math.max(0, page - 1);
            return true;
        }
        if (keyCode == GLFW.GLFW_KEY_RIGHT || keyCode == GLFW.GLFW_KEY_PAGE_DOWN) {
            page = Math.min(layout.pageCount(available.size()) - 1, page + 1);
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

    static Optional<Component> hazardTooltip(HazardPreflightPayload.Entry entry) {
        return entry == null ? Optional.empty() : Optional.of(BlackArcanaHudLayer.preflightLine(entry));
    }

    private String displayName(ArcanaSpellId spell, int panelWidth) {
        SpellPresentationPayload.Entry entry = presentation.get(spell);
        String raw = entry == null
                ? spell.path().replace('_', ' ')
                : Component.translatable(entry.translationKey()).getString();
        return font.plainSubstrByWidth(raw, Math.max(1, panelWidth - 50));
    }
}
