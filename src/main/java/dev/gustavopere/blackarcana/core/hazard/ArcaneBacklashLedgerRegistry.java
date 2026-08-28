package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.hazard.ArcaneBacklashPolicy;
import dev.gustavopere.blackarcana.api.hazard.ArcaneBacklashSettlement;
import dev.gustavopere.blackarcana.api.hazard.ArcaneBacklashSnapshot;
import dev.gustavopere.blackarcana.api.hazard.ArcaneConfirmedDamage;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceSnapshot;

import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;

/** Per-server bounded registry of root-cast backlash ledgers. */
public final class ArcaneBacklashLedgerRegistry {
    public static final int ABSOLUTE_MAX_LEDGERS = ArcaneHazardSessionRegistry.ABSOLUTE_MAX_SESSIONS;

    private final int maxLedgers;
    private final Map<ArcanaCastId, ArcaneBacklashLedger> ledgers = new LinkedHashMap<>();

    public ArcaneBacklashLedgerRegistry(int maxLedgers) {
        if (maxLedgers <= 0 || maxLedgers > ABSOLUTE_MAX_LEDGERS) {
            throw new IllegalArgumentException("maxLedgers outside absolute bounds");
        }
        this.maxLedgers = maxLedgers;
    }

    public synchronized Optional<ArcaneBacklashLedger> open(
        ArcaneHazardSession session,
        ArcaneResistanceSnapshot resistance,
        ArcaneBacklashPolicy policy
    ) {
        Objects.requireNonNull(session, "session");
        Objects.requireNonNull(resistance, "resistance");
        Objects.requireNonNull(policy, "policy");
        pruneExpired(session.snapshot().activatedAtTick());
        ArcanaCastId castId = session.snapshot().rootCastId();
        if (session.closed() || ledgers.containsKey(castId) || ledgers.size() >= maxLedgers) {
            return Optional.empty();
        }
        ArcaneBacklashLedger ledger = new ArcaneBacklashLedger(
            session,
            new ArcaneBacklashSnapshot(session.snapshot(), resistance, policy));
        ledgers.put(castId, ledger);
        return Optional.of(ledger);
    }

    public synchronized Optional<ArcaneBacklashLedger> find(ArcanaCastId castId) {
        return Optional.ofNullable(ledgers.get(Objects.requireNonNull(castId, "castId")));
    }

    public synchronized ArcaneBacklashSettlement settle(ArcaneConfirmedDamage damage) {
        Objects.requireNonNull(damage, "damage");
        ArcaneBacklashLedger ledger = ledgers.get(damage.provenance().rootCastId());
        if (ledger == null) {
            return ArcaneBacklashSettlement.denied(damage.healthDamage(), "backlash_ledger_missing");
        }
        return ledger.settle(damage);
    }

    public synchronized boolean close(ArcanaCastId castId) {
        return ledgers.remove(Objects.requireNonNull(castId, "castId")) != null;
    }

    public synchronized int pruneExpired(long currentTick) {
        if (currentTick < 0L) throw new IllegalArgumentException("currentTick cannot be negative");
        int removed = 0;
        Iterator<ArcaneBacklashLedger> iterator = ledgers.values().iterator();
        while (iterator.hasNext()) {
            ArcaneBacklashLedger ledger = iterator.next();
            if (ledger.snapshot().hazard().activatedAtTick() > currentTick
                || currentTick >= ledger.snapshot().hazard().activatedAtTick()
                    + ledger.snapshot().hazard().profile().damageLeaseTicks()) {
                iterator.remove();
                removed++;
            }
        }
        return removed;
    }

    public synchronized int size() {
        return ledgers.size();
    }
}
