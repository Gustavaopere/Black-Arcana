package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDangerProfile;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceContribution;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceProvider;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceQuery;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceSourceCategory;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ArcaneResistancePreviewRuntimeStoreTest {
    private ArcanaServerRuntime runtime;

    @AfterEach
    void cleanup() {
        ArcaneResistancePreviewRuntimeStore.remove(runtime);
    }

    @Test
    void previewFailsClosedUntilEveryGameplayProviderHasAReadOnlyMirror() {
        runtime = ArcanaServerRuntime.createDefault();
        ArcaneResistanceProvider provider = provider("test:readonly", 7.0D);
        runtime.arcaneResistanceProviders().register(provider);
        ArcaneResistanceQuery query = query();

        assertTrue(ArcaneResistancePreviewRuntimeStore.snapshotIfComplete(runtime, query).isEmpty());

        ArcaneResistancePreviewRuntimeStore.register(runtime, provider);
        var preview = ArcaneResistancePreviewRuntimeStore.snapshotIfComplete(runtime, query).orElseThrow();
        assertEquals(7.0D, preview.effectiveResistance());
        assertEquals(1, ArcaneResistancePreviewRuntimeStore.previewProviderCount(runtime));
    }

    @Test
    void previewFailsClosedWhenMirroredProviderThrowsAndRegistryRecordsDiagnostic() {
        runtime = ArcanaServerRuntime.createDefault();
        ArcaneResistanceProvider gameplay = provider("test:failing", 5.0D);
        ArcaneResistanceProvider failingPreview = new ArcaneResistanceProvider() {
            @Override public String providerId() { return "test:failing"; }

            @Override
            public List<ArcaneResistanceContribution> contributions(ArcaneResistanceQuery query) {
                throw new IllegalStateException("synthetic preview failure");
            }
        };
        runtime.arcaneResistanceProviders().register(gameplay);
        ArcaneResistancePreviewRuntimeStore.register(runtime, failingPreview);

        assertTrue(ArcaneResistancePreviewRuntimeStore.snapshotIfComplete(runtime, query()).isEmpty());
    }

    private static ArcaneResistanceProvider provider(String id, double amount) {
        return new ArcaneResistanceProvider() {
            @Override public String providerId() { return id; }

            @Override
            public List<ArcaneResistanceContribution> contributions(ArcaneResistanceQuery query) {
                return List.of(new ArcaneResistanceContribution(
                    "test:source", ArcaneResistanceSourceCategory.RPG, amount));
            }
        };
    }

    private static ArcaneResistanceQuery query() {
        return new ArcaneResistanceQuery(
            ArcanaCastId.random(),
            ArcanaSpellId.parse("black_arcana:test"),
            UUID.randomUUID(),
            "minecraft:overworld",
            10L,
            ArcaneDangerProfile.normal());
    }
}
