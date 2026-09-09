package dev.gustavopere.blackarcana.client;

import dev.gustavopere.blackarcana.api.ArcanaCastResult;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDangerTier;
import dev.gustavopere.blackarcana.network.HazardResistanceForecastPayload;

import java.util.Objects;

/**
 * Pure client-presentation semantics for Stage 05.08/05.09.
 *
 * <p>This class maps facts the client already legitimately owns or has received from the server into
 * surface-neutral semantic roles. It performs no gameplay admission, world queries, provider calls or
 * resource/cooldown inference.</p>
 */
public final class CastingUxSemantics {
    public enum FocusState {
        NONE,
        SELECTED,
        HOVERED,
        FOCUSED,
        SELECTED_HOVERED,
        SELECTED_FOCUSED,
        HOVERED_FOCUSED,
        SELECTED_HOVERED_FOCUSED
    }

    public enum AdmissionState {
        FORECAST_CLEAR,
        FORECAST_BLOCKED,
        FORECAST_UNAVAILABLE,
        CAST_DENIED,
        CAST_FAILED,
        CAST_SUCCEEDED
    }

    public enum HazardState {
        NONE,
        DANGER_PRESENT,
        BELOW_MINIMUM,
        BELOW_RECOMMENDED,
        RECOMMENDATION_MET,
        FORECAST_UNAVAILABLE
    }

    public enum LoadoutMembership {
        NOT_INCLUDED,
        ACCEPTED,
        DRAFT_ADDED,
        DRAFT_REMOVED
    }

    private CastingUxSemantics() { }

    public static FocusState focus(boolean selected, boolean hovered) {
        return focus(selected, hovered, false);
    }

    public static FocusState focus(boolean selected, boolean hovered, boolean focused) {
        if (selected && hovered && focused) return FocusState.SELECTED_HOVERED_FOCUSED;
        if (selected && hovered) return FocusState.SELECTED_HOVERED;
        if (selected && focused) return FocusState.SELECTED_FOCUSED;
        if (hovered && focused) return FocusState.HOVERED_FOCUSED;
        if (selected) return FocusState.SELECTED;
        if (hovered) return FocusState.HOVERED;
        if (focused) return FocusState.FOCUSED;
        return FocusState.NONE;
    }

    public static AdmissionState admissionForGate(HazardResistanceForecastPayload.GateStatus status) {
        Objects.requireNonNull(status, "status");
        return switch (status) {
            case CLEAR -> AdmissionState.FORECAST_CLEAR;
            case UNAVAILABLE -> AdmissionState.FORECAST_UNAVAILABLE;
            case IDENTITY, PROGRESSION, COOLDOWN, COST -> AdmissionState.FORECAST_BLOCKED;
        };
    }

    public static AdmissionState admissionForResult(ArcanaCastResult.Status status) {
        Objects.requireNonNull(status, "status");
        return switch (status) {
            case SUCCESS -> AdmissionState.CAST_SUCCEEDED;
            case EFFECT_FAILED -> AdmissionState.CAST_FAILED;
            case DENIED_INGRESS,
                    DENIED_IDENTITY,
                    DENIED_REPLAY,
                    DENIED_CHANNEL,
                    DENIED_PROGRESSION,
                    DENIED_COOLDOWN,
                    DENIED_TARGET,
                    DENIED_COST,
                    DENIED_WORLD_POLICY,
                    DENIED_HAZARD -> AdmissionState.CAST_DENIED;
        };
    }

    public static HazardState hazardForTier(ArcaneDangerTier tier) {
        Objects.requireNonNull(tier, "tier");
        return tier == ArcaneDangerTier.NORMAL ? HazardState.NONE : HazardState.DANGER_PRESENT;
    }

    public static HazardState hazardForResistance(HazardResistanceForecastPayload.Status status) {
        Objects.requireNonNull(status, "status");
        return switch (status) {
            case NORMAL -> HazardState.NONE;
            case BELOW_MINIMUM -> HazardState.BELOW_MINIMUM;
            case BELOW_RECOMMENDED -> HazardState.BELOW_RECOMMENDED;
            case RECOMMENDED -> HazardState.RECOMMENDATION_MET;
            case UNAVAILABLE -> HazardState.FORECAST_UNAVAILABLE;
        };
    }

    public static LoadoutMembership loadoutMembership(boolean accepted, boolean draft) {
        if (accepted && draft) return LoadoutMembership.ACCEPTED;
        if (accepted) return LoadoutMembership.DRAFT_REMOVED;
        if (draft) return LoadoutMembership.DRAFT_ADDED;
        return LoadoutMembership.NOT_INCLUDED;
    }
}
