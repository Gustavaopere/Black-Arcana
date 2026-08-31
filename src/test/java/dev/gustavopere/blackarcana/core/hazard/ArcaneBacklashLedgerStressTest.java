package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.api.hazard.*;
import org.junit.jupiter.api.Test;

import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.EnumMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.TimeUnit;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ArcaneBacklashLedgerStressTest {
    private static final UUID CASTER = UUID.fromString("74000000-0000-0000-0000-000000000001");
    private static final ArcanaSpellId SPELL = ArcanaSpellId.parse("black_arcana:ledger_stress_probe");

    @Test
    void concurrentRootsDelayedSettlementsAndCapacityReclamationStayBounded() throws Exception {
        int capacity = 32;
        int openAttempts = 48;
        int delayedHitsPerRoot = 4;
        long activatedAt = 100L;
        long leaseTicks = 50L;
        long lastValidTick = 149L;
        long expiryTick = 150L;

        ArcaneBacklashLedgerRegistry registry = new ArcaneBacklashLedgerRegistry(capacity);

        List<OpenAttempt> initialAttempts = raceOpen(
            registry,
            "initial",
            openAttempts,
            activatedAt,
            leaseTicks,
            delayedHitsPerRoot + 2);
        List<ArcanaCastId> initialRoots = initialAttempts.stream()
            .filter(OpenAttempt::opened)
            .map(OpenAttempt::castId)
            .toList();

        assertEquals(capacity, initialRoots.size());
        assertEquals(openAttempts - capacity,
            initialAttempts.stream().filter(attempt -> !attempt.opened()).count());
        assertEquals(capacity, registry.size());

        List<SettlementAttempt> delayed = settleConcurrently(
            registry,
            initialRoots,
            "last-valid",
            delayedHitsPerRoot,
            lastValidTick);

        assertEquals(capacity * delayedHitsPerRoot, delayed.size());
        assertTrue(delayed.stream().allMatch(attempt ->
            attempt.settlement().status() == ArcaneBacklashSettlement.Status.SETTLED));
        assertTrue(delayed.stream().allMatch(attempt ->
            attempt.settlement().backlashDamage() == 1.0D));

        for (ArcanaCastId castId : initialRoots) {
            ArcaneBacklashLedger ledger = registry.find(castId).orElseThrow();
            assertEquals(delayedHitsPerRoot, ledger.confirmedEligibleDamage(), 0.0D);
            assertEquals(delayedHitsPerRoot, ledger.backlashSettled(), 0.0D);
        }
        assertEquals(capacity, registry.size());

        List<SettlementAttempt> expired = settleConcurrently(
            registry,
            initialRoots,
            "expired",
            1,
            expiryTick);

        assertEquals(capacity, expired.size());
        assertTrue(expired.stream().allMatch(attempt ->
            attempt.settlement().status() == ArcaneBacklashSettlement.Status.DENIED));
        assertTrue(expired.stream().allMatch(attempt ->
            "hazard_claim_expired".equals(attempt.settlement().code())));

        for (ArcanaCastId castId : initialRoots) {
            ArcaneBacklashLedger ledger = registry.find(castId).orElseThrow();
            assertEquals(delayedHitsPerRoot, ledger.confirmedEligibleDamage(), 0.0D);
            assertEquals(delayedHitsPerRoot, ledger.backlashSettled(), 0.0D);
        }
        assertEquals(capacity, registry.size());

        List<OpenAttempt> replacementAttempts = raceOpen(
            registry,
            "replacement",
            openAttempts,
            expiryTick,
            leaseTicks,
            delayedHitsPerRoot + 2);
        List<ArcanaCastId> replacementRoots = replacementAttempts.stream()
            .filter(OpenAttempt::opened)
            .map(OpenAttempt::castId)
            .toList();

        assertEquals(capacity, replacementRoots.size());
        assertEquals(openAttempts - capacity,
            replacementAttempts.stream().filter(attempt -> !attempt.opened()).count());
        assertEquals(capacity, registry.size());
        assertTrue(initialRoots.stream().allMatch(castId -> registry.find(castId).isEmpty()));
        assertTrue(replacementRoots.stream().allMatch(castId -> registry.find(castId).isPresent()));
        assertTrue(replacementRoots.stream().allMatch(castId -> {
            ArcaneBacklashLedger ledger = registry.find(castId).orElseThrow();
            return ledger.confirmedEligibleDamage() == 0.0D && ledger.backlashSettled() == 0.0D;
        }));
    }

    private static List<OpenAttempt> raceOpen(
        ArcaneBacklashLedgerRegistry registry,
        String phase,
        int attempts,
        long activatedAt,
        long leaseTicks,
        int maxDamageInstances
    ) throws Exception {
        CountDownLatch ready = new CountDownLatch(attempts);
        CountDownLatch start = new CountDownLatch(1);
        ExecutorService pool = Executors.newFixedThreadPool(attempts);
        List<Future<OpenAttempt>> futures = new ArrayList<>(attempts);

        try {
            for (int i = 0; i < attempts; i++) {
                ArcanaCastId castId = cast(phase + "-root-" + i);
                futures.add(pool.submit(() -> {
                    ready.countDown();
                    if (!start.await(5, TimeUnit.SECONDS)) {
                        throw new IllegalStateException("open race start barrier timed out");
                    }
                    boolean opened = registry.open(
                        session(castId, activatedAt, leaseTicks, maxDamageInstances),
                        zeroResistance(),
                        ArcaneBacklashPolicy.canonical()).isPresent();
                    return new OpenAttempt(castId, opened);
                }));
            }

            assertTrue(ready.await(5, TimeUnit.SECONDS), "open workers did not reach start barrier");
            start.countDown();

            List<OpenAttempt> results = new ArrayList<>(attempts);
            for (Future<OpenAttempt> future : futures) {
                results.add(future.get(5, TimeUnit.SECONDS));
            }
            return results;
        } finally {
            start.countDown();
            pool.shutdownNow();
            assertTrue(pool.awaitTermination(5, TimeUnit.SECONDS), "open worker pool did not terminate");
        }
    }

    private static List<SettlementAttempt> settleConcurrently(
        ArcaneBacklashLedgerRegistry registry,
        List<ArcanaCastId> roots,
        String phase,
        int hitsPerRoot,
        long tick
    ) throws Exception {
        int taskCount = roots.size() * hitsPerRoot;
        CountDownLatch start = new CountDownLatch(1);
        ExecutorService pool = Executors.newFixedThreadPool(Math.min(32, taskCount));
        List<Future<SettlementAttempt>> futures = new ArrayList<>(taskCount);

        try {
            for (ArcanaCastId castId : roots) {
                for (int hit = 0; hit < hitsPerRoot; hit++) {
                    int hitIndex = hit;
                    futures.add(pool.submit(() -> {
                        if (!start.await(5, TimeUnit.SECONDS)) {
                            throw new IllegalStateException("settlement race start barrier timed out");
                        }
                        ArcaneBacklashSettlement settlement = registry.settle(
                            damage(castId, phase, hitIndex, tick));
                        return new SettlementAttempt(castId, settlement);
                    }));
                }
            }

            start.countDown();
            List<SettlementAttempt> results = new ArrayList<>(taskCount);
            for (Future<SettlementAttempt> future : futures) {
                results.add(future.get(5, TimeUnit.SECONDS));
            }
            return results;
        } finally {
            start.countDown();
            pool.shutdownNow();
            assertTrue(pool.awaitTermination(5, TimeUnit.SECONDS), "settlement worker pool did not terminate");
        }
    }

    private static ArcaneConfirmedDamage damage(
        ArcanaCastId castId,
        String phase,
        int hit,
        long tick
    ) {
        String seed = "damage-" + phase + "-" + castId + "-" + hit;
        return new ArcaneConfirmedDamage(
            new ArcanaDamageProvenance(
                castId,
                ArcanaDamageInstanceId.parse(namedUuid(seed).toString()),
                CASTER,
                SPELL,
                ArcaneDamageFamily.DAMAGE_OVER_TIME,
                true),
            1.0D,
            tick);
    }

    private static ArcaneHazardSession session(
        ArcanaCastId castId,
        long activatedAt,
        long leaseTicks,
        int maxDamageInstances
    ) {
        ArcaneDangerProfile profile = new ArcaneDangerProfile(
            ArcaneDangerTier.FORBIDDEN,
            1.0D,
            0.25D,
            0.25D,
            leaseTicks,
            maxDamageInstances);
        return new ArcaneHazardSession(new ArcaneHazardSnapshot(
            castId,
            SPELL,
            CASTER,
            "minecraft:overworld",
            activatedAt,
            profile));
    }

    private static ArcanaCastId cast(String seed) {
        return ArcanaCastId.parse(namedUuid("cast-" + seed).toString());
    }

    private static UUID namedUuid(String seed) {
        return UUID.nameUUIDFromBytes(seed.getBytes(StandardCharsets.UTF_8));
    }

    private static ArcaneResistanceSnapshot zeroResistance() {
        Map<ArcaneResistanceSourceCategory, Double> categories =
            new EnumMap<>(ArcaneResistanceSourceCategory.class);
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

    private record OpenAttempt(ArcanaCastId castId, boolean opened) {}

    private record SettlementAttempt(ArcanaCastId castId, ArcaneBacklashSettlement settlement) {}
}
