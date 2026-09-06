package dev.gustavopere.blackarcana.core.runtime;

import dev.gustavopere.blackarcana.core.world.LoadedChunkGuard;
import dev.gustavopere.blackarcana.core.world.TemporaryBlockBackend;
import dev.gustavopere.blackarcana.core.world.TemporaryMutationKey;
import org.junit.jupiter.api.Test;

import java.util.Optional;

import static org.junit.jupiter.api.Assertions.assertSame;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ArcanaServerRuntimeWorldMutationAuthorityTest {
    @Test
    void installWorldBackendExposesOneSharedMutationProtectionAuthorityAndPermanentGateway() {
        ArcanaServerRuntime runtime = ArcanaServerRuntime.createDefault();
        TemporaryBlockBackend backend = new TemporaryBlockBackend() {
            @Override
            public Optional<String> readLoadedState(TemporaryMutationKey key) {
                return Optional.of("minecraft:stone");
            }

            @Override
            public boolean replaceIfCurrent(TemporaryMutationKey key, String expectedState, String replacementState) {
                return true;
            }
        };
        LoadedChunkGuard.LoadedChunkProbe loaded = chunk -> true;

        runtime.installWorldBackend(backend, loaded);

        assertTrue(runtime.temporaryBlockGateway().isPresent());
        assertTrue(runtime.permanentBlockGateway().isPresent());
        assertSame(runtime.worldMutationProtectionAdapters(), runtime.worldMutationProtectionAdapters(),
            "runtime must own one stable server-scoped mutation-protection registry");
    }
}
