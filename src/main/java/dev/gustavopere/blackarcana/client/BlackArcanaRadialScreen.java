package dev.gustavopere.blackarcana.client;

import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.network.ClientArcanaSyncState;
import dev.gustavopere.blackarcana.network.SpellPresentationPayload;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.network.chat.Component;
import org.lwjgl.glfw.GLFW;

import java.util.List;
import java.util.Map;

/** Compact selector only: choosing a wedge changes selection but never executes a cast. */
public final class BlackArcanaRadialScreen extends Screen {
    private static final double RADIUS = 78.0D;
    private static final double INNER_HIT_RADIUS = 28.0D;
    private static final double OUTER_HIT_RADIUS = 112.0D;
    private static final int SLOT_HALF_WIDTH = 45;
    private static final int SLOT_HALF_HEIGHT = 12;

    private final List<ArcanaSpellId> loadout;
    private final Map<ArcanaSpellId, SpellPresentationPayload.Entry> presentation;
    private int page;
    private int hoveredSlot = -1;

    private BlackArcanaRadialScreen() {
        super(Component.translatable("screen.black_arcana.radial"));
        this.loadout = ClientArcanaSyncState.loadoutSnapshot();
        this.presentation = ClientArcanaSyncState.presentationSnapshot();
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
        List<Integer> visible = RadialLayout.visibleSlots(loadout.size(), page);
        hoveredSlot = RadialLayout.hoveredSlot(
                loadout.size(), page, mouseX, mouseY, centerX, centerY,
                INNER_HIT_RADIUS, OUTER_HIT_RADIUS);

        for (int visibleIndex = 0; visibleIndex < visible.size(); visibleIndex++) {
            int slot = visible.get(visibleIndex);
            ArcanaSpellId spell = loadout.get(slot);
            RadialLayout.Point point = RadialLayout.slotCenter(
                    visibleIndex, visible.size(), centerX, centerY, RADIUS);
            int x = (int) Math.round(point.x());
            int y = (int) Math.round(point.y());
            boolean selected = slot == ClientInputController.selection().selectedSlot();
            boolean hovered = slot == hoveredSlot;
            int background = hovered ? 0xDD6B376D : selected ? 0xCC3D2748 : 0xB815101A;
            int border = hovered ? 0xFFF2D0F2 : selected ? 0xFFB991C0 : 0xFF5A4A60;
            graphics.fill(x - SLOT_HALF_WIDTH - 1, y - SLOT_HALF_HEIGHT - 1,
                    x + SLOT_HALF_WIDTH + 1, y + SLOT_HALF_HEIGHT + 1, border);
            graphics.fill(x - SLOT_HALF_WIDTH, y - SLOT_HALF_HEIGHT,
                    x + SLOT_HALF_WIDTH, y + SLOT_HALF_HEIGHT, background);

            String name = displayName(spell);
            graphics.drawCenteredString(font, (slot + 1) + " · " + name, x, y - 4, 0xFFFFFFFF);
        }

        graphics.drawCenteredString(font, title, centerX, centerY - 4, 0xFFEADCEA);
        if (RadialLayout.pageCount(loadout.size()) > 1) {
            Component pages = Component.translatable(
                    "screen.black_arcana.radial.page", page + 1, RadialLayout.pageCount(loadout.size()));
            graphics.drawCenteredString(font, pages, centerX, centerY + 10, 0xFFB9ABB9);
        }
        graphics.drawCenteredString(
                font,
                Component.translatable("screen.black_arcana.radial.hint"),
                centerX,
                height - 24,
                0xFFD0C6D0);
        super.render(graphics, mouseX, mouseY, partialTick);
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

    @Override
    public boolean isPauseScreen() {
        return false;
    }

    private String displayName(ArcanaSpellId spell) {
        SpellPresentationPayload.Entry entry = presentation.get(spell);
        String raw = entry == null
                ? spell.path().replace('_', ' ')
                : Component.translatable(entry.translationKey()).getString();
        return font.plainSubstrByWidth(raw, 70);
    }
}
