package dev.gustavopere.blackarcana.content.forbidden;

/** Fail-closed aggregate of the world facts required before a localized field may start. */
public record ForbiddenDomainAdmission(
        boolean chunksLoaded,
        boolean insideWorldBorder,
        boolean protectionAllowed,
        boolean safeRecoveryAvailable
) {
    public boolean admitted() {
        return chunksLoaded && insideWorldBorder && protectionAllowed && safeRecoveryAvailable;
    }
}
