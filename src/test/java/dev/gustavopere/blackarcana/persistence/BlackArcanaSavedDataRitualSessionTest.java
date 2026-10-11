package dev.gustavopere.blackarcana.persistence;

import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.core.cast.LoadoutRegistry;
import dev.gustavopere.blackarcana.core.cooldown.ChargePoolCooldownService;
import dev.gustavopere.blackarcana.core.cooldown.PersistentCooldownService;
import dev.gustavopere.blackarcana.core.ritual.ArcanaRitualId;
import dev.gustavopere.blackarcana.core.ritual.RitualActivationGuard;
import dev.gustavopere.blackarcana.core.ritual.RitualActivationId;
import dev.gustavopere.blackarcana.core.ritual.RitualAnchor;
import dev.gustavopere.blackarcana.core.ritual.RitualComponentProvider;
import dev.gustavopere.blackarcana.core.ritual.RitualComponentReservation;
import dev.gustavopere.blackarcana.core.ritual.RitualContext;
import dev.gustavopere.blackarcana.core.ritual.RitualDefinition;
import dev.gustavopere.blackarcana.core.ritual.RitualEngine;
import dev.gustavopere.blackarcana.core.ritual.RitualSessionRegistry;
import dev.gustavopere.blackarcana.core.world.TemporaryMutationTracker;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.nbt.ListTag;
import net.minecraft.nbt.Tag;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.UUID;
import java.util.concurrent.atomic.AtomicInteger;

import static org.junit.jupiter.api.Assertions.assertEquals;

class BlackArcanaSavedDataRitualSessionTest {
    @Test
    void committedRitualSurvivesNbtWithoutDoubleConsumption() {
        RitualDefinition definition = new RitualDefinition(
                ArcanaRitualId.parse("black_arcana:persistent_rite"), 20L, 40L);
        AtomicInteger initialCommits = new AtomicInteger();
        RitualEngine beforeRestart = engine(initialCommits, new AtomicInteger());
        beforeRestart.start(
                definition,
                RitualActivationId.parse("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"),
                new RitualContext(
                        UUID.fromString("11111111-1111-1111-1111-111111111111"),
                        List.of(UUID.fromString("22222222-2222-2222-2222-222222222222")),
                        new RitualAnchor("minecraft:overworld", 123L)),
                100L);
        beforeRestart.tick(120L, 8);
        assertEquals(1, initialCommits.get());

        var cooldowns = new PersistentCooldownService(request -> null);
        var charges = new ChargePoolCooldownService(request -> null);
        var loadouts = new LoadoutRegistry();
        var temporary = new TemporaryMutationTracker(8);
        BlackArcanaSavedData saved = new BlackArcanaSavedData();
        saved.capture(cooldowns, charges, loadouts, temporary, beforeRestart, 125L);

        CompoundTag root = saved.save(new CompoundTag(), null);
        BlackArcanaSavedData loaded = BlackArcanaSavedData.load(root, null);
        AtomicInteger restoredCommits = new AtomicInteger();
        AtomicInteger restoredOutcomes = new AtomicInteger();
        RitualEngine afterRestart = engine(restoredCommits, restoredOutcomes);

        var restore = loaded.restore(
                cooldowns,
                charges,
                loadouts,
                new TemporaryMutationTracker(8),
                afterRestart,
                List.of(definition),
                125L);

        assertEquals(1, restore.restored());
        assertEquals(0, restore.rejected());
        afterRestart.tick(140L, 8);
        assertEquals(0, restoredCommits.get(), "committed ritual must not consume components twice after restart");
        assertEquals(1, restoredOutcomes.get());
    }

