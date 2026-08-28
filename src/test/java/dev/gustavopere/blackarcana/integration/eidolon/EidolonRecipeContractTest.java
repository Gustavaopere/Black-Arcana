package dev.gustavopere.blackarcana.integration.eidolon;

import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;

import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

class EidolonRecipeContractTest {
    private static final String RESOURCE =
        "/data/black_arcana/recipe/rituals/eidolon_integration_probe.json";

    @Test
    void probeRecipeIsConditionedOnEidolonAndTargetsRegisteredRitual() throws IOException {
        try (InputStream stream = EidolonRecipeContractTest.class.getResourceAsStream(RESOURCE)) {
            assertNotNull(stream, "Eidolon probe recipe must be packaged as a main resource");
            String json = new String(stream.readAllBytes(), StandardCharsets.UTF_8);

            assertTrue(json.contains("\"type\": \"neoforge:mod_loaded\""));
            assertTrue(json.contains("\"modid\": \"eidolon_repraised\""));
            assertTrue(json.contains("\"type\": \"eidolon_repraised:ritual_brazier\""));
            assertTrue(json.contains("\"ritual\": \"black_arcana:eidolon_integration_probe\""));
        }
    }
}
