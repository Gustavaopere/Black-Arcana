package dev.gustavopere.blackarcana.persistence;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDangerProfile;
import dev.gustavopere.blackarcana.api.hazard.ArcaneStrainProfile;
import dev.gustavopere.blackarcana.api.hazard.CorruptionAcquisitionProfile;
import dev.gustavopere.blackarcana.api.hazard.CorruptionResistanceQuery;
import dev.gustavopere.blackarcana.core.hazard.ArcaneStrainStateService;
import dev.gustavopere.blackarcana.core.hazard.CorruptionResistanceProviderRegistry;
import dev.gustavopere.blackarcana.core.hazard.CorruptionStateService;
import dev.gustavopere.blackarcana.core.hazard.PendingBacklashRegistry;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.nbt.ListTag;
import org.junit.jupiter.api.Test;

import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;

class BlackArcanaSavedDataHazardStateTest {
    @Test
    void corruptionAndStrainRoundTripThroughGlobalSavedData() {
        UUID player = UUID.randomUUID();
        CorruptionStateService corruption = CorruptionStateService.canonical(16);
        ArcaneStrainStateService strain = ArcaneStrainStateService.canonical(16);
        var resistance = CorruptionResistanceProviderRegistry.canonical(4).snapshot(new CorruptionResistanceQuery(
            new ArcanaCastId(UUID.randomUUID()),
            ArcanaSpellId.parse("black_arcana:test"),
            player,
            "minecraft:overworld",
            100L,
            ArcaneDangerProfile.normal()));
        corruption.acquireFromCommittedCast(
            player, 100L, CorruptionAcquisitionProfile.committedCastOnly(25.0D, 0.0D), resistance);
        strain.commitCast(player, 100L,
            new ArcaneStrainProfile(80.0D, 0.0D, 0.0D, 0.0D, 0.0D, 0.0D, 0.0D),
            1.0D, 0.0D, 0L);

        BlackArcanaSavedData saved = new BlackArcanaSavedData();
        saved.captureHazards(corruption, strain);
        CompoundTag root = saved.save(new CompoundTag(), null);
        BlackArcanaSavedData loaded = BlackArcanaSavedData.load(root, null);

        CorruptionStateService restoredCorruption = CorruptionStateService.canonical(16);
        ArcaneStrainStateService restoredStrain = ArcaneStrainStateService.canonical(16);
        loaded.restoreHazards(restoredCorruption, restoredStrain);
        assertEquals(25.0D, restoredCorruption.snapshot(player).units(), 1.0E-9D);
        assertEquals(77.5D, restoredStrain.snapshot(player, 150L).units(), 1.0E-9D);
    }

    @Test
    void pendingBacklashRoundTripsAndRemainsExactlyOnceAcrossRestartBoundary() {
        UUID player = UUID.fromString("61000000-0000-0000-0000-000000000001");
        PendingBacklashRegistry pending = new PendingBacklashRegistry(16, 1_000.0D);
        pending.accrue(player, 23.5D);

        BlackArcanaSavedData saved = new BlackArcanaSavedData();
        saved.capturePendingBacklash(pending);
        CompoundTag root = saved.save(new CompoundTag(), null);
        BlackArcanaSavedData loaded = BlackArcanaSavedData.load(root, null);

        PendingBacklashRegistry restored = new PendingBacklashRegistry(16, 1_000.0D);
        loaded.restorePendingBacklash(restored);
        assertEquals(23.5D, restored.pending(player), 0.0D);
        assertEquals(23.5D, restored.drain(player), 0.0D);
        assertEquals(0.0D, restored.drain(player), 0.0D);
    }

    @Test
    void oversizedHazardValuesAreSanitizedInsteadOfPoisoningSave() {
        UUID player = UUID.randomUUID();
        CompoundTag root = new CompoundTag();
        root.putInt("schema", 1);

        CompoundTag corruptionEntry = new CompoundTag();
        corruptionEntry.putUUID("player", player);
        corruptionEntry.putDouble("units", Double.POSITIVE_INFINITY);
        corruptionEntry.putLong("updated", -10L);
        corruptionEntry.putLong("recovery", -99L);
        corruptionEntry.putLong("acquisitions", Long.MAX_VALUE);
        corruptionEntry.putLong("recoveries", Long.MAX_VALUE);
        corruptionEntry.putInt("state_schema", CorruptionStateService.STATE_SCHEMA_VERSION);
        ListTag corruptionList = new ListTag();
        corruptionList.add(corruptionEntry);
        root.put("corruption", corruptionList);

        CompoundTag strainEntry = new CompoundTag();
        strainEntry.putUUID("player", player);
        strainEntry.putDouble("units", ArcaneStrainStateService.ABSOLUTE_MAX_STRAIN_UNITS * 10.0D);
        strainEntry.putLong("updated", -5L);
        strainEntry.putLong("acquisitions", Long.MAX_VALUE);
        strainEntry.putLong("recoveries", Long.MAX_VALUE);
        strainEntry.putInt("state_schema", ArcaneStrainStateService.STATE_SCHEMA_VERSION);
        ListTag strainList = new ListTag();
        strainList.add(strainEntry);
        root.put("strain", strainList);

        BlackArcanaSavedData loaded = BlackArcanaSavedData.load(root, null);
        CorruptionStateService corruption = CorruptionStateService.canonical(16);
        ArcaneStrainStateService strain = ArcaneStrainStateService.canonical(16);
        loaded.restoreHazards(corruption, strain);

        assertEquals(0.0D, corruption.snapshot(player).units(), 1.0E-9D);
        assertEquals(ArcaneStrainStateService.CANONICAL_MAX_STRAIN_UNITS, strain.snapshot(player, 0L).units(), 1.0E-9D);
    }
}
