package dev.gustavopere.blackarcana.network;

import dev.gustavopere.blackarcana.content.noetic.AstralSeveranceRuntime;
import org.junit.jupiter.api.Test;

import java.util.Arrays;
import java.util.Set;
import java.util.UUID;
import java.util.stream.Collectors;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;

class AstralSeveranceNetworkIntentTest {
    @Test
    void movePayloadCarriesOnlyExactProjectionIdentitySequenceAndBoundedAxes() {
        UUID projectionId = UUID.randomUUID();
        AstralMoveIntentPayload payload = new AstralMoveIntentPayload(
                ArcanaProtocol.VERSION,
                projectionId,
                7L,
                -0.5D,
                0.25D,
                1.0D,
                12.0F,
                -8.0F);

        assertEquals(
                new AstralSeveranceRuntime.ControlIntent(
                        projectionId, 7L, -0.5D, 0.25D, 1.0D, 12.0F, -8.0F),
                payload.toControlIntent());
        assertEquals(
                Set.of(
                        "protocolVersion",
                        "projectionId",
                        "sequence",
                        "strafeAxis",
                        "verticalAxis",
                        "forwardAxis",
                        "yawDeltaDegrees",
                        "pitchDeltaDegrees"),
                componentNames(AstralMoveIntentPayload.class));
        assertFalse(componentNames(AstralMoveIntentPayload.class).contains("casterId"));
        assertFalse(componentNames(AstralMoveIntentPayload.class).contains("x"));
        assertFalse(componentNames(AstralMoveIntentPayload.class).contains("y"));
        assertFalse(componentNames(AstralMoveIntentPayload.class).contains("z"));

        assertThrows(IllegalArgumentException.class, () -> new AstralMoveIntentPayload(
                ArcanaProtocol.VERSION, projectionId, 0L, 0.0D, 0.0D, 0.0D, 0.0F, 0.0F));
        assertThrows(IllegalArgumentException.class, () -> new AstralMoveIntentPayload(
                ArcanaProtocol.VERSION, projectionId, 1L, Double.NaN, 0.0D, 0.0D, 0.0F, 0.0F));
        assertThrows(IllegalArgumentException.class, () -> new AstralMoveIntentPayload(
                ArcanaProtocol.VERSION, projectionId, 1L, 1.01D, 0.0D, 0.0D, 0.0F, 0.0F));
        assertThrows(IllegalArgumentException.class, () -> new AstralMoveIntentPayload(
                ArcanaProtocol.VERSION, projectionId, 1L, 0.0D, 0.0D, 0.0D, Float.NaN, 0.0F));
    }

    @Test
    void returnPayloadCarriesOnlyExactProjectionIdentityAndMonotonicSequence() {
        UUID projectionId = UUID.randomUUID();
        AstralReturnIntentPayload payload = new AstralReturnIntentPayload(
                ArcanaProtocol.VERSION,
                projectionId,
                8L);

        assertEquals(projectionId, payload.projectionId());
        assertEquals(8L, payload.sequence());
        assertEquals(
                Set.of("protocolVersion", "projectionId", "sequence"),
                componentNames(AstralReturnIntentPayload.class));
        assertFalse(componentNames(AstralReturnIntentPayload.class).contains("casterId"));
        assertThrows(IllegalArgumentException.class, () -> new AstralReturnIntentPayload(
                ArcanaProtocol.VERSION, projectionId, 0L));
    }

    private static Set<String> componentNames(Class<?> recordType) {
        return Arrays.stream(recordType.getRecordComponents())
                .map(component -> component.getName())
                .collect(Collectors.toUnmodifiableSet());
    }
}
