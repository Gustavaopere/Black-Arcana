package dev.gustavopere.blackarcana.config;

import com.google.gson.JsonParser;
import dev.gustavopere.blackarcana.api.ArcanaCost;
import dev.gustavopere.blackarcana.content.noetic.NoeticSafetyCeilings;
import net.minecraft.resources.ResourceLocation;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class AstralInvocationConfigContractTest {
    private static final ResourceLocation ASTRAL_ID =
            ResourceLocation.fromNamespaceAndPath("black_arcana", "astral_severance");

    @AfterEach
    void resetAuthority() {
        AstralInvocationConfigAuthority.reload(List.of());
    }

    @Test
    void explicitServerProfilePublishesExactInvocationValues() {
        AstralInvocationDataDefinition definition = fixtureDefinition();

        assertTrue(definition.validate().isEmpty());
        AstralInvocationConfigAuthority.reload(List.of(definition));

        var invocation = AstralInvocationConfigAuthority.current().orElseThrow();
        assertEquals("black_arcana:test_resource", invocation.cost().resourceId());
        assertEquals(7.5D, invocation.cost().amount());
        assertEquals(ArcanaCost.Unit.FLAT, invocation.cost().unit());
        assertEquals("black_arcana:test_astral", invocation.cooldown().groupId());
        assertEquals(60L, invocation.cooldown().durationTicks());
        assertTrue(invocation.cooldown().persistent());
        assertEquals(6, invocation.channelSpec().minimumTicks());
        assertEquals(40, invocation.channelSpec().maximumTicks());
        assertEquals(80, invocation.projectionDurationTicks());
        assertEquals(12.5D, invocation.maxRangeBlocks());
    }

    @Test
    void absenceIsExplicitFailClosedStateWithNoDefaults() {
        AstralInvocationConfigAuthority.reload(List.of());
        assertTrue(AstralInvocationConfigAuthority.current().isEmpty());
    }

    @Test
    void onlyServerScopeAndExactAstralIdAreAccepted() {
        AstralInvocationDataDefinition client = withScope(fixtureDefinition(), ConfigScope.CLIENT);
        AstralInvocationDataDefinition foreign = withId(fixtureDefinition(), "black_arcana:not_astral_severance");

        assertFalse(client.validate().isEmpty());
        assertFalse(foreign.validate().isEmpty());
        assertThrows(IllegalArgumentException.class,
                () -> AstralInvocationConfigAuthority.reload(List.of(client)));
        assertTrue(AstralInvocationConfigAuthority.current().isEmpty());
    }

    @Test
    void hardCeilingsBoundProjectionButNeverSupplyItsValues() {
        AstralInvocationDataDefinition excessiveDuration = withProjection(
                fixtureDefinition(), NoeticSafetyCeilings.MAX_DURATION_TICKS + 1, 12.5D);
        AstralInvocationDataDefinition excessiveRange = withProjection(
                fixtureDefinition(), 80, NoeticSafetyCeilings.MAX_RANGE_BLOCKS + 0.001D);

        assertFalse(excessiveDuration.validate().isEmpty());
        assertFalse(excessiveRange.validate().isEmpty());
        assertTrue(AstralInvocationConfigAuthority.current().isEmpty());
    }

    @Test
    void authorityRejectsDuplicateProfilesAtomically() {
        AstralInvocationDataDefinition valid = fixtureDefinition();
        assertThrows(IllegalArgumentException.class,
                () -> AstralInvocationConfigAuthority.reload(List.of(valid, valid)));
        assertTrue(AstralInvocationConfigAuthority.current().isEmpty());
    }

    @Test
    void loaderRequiresCompleteStrictSchemaAndExactCostUnit() {
        var parsed = AstralInvocationDataReloadListener.parseDefinition(
                ASTRAL_ID,
                JsonParser.parseString("""
                        {
                          "schemaVersion": 1,
                          "id": "black_arcana:astral_severance",
                          "scope": "SERVER",
                          "resourceId": "black_arcana:test_resource",
                          "resourceAmount": 7.5,
                          "resourceUnit": "FLAT",
                          "cooldownGroup": "black_arcana:test_astral",
                          "cooldownDurationTicks": 60,
                          "cooldownPersistent": true,
                          "channelMinimumTicks": 6,
                          "channelMaximumTicks": 40,
                          "projectionDurationTicks": 80,
                          "maxRangeBlocks": 12.5
                        }
                        """));

        assertTrue(parsed.validate().isEmpty());
        assertEquals(ArcanaCost.Unit.FLAT, parsed.toInvocation().cost().unit());

        assertThrows(RuntimeException.class, () -> AstralInvocationDataReloadListener.parseDefinition(
                ASTRAL_ID,
                JsonParser.parseString("""
                        {
                          "schemaVersion": 1,
                          "id": "black_arcana:astral_severance",
                          "scope": "SERVER",
                          "resourceId": "black_arcana:test_resource",
                          "resourceAmount": 7.5,
                          "resourceUnit": "GUESS_FROM_PROVIDER",
                          "cooldownGroup": "black_arcana:test_astral",
                          "cooldownDurationTicks": 60,
                          "cooldownPersistent": true,
                          "channelMinimumTicks": 6,
                          "channelMaximumTicks": 40,
                          "projectionDurationTicks": 80,
                          "maxRangeBlocks": 12.5
                        }
                        """)));
    }

    @Test
    void loaderRejectsUnknownFieldsAndFractionalIntegerValues() {
        assertThrows(RuntimeException.class, () -> AstralInvocationDataReloadListener.parseDefinition(
                ASTRAL_ID,
                JsonParser.parseString("""
                        {
                          "schemaVersion": 1,
                          "id": "black_arcana:astral_severance",
                          "scope": "SERVER",
                          "resourceId": "black_arcana:test_resource",
                          "resourceAmount": 7.5,
                          "resourceUnit": "FLAT",
                          "cooldownGroup": "black_arcana:test_astral",
                          "cooldownDurationTicks": 60,
                          "cooldownPersistent": true,
                          "channelMinimumTicks": 6.5,
                          "channelMaximumTicks": 40,
                          "projectionDurationTicks": 80,
                          "maxRangeBlocks": 12.5,
                          "fallbackToSafetyCeilings": true
                        }
                        """)));
    }

    @Test
    void modRegistersOptionalInvocationAuthorityWithoutInstallingAstralProfile() throws IOException {
        String source = Files.readString(repositoryRoot().resolve(
                "src/main/java/dev/gustavopere/blackarcana/BlackArcanaMod.java"));

        assertTrue(source.contains("AstralInvocationDataReloadListener.register(NeoForge.EVENT_BUS);"));
        assertFalse(source.contains("AstralSeveranceCastBinding.install("),
                "loading config must not activate Astral without explicit resource/progression/upkeep authorities");
    }

    private static AstralInvocationDataDefinition fixtureDefinition() {
        return new AstralInvocationDataDefinition(
                1,
                ASTRAL_ID.toString(),
                ConfigScope.SERVER,
                "black_arcana:test_resource",
                7.5D,
                ArcanaCost.Unit.FLAT,
                "black_arcana:test_astral",
                60L,
                true,
                6,
                40,
                80,
                12.5D);
    }

    private static AstralInvocationDataDefinition withScope(
            AstralInvocationDataDefinition source,
            ConfigScope scope
    ) {
        return new AstralInvocationDataDefinition(
                source.schemaVersion(), source.id(), scope,
                source.resourceId(), source.resourceAmount(), source.resourceUnit(),
                source.cooldownGroup(), source.cooldownDurationTicks(), source.cooldownPersistent(),
                source.channelMinimumTicks(), source.channelMaximumTicks(),
                source.projectionDurationTicks(), source.maxRangeBlocks());
    }

    private static AstralInvocationDataDefinition withId(
            AstralInvocationDataDefinition source,
            String id
    ) {
        return new AstralInvocationDataDefinition(
                source.schemaVersion(), id, source.scope(),
                source.resourceId(), source.resourceAmount(), source.resourceUnit(),
                source.cooldownGroup(), source.cooldownDurationTicks(), source.cooldownPersistent(),
                source.channelMinimumTicks(), source.channelMaximumTicks(),
                source.projectionDurationTicks(), source.maxRangeBlocks());
    }

    private static AstralInvocationDataDefinition withProjection(
            AstralInvocationDataDefinition source,
            int durationTicks,
            double maxRangeBlocks
    ) {
        return new AstralInvocationDataDefinition(
                source.schemaVersion(), source.id(), source.scope(),
                source.resourceId(), source.resourceAmount(), source.resourceUnit(),
                source.cooldownGroup(), source.cooldownDurationTicks(), source.cooldownPersistent(),
                source.channelMinimumTicks(), source.channelMaximumTicks(),
                durationTicks, maxRangeBlocks);
    }

    private static Path repositoryRoot() {
        String workspace = System.getenv("GITHUB_WORKSPACE");
        if (workspace != null && !workspace.isBlank()) {
            return Path.of(workspace);
        }
        return Path.of("").toAbsolutePath();
    }
}