    @Test
    void deniedAlreadyCompletedSnapshotIsScrubbedBeforeNextSavedDataSerialization() {
        RitualDefinition definition = new RitualDefinition(
                ArcanaRitualId.parse("black_arcana:persistent_rite"), 20L, 40L);
        var cooldowns = new PersistentCooldownService(request -> null);
        var charges = new ChargePoolCooldownService(request -> null);
        var loadouts = new LoadoutRegistry();
        var temporary = new TemporaryMutationTracker(8);
        RitualEngine prior = engine(new AtomicInteger(), new AtomicInteger());
        assertEquals(dev.gustavopere.blackarcana.core.ritual.RitualResult.Status.STARTED,
                prior.start(definition,
                        RitualActivationId.parse("bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"),
                        new RitualContext(UUID.fromString("11111111-1111-1111-1111-111111111111"),
                                List.of(), new RitualAnchor("minecraft:overworld", 123L)), 100L).status());
        prior.tick(120L, 8);

        BlackArcanaSavedData data = new BlackArcanaSavedData();
        data.capture(cooldowns, charges, loadouts, temporary, prior, 125L);
        BlackArcanaSavedData loaded = BlackArcanaSavedData.load(data.save(new CompoundTag(), null), null);
        assertEquals(1, loaded.save(new CompoundTag(), null)
                .getList("ritual_sessions", net.minecraft.nbt.Tag.TAG_COMPOUND).size());

        RitualEngine restored = engine(new AtomicInteger(), new AtomicInteger());
        // Models a completion key already present in the independently durable
        // completion ledger at startup: provider restore admission must fail closed.
        restored.registerRestoreAdmission(definition.id(),
                (def, context, now) -> ArcanaDecision.deny(
                        "grand_ritual_already_completed", "completion already in ledger"));
        var result = loaded.restore(cooldowns, charges, loadouts,
                new TemporaryMutationTracker(8), restored, List.of(definition), 125L);
        assertEquals(0, result.restored());
        assertEquals(1, result.rejected());
        assertEquals(0, restored.activeSessionCount());

        CompoundTag reconciled = loaded.save(new CompoundTag(), null);
        assertEquals(0, reconciled.getList("ritual_sessions", net.minecraft.nbt.Tag.TAG_COMPOUND).size(),
                "rejected completion must not remain in the next SavedData write");
        org.junit.jupiter.api.Assertions.assertTrue(loaded.isDirty(),
                "reconciled rejection must be scheduled for persistence");

        // Without a persisted tombstone, removing the rejected stale snapshot is
        // essential: a later restart without the original provider must not revive it.
        BlackArcanaSavedData reloaded = BlackArcanaSavedData.load(reconciled, null);
        RitualEngine next = engine(new AtomicInteger(), new AtomicInteger());
        var secondRestore = reloaded.restore(cooldowns, charges, loadouts,
                new TemporaryMutationTracker(8), next, List.of(definition), 125L);
        assertEquals(0, secondRestore.restored());
        assertEquals(0, secondRestore.rejected());
        assertEquals(0, next.activeSessionCount());
    }

    @Test
    void restoreReconciliationRetainsOnlyAcceptedCommittedRituals() {
        RitualDefinition definition = new RitualDefinition(
                ArcanaRitualId.parse("black_arcana:persistent_rite"), 20L, 40L);
        UUID acceptedCaster = UUID.fromString("11111111-1111-1111-1111-111111111111");
        UUID rejectedCaster = UUID.fromString("22222222-2222-2222-2222-222222222222");
        var cooldowns = new PersistentCooldownService(request -> null);
        var charges = new ChargePoolCooldownService(request -> null);
        var loadouts = new LoadoutRegistry();
        var temporary = new TemporaryMutationTracker(8);
        RitualEngine prior = engine(new AtomicInteger(), new AtomicInteger());
        assertEquals(dev.gustavopere.blackarcana.core.ritual.RitualResult.Status.STARTED,
                prior.start(definition,
                        RitualActivationId.parse("cccccccc-cccc-cccc-cccc-ccccccccccc1"),
                        new RitualContext(acceptedCaster, List.of(),
                                new RitualAnchor("minecraft:overworld", 123L)), 100L).status());
        assertEquals(dev.gustavopere.blackarcana.core.ritual.RitualResult.Status.STARTED,
                prior.start(definition,
                        RitualActivationId.parse("cccccccc-cccc-cccc-cccc-ccccccccccc2"),
                        new RitualContext(rejectedCaster, List.of(),
                                new RitualAnchor("minecraft:overworld", 124L)), 100L).status());
        assertEquals(2, prior.tick(120L, 8).committed());
        BlackArcanaSavedData data = new BlackArcanaSavedData();
        data.capture(cooldowns, charges, loadouts, temporary, prior, 125L);
        BlackArcanaSavedData loaded = BlackArcanaSavedData.load(data.save(new CompoundTag(), null), null);

        AtomicInteger afterRestartCommits = new AtomicInteger();
        AtomicInteger afterRestartOutcomes = new AtomicInteger();
        RitualEngine restored = engine(afterRestartCommits, afterRestartOutcomes);
        restored.registerRestoreAdmission(definition.id(), (def, context, now) ->
                context.casterId().equals(rejectedCaster)
                        ? ArcanaDecision.deny("stale_ritual", "invalid legacy snapshot")
                        : ArcanaDecision.allow());

        var result = loaded.restore(cooldowns, charges, loadouts,
                new TemporaryMutationTracker(8), restored, List.of(definition), 125L);
        assertEquals(1, result.restored());
        assertEquals(1, result.rejected());
        CompoundTag reconciled = loaded.save(new CompoundTag(), null);
        var entries = reconciled.getList("ritual_sessions", net.minecraft.nbt.Tag.TAG_COMPOUND);
        assertEquals(1, entries.size(), "accepted committed session must remain while stale session is removed");
        assertEquals(acceptedCaster, entries.getCompound(0).getUUID("caster"));
        assertEquals(1, restored.tick(140L, 8).completed());
        assertEquals(0, afterRestartCommits.get(), "restore must not charge committed costs again");
        assertEquals(1, afterRestartOutcomes.get());
    }

