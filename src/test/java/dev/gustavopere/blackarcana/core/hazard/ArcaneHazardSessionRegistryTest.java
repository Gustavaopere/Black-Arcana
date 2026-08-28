package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.api.hazard.ArcanaDamageInstanceId;
import dev.gustavopere.blackarcana.api.hazard.ArcanaDamageProvenance;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDamageFamily;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDangerProfile;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDangerTier;
import dev.gustavopere.blackarcana.api.hazard.ArcaneHazardSnapshot;
import org.junit.jupiter.api.Test;

import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ArcaneHazardSessionRegistryTest {
    private static final UUID CASTER = UUID.fromString("11111111-1111-1111-1111-111111111111");
    private static final ArcanaSpellId SPELL = ArcanaSpellId.parse("black_arcana:danger_probe");

    @Test
    void preservesRootIdentityAndDeduplicatesDamageInstances() {
        ArcanaCastId root = ArcanaCastId.parse("22222222-2222-2222-2222-222222222222");
        ArcaneHazardSnapshot snapshot = snapshot(root, 100L, 40L, 4);
        ArcaneHazardSessionRegistry registry = new ArcaneHazardSessionRegistry(4);

        ArcaneHazardSessionRegistry.OpenResult opened = registry.open(snapshot);
        assertTrue(opened.opened());
        ArcaneHazardSession session = opened.session().orElseThrow();
        assertEquals(root, session.snapshot().rootCastId());

        ArcanaDamageInstanceId damageId = ArcanaDamageInstanceId.parse("33333333-3333-3333-3333-333333333333");
        ArcanaDamageProvenance provenance = new ArcanaDamageProvenance(
            root,
            damageId,
            CASTER,
            SPELL,
            ArcaneDamageFamily.DIRECT,
            true);

        assertEquals(ArcaneHazardSession.ClaimResult.ACCEPTED, session.claim(provenance, 101L));
        assertEquals(ArcaneHazardSession.ClaimResult.DUPLICATE, session.claim(provenance, 102L));
        assertEquals(1, session.seenDamageInstances());
    }

    @Test
    void rejectsMismatchedRootWithoutConsumingCapacity() {
        ArcanaCastId root = ArcanaCastId.parse("44444444-4444-4444-4444-444444444444");
        ArcaneHazardSession session = new ArcaneHazardSession(snapshot(root, 10L, 40L, 2));
        ArcanaDamageProvenance wrongRoot = new ArcanaDamageProvenance(
            ArcanaCastId.parse("55555555-5555-5555-5555-555555555555"),
            ArcanaDamageInstanceId.random(),
            CASTER,
            SPELL,
            ArcaneDamageFamily.PROJECTILE,
            true);

        assertEquals(ArcaneHazardSession.ClaimResult.PROVENANCE_MISMATCH, session.claim(wrongRoot, 11L));
        assertEquals(0, session.seenDamageInstances());
    }

    @Test
    void boundedRegistryRecoversCapacityAfterExpiry() {
        ArcaneHazardSessionRegistry registry = new ArcaneHazardSessionRegistry(1);
        ArcanaCastId first = ArcanaCastId.parse("66666666-6666-6666-6666-666666666666");
        ArcanaCastId second = ArcanaCastId.parse("77777777-7777-7777-7777-777777777777");

        assertTrue(registry.open(snapshot(first, 100L, 10L, 2)).opened());
        ArcaneHazardSessionRegistry.OpenResult full = registry.open(snapshot(second, 101L, 10L, 2));
        assertFalse(full.opened());
        assertEquals("hazard_session_capacity", full.code());

        assertEquals(1, registry.pruneExpired(110L));
        assertTrue(registry.open(snapshot(second, 110L, 10L, 2)).opened());
        assertEquals(1, registry.size());
    }

    @Test
    void profileDamageInstanceLimitFailsClosed() {
        ArcanaCastId root = ArcanaCastId.parse("88888888-8888-8888-8888-888888888888");
        ArcaneHazardSession session = new ArcaneHazardSession(snapshot(root, 0L, 20L, 1));
        ArcanaDamageProvenance first = provenance(root, ArcanaDamageInstanceId.random());
        ArcanaDamageProvenance second = provenance(root, ArcanaDamageInstanceId.random());

        assertEquals(ArcaneHazardSession.ClaimResult.ACCEPTED, session.claim(first, 1L));
        assertEquals(ArcaneHazardSession.ClaimResult.PROFILE_LIMIT, session.claim(second, 2L));
        assertEquals(1, session.seenDamageInstances());
    }

    private static ArcanaDamageProvenance provenance(ArcanaCastId root, ArcanaDamageInstanceId damageId) {
        return new ArcanaDamageProvenance(root, damageId, CASTER, SPELL, ArcaneDamageFamily.DIRECT, true);
    }

    private static ArcaneHazardSnapshot snapshot(ArcanaCastId root, long tick, long lease, int maxInstances) {
        ArcaneDangerProfile profile = new ArcaneDangerProfile(
            ArcaneDangerTier.DANGEROUS,
            1.0D,
            0.25D,
            0.5D,
            lease,
            maxInstances);
        return new ArcaneHazardSnapshot(root, SPELL, CASTER, "minecraft:overworld", tick, profile);
    }
}
