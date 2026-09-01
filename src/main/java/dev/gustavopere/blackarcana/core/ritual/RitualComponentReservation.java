package dev.gustavopere.blackarcana.core.ritual;

import dev.gustavopere.blackarcana.api.ArcanaDecision;

import java.util.Objects;

public final class RitualComponentReservation {
    private enum State { RESERVED, COMMITTED, REFUNDED, DENIED }

    private final ArcanaDecision decision;
    private final Runnable commitAction;
    private final Runnable refundAction;
    private State state;

    private RitualComponentReservation(
            ArcanaDecision decision,
            Runnable commitAction,
            Runnable refundAction,
            State state
    ) {
        this.decision = Objects.requireNonNull(decision, "decision");
        this.commitAction = Objects.requireNonNull(commitAction, "commitAction");
        this.refundAction = Objects.requireNonNull(refundAction, "refundAction");
        this.state = Objects.requireNonNull(state, "state");
    }

    public static RitualComponentReservation reserved(Runnable commitAction, Runnable refundAction) {
        return new RitualComponentReservation(
                ArcanaDecision.allow(), commitAction, refundAction, State.RESERVED);
    }

    public static RitualComponentReservation denied(String code, String detail) {
        return new RitualComponentReservation(
                ArcanaDecision.deny(code, detail), () -> { }, () -> { }, State.DENIED);
    }

    public ArcanaDecision decision() {
        return decision;
    }

    public synchronized void commit() {
        if (state != State.RESERVED) return;
        commitAction.run();
        state = State.COMMITTED;
    }

    public synchronized void refund() {
        if (state != State.RESERVED) return;
        refundAction.run();
        state = State.REFUNDED;
    }
}