    @Test
    void malformedRitualEntryRequiresDirtyRewriteEvenWithoutAnyRestoredSession() {
        CompoundTag root = new BlackArcanaSavedData().save(new CompoundTag(), null);
        ListTag entries = new ListTag();
        CompoundTag invalid = new CompoundTag();
        invalid.putString("ritual", "black_arcana:persistent_rite");
        invalid.putString("state", "COMMITTED");
        // Missing activation/caster UUIDs: the existing NBT reader drops this record.
        entries.add(invalid);
        root.put("ritual_sessions", entries);

        BlackArcanaSavedData recovered = BlackArcanaSavedData.load(root, null);

        assertEquals(0, recovered.save(new CompoundTag(), null)
                .getList("ritual_sessions", Tag.TAG_COMPOUND).size());
        org.junit.jupiter.api.Assertions.assertTrue(recovered.isDirty(),
                "a silently discarded ritual entry must schedule a clean SavedData rewrite");
    }

    @Test
    void corruptedRitualEntryIsRemovedWithoutDroppingValidCommittedSnapshotOnNextSave() {
        RitualDefinition definition = new RitualDefinition(
                ArcanaRitualId.parse("black_arcana:persistent_rite"), 20L, 40L);
        var cooldowns = new PersistentCooldownService(request -> null);
        var charges = new ChargePoolCooldownService(request -> null);
        var loadouts = new LoadoutRegistry();
        var temporary = new TemporaryMutationTracker(8);
        RitualEngine original = engine(new AtomicInteger(), new AtomicInteger());
        UUID caster = UUID.fromString("11111111-1111-1111-1111-111111111111");
        assertEquals(dev.gustavopere.blackarcana.core.ritual.RitualResult.Status.STARTED,
                original.start(definition,
                        RitualActivationId.parse("dddddddd-dddd-dddd-dddd-dddddddddddd"),
                        new RitualContext(caster, List.of(), new RitualAnchor("minecraft:overworld", 123L)),
                        100L).status());
        assertEquals(1, original.tick(120L, 8).committed());

        BlackArcanaSavedData saved = new BlackArcanaSavedData();
        saved.capture(cooldowns, charges, loadouts, temporary, original, 125L);
        CompoundTag root = saved.save(new CompoundTag(), null);
        ListTag entries = root.getList("ritual_sessions", Tag.TAG_COMPOUND);
        entries.add(new CompoundTag()); // corrupted sibling of a valid COMMITTED record

        BlackArcanaSavedData loaded = BlackArcanaSavedData.load(root, null);
        org.junit.jupiter.api.Assertions.assertTrue(loaded.isDirty(),
                "dropping malformed sibling must be persisted even if other snapshots remain valid");
        CompoundTag normalized = loaded.save(new CompoundTag(), null);
        assertEquals(1, normalized.getList("ritual_sessions", Tag.TAG_COMPOUND).size());
        assertEquals(caster, normalized.getList("ritual_sessions", Tag.TAG_COMPOUND)
                .getCompound(0).getUUID("caster"));

        AtomicInteger afterRestartCommits = new AtomicInteger();
        AtomicInteger afterRestartOutcomes = new AtomicInteger();
        RitualEngine restored = engine(afterRestartCommits, afterRestartOutcomes);
        var recovery = BlackArcanaSavedData.load(normalized, null).restore(
                cooldowns, charges, loadouts, new TemporaryMutationTracker(8),
                restored, List.of(definition), 125L);
        assertEquals(1, recovery.restored());
        assertEquals(0, recovery.rejected());
        assertEquals(1, restored.tick(140L, 8).completed());
        assertEquals(0, afterRestartCommits.get());
        assertEquals(1, afterRestartOutcomes.get());
    }

