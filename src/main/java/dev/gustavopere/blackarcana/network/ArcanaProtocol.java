package dev.gustavopere.blackarcana.network;

import dev.gustavopere.blackarcana.api.ArcanaCastRequest;

public final class ArcanaProtocol {
    public static final int VERSION = 1;
    public static final int MAX_CAST_ID_LENGTH = 36;
    public static final int MAX_RESOURCE_ID_LENGTH = 192;
    public static final int MAX_LOADOUT_SLOTS = ArcanaCastRequest.MAX_LOADOUT_SLOTS;
    public static final int MAX_TARGET_HINT_LENGTH = ArcanaCastRequest.MAX_TARGET_HINT_LENGTH;
    public static final int MAX_RESULT_STATUS_LENGTH = 48;
    public static final int MAX_RESULT_CODE_LENGTH = 64;
    public static final int MAX_RESULT_DETAIL_LENGTH = 256;
    public static final int MAX_TRANSLATION_KEY_LENGTH = 160;
    public static final int MAX_ICON_ID_LENGTH = 192;
    public static final int MAX_COOLDOWN_ENTRIES = 128;
    public static final int MAX_PRESENTATION_ENTRIES = 512;

    private ArcanaProtocol() { }

    public static void requireCompatible(int version) {
        if (version != VERSION) throw new IllegalArgumentException("unsupported Black Arcana protocol version: " + version);
    }
}
