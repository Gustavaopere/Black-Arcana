package dev.gustavopere.blackarcana.integration.irons;

import dev.gustavopere.blackarcana.api.ArcanaIntegration;
import dev.gustavopere.blackarcana.api.ArcanaIntegrationAvailability;
import dev.gustavopere.blackarcana.api.ArcanaIntegrationCapability;
import net.minecraft.server.MinecraftServer;

import java.util.Objects;
import java.util.Set;

/** Server-scoped descriptor and resource bridge for Iron's Spells 'n Spellbooks. */
public final class IronsIntegrationBridge implements ArcanaIntegration {
    public static final String MOD_ID = "irons_spellbooks";

    private static final String ABSTRACT_SPELL = "io.redspace.ironsspellbooks.api.spells.AbstractSpell";
    private static final String SPELL_REGISTRY = "io.redspace.ironsspellbooks.api.registry.SpellRegistry";
    private static final String CAST_EVENT = "io.redspace.ironsspellbooks.api.events.SpellOnCastEvent";

    private final ArcanaIntegrationAvailability availability;
    private final String version;
    private final String diagnostic;
    private final NeoForgeIronsManaAccess manaAccess;

    private IronsIntegrationBridge(
        ArcanaIntegrationAvailability availability,
        String version,
        String diagnostic,
        NeoForgeIronsManaAccess manaAccess
    ) {
        this.availability = Objects.requireNonNull(availability, "availability");
        this.version = normalizeVersion(version);
        this.diagnostic = Objects.requireNonNull(diagnostic, "diagnostic");
        this.manaAccess = manaAccess;
    }

    public static IronsIntegrationBridge probe(boolean modLoaded, String version, MinecraftServer server) {
        Objects.requireNonNull(server, "server");
        if (!modLoaded) {
            return new IronsIntegrationBridge(
                ArcanaIntegrationAvailability.MISSING_MOD,
                version,
                "Iron's Spells 'n Spellbooks is not loaded",
                null);
        }

        try {
            ClassLoader loader = IronsIntegrationBridge.class.getClassLoader();
            Class.forName(ABSTRACT_SPELL, false, loader);
            Class.forName(SPELL_REGISTRY, false, loader);
            Class.forName(CAST_EVENT, false, loader);
            NeoForgeIronsManaAccess access = NeoForgeIronsManaAccess.probe(server);
            return new IronsIntegrationBridge(
                ArcanaIntegrationAvailability.AVAILABLE,
                version,
                "",
                access);
        } catch (ReflectiveOperationException | LinkageError failure) {
            return new IronsIntegrationBridge(
                ArcanaIntegrationAvailability.API_INCOMPATIBLE,
                version,
                "Iron's 1.21.1 API probe failed: " + failure.getClass().getSimpleName(),
                null);
        }
    }

    @Override
    public String integrationId() {
        return MOD_ID;
    }

    @Override
    public boolean available() {
        return availability.usable();
    }

    @Override
    public String implementationVersion() {
        return version;
    }

    @Override
    public ArcanaIntegrationAvailability availability() {
        return availability;
    }

    @Override
    public Set<ArcanaIntegrationCapability> capabilities() {
        if (!available()) return Set.of();
        return Set.of(
            ArcanaIntegrationCapability.SPELL_HOST,
            ArcanaIntegrationCapability.RESOURCE_COST,
            ArcanaIntegrationCapability.MANA_RESOURCE);
    }

    @Override
    public String diagnostic() {
        return diagnostic;
    }

    public IronsManaAccess manaAccess() {
        if (!available() || manaAccess == null) {
            throw new IllegalStateException("Iron's mana access is unavailable: " + diagnostic);
        }
        return manaAccess;
    }

    private static String normalizeVersion(String version) {
        if (version == null || version.isBlank()) return "unknown";
        return version.length() > 96 ? version.substring(0, 96) : version;
    }
}
