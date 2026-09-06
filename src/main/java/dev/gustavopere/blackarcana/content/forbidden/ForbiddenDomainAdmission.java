package dev.gustavopere.blackarcana.content.forbidden;

/** Fail-closed aggregate of the world facts required before a localized field may start. */
public record ForbiddenDomainAdmission(
        boolean chunksLoaded,
        boolean insideWorldBorder,
        boolean protectionAllowed,
        boolean worldEffectAllowed,
        boolean safeRecoveryAvailable
) {
    /**
     * Convenience form for callers that only have the four world-admission facts.
     * Missing recovery evidence is unknown, therefore it fails closed. The Minecraft adapter uses the
     * canonical five-argument form after explicitly proving recovery safety.
     */
    public ForbiddenDomainAdmission(
            boolean chunksLoaded,
            boolean insideWorldBorder,
            boolean protectionAllowed,
            boolean worldEffectAllowed
    ) {
        this(chunksLoaded, insideWorldBorder, protectionAllowed, worldEffectAllowed, false);
    }

    public boolean admitted() {
        return chunksLoaded
                && insideWorldBorder
                && protectionAllowed
                && worldEffectAllowed
                && safeRecoveryAvailable;
    }
}
