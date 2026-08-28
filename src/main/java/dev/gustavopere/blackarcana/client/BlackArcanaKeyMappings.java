package dev.gustavopere.blackarcana.client;

import net.minecraft.client.KeyMapping;
import net.neoforged.neoforge.client.event.RegisterKeyMappingsEvent;
import org.lwjgl.glfw.GLFW;

/** Client-only key mappings. Quick-slot bindings default to unbound to avoid pack conflicts. */
public final class BlackArcanaKeyMappings {
    public static final String CATEGORY = "key.categories.black_arcana";
    public static final KeyMapping OPEN_RADIAL = new KeyMapping(
            "key.black_arcana.open_radial", GLFW.GLFW_KEY_R, CATEGORY);
    public static final KeyMapping CAST_SELECTED = new KeyMapping(
            "key.black_arcana.cast_selected", GLFW.GLFW_KEY_V, CATEGORY);
    public static final KeyMapping EDIT_LOADOUT = new KeyMapping(
            "key.black_arcana.edit_loadout", GLFW.GLFW_KEY_UNKNOWN, CATEGORY);
    public static final KeyMapping[] QUICK_CAST = new KeyMapping[8];

    static {
        for (int index = 0; index < QUICK_CAST.length; index++) {
            QUICK_CAST[index] = new KeyMapping(
                    "key.black_arcana.quick_cast_" + (index + 1),
                    GLFW.GLFW_KEY_UNKNOWN,
                    CATEGORY);
        }
    }

    private BlackArcanaKeyMappings() { }

    public static void register(RegisterKeyMappingsEvent event) {
        event.register(OPEN_RADIAL);
        event.register(CAST_SELECTED);
        event.register(EDIT_LOADOUT);
        for (KeyMapping mapping : QUICK_CAST) event.register(mapping);
    }
}
