package dev.gustavopere.blackarcana.integration.malum;

import dev.gustavopere.blackarcana.api.ArcanaIntegration;
import dev.gustavopere.blackarcana.api.ArcanaIntegrationAvailability;
import dev.gustavopere.blackarcana.api.ArcanaIntegrationCapability;
import net.minecraft.server.MinecraftServer;

import java.util.Objects;
import java.util.Set;

/** Server-scoped Malum spirit-resource bridge. */
public final class MalumIntegrationBridge implements ArcanaIntegration {
    private final ArcanaIntegrationAvailability availability;
    private final String version;
    private final String diagnostic;
    private final NeoForgeMalumSpiritInventoryAccess spiritAccess;

    private MalumIntegrationBridge(
        ArcanaIntegrationAvailability availability,
        String version,
        String diagnostic,
        NeoForgeMalumSpiritInventoryAccess spiritAccess
    ) {
        this.availability = Objects.requireNonNull(availability, "availability");
        this.version = normalizeVersion(version);
        this.diagnostic = Objects.requireNonNull(diagnostic, "diagnostic");
        this.spiritAccess = spiritAccess;
    }

    public static MalumIntegrationBridge probe(boolean modLoaded, String version, MinecraftServer server) {
        if (!modLoaded) {
            return new MalumIntegrationBridge(
                ArcanaIntegrationAvailability.MISSING_MOD,
                version,
                "Malum is not loaded",
                null);
        }
        Objects.requireNonNull(server, "server");
        try {
            NeoForgeMalumSpiritInventoryAccess access = NeoForgeMalumSpiritInventoryAccess.probe(server);
            return new MalumIntegrationBridge(
                ArcanaIntegrationAvailability.AVAILABLE,
                version,
                "",
                access);
        } catch (ReflectiveOperationException | RuntimeException | LinkageError failure) {
            return new MalumIntegrationBridge(
                ArcanaIntegrationAvailability.API_INCOMPATIBLE,
                version,
                "Malum 1.21.1 spirit probe failed: " + failure.getClass().getSimpleName(),
                null);
        }
    }

    @Override public String integrationId() { return MalumIntegrationIds.MOD_ID; }
    @Override public boolean available() { return availability.usable(); }
    @Override public String implementationVersion() { return version; }
    @Override public ArcanaIntegrationAvailability availability() { return availability; }
    @Override public String diagnostic() { return diagnostic; }

    @Override
    public Set<ArcanaIntegrationCapability> capabilities() {
        if (!available()) return Set.of();
        return Set.of(
            ArcanaIntegrationCapability.RESOURCE_COST,
            ArcanaIntegrationCapability.SOUL_RESOURCE);
    }

    public MalumSpiritAccess spiritAccess() {
        if (!available() || spiritAccess == null) {
            throw new IllegalStateException("Malum spirit access is unavailable: " + diagnostic);
        }
        return spiritAccess;
    }

    private static String normalizeVersion(String version) {
        if (version == null || version.isBlank()) return "unknown";
        return version.length() > 96 ? version.substring(0, 96) : version;
    }
}
