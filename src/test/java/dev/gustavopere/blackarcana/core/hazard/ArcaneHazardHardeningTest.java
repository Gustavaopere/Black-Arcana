package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.api.hazard.*;
import org.junit.jupiter.api.Test;

import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.EnumMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.stream.IntStream;

import static org.junit.jupiter.api.Assertions.*;

class ArcaneHazardHardeningTest {
    private static final UUID CASTER = UUID.fromString("70000000-0000-0000-0000-000000000001");
    private static final ArcanaSpellId SPELL = ArcanaSpellId.parse("black_arcana:hardening_probe");

    @Test
    void everyCanonicalEligibleDamageFamilySettlesAndBacklashStaysTerminal() {
        ArcaneBacklashLedger ledger = ledger(cast("families"), 10L, 100L, 32, true);
        List<ArcaneDamageFamily> eligible = List.of(
                ArcaneDamageFamily.DIRECT,
                ArcaneDamageFamily.PROJECTILE,
                ArcaneDamageFamily.DAMAGE_OVER_TIME,
                ArcaneDamageFamily.CHAIN,
                ArcaneDamageFamily.OWNED_SUMMON);

        for (int i = 0; i < eligible.size(); i++) {
            ArcaneBacklashSettlement settlement = ledger.settle(damage(
                    cast("families"), "family-" + i, eligible.get(i), 2.0D, true, 20L));
            assertEquals(ArcaneBacklashSettlement.Status.SETTLED, settlement.status());
            assertEquals(2.0D, settlement.backlashDamage(), 0.0D);
        }

        ArcaneBacklashSettlement recursive = ledger.settle(damage(
                cast("families"), "backlash", ArcaneDamageFamily.ARCANE_BACKLASH, 50.0D, false, 20L));
        assertEquals(ArcaneBacklashSettlement.Status.IGNORED, recursive.status());
        assertEquals("backlash_non_recursive", recursive.code());
        assertEquals(10.0D, ledger.confirmedEligibleDamage(), 0.0D);
        assertEquals(10.0D, ledger.backlashSettled(), 0.0D);
    }

    @Test
    void delayedDamageIsAcceptedBeforeLeaseAndFailsClosedAtBoundary() {
        ArcanaCastId cast = cast("lease");
        ArcaneBacklashLedger ledger = ledger(cast, 10L, 20L, 8, false);

        assertEquals(ArcaneBacklashSettlement.Status.SETTLED,
                ledger.settle(damage(cast, "before-expiry", ArcaneDamageFamily.DIRECT, 1.0D, true, 29L)).status());
        ArcaneBacklashSettlement expired = ledger.settle(
                damage(cast, "at-expiry", ArcaneDamageFamily.DAMAGE_OVER_TIME, 1.0D, true, 30L));
        assertEquals(ArcaneBacklashSettlement.Status.DENIED, expired.status());
        assertEquals("hazard_claim_expired", expired.code());
    }

    @Test
    void damageBeforeRootActivationFailsClosedWithoutConsumingLedger() {
        ArcanaCastId cast = cast("pre-activation");
        ArcaneBacklashLedger ledger = ledger(cast, 100L, 20L, 8, false);

        ArcaneBacklashSettlement beforeActivation = ledger.settle(
                damage(cast, "before-activation", ArcaneDamageFamily.PROJECTILE, 4.0D, true, 99L));
        assertEquals(ArcaneBacklashSettlement.Status.DENIED, beforeActivation.status());
        assertEquals("hazard_claim_not_active", beforeActivation.code());
        assertEquals(0.0D, ledger.confirmedEligibleDamage(), 0.0D);
        assertEquals(0.0D, ledger.backlashSettled(), 0.0D);

        ArcaneBacklashSettlement atActivation = ledger.settle(
                damage(cast, "at-activation", ArcaneDamageFamily.PROJECTILE, 4.0D, true, 100L));
        assertEquals(ArcaneBacklashSettlement.Status.SETTLED, atActivation.status());
        assertEquals(4.0D, ledger.confirmedEligibleDamage(), 0.0D);
        assertEquals(4.0D, ledger.backlashSettled(), 0.0D);
    }

    @Test
    void hazardClaimDenialCodeIsLocaleIndependent() {
        Locale original = Locale.getDefault();
        try {
            Locale.setDefault(Locale.forLanguageTag("tr-TR"));
            ArcanaCastId cast = cast("locale-independent-code");
            ArcaneBacklashLedger ledger = ledger(cast, 100L, 20L, 8, false);

            ArcaneBacklashSettlement denied = ledger.settle(
                    damage(cast, "locale-before-activation", ArcaneDamageFamily.DIRECT, 1.0D, true, 99L));

            assertEquals(ArcaneBacklashSettlement.Status.DENIED, denied.status());
            assertEquals("hazard_claim_not_active", denied.code());
        } finally {
            Locale.setDefault(original);
        }
    }

