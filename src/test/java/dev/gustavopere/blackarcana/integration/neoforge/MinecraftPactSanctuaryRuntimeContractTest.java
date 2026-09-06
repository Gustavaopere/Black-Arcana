package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.content.noetic.FamiliarOwnershipRegistry;
import dev.gustavopere.blackarcana.content.noetic.PactSanctuarySpec;
import net.minecraft.server.MinecraftServer;
import org.junit.jupiter.api.Test;

import java.util.Set;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;

class MinecraftPactSanctuaryRuntimeContractTest {
    @Test
    void sanctuaryRuntimeExposesBoundedServerAuthoritativeSurface() throws Exception {
        MinecraftPactSanctuaryRuntime runtime = new MinecraftPactSanctuaryRuntime(new FamiliarOwnershipRegistry(4));
        assertNotNull(runtime);

        assertEquals(ArcanaDecision.class,
                MinecraftPactSanctuaryRuntime.class.getMethod(
                        "activate",
                        MinecraftServer.class,
                        UUID.class,
                        UUID.class,
                        PactSanctuarySpec.class,
                        Set.class).getReturnType());
        assertEquals(int.class,
                MinecraftPactSanctuaryRuntime.class.getMethod("tick", MinecraftServer.class).getReturnType());
        assertEquals(int.class,
                MinecraftPactSanctuaryRuntime.class.getMethod("activeSanctuaries", MinecraftServer.class).getReturnType());
        assertEquals(int.class,
                MinecraftPactSanctuaryRuntime.class.getMethod(
                        "clearEntity", MinecraftServer.class, UUID.class).getReturnType());
        assertEquals(int.class,
                MinecraftPactSanctuaryRuntime.class.getMethod(
                        "clearForServerStop", MinecraftServer.class).getReturnType());
    }
}