    @Test
    void interruptedCommittedRitualDoesNotReappearAfterCapturedSaveAndReload() {
        RitualDefinition definition = new RitualDefinition(
                ArcanaRitualId.parse("black_arcana:persistent_rite"), 20L, 40L);
        UUID caster = UUID.fromString("11111111-1111-1111-1111-111111111111");
        var cooldowns = new PersistentCooldownService(request -> null);
        var charges = new ChargePoolCooldownService(request -> null);
        var loadouts = new LoadoutRegistry();
        var temporary = new TemporaryMutationTracker(8);

        AtomicInteger spent = new AtomicInteger();
        RitualEngine before = engine(spent, new AtomicInteger());
        assertEquals(dev.gustavopere.blackarcana.core.ritual.RitualResult.Status.STARTED,
                before.start(definition,
                        RitualActivationId.parse("eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee"),
                        new RitualContext(caster, List.of(),
                                new RitualAnchor("minecraft:overworld", 123L)), 100L).status());
        assertEquals(1, before.tick(120L, 8).committed());
        BlackArcanaSavedData data = new BlackArcanaSavedData();
        data.capture(cooldowns, charges, loadouts, temporary, before, 125L);
        assertEquals(1, data.save(new CompoundTag(), null)
                .getList("ritual_sessions", Tag.TAG_COMPOUND).size());

        assertEquals(1, before.interruptCaster(caster, "ritual_caster_disconnected"));
        data.capture(cooldowns, charges, loadouts, temporary, before, 126L);
        CompoundTag persistedAfterInterruption = data.save(new CompoundTag(), null);
        assertEquals(0, persistedAfterInterruption.getList("ritual_sessions", Tag.TAG_COMPOUND).size());
        assertEquals(1, spent.get(), "committed components remain spent after interruption");

        AtomicInteger restartedCommits = new AtomicInteger();
        AtomicInteger restartedOutcomes = new AtomicInteger();
        RitualEngine reloaded = engine(restartedCommits, restartedOutcomes);
        var result = BlackArcanaSavedData.load(persistedAfterInterruption, null).restore(
                cooldowns, charges, loadouts, new TemporaryMutationTracker(8),
                reloaded, List.of(definition), 126L);
        assertEquals(0, result.restored());
        assertEquals(0, result.rejected());
        assertEquals(0, reloaded.tick(140L, 8).completed());
        assertEquals(0, restartedCommits.get());
        assertEquals(0, restartedOutcomes.get());
    }

    private static RitualEngine engine(AtomicInteger commits, AtomicInteger outcomes) {
        return new RitualEngine(
                new RitualSessionRegistry(8),
                new RitualActivationGuard(32, 1_200L),
                (definition, context, now) -> ArcanaDecision.allow(),
                new RitualComponentProvider() {
                    @Override
                    public ArcanaDecision check(RitualDefinition definition, RitualContext context, long nowTick) {
                        return ArcanaDecision.allow();
                    }

                    @Override
                    public RitualComponentReservation reserve(RitualDefinition definition, RitualContext context, long nowTick) {
                        return RitualComponentReservation.reserved(commits::incrementAndGet, () -> { });
                    }
                },
                (definition, context, now) -> {
                    outcomes.incrementAndGet();
                    return ArcanaDecision.allow();
                });
    }
}
