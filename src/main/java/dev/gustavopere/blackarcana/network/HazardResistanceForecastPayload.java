package dev.gustavopere.blackarcana.network;

import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDangerTier;

import java.util.Objects;

/** Server-authored, presentation-only resistance and predictable-gate projection for one selected spell. */
public record HazardResistanceForecastPayload(
    int protocolVersion,
    long requestId,
    String spellId,
    boolean available,
    String status,
    String dangerTier,
    double effectiveArcaneResistance,
    double minimumArcaneResistance,
    double recommendedArcaneResistance,
    boolean gateForecastAvailable,
    String gateStatus
) {
    public enum Status {
        UNAVAILABLE,
        NORMAL,
        BELOW_MINIMUM,
        BELOW_RECOMMENDED,
        RECOMMENDED
    }

    public enum GateStatus {
        UNAVAILABLE,
        CLEAR,
        IDENTITY,
        PROGRESSION,
        COOLDOWN,
        COST
    }

    /** Compatibility constructor for resistance-only callers while the combined projection is being populated. */
    public HazardResistanceForecastPayload(
        int protocolVersion,
        long requestId,
        String spellId,
        boolean available,
        String status,
        String dangerTier,
        double effectiveArcaneResistance,
        double minimumArcaneResistance,
        double recommendedArcaneResistance
    ) {
        this(
            protocolVersion,
            requestId,
            spellId,
            available,
            status,
            dangerTier,
            effectiveArcaneResistance,
            minimumArcaneResistance,
            recommendedArcaneResistance,
            false,
            GateStatus.UNAVAILABLE.name());
    }

    public HazardResistanceForecastPayload {
        ArcanaProtocol.requireCompatible(protocolVersion);
        if (requestId < 0L) throw new IllegalArgumentException("requestId cannot be negative");
        Objects.requireNonNull(spellId, "spellId");
        Objects.requireNonNull(status, "status");
        Objects.requireNonNull(dangerTier, "dangerTier");
        Objects.requireNonNull(gateStatus, "gateStatus");
        if (spellId.isBlank() || spellId.length() > ArcanaProtocol.MAX_RESOURCE_ID_LENGTH) {
            throw new IllegalArgumentException("spellId must be non-blank and bounded");
        }
        if (status.isBlank() || status.length() > ArcanaProtocol.MAX_RESULT_STATUS_LENGTH) {
            throw new IllegalArgumentException("status must be non-blank and bounded");
        }
        if (dangerTier.isBlank() || dangerTier.length() > ArcanaProtocol.MAX_DANGER_TIER_LENGTH) {
            throw new IllegalArgumentException("dangerTier must be non-blank and bounded");
        }
        if (gateStatus.isBlank() || gateStatus.length() > ArcanaProtocol.MAX_RESULT_STATUS_LENGTH) {
            throw new IllegalArgumentException("gateStatus must be non-blank and bounded");
        }
        ArcanaSpellId.parse(spellId);
        Status parsedStatus = Status.valueOf(status);
        GateStatus parsedGateStatus = GateStatus.valueOf(gateStatus);
        ArcaneDangerTier.valueOf(dangerTier);
        if (available == (parsedStatus == Status.UNAVAILABLE)) {
            throw new IllegalArgumentException("availability and status disagree");
        }
        if (gateForecastAvailable == (parsedGateStatus == GateStatus.UNAVAILABLE)) {
            throw new IllegalArgumentException("gate forecast availability and status disagree");
        }
        validateResistance("effectiveArcaneResistance", effectiveArcaneResistance);
        validateResistance("minimumArcaneResistance", minimumArcaneResistance);
        validateResistance("recommendedArcaneResistance", recommendedArcaneResistance);
        if (minimumArcaneResistance > recommendedArcaneResistance) {
            throw new IllegalArgumentException("minimum resistance cannot exceed recommended resistance");
        }
    }

    public ArcanaSpellId parsedSpellId() {
        return ArcanaSpellId.parse(spellId);
    }

    public Status parsedStatus() {
        return Status.valueOf(status);
    }

    public ArcaneDangerTier parsedTier() {
        return ArcaneDangerTier.valueOf(dangerTier);
    }

    public GateStatus parsedGateStatus() {
        return GateStatus.valueOf(gateStatus);
    }

    private static void validateResistance(String name, double value) {
        if (!Double.isFinite(value) || value < 0.0D || value > ArcanaProtocol.MAX_HAZARD_RESISTANCE_HINT) {
            throw new IllegalArgumentException(name + " outside protocol bounds");
        }
    }
}
