package dev.gustavopere.blackarcana.core.runtime;

import dev.gustavopere.blackarcana.api.ArcanaCastContext;
import dev.gustavopere.blackarcana.api.ArcanaCastEngine;
import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaCost;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaGatePreflight;
import dev.gustavopere.blackarcana.api.ArcanaServices;
import dev.gustavopere.blackarcana.api.ArcanaSpellDefinition;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import org.junit.jupiter.api.Test;

import java.util.Optional;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ArcanaServerRuntimeGatePreflightTest {
    @Test
    void delegatesToInstalledSpellEngineWithoutExecutingMutatingStages() {
        ArcanaServerRuntime runtime = ArcanaServerRuntime.createDefault();
        ArcanaCastRequest request = request("black_arcana:runtime_preflight");
        runtime.installEngine(request.spell().id(), engineWithProgressionDenial());

        Optional<ArcanaGatePreflight> result = runtime.previewReadOnlyGates(request);

        assertTrue(result.isPresent());
        assertEquals(ArcanaGatePreflight.Gate.PROGRESSION, result.orElseThrow().gate());
        assertEquals("progression_locked", result.orElseThrow().decision().code());
    }

    @Test
    void missingSpellEngineFailsClosedAsUnavailable() {
        ArcanaServerRuntime runtime = ArcanaServerRuntime.createDefault();

        assertTrue(runtime.previewReadOnlyGates(request("black_arcana:missing_preflight")).isEmpty());
    }

    private static ArcanaCastEngine engineWithProgressionDenial() {
        return new ArcanaCastEngine(
            req -> ArcanaDecision.allow(),
            req -> { throw new AssertionError("preview must not claim replay state"); },
            req -> ArcanaDecision.deny("progression_locked", "progression requirement not met"),
            new ArcanaServices.CooldownService() {
                @Override public ArcanaDecision check(ArcanaCastRequest req) { throw new AssertionError("must stop before cooldown"); }
                @Override public void start(ArcanaCastRequest req) { throw new AssertionError("preview must not start cooldown"); }
            },
            req -> { throw new AssertionError("preview must not resolve target"); },
            new ArcanaServices.CostProvider() {
                @Override public ArcanaDecision check(ArcanaCastRequest req) { throw new AssertionError("must stop before cost"); }
                @Override public ArcanaServices.CostReservation reserve(ArcanaCastRequest req) { throw new AssertionError("preview must not reserve cost"); }
            },
            (req, target) -> { throw new AssertionError("preview must not authorize world effects"); },
            (req, target) -> { throw new AssertionError("preview must not execute effects"); });
    }

    private static ArcanaCastRequest request(String spellId) {
        ArcanaSpellDefinition spell = new ArcanaSpellDefinition(
            ArcanaSpellId.parse(spellId),
            "spell." + spellId.replace(':', '.'),
            "black_arcana:textures/spell/runtime_preflight.png",
            new ArcanaCost("black_arcana:test_resource", 2.0D),
            true);
        return new ArcanaCastRequest(
            ArcanaCastId.parse("22222222-2222-2222-2222-222222222222"),
            spell,
            new ArcanaCastContext(UUID.fromString("f46f38b2-bf40-401d-b497-106b89806048"), 80L, "minecraft:overworld"));
    }
}
