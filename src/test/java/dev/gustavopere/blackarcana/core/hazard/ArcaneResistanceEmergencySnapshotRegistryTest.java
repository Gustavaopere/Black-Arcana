package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.hazard.ArcaneEmergencyProtectionSnapshot;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceContribution;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceProvider;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceQuery;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.UUID;
import java.util.concurrent.atomic.AtomicInteger;

import static org.junit.jupiter.api.Assertions.assertEquals;

class ArcaneResistanceEmergencySnapshotRegistryTest {
    private static final ArcanaCastId CAST = ArcanaCastId.parse("11111111-2222-3333-4444-555555555555");
    private static final UUID CASTER = UUID.fromString("aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee");

    @Test
    void registeredResistanceProvidersAggregateEmergencyFactsDeterministically() {
        ArcaneResistanceProviderRegistry registry = ArcaneResistanceProviderRegistry.canonical(8);
        registry.register(provider(
            "z_provider",
            new ArcaneEmergencyProtectionSnapshot.Candidate("test:z", "test:z", 4.0D, 40L),
            new AtomicInteger()));
        registry.register(provider(
            "a_provider",
            new ArcaneEmergencyProtectionSnapshot.Candidate("test:a", "test:a", 8.0D, 80L),
            new AtomicInteger()));

        ArcaneEmergencyProtectionSnapshot snapshot = registry.takeEmergencyProtectionSnapshot(CAST, CASTER, 100L);

        assertEquals(List.of("test:a", "test:z"), snapshot.candidates().stream()
            .map(ArcaneEmergencyProtectionSnapshot.Candidate::resourceId)
            .toList());
    }

    @Test
    void abortedPreflightReleasesEveryEmergencyCapableResistanceProvider() {
        ArcaneResistanceProviderRegistry registry = ArcaneResistanceProviderRegistry.canonical(8);
        AtomicInteger firstReleases = new AtomicInteger();
        AtomicInteger secondReleases = new AtomicInteger();
        registry.register(provider(
            "first",
            new ArcaneEmergencyProtectionSnapshot.Candidate("test:first", "test:first", 1.0D, 20L),
            firstReleases));
        registry.register(provider(
            "second",
            new ArcaneEmergencyProtectionSnapshot.Candidate("test:second", "test:second", 1.0D, 20L),
            secondReleases));

        registry.releaseEmergencyProtectionSnapshots(CAST);

        assertEquals(1, firstReleases.get());
        assertEquals(1, secondReleases.get());
    }

    private static ArcaneResistanceProvider provider(
        String id,
        ArcaneEmergencyProtectionSnapshot.Candidate candidate,
        AtomicInteger releases
    ) {
        return new TestProvider(id, candidate, releases);
    }

    private record TestProvider(
        String providerId,
        ArcaneEmergencyProtectionSnapshot.Candidate candidate,
        AtomicInteger releases
    ) implements ArcaneResistanceProvider, ArcaneEmergencyProtectionSnapshotProvider {
        @Override
        public List<ArcaneResistanceContribution> contributions(ArcaneResistanceQuery query) {
            return List.of();
        }

        @Override
        public ArcaneEmergencyProtectionSnapshot takeEmergencySnapshot(
            ArcanaCastId castId,
            UUID casterId,
            long serverTick
        ) {
            return new ArcaneEmergencyProtectionSnapshot(List.of(candidate));
        }

        @Override
        public void release(ArcanaCastId castId) {
            releases.incrementAndGet();
        }
    }
}
