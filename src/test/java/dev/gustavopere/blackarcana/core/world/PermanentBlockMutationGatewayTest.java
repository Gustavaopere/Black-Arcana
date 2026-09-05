package dev.gustavopere.blackarcana.core.world;

import dev.gustavopere.blackarcana.api.ArcanaCastContext;
import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaCost;
import dev.gustavopere.blackarcana.api.ArcanaServices;
import dev.gustavopere.blackarcana.api.ArcanaSpellDefinition;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import org.junit.jupiter.api.Test;

import java.util.HashMap;
import java.util.Map;
import java.util.Optional;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class PermanentBlockMutationGatewayTest {
    private static final ArcanaSpellId ID = ArcanaSpellId.parse("black_arcana:black_pyre");
    private static final TemporaryMutationKey KEY = new TemporaryMutationKey("minecraft:overworld", 42L);
    private static final ChunkRef CHUNK = new ChunkRef("minecraft:overworld", 0, 0);

    @Test
    void protectionDenialHappensBeforeCanonicalBudgetConsumption() {
        var fixture = fixture(WorldEffectMode.FULL);
        fixture.backend.states.put(KEY, "minecraft:stone");
        fixture.protection.register("claim", ignored ->
            dev.gustavopere.blackarcana.api.ArcanaDecision.deny("claim_denied", "protected"));

        var decision = fixture.gateway.replace(
            request(), target(), CHUNK, KEY, "black_arcana:scorched_stone",
            WorldMutationType.FIRE_SPREAD, WorldMutationClass.PERMANENT);

        assertFalse(decision.allowed());
        assertEquals("claim_denied", decision.code());
        assertEquals(0, fixture.ledger.usedUnits(request().castId()));
        assertEquals("minecraft:stone", fixture.backend.states.get(KEY));
    }

    @Test
    void permanentGatewayRejectsTemporaryClassWithoutGuessing() {
        var fixture = fixture(WorldEffectMode.FULL);
        fixture.backend.states.put(KEY, "minecraft:stone");

        var decision = fixture.gateway.replace(
            request(), target(), CHUNK, KEY, "black_arcana:scorched_stone",
            WorldMutationType.FIRE_SPREAD, WorldMutationClass.TEMPORARY);

        assertFalse(decision.allowed());
        assertEquals("permanent_mutation_class", decision.code());
        assertEquals(0, fixture.ledger.usedUnits(request().castId()));
    }

    @Test
    void staleCompareAndSetFailsClosedAfterOneAdmittedAttempt() {
        var fixture = fixture(WorldEffectMode.FULL);
        fixture.backend.states.put(KEY, "minecraft:stone");
        fixture.backend.forceCompareFailure = true;

        var decision = fixture.gateway.replace(
            request(), target(), CHUNK, KEY, "black_arcana:scorched_stone",
            WorldMutationType.FIRE_SPREAD, WorldMutationClass.PERMANENT);

        assertFalse(decision.allowed());
        assertEquals("world_state_changed", decision.code());
        assertEquals(1, fixture.ledger.usedUnits(request().castId()));
        assertEquals("minecraft:stone", fixture.backend.states.get(KEY));
    }

    @Test
    void limitedPermanentMutationUsesBoundedCasWhenModeAllowsIt() {
        var fixture = fixture(WorldEffectMode.LIMITED);
        fixture.backend.states.put(KEY, "minecraft:stone");

        var decision = fixture.gateway.replace(
            request(), target(), CHUNK, KEY, "black_arcana:scorched_stone",
            WorldMutationType.FIRE_SPREAD, WorldMutationClass.LIMITED);

        assertTrue(decision.allowed());
        assertEquals(1, fixture.ledger.usedUnits(request().castId()));
        assertEquals("black_arcana:scorched_stone", fixture.backend.states.get(KEY));
    }

    private static Fixture fixture(WorldEffectMode mode) {
        var profiles = new WorldEffectProfileRegistry();
        profiles.register(ID, new WorldEffectProfile(
            WorldMutationType.FIRE_SPREAD,
            WorldMutationClass.PERMANENT,
            8,
            false));
        var ledger = new WorldEffectBudgetLedger(8, 8, 100);
        var admission = new WorldEffectAdmissionService(
            new ConfigurableWorldEffectPolicy(
                profiles,
                new WorldEffectPolicyConfig(mode, 8, true, Map.of())),
            new LoadedChunkGuard(4, chunk -> true),
            ledger);
        var protection = new WorldMutationProtectionAdapterRegistry(4);
        var backend = new MapBackend();
        return new Fixture(new PermanentBlockMutationGateway(admission, protection, backend), protection, ledger, backend);
    }

    private static ArcanaCastRequest request() {
        return new ArcanaCastRequest(
            ArcanaCastId.parse("11111111-1111-1111-1111-111111111111"),
            new ArcanaSpellDefinition(
                ID,
                "spell.black_arcana.black_pyre",
                "black_arcana:textures/spell/black_pyre.png",
                new ArcanaCost("black_arcana:test", 1),
                true),
            new ArcanaCastContext(
                UUID.fromString("22222222-2222-2222-2222-222222222222"),
                20L,
                "minecraft:overworld"));
    }

    private static ArcanaServices.TargetResolution target() {
        return ArcanaServices.TargetResolution.resolved("block:0,64,0");
    }

    private record Fixture(
        PermanentBlockMutationGateway gateway,
        WorldMutationProtectionAdapterRegistry protection,
        WorldEffectBudgetLedger ledger,
        MapBackend backend
    ) { }

    private static final class MapBackend implements TemporaryBlockBackend {
        final Map<TemporaryMutationKey, String> states = new HashMap<>();
        boolean forceCompareFailure;

        @Override
        public Optional<String> readLoadedState(TemporaryMutationKey key) {
            return Optional.ofNullable(states.get(key));
        }

        @Override
        public boolean replaceIfCurrent(TemporaryMutationKey key, String expectedState, String replacementState) {
            if (forceCompareFailure) return false;
            if (!expectedState.equals(states.get(key))) return false;
            states.put(key, replacementState);
            return true;
        }
    }
}