    @Test
    void concurrentRootSessionOpenIsDeterministicAndBounded() {
        int capacity = 512;
        ArcaneHazardSessionRegistry registry = new ArcaneHazardSessionRegistry(capacity);
        AtomicInteger opened = new AtomicInteger();

        IntStream.range(0, capacity).parallel().forEach(i -> {
            ArcaneHazardSnapshot snapshot = snapshot(cast("root-" + i), 100L, 200L, 8);
            if (registry.open(snapshot).opened()) opened.incrementAndGet();
        });

        assertEquals(capacity, opened.get());
        assertEquals(capacity, registry.size());
        var overflow = registry.open(snapshot(cast("overflow"), 100L, 200L, 8));
        assertFalse(overflow.opened());
        assertEquals("hazard_session_capacity", overflow.code());
        assertEquals(capacity, registry.pruneExpired(300L));
        assertEquals(0, registry.size());
    }

    @Test
    void simultaneousRootSessionOverflowAdmitsExactlyCapacity() throws Exception {
        int capacity = 8;
        int attempts = 24;
        ArcaneHazardSessionRegistry registry = new ArcaneHazardSessionRegistry(capacity);
        CountDownLatch ready = new CountDownLatch(attempts);
        CountDownLatch start = new CountDownLatch(1);
        ExecutorService pool = Executors.newFixedThreadPool(attempts);
        List<Future<ArcaneHazardSessionRegistry.OpenResult>> futures = new ArrayList<>(attempts);

        try {
            for (int i = 0; i < attempts; i++) {
                int attempt = i;
                futures.add(pool.submit(() -> {
                    ready.countDown();
                    if (!start.await(5, TimeUnit.SECONDS)) {
                        throw new IllegalStateException("concurrent session start barrier timed out");
                    }
                    return registry.open(snapshot(cast("overflow-race-" + attempt), 100L, 200L, 8));
                }));
            }

            assertTrue(ready.await(5, TimeUnit.SECONDS), "workers did not reach the start barrier");
            start.countDown();

            int opened = 0;
            int capacityDenied = 0;
            for (Future<ArcaneHazardSessionRegistry.OpenResult> future : futures) {
                ArcaneHazardSessionRegistry.OpenResult result = future.get(5, TimeUnit.SECONDS);
                if (result.opened()) {
                    opened++;
                } else {
                    assertEquals("hazard_session_capacity", result.code());
                    capacityDenied++;
                }
            }

            assertEquals(capacity, opened);
            assertEquals(attempts - capacity, capacityDenied);
            assertEquals(capacity, registry.size());
        } finally {
            start.countDown();
            pool.shutdownNow();
            assertTrue(pool.awaitTermination(5, TimeUnit.SECONDS), "worker pool did not terminate");
        }
    }

    @Test
    void simultaneousClaimsForSameDamageInstanceAreExactlyOnce() throws Exception {
        ArcanaCastId cast = cast("same-damage-race");
        ArcaneHazardSession session = new ArcaneHazardSession(snapshot(cast, 100L, 200L, 8));
        ArcanaDamageProvenance shared = new ArcanaDamageProvenance(
                cast,
                ArcanaDamageInstanceId.parse(namedUuid("shared-damage-instance").toString()),
                CASTER,
                SPELL,
                ArcaneDamageFamily.DIRECT,
                true);
        int contenders = 24;
        CountDownLatch ready = new CountDownLatch(contenders);
        CountDownLatch start = new CountDownLatch(1);
        ExecutorService pool = Executors.newFixedThreadPool(contenders);
        List<Future<ArcaneHazardSession.ClaimResult>> futures = new ArrayList<>(contenders);

        try {
            for (int i = 0; i < contenders; i++) {
                futures.add(pool.submit(() -> {
                    ready.countDown();
                    if (!start.await(5, TimeUnit.SECONDS)) {
                        throw new IllegalStateException("concurrent claim start barrier timed out");
                    }
                    return session.claim(shared, 101L);
                }));
            }

            assertTrue(ready.await(5, TimeUnit.SECONDS), "workers did not reach the start barrier");
            start.countDown();

            int accepted = 0;
            int duplicates = 0;
            for (Future<ArcaneHazardSession.ClaimResult> future : futures) {
                ArcaneHazardSession.ClaimResult result = future.get(5, TimeUnit.SECONDS);
                if (result == ArcaneHazardSession.ClaimResult.ACCEPTED) {
                    accepted++;
                } else {
                    assertEquals(ArcaneHazardSession.ClaimResult.DUPLICATE, result);
                    duplicates++;
                }
            }

            assertEquals(1, accepted);
            assertEquals(contenders - 1, duplicates);
            assertEquals(1, session.seenDamageInstances());
        } finally {
            start.countDown();
            pool.shutdownNow();
            assertTrue(pool.awaitTermination(5, TimeUnit.SECONDS), "worker pool did not terminate");
        }
    }

