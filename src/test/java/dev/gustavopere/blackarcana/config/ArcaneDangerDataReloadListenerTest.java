package dev.gustavopere.blackarcana.config;

import com.google.gson.JsonParseException;
import com.google.gson.JsonParser;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDangerTier;
import dev.gustavopere.blackarcana.api.hazard.ArcaneInsufficientResistancePolicy;
import net.minecraft.resources.ResourceLocation;
import org.junit.jupiter.api.Test;

import java.util.Map;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

class ArcaneDangerDataReloadListenerTest {
    private static final ResourceLocation ID = ResourceLocation.fromNamespaceAndPath("black_arcana", "test_dangerous");

    @Test
    void parsesBoundedDeclarativeProfile() {
        var definition = ArcaneDangerDataReloadListener.parseDefinition(ID, JsonParser.parseString(validJson()));
        assertEquals("black_arcana:test_dangerous", definition.id());
        assertEquals(ArcaneDangerTier.DANGEROUS, definition.tier());
        assertEquals(1.0D, definition.backlashMultiplier());
        assertEquals(25.0D, definition.minimumArcaneResistance());
        assertEquals(ArcaneInsufficientResistancePolicy.ALLOW_WITH_RISK, definition.belowMinimumPolicy());
    }

    @Test
    void legacyProfileWithoutPolicyDefaultsToHardDenial() {
        String legacy = validJson().replace(
            "  \"belowMinimumPolicy\": \"ALLOW_WITH_RISK\",\n",
            "");
        var definition = ArcaneDangerDataReloadListener.parseDefinition(ID, JsonParser.parseString(legacy));

        assertEquals(ArcaneInsufficientResistancePolicy.DENY_CAST, definition.belowMinimumPolicy());
    }

    @Test
    void rejectsUnknownBelowMinimumPolicy() {
        String json = validJson().replace("ALLOW_WITH_RISK", "UNKNOWN_POLICY");
        assertThrows(JsonParseException.class, () ->
            ArcaneDangerDataReloadListener.parseDefinition(ID, JsonParser.parseString(json)));
    }

    @Test
    void canonicalDefinitionRoundTripsThroughJsonCodec() {
        var definition = ArcaneDangerDataReloadListener.parseDefinition(ID, JsonParser.parseString(validJson()));

        var reparsed = ArcaneDangerDataReloadListener.parseDefinition(ID, definition.toJson());

        assertEquals(definition, reparsed);
    }

    @Test
    void appliesDeterministicChainedSpellIdMigrationsBeforePublication() {
        ArcanaSpellId legacy = ArcanaSpellId.parse("black_arcana:legacy_dangerous");
        ArcanaSpellId intermediate = ArcanaSpellId.parse("black_arcana:intermediate_dangerous");
        ArcanaSpellId canonical = ArcanaSpellId.parse("black_arcana:canonical_dangerous");
        ResourceLocation resource = ResourceLocation.fromNamespaceAndPath("black_arcana", "legacy_dangerous");
        var definition = ArcaneDangerDataReloadListener.parseDefinition(
            resource,
            JsonParser.parseString(validJsonFor(legacy.canonical())));
        var migrations = new SpellIdMigrations(
            Map.of(legacy, intermediate, intermediate, canonical),
            Map.of());

        var migrated = ArcaneDangerDataReloadListener.migrateDefinitions(
            Map.of(legacy, definition),
            migrations);

        assertEquals(1, migrated.size());
        assertEquals(canonical.canonical(), migrated.get(canonical).id());
        assertEquals(definition.profileVersion(), migrated.get(canonical).profileVersion());
    }

    @Test
    void removedLegacyProfileIsOmittedRatherThanReappearingUnderOldIdentity() {
        ArcanaSpellId legacy = ArcanaSpellId.parse("black_arcana:legacy_removed");
        ResourceLocation resource = ResourceLocation.fromNamespaceAndPath("black_arcana", "legacy_removed");
        var definition = ArcaneDangerDataReloadListener.parseDefinition(
            resource,
            JsonParser.parseString(validJsonFor(legacy.canonical())));
        var migrations = new SpellIdMigrations(
            Map.of(),
            Map.of(legacy, "removed spell"));

        var migrated = ArcaneDangerDataReloadListener.migrateDefinitions(
            Map.of(legacy, definition),
            migrations);

        assertEquals(Map.of(), migrated);
    }

