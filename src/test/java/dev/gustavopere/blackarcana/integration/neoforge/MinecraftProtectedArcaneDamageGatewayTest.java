package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDamageFamily;
import dev.gustavopere.blackarcana.api.hazard.ArcanaDamageInstanceId;
import dev.gustavopere.blackarcana.api.hazard.ArcanaDamageProvenance;
import org.junit.jupiter.api.Test;

import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class MinecraftProtectedArcaneDamageGatewayTest {
    @Test
    void casterIdentityMismatchFailsClosedBeforeMinecraftStateIsRequired() {
        UUID caster = UUID.fromString("72000000-0000-0000-0000-000000000001");
        UUID other = UUID.fromString("72000000-0000-0000-0000-000000000002");
        var provenance = new ArcanaDamageProvenance(
            ArcanaCastId.parse("72000000-0000-0000-0000-000000000003"),
            ArcanaDamageInstanceId.parse("72000000-0000-0000-0000-000000000004"),
            other,
            ArcanaSpellId.parse("black_arcana:identity_probe"),
            ArcaneDamageFamily.DIRECT,
            true);

        var result = MinecraftProtectedArcaneDamageGateway.validateCasterIdentity(caster, provenance);
        assertFalse(result.allowed());
        assertEquals("damage_caster_mismatch", result.code());
    }

    @Test
    void matchingCasterIdentityIsAllowed() {
        UUID caster = UUID.fromString("72000000-0000-0000-0000-000000000005");
        var provenance = new ArcanaDamageProvenance(
            ArcanaCastId.parse("72000000-0000-0000-0000-000000000006"),
            ArcanaDamageInstanceId.parse("72000000-0000-0000-0000-000000000007"),
            caster,
            ArcanaSpellId.parse("black_arcana:identity_probe"),
            ArcaneDamageFamily.DIRECT,
            true);

        var result = MinecraftProtectedArcaneDamageGateway.validateCasterIdentity(caster, provenance);
        assertTrue(result.allowed());
        assertEquals("ok", result.code());
    }
}
