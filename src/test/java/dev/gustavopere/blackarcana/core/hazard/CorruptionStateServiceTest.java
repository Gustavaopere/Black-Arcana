package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDangerProfile;
import dev.gustavopere.blackarcana.api.hazard.CorruptionAcquisitionProfile;
import dev.gustavopere.blackarcana.api.hazard.CorruptionBand;
import dev.gustavopere.blackarcana.api.hazard.CorruptionResistanceContribution;
import dev.gustavopere.blackarcana.api.hazard.CorruptionResistanceProvider;
import dev.gustavopere.blackarcana.api.hazard.CorruptionResistanceQuery;
import dev.gustavopere.blackarcana.api.hazard.CorruptionResistanceSourceCategory;
import org.junit.jupiter.api.Test;

import java.util.ArrayList;
import java.util.EnumMap;
import java.util.List;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class CorruptionStateServiceTest {
    private static final UUID PLAYER = UUID.fromString("22222222-2222-2222-2222-222222222222");

    @Test
    void zeroResistanceLeavesFullConfiguredAcquisition() {
        CorruptionStateService service = CorruptionStateService.canonical(16);
        var resistance = CorruptionResistanceProviderRegistry.canonical(8).snapshot(query());
        var profile = CorruptionAcquisitionProfile.committedCastOnly(80.0D, 0.10D);

        var update = service.acquireFromCommittedCast(PLAYER, 100L, profile, resistance);
        assertEquals(80.0D, update.appliedDelta(), 1.0E-9D);
        assertEquals(80.0D, update.after().units(), 1.0E-9D);
    }

    @Test
    void highResistanceCannotBypassUnavoidableFloor() {
        EnumMap<CorruptionResistanceSourceCategory, Double> caps = new EnumMap<>(CorruptionResistanceSourceCategory.class);
        for (var category : CorruptionResistanceSourceCategory.values()) caps.put(category, 10_000.0D);
        CorruptionResistanceProviderRegistry registry = new CorruptionResistanceProviderRegistry(
            8,
            new CorruptionResistanceCurve(1.0D, 10_000.0D),
            caps);
        registry.register(provider(10_000.0D));
        var profile = new CorruptionAcquisitionProfile(100.0D, 0.0D, 0.20D, 1.0D, 10_000.0D);

        CorruptionStateService service = CorruptionStateService.canonical(16);
        var update = service.acquireFromCommittedCast(PLAYER, 100L, profile, registry.snapshot(query()));
        assertEquals(20.0D, update.appliedDelta(), 1.0E-9D);
    }

    @Test
    void thresholdTransitionsFireOnlyWhenBandsChange() {
        CorruptionStateService service = CorruptionStateService.canonical(16);
        List<CorruptionStateService.CorruptionTransition> observed = new ArrayList<>();
        service.registerThresholdListener("black_arcana:test", observed::add);
        var resistance = CorruptionResistanceProviderRegistry.canonical(8).snapshot(query());
        var profile = CorruptionAcquisitionProfile.committedCastOnly(650.0D, 0.0D);

        var first = service.acquireFromCommittedCast(PLAYER, 100L, profile, resistance);
        assertEquals(CorruptionBand.CORRUPTED, first.after().band());
        assertEquals(3, first.transitions().size());
        assertEquals(3, observed.size());

        // Snapshot/read operations do not replay threshold consequences.
        service.snapshot(PLAYER);
        service.snapshot(PLAYER);
        assertEquals(3, observed.size());

        var recovery = service.recover(PLAYER, 120L, 400.0D);
        assertEquals(CorruptionBand.TRACE, recovery.after().band());
        assertEquals(2, recovery.transitions().size());
        assertEquals(5, observed.size());
    }

    @Test
    void persistenceSnapshotRestoresStateAndMetadata() {
        CorruptionStateService first = CorruptionStateService.canonical(16);
        var resistance = CorruptionResistanceProviderRegistry.canonical(8).snapshot(query());
        first.acquireFromCommittedCast(
            PLAYER,
            100L,
            CorruptionAcquisitionProfile.committedCastOnly(120.0D, 0.0D),
            resistance);
        first.recover(PLAYER, 140L, 20.0D);

        CorruptionStateService second = CorruptionStateService.canonical(16);
        second.restoreSnapshot(first.persistentSnapshot());
        var restored = second.snapshot(PLAYER);
        assertEquals(100.0D, restored.units(), 1.0E-9D);
        assertEquals(CorruptionBand.TRACE, restored.band());
        assertEquals(140L, restored.lastMeaningfulUpdateTick());
        assertEquals(140L, restored.lastRecoveryTick());
        assertEquals(1L, restored.acquisitionEvents());
        assertEquals(1L, restored.recoveryEvents());
    }

    @Test
    void persistedStateSanitizerClampsOversizedAndMalformedValues() {
        var sanitized = CorruptionStateService.PersistedState.sanitize(
            Double.POSITIVE_INFINITY,
            -100L,
            -100L,
            Long.MAX_VALUE,
            Long.MAX_VALUE);
        assertEquals(0.0D, sanitized.units(), 1.0E-9D);
        assertEquals(0L, sanitized.lastMeaningfulUpdateTick());
        assertEquals(-1L, sanitized.lastRecoveryTick());
        assertEquals(CorruptionStateService.MAX_TELEMETRY_EVENTS, sanitized.acquisitionEvents());
        assertEquals(CorruptionStateService.MAX_TELEMETRY_EVENTS, sanitized.recoveryEvents());
    }

    private static CorruptionResistanceProvider provider(double amount) {
        return new CorruptionResistanceProvider() {
            @Override public String providerId() { return "black_arcana:test"; }
            @Override public List<CorruptionResistanceContribution> contributions(CorruptionResistanceQuery query) {
                return List.of(new CorruptionResistanceContribution(
                    "black_arcana:test",
                    CorruptionResistanceSourceCategory.NATIVE,
                    amount));
            }
        };
    }

    private static CorruptionResistanceQuery query() {
        return new CorruptionResistanceQuery(
            ArcanaCastId.random(),
            ArcanaSpellId.parse("black_arcana:corruption_probe"),
            PLAYER,
            "minecraft:overworld",
            100L,
            ArcaneDangerProfile.normal());
    }
}