    @Test
    void migrationCollisionFailsClosedWithoutPartialPublication() {
        ArcanaSpellId first = ArcanaSpellId.parse("black_arcana:legacy_first");
        ArcanaSpellId second = ArcanaSpellId.parse("black_arcana:legacy_second");
        ArcanaSpellId canonical = ArcanaSpellId.parse("black_arcana:canonical");
        var firstDefinition = ArcaneDangerDataReloadListener.parseDefinition(
            ResourceLocation.fromNamespaceAndPath("black_arcana", "legacy_first"),
            JsonParser.parseString(validJsonFor(first.canonical())));
        var secondDefinition = ArcaneDangerDataReloadListener.parseDefinition(
            ResourceLocation.fromNamespaceAndPath("black_arcana", "legacy_second"),
            JsonParser.parseString(validJsonFor(second.canonical())));
        var migrations = new SpellIdMigrations(
            Map.of(first, canonical, second, canonical),
            Map.of());

        assertThrows(JsonParseException.class, () ->
            ArcaneDangerDataReloadListener.migrateDefinitions(
                Map.of(first, firstDefinition, second, secondDefinition),
                migrations));
    }

    @Test
    void cyclicProfileMigrationIsRejectedByCanonicalMigrationContract() {
        ArcanaSpellId first = ArcanaSpellId.parse("black_arcana:first");
        ArcanaSpellId second = ArcanaSpellId.parse("black_arcana:second");

        assertThrows(IllegalArgumentException.class, () ->
            new SpellIdMigrations(Map.of(first, second, second, first), Map.of()));
    }

    @Test
    void rejectsUnknownExecutableLikeFields() {
        String json = validJson().replace("\n}", ",\n  \"command\": \"kill @e\"\n}");
        assertThrows(JsonParseException.class, () ->
            ArcaneDangerDataReloadListener.parseDefinition(ID, JsonParser.parseString(json)));
    }

    @Test
    void rejectsResourceIdMismatch() {
        String json = validJson().replace("black_arcana:test_dangerous", "black_arcana:other");
        assertThrows(JsonParseException.class, () ->
            ArcaneDangerDataReloadListener.parseDefinition(ID, JsonParser.parseString(json)));
    }

    @Test
    void rejectsUnsupportedSchemaVersion() {
        String json = validJson().replace("\"schemaVersion\": 1", "\"schemaVersion\": 2");
        assertThrows(JsonParseException.class, () ->
            ArcaneDangerDataReloadListener.parseDefinition(ID, JsonParser.parseString(json)));
    }

    @Test
    void rejectsOutOfBoundsProfileVersion() {
        String zeroVersion = validJson().replace("\"profileVersion\": 1", "\"profileVersion\": 0");
        assertThrows(JsonParseException.class, () ->
            ArcaneDangerDataReloadListener.parseDefinition(ID, JsonParser.parseString(zeroVersion)));

        String excessiveVersion = validJson().replace(
            "\"profileVersion\": 1",
            "\"profileVersion\": " + (ArcaneDangerDataDefinition.MAX_PROFILE_VERSION + 1));
        assertThrows(JsonParseException.class, () ->
            ArcaneDangerDataReloadListener.parseDefinition(ID, JsonParser.parseString(excessiveVersion)));
    }

    @Test
    void rejectsImpossibleResistanceHints() {
        String json = validJson().replace("\"minimumArcaneResistance\": 25.0", "\"minimumArcaneResistance\": 75.0")
            .replace("\"recommendedArcaneResistance\": 50.0", "\"recommendedArcaneResistance\": 50.0");
        assertThrows(JsonParseException.class, () ->
            ArcaneDangerDataReloadListener.parseDefinition(ID, JsonParser.parseString(json)));
    }

    @Test
    void rejectsDangerousProfileThatConfiguresAwayBacklash() {
        String json = validJson().replace("\"backlashMultiplier\": 1.0", "\"backlashMultiplier\": 0.0");
        assertThrows(JsonParseException.class, () ->
            ArcaneDangerDataReloadListener.parseDefinition(ID, JsonParser.parseString(json)));
    }

    private static String validJson() {
        return validJsonFor("black_arcana:test_dangerous");
    }

    private static String validJsonFor(String id) {
        return """
            {
              "schemaVersion": 1,
              "profileVersion": 1,
              "id": "%s",
              "tier": "DANGEROUS",
              "backlashMultiplier": 1.0,
              "corruptionCoefficient": 2.0,
              "strainCoefficient": 3.0,
              "damageLeaseTicks": 100,
              "maxDamageInstances": 16,
              "minimumArcaneResistance": 25.0,
              "recommendedArcaneResistance": 50.0,
              "belowMinimumPolicy": "ALLOW_WITH_RISK",
              "emergencyProtectionAllowed": true
            }
            """.formatted(id);
    }
}
