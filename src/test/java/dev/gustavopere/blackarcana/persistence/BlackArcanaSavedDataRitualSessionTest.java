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