    @Test
    void twoHundredConcurrentSettlementsRemainExactlyOnceAndLinear() {
        ArcanaCastId cast = cast("concurrent-settlement");
        ArcaneBacklashLedger ledger = ledger(cast, 10L, 1_000L, 256, false);
        AtomicInteger settled = new AtomicInteger();

        IntStream.range(0, 200).parallel().forEach(i -> {
            ArcaneBacklashSettlement result = ledger.settle(damage(
                    cast, "hit-" + i, ArcaneDamageFamily.DIRECT, 1.0D, true, 20L));
            if (result.status() == ArcaneBacklashSettlement.Status.SETTLED) settled.incrementAndGet();
        });

        assertEquals(200, settled.get());
        assertEquals(200.0D, ledger.confirmedEligibleDamage(), 0.0D);
        assertEquals(200.0D, ledger.backlashSettled(), 0.0D);

        ArcaneBacklashSettlement duplicate = ledger.settle(damage(
                cast, "hit-0", ArcaneDamageFamily.DIRECT, 1.0D, true, 21L));
        assertEquals(ArcaneBacklashSettlement.Status.DENIED, duplicate.status());
        assertEquals("hazard_claim_duplicate", duplicate.code());
        assertEquals(200.0D, ledger.backlashSettled(), 0.0D);
    }

    private static ArcaneBacklashLedger ledger(
            ArcanaCastId cast,
            long startTick,
            long leaseTicks,
            int maxDamageInstances,
            boolean allowOwnedSummon
    ) {
        ArcaneHazardSnapshot snapshot = snapshot(cast, startTick, leaseTicks, maxDamageInstances);
        ArcaneHazardSession session = new ArcaneHazardSession(snapshot);
        ArcaneBacklashPolicy policy = new ArcaneBacklashPolicy(
                allowOwnedSummon, 0.0D, 1_000_000.0D, 1_000_000.0D);
        return new ArcaneBacklashLedger(
                session,
                new ArcaneBacklashSnapshot(snapshot, zeroResistance(), policy));
    }

    private static ArcaneHazardSnapshot snapshot(
            ArcanaCastId cast,
            long startTick,
            long leaseTicks,
            int maxDamageInstances
    ) {
        return new ArcaneHazardSnapshot(
                cast,
                SPELL,
                CASTER,
                "minecraft:overworld",
                startTick,
                new ArcaneDangerProfile(
                        ArcaneDangerTier.FORBIDDEN,
                        1.0D,
                        0.25D,
                        0.25D,
                        leaseTicks,
                        maxDamageInstances));
    }

    private static ArcaneConfirmedDamage damage(
            ArcanaCastId cast,
            String seed,
            ArcaneDamageFamily family,
            double healthDamage,
            boolean hazardEligible,
            long tick
    ) {
        return new ArcaneConfirmedDamage(
                new ArcanaDamageProvenance(
                        cast,
                        ArcanaDamageInstanceId.parse(namedUuid("damage-" + seed).toString()),
                        CASTER,
                        SPELL,
                        family,
                        hazardEligible),
                healthDamage,
                tick);
    }

    private static ArcanaCastId cast(String seed) {
        return ArcanaCastId.parse(namedUuid("cast-" + seed).toString());
    }

    private static UUID namedUuid(String seed) {
        return UUID.nameUUIDFromBytes(seed.getBytes(StandardCharsets.UTF_8));
    }

    private static ArcaneResistanceSnapshot zeroResistance() {
        Map<ArcaneResistanceSourceCategory, Double> categories = new EnumMap<>(ArcaneResistanceSourceCategory.class);
        for (ArcaneResistanceSourceCategory category : ArcaneResistanceSourceCategory.values()) {
            categories.put(category, 0.0D);
        }
        return new ArcaneResistanceSnapshot(
                0.0D,
                1.0D,
                100.0D,
                1_000.0D,
                List.of(),
                categories,
                List.of());
    }
}
