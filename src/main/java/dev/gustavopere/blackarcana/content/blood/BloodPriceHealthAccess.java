package dev.gustavopere.blackarcana.content.blood;

import dev.gustavopere.blackarcana.api.ArcanaServices.CostReservation;

import java.util.UUID;

/**
 * Server-owned access to real health for Blood Price.
 *
 * Implementations must not consume absorption or temporary-health buffers. A reservation
 * must revalidate the minimum remaining-health floor at mutation time and be refundable
 * until committed by the canonical cast transaction.
 */
public interface BloodPriceHealthAccess {
    double currentHealth(UUID casterId);

    CostReservation reserve(UUID casterId, double amount, double minimumRemainingHealth);
}
