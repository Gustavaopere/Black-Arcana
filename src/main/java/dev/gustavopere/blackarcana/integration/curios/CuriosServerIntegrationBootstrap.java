package dev.gustavopere.blackarcana.integration.curios;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.api.ArcanaIntegrationAvailability;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceSourceCategory;
import dev.gustavopere.blackarcana.core.hazard.ArcaneEquipmentSnapshotService;
import dev.gustavopere.blackarcana.core.hazard.ArcaneResistancePreviewRuntimeStore;
import dev.gustavopere.blackarcana.core.hazard.SnapshotArcaneResistancePreviewProvider;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerPlayer;
import net.neoforged.fml.ModList;

import java.util.List;
import java.util.Objects;

/** Loaded reflectively only after NeoForge confirms that Curios is installed. */
public final class CuriosServerIntegrationBootstrap {
    public static final String INSTALLED_FIRST_BASELINE = "9.5.1+1.21.1";

    private CuriosServerIntegrationBootstrap() { }

    public static void install(MinecraftServer server, ArcanaServerRuntime runtime) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(runtime, "runtime");

        String version = ModList.get().getModContainerById(CuriosHazardIntegration.MOD_ID)
            .map(container -> container.getModInfo().getVersion().toString())
            .orElse("unknown");
        CuriosEquipmentSnapshotAdapter adapter = CuriosEquipmentSnapshotAdapter.probe(
            true,
            CuriosServerIntegrationBootstrap.class.getClassLoader());
        ArcanaIntegrationAvailability availability = switch (adapter.availability()) {
            case AVAILABLE -> ArcanaIntegrationAvailability.AVAILABLE;
            case MISSING_MOD -> ArcanaIntegrationAvailability.MISSING_MOD;
            case API_INCOMPATIBLE -> ArcanaIntegrationAvailability.API_INCOMPATIBLE;
        };
        String diagnostic = availability == ArcanaIntegrationAvailability.API_INCOMPATIBLE
            ? "Curios API does not match the installed-first " + INSTALLED_FIRST_BASELINE + " snapshot contract"
            : "";
        CuriosHazardIntegration integration = new CuriosHazardIntegration(availability, version, diagnostic);
        runtime.integrations().register(integration);

        BlackArcanaMod.LOGGER.info(
            "Black Arcana integration {}: {} version={} baseline={}{}",
            integration.integrationId(),
            integration.availability(),
            integration.implementationVersion(),
            INSTALLED_FIRST_BASELINE,
            integration.diagnostic().isBlank() ? "" : " diagnostic=" + integration.diagnostic());

        if (!integration.available()) return;

        ArcaneEquipmentSnapshotService emptySnapshots =
            new ArcaneEquipmentSnapshotService(runtime.arcaneEquipmentProfiles());
        CuriosHazardResistanceProvider.SnapshotSource source = playerId -> {
            ServerPlayer player = server.getPlayerList().getPlayer(playerId);
            return player == null
                ? emptySnapshots.capture(List.of())
                : adapter.snapshot(player, runtime.arcaneEquipmentProfiles());
        };
        CuriosHazardResistanceProvider provider = new CuriosHazardResistanceProvider(source);
        runtime.arcaneResistanceProviders().register(provider);
        runtime.corruptionResistanceProviders().register(provider);
        ArcaneResistancePreviewRuntimeStore.register(
            runtime,
            new SnapshotArcaneResistancePreviewProvider(
                CuriosHazardResistanceProvider.PROVIDER_ID,
                "curios:equipped_containment",
                ArcaneResistanceSourceCategory.CURIO,
                source::snapshot));
    }
}
