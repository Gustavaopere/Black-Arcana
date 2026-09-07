package dev.gustavopere.blackarcana.integration.ars;

import dev.gustavopere.blackarcana.api.ArcanaIntegration;
import dev.gustavopere.blackarcana.api.ArcanaIntegrationAvailability;
import dev.gustavopere.blackarcana.api.ArcanaIntegrationCapability;
import dev.gustavopere.blackarcana.content.noetic.FamiliarOwnershipProvider;
import net.minecraft.server.MinecraftServer;

import java.util.EnumSet;
import java.util.Objects;
import java.util.Optional;
import java.util.Set;

/** Server-scoped Ars Nouveau resource and familiar-ownership bridge. */
public final class ArsIntegrationBridge implements ArcanaIntegration {
    public static final String MOD_ID = "ars_nouveau";
    private static final String API_MANA = "com.hollingsworth.arsnouveau.api.mana.IManaCap";
    private static final String API_FAMILIAR = "com.hollingsworth.arsnouveau.api.familiar.IFamiliar";

    private final ArcanaIntegrationAvailability availability;
    private final String version;
    private final String diagnostic;
    private final NeoForgeArsManaAccess manaAccess;
    private final FamiliarOwnershipProvider familiarOwnershipProvider;

    private ArsIntegrationBridge(
        ArcanaIntegrationAvailability availability,
        String version,
        String diagnostic,
        NeoForgeArsManaAccess manaAccess,
        FamiliarOwnershipProvider familiarOwnershipProvider
    ) {
        this.availability = Objects.requireNonNull(availability, "availability");
        this.version = normalizeVersion(version);
        this.diagnostic = Objects.requireNonNull(diagnostic, "diagnostic");
        this.manaAccess = manaAccess;
        this.familiarOwnershipProvider = familiarOwnershipProvider;
    }

    public static ArsIntegrationBridge probe(boolean modLoaded, String version, MinecraftServer server) {
        Objects.requireNonNull(server, "server");
        if (!modLoaded) {
            return new ArsIntegrationBridge(
                ArcanaIntegrationAvailability.MISSING_MOD,
                version,
                "Ars Nouveau is not loaded",
                null,
                null);
        }
        try {
            Class.forName(API_MANA, false, ArsIntegrationBridge.class.getClassLoader());
            NeoForgeArsManaAccess access = NeoForgeArsManaAccess.probe(server);

            FamiliarOwnershipProvider familiarProvider = null;
            String familiarDiagnostic = "";
            try {
                Class.forName(API_FAMILIAR, false, ArsIntegrationBridge.class.getClassLoader());
                familiarProvider = new ArsFamiliarOwnershipProvider();
            } catch (ReflectiveOperationException | LinkageError failure) {
                familiarDiagnostic = "Ars familiar ownership API unavailable: " + failure.getClass().getSimpleName();
            }

            return new ArsIntegrationBridge(
                ArcanaIntegrationAvailability.AVAILABLE,
                version,
                familiarDiagnostic,
                access,
                familiarProvider);
        } catch (ReflectiveOperationException | LinkageError failure) {
            return new ArsIntegrationBridge(
                ArcanaIntegrationAvailability.API_INCOMPATIBLE,
                version,
                "Ars Nouveau 1.21.1 API probe failed: " + failure.getClass().getSimpleName(),
                null,
                null);
        }
    }

    @Override public String integrationId() { return MOD_ID; }
    @Override public boolean available() { return availability.usable(); }
    @Override public String implementationVersion() { return version; }
    @Override public ArcanaIntegrationAvailability availability() { return availability; }
    @Override public String diagnostic() { return diagnostic; }

    @Override
    public Set<ArcanaIntegrationCapability> capabilities() {
        if (!available()) return Set.of();
        EnumSet<ArcanaIntegrationCapability> capabilities = EnumSet.of(
            ArcanaIntegrationCapability.RESOURCE_COST,
            ArcanaIntegrationCapability.MANA_RESOURCE);
        if (familiarOwnershipProvider != null) {
            capabilities.add(ArcanaIntegrationCapability.FAMILIAR_OWNERSHIP);
        }
        return Set.copyOf(capabilities);
    }

    public ArsManaAccess manaAccess() {
        if (!available() || manaAccess == null) {
            throw new IllegalStateException("Ars mana access is unavailable: " + diagnostic);
        }
        return manaAccess;
    }

    public Optional<FamiliarOwnershipProvider> familiarOwnershipProvider() {
        if (!available()) return Optional.empty();
        return Optional.ofNullable(familiarOwnershipProvider);
    }

    private static String normalizeVersion(String version) {
        if (version == null || version.isBlank()) return "unknown";
        return version.length() > 96 ? version.substring(0, 96) : version;
    }
}
