package dev.gustavopere.blackarcana.api;

/** Why an optional integration is or is not usable in the current runtime. */
public enum ArcanaIntegrationAvailability {
    AVAILABLE(true),
    MISSING_MOD(false),
    API_INCOMPATIBLE(false),
    DISABLED(false);

    private final boolean usable;

    ArcanaIntegrationAvailability(boolean usable) {
        this.usable = usable;
    }

    public boolean usable() {
        return usable;
    }
}
