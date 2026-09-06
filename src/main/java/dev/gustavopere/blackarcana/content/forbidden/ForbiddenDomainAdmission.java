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
     * Compatibility convenience for callers that only need the four world-admission facts.
     * The Minecraft adapter uses the canonical five-argument form and proves recovery separately.
     */
    public ForbiddenDomainAdmission(
            boolean chunksLoaded,
            boolean insideWorldBorder,
            boolean protectionAllowed,
            boolean worldEffectAllowed
    ) {
        this(chunksLoaded, insideWorldBorder, protectionAllowed, worldEffectAllowed, true);
    }

    public boolean admitted() {
        return chunksLoaded
                && insideWorldBorder
                && protectionAllowed
                && worldEffectAllowed
                && safeRecoveryAvailable;
    }
}
