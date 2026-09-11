package dev.gustavopere.blackarcana.network.neoforge;

import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class AstralProjectionNetworkWiringTest {
    private static final Path NETWORK_ROOT = Path.of(
            "src/main/java/dev/gustavopere/blackarcana/network/neoforge");
    private static final Path MAIN_ROOT = Path.of(
            "src/main/java/dev/gustavopere/blackarcana");

    @Test
    void astralNetworkingCarriesExactSessionIntentWithoutClientAuthority() throws IOException {
        Path movePath = NETWORK_ROOT.resolve("AstralProjectionMovePacket.java");
        Path returnPath = NETWORK_ROOT.resolve("AstralProjectionReturnPacket.java");
        Path viewPath = NETWORK_ROOT.resolve("AstralProjectionViewPacket.java");
        Path bridgePath = NETWORK_ROOT.resolve("AstralProjectionNetworkBridge.java");

        assertTrue(Files.exists(movePath), "Astral projection MOVE needs a dedicated bounded C2S payload");
        assertTrue(Files.exists(returnPath), "Astral projection RETURN needs an exact-session C2S payload");
        assertTrue(Files.exists(viewPath), "Astral projection BEGIN/END needs a server-authored S2C payload");
        assertTrue(Files.exists(bridgePath), "Astral projection transport needs its own bounded network bridge");

        String move = Files.readString(movePath);
        String returned = Files.readString(returnPath);
        String view = Files.readString(viewPath);
        String bridge = Files.readString(bridgePath);
        String runtime = Files.readString(MAIN_ROOT.resolve("integration/neoforge/MinecraftNoeticRuntime.java"));
        String mod = Files.readString(MAIN_ROOT.resolve("BlackArcanaMod.java"));

        assertTrue(move.contains("UUID projectionId"));
        assertTrue(move.contains("long sequence"));
        assertTrue(move.contains("float strafe"));
        assertTrue(move.contains("float forward"));
        assertTrue(move.contains("float vertical"));
        assertTrue(move.contains("float yaw"));
        assertTrue(move.contains("float pitch"));
        assertFalse(move.contains("casterId"), "Caster identity must come from the authenticated connection");
        assertFalse(move.contains("double x") || move.contains("double y") || move.contains("double z"),
                "MOVE must never accept client-authored absolute coordinates");

        assertTrue(returned.contains("UUID projectionId"));
        assertFalse(returned.contains("casterId"), "RETURN caster identity must come from the authenticated connection");

        assertTrue(view.contains("BEGIN"));
        assertTrue(view.contains("END"));
        assertTrue(view.contains("UUID projectionId"));
        assertTrue(view.contains("int projectionEntityId"));

        assertTrue(bridge.contains("playToServer(AstralProjectionMovePacket.TYPE"));
        assertTrue(bridge.contains("playToServer(AstralProjectionReturnPacket.TYPE"));
        assertTrue(bridge.contains("playToClient(AstralProjectionViewPacket.TYPE"));
        assertTrue(bridge.contains("context.player()"),
                "Serverbound handlers must derive the caster from the authenticated packet context");
        assertTrue(mod.contains("modEventBus.addListener(AstralProjectionNetworkBridge::register)"));
        assertTrue(runtime.contains("AstralProjectionNetworkBridge.sendBegin"));
        assertTrue(runtime.contains("AstralProjectionNetworkBridge.sendEnd"));
    }
}
