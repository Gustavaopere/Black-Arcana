package dev.gustavopere.blackarcana.network;

import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDangerTier;
import dev.gustavopere.blackarcana.api.hazard.ArcaneInsufficientResistancePolicy;

import java.util.Objects;

/** Server-authored, presentation-only resistance and predictable-gate projection for one selected spell. */
public record HazardResistanceForecastPayload(
    int protocolVersion,
    long requestId,
    String spellId,
    boolean available,
    String status,
    String dangerTier,
    String belowMinimumPolicy,
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
        BELOW_MINIMUM_ALLOWED,
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
            ArcaneInsufficientResistancePolicy.DENY_CAST.name(),
            effectiveArcaneResistance,
            minimumArcaneResistance,
            recommendedArcaneResistance,
            false,
            GateStatus.UNAVAILABLE.name());
    }

    /** Compatibility constructor for combined projections created before policy metadata was added. */
    public HazardResistanceForecastPayload(
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
        this(
            protocolVersion,
            requestId,
            spellId,
            available,
            status,
            dangerTier,
            ArcaneInsufficientResistancePolicy.DENY_CAST.name(),
            effectiveArcaneResistance,
            minimumArcaneResistance,
            recommendedArcaneResistance,
            gateForecastAvailable,
            gateStatus);
    }

    public HazardResistanceForecastPayload {
        ArcanaProtocol.requireCompatible(protocolVersion);
        if (requestId < 0L) throw new IllegalArgumentException("requestId cannot be negative");
        Objects.requireNonNull(spellId, "spellId");
        Objects.requireNonNull(status, "status");
        Objects.requireNonNull(dangerTier, "dangerTier");
        Objects.requireNonNull(belowMinimumPolicy, "belowMinimumPolicy");
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
        if (belowMinimumPolicy.isBlank()
            || belowMinimumPolicy.length() > ArcanaProtocol.MAX_HAZARD_POLICY_LENGTH) {
            throw new IllegalArgumentException("belowMinimumPolicy must be non-blank and bounded");
        }
        if (gateStatus.isBlank() || gateStatus.length() > ArcanaProtocol.MAX_RESULT_STATUS_LENGTH) {
            throw new IllegalArgumentException("gateStatus must be non-blank and bounded");
        }
        ArcanaSpellId.parse(spellId);
        Status parsedStatus = Status.valueOf(status);
        GateStatus parsedGateStatus = GateStatus.valueOf(gateStatus);
        ArcaneDangerTier parsedTier = ArcaneDangerTier.valueOf(dangerTier);
        ArcaneInsufficientResistancePolicy parsedPolicy =
            ArcaneInsufficientResistancePolicy.valueOf(belowMinimumPolicy);
        if (parsedTier == ArcaneDangerTier.NORMAL
            && parsedPolicy != ArcaneInsufficientResistancePolicy.DENY_CAST) {
            throw new IllegalArgumentException("NORMAL forecast cannot carry allow-with-risk policy");
        }
        if (parsedStatus == Status.BELOW_MINIMUM
            && parsedPolicy != ArcaneInsufficientResistancePolicy.DENY_CAST) {
            throw new IllegalArgumentException("blocked below-minimum status requires DENY_CAST policy");
        }
        if (parsedStatus == Status.BELOW_MINIMUM_ALLOWED
            && parsedPolicy != ArcaneInsufficientResistancePolicy.ALLOW_WITH_RISK) {
            throw new IllegalArgumentException("allowed below-minimum status requires ALLOW_WITH_RISK policy");
        }
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

    public ArcaneInsufficientResistancePolicy parsedBelowMinimumPolicy() {
        return ArcaneInsufficientResistancePolicy.valueOf(belowMinimumPolicy);
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
