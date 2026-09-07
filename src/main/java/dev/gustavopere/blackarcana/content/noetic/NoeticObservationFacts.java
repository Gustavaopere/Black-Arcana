package dev.gustavopere.blackarcana.content.noetic;

/** Server-derived admission facts only; client assertions never populate this record authoritatively. */
public record NoeticObservationFacts(
        boolean targetLoaded,
        boolean sameDimension,
        boolean withinRange,
        boolean lineOfSight,
        boolean targetAlive,
        boolean targetPlayer,
        boolean explicitConsent,
        boolean ownedFamiliar
) { }
