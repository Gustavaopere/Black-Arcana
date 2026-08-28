package dev.gustavopere.blackarcana.integration.eidolon;

import alexthw.eidolon_repraised.api.ritual.Ritual;
import alexthw.eidolon_repraised.registries.RitualRegistry;

/** Public-API-only registration of Black Arcana rituals into Eidolon's host. */
public final class EidolonRitualRegistration {
    private static boolean registered;

    private EidolonRitualRegistration() { }

    public static synchronized void register() {
        Ritual existing = RitualRegistry.find(EidolonIntegrationIds.PROBE_RITUAL_ID);
        if (existing != null) {
            if (!(existing instanceof EidolonArcanaProbeRitual)) {
                throw new IllegalStateException("Eidolon ritual id is already owned by another implementation");
            }
            registered = true;
            return;
        }
        RitualRegistry.register(
            EidolonIntegrationIds.PROBE_RITUAL_ID,
            new EidolonArcanaProbeRitual());
        registered = true;
    }

    public static synchronized boolean isRegistered() {
        return registered
            && RitualRegistry.find(EidolonIntegrationIds.PROBE_RITUAL_ID) instanceof EidolonArcanaProbeRitual;
    }
}
