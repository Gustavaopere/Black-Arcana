package dev.gustavopere.blackarcana.integration.neoforge;

import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

import static org.junit.jupiter.api.Assertions.assertTrue;

class AstralProjectionEntityWiringTest {
    private static final Path ROOT = repositoryRoot();
    private static final Path ENTITY_SOURCE = ROOT.resolve(
            "src/main/java/dev/gustavopere/blackarcana/content/noetic/AstralProjectionEntity.java");
    private static final Path REGISTRY_SOURCE = ROOT.resolve(
            "src/main/java/dev/gustavopere/blackarcana/content/noetic/BlackArcanaNoeticEntities.java");
    private static final Path CLIENT_SOURCE = ROOT.resolve(
            "src/main/java/dev/gustavopere/blackarcana/client/AstralProjectionClientRegistration.java");
    private static final Path MOD_SOURCE = ROOT.resolve(
            "src/main/java/dev/gustavopere/blackarcana/BlackArcanaMod.java");
    private static final Path CLIENT_ENTRYPOINT_SOURCE = ROOT.resolve(
            "src/main/java/dev/gustavopere/blackarcana/client/BlackArcanaClient.java");

    @Test
    void astralAvatarIsDedicatedNonPersistentNonInteractiveAndClientInvisible() throws IOException {
        assertTrue(Files.exists(ENTITY_SOURCE),
                "Astral Severance needs a dedicated Black Arcana projection entity, not an arbitrary observed entity");
        assertTrue(Files.exists(REGISTRY_SOURCE),
                "Astral projection entity type must be registered on the common mod event bus");
        assertTrue(Files.exists(CLIENT_SOURCE),
                "Astral projection renderer registration must stay in the physical-client package");

        String entity = Files.readString(ENTITY_SOURCE);
        String registry = Files.readString(REGISTRY_SOURCE);
        String client = Files.readString(CLIENT_SOURCE);
        String mod = Files.readString(MOD_SOURCE);
        String clientEntrypoint = Files.readString(CLIENT_ENTRYPOINT_SOURCE);

        assertTrue(entity.contains("extends Entity"),
                "Astral avatar must be a dedicated non-living viewpoint entity");
        assertTrue(entity.contains("public boolean isPickable()") && entity.contains("return false;"),
                "Astral avatar must not become a remote interaction/attack target");

        assertTrue(registry.contains("DeferredRegister.create(BuiltInRegistries.ENTITY_TYPE, BlackArcanaMod.MOD_ID)"),
                "Entity type registration must use the verified NeoForge 1.21.1 DeferredRegister API");
        assertTrue(registry.contains("EntityType.Builder.of(AstralProjectionEntity::new, MobCategory.MISC)"),
                "Astral avatar must use its dedicated entity factory");
        assertTrue(registry.contains(".noSave()"),
                "Astral avatars must never persist across restart");
        assertTrue(registry.contains(".noSummon()"),
                "Astral avatars must not be command/summon-owned gameplay entities");
        assertTrue(mod.contains("BlackArcanaNoeticEntities.register(modEventBus)"),
                "Common entity registration must be installed from the Black Arcana mod entrypoint");

        assertTrue(client.contains("EntityRenderersEvent.RegisterRenderers"),
                "Astral renderer must be registered through the verified client renderer event");
        assertTrue(client.contains("NoopRenderer::new"),
                "Astral viewpoint representation must remain visually inert in this checkpoint");
        assertTrue(clientEntrypoint.contains("AstralProjectionClientRegistration::register"),
                "Client-only renderer registration must be installed only by the physical-client entrypoint");
    }

    private static Path repositoryRoot() {
        String workspace = System.getenv("GITHUB_WORKSPACE");
        if (workspace != null && !workspace.isBlank()) {
            return Path.of(workspace);
        }

        Path candidate = Path.of("").toAbsolutePath();
        while (candidate != null) {
            if (Files.exists(candidate.resolve("settings.gradle")) && Files.isDirectory(candidate.resolve(".github"))) {
                return candidate;
            }
            candidate = candidate.getParent();
        }
        throw new IllegalStateException("Unable to locate repository root from test working directory");
    }
}
