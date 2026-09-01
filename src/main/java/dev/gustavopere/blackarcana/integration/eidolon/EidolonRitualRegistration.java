package dev.gustavopere.blackarcana.integration.eidolon;

import alexthw.eidolon_repraised.api.ritual.Ritual;
import alexthw.eidolon_repraised.registries.RitualRegistry;

/** Public-API-only registration of Black Arcana rituals into Eidolon's host. */
public final class EidolonRitualRegistration {
    private static boolean registered;

    private EidolonRitualRegistration() { }

    public static synchronized void register() {
        registerOwned(
            EidolonIntegrationIds.PROBE_RITUAL_ID,
            EidolonArcanaProbeRitual.class,
            EidolonArcanaProbeRitual::new);
        registerOwned(
            EidolonIntegrationIds.ANCHOR_ATTUNEMENT_RITUAL_ID,
            EidolonAnchorAttunementRitual.class,
            EidolonAnchorAttunementRitual::new);
        registered = true;
    }

    private static <T extends Ritual> void registerOwned(
        net.minecraft.resources.ResourceLocation id,
        Class<T> expectedType,
        java.util.function.Supplier<T> factory
    ) {
        Ritual existing = RitualRegistry.find(id);
        if (existing != null) {
            if (!expectedType.isInstance(existing)) {
                throw new IllegalStateException("Eidolon ritual id is already owned by another implementation: " + id);
            }
            return;
        }
        RitualRegistry.register(id, factory.get());
    }

    public static synchronized boolean isRegistered() {
        return registered
            && RitualRegistry.find(EidolonIntegrationIds.PROBE_RITUAL_ID) instanceof EidolonArcanaProbeRitual
            && RitualRegistry.find(EidolonIntegrationIds.ANCHOR_ATTUNEMENT_RITUAL_ID) instanceof EidolonAnchorAttunementRitual;
    }
}
