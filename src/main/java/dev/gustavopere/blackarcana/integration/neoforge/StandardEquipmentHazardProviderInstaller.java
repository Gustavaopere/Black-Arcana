package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.core.hazard.ArcaneEquipmentHazardResistanceProvider;
import dev.gustavopere.blackarcana.core.hazard.ArcaneEquipmentSnapshotService;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerPlayer;

import java.util.List;
import java.util.Objects;

/** Installs the standard player-equipment snapshot provider into both hazard resistance channels. */
public final class StandardEquipmentHazardProviderInstaller {
    private StandardEquipmentHazardProviderInstaller() { }

    public static void install(MinecraftServer server, ArcanaServerRuntime runtime) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(runtime, "runtime");
        MinecraftStandardEquipmentSnapshotAdapter adapter =
            new MinecraftStandardEquipmentSnapshotAdapter(runtime.arcaneEquipmentProfiles());
        install(runtime, playerId -> {
            ServerPlayer player = server.getPlayerList().getPlayer(playerId);
            if (player == null) {
                return new ArcaneEquipmentSnapshotService(runtime.arcaneEquipmentProfiles()).capture(List.of());
            }
            return adapter.snapshot(player);
        });
    }

    static void install(
        ArcanaServerRuntime runtime,
        ArcaneEquipmentHazardResistanceProvider.SnapshotSource source
    ) {
        Objects.requireNonNull(runtime, "runtime");
        Objects.requireNonNull(source, "source");
        ArcaneEquipmentHazardResistanceProvider provider =
            new ArcaneEquipmentHazardResistanceProvider(source);
        runtime.arcaneResistanceProviders().register(provider);
        runtime.corruptionResistanceProviders().register(provider);
    }
}
