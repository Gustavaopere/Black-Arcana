package dev.gustavopere.blackarcana.config;

import com.google.gson.JsonParser;
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

class AstralControlConfigContractTest {
    private static final ResourceLocation ASTRAL_ID =
            ResourceLocation.fromNamespaceAndPath("black_arcana", "astral_severance");

    @AfterEach
    void resetAuthority() {
        AstralControlConfigAuthority.reload(List.of());
    }

    @Test
    void validServerProfilePublishesExactControlLimits() {
        AstralControlDataDefinition definition = new AstralControlDataDefinition(
                AstralControlDataDefinition.CURRENT_SCHEMA_VERSION,
                ASTRAL_ID.toString(),
                ConfigScope.SERVER,
                0.375D,
                17.5F);

        assertTrue(definition.validate().isEmpty());
        AstralControlConfigAuthority.reload(List.of(definition));

        var limits = AstralControlConfigAuthority.currentLimits().orElseThrow();
        assertEquals(0.375D, limits.maxStepBlocks());
        assertEquals(17.5F, limits.maxLookDeltaDegrees());
    }

    @Test
    void absenceOfProfileIsExplicitFailClosedState() {
        AstralControlConfigAuthority.reload(List.of());
        assertTrue(AstralControlConfigAuthority.currentLimits().isEmpty());
    }

    @Test
    void onlyServerScopeCanAuthorizeAstralMovement() {
        AstralControlDataDefinition client = new AstralControlDataDefinition(
                1, ASTRAL_ID.toString(), ConfigScope.CLIENT, 0.25D, 10.0F);
        AstralControlDataDefinition common = new AstralControlDataDefinition(
                1, ASTRAL_ID.toString(), ConfigScope.COMMON, 0.25D, 10.0F);

        assertFalse(client.validate().isEmpty());
        assertFalse(common.validate().isEmpty());
        assertThrows(IllegalArgumentException.class, () -> AstralControlConfigAuthority.reload(List.of(client)));
        assertTrue(AstralControlConfigAuthority.currentLimits().isEmpty());
    }

    @Test
    void safetyCeilingsBoundButDoNotSupplyControlValues() {
        AstralControlDataDefinition excessiveStep = new AstralControlDataDefinition(
                1,
                ASTRAL_ID.toString(),
                ConfigScope.SERVER,
                NoeticSafetyCeilings.MAX_RANGE_BLOCKS + 0.001D,
                10.0F);
        AstralControlDataDefinition excessiveLook = new AstralControlDataDefinition(
                1, ASTRAL_ID.toString(), ConfigScope.SERVER, 0.25D, 180.001F);

        assertFalse(excessiveStep.validate().isEmpty());
        assertFalse(excessiveLook.validate().isEmpty());
        assertTrue(AstralControlConfigAuthority.currentLimits().isEmpty());
    }

    @Test
    void authorityRejectsDuplicateOrForeignProfilesAtomically() {
        AstralControlDataDefinition valid = new AstralControlDataDefinition(
                1, ASTRAL_ID.toString(), ConfigScope.SERVER, 0.25D, 10.0F);
        AstralControlDataDefinition foreign = new AstralControlDataDefinition(
                1, "black_arcana:not_astral_severance", ConfigScope.SERVER, 0.5D, 15.0F);

        assertThrows(IllegalArgumentException.class,
                () -> AstralControlConfigAuthority.reload(List.of(valid, valid)));
        assertTrue(AstralControlConfigAuthority.currentLimits().isEmpty());
        assertThrows(IllegalArgumentException.class,
                () -> AstralControlConfigAuthority.reload(List.of(foreign)));
        assertTrue(AstralControlConfigAuthority.currentLimits().isEmpty());
    }

    @Test
    void loaderAcceptsOnlyStrictServerOwnedAstralSchema() {
        var parsed = AstralControlDataReloadListener.parseDefinition(
                ASTRAL_ID,
                JsonParser.parseString("""
                        {
                          "schemaVersion": 1,
                          "id": "black_arcana:astral_severance",
                          "scope": "SERVER",
                          "maxStepBlocks": 0.25,
                          "maxLookDeltaDegrees": 12.0
                        }
                        """));

        assertTrue(parsed.validate().isEmpty());
        assertEquals(ConfigScope.SERVER, parsed.scope());

        assertThrows(RuntimeException.class, () -> AstralControlDataReloadListener.parseDefinition(
                ASTRAL_ID,
                JsonParser.parseString("""
                        {
                          "schemaVersion": 1,
                          "id": "black_arcana:astral_severance",
                          "scope": "SERVER",
                          "maxStepBlocks": 0.25,
                          "maxLookDeltaDegrees": 12.0,
                          "defaultMovement": true
                        }
                        """)));
    }

    @Test
    void modRegistersServerConfigAuthorityWithoutEnablingMoveGameplay() throws IOException {
        String source = Files.readString(repositoryRoot().resolve(
                "src/main/java/dev/gustavopere/blackarcana/BlackArcanaMod.java"));

        assertTrue(source.contains("AstralControlDataReloadListener.register(NeoForge.EVENT_BUS);"));
        assertFalse(source.contains("AstralSeveranceNetworkBridge.installMoveHandler("),
                "config authority must not silently enable MOVE gameplay before approved production values exist");
    }

    private static Path repositoryRoot() {
        String workspace = System.getenv("GITHUB_WORKSPACE");
        if (workspace != null && !workspace.isBlank()) {
            return Path.of(workspace);
        }
        return Path.of("").toAbsolutePath();
    }
}
