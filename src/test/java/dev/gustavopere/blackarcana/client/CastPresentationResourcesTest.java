package dev.gustavopere.blackarcana.client;

import net.minecraft.resources.ResourceLocation;
import org.junit.jupiter.api.Test;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Set;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class CastPresentationResourcesTest {
    private static final Path ROOT = repositoryRoot();

    @Test
    void catalogUsesBlackArcanaOwnedBoundedResourceIds() {
        Set<ResourceLocation> assets = Set.of(
                CastPresentationResources.soundAsset(CastAudiovisualOrchestration.Kind.ANTICIPATION),
                CastPresentationResources.soundAsset(CastAudiovisualOrchestration.Kind.RESULT_SUCCESS),
                CastPresentationResources.soundAsset(CastAudiovisualOrchestration.Kind.RESULT_DENIED),
                CastPresentationResources.soundAsset(CastAudiovisualOrchestration.Kind.RESULT_FAILED));

        assertEquals(4, assets.size());
        for (ResourceLocation asset : assets) {
            assertEquals("black_arcana", asset.getNamespace());
            assertTrue(asset.getPath().startsWith("sounds/cast/"));
            assertTrue(asset.getPath().endsWith(".ogg"));
        }
    }

    @Test
    void missingOrThrowingResourceLookupFailsClosedWithoutGameplayImpact() {
        var missing = CastPresentationResources.resolveSoundEvent(
                CastAudiovisualOrchestration.Kind.RESULT_SUCCESS,
                ignored -> false);
        var broken = CastPresentationResources.resolveSoundEvent(
                CastAudiovisualOrchestration.Kind.RESULT_DENIED,
                ignored -> { throw new IllegalStateException("resource manager unavailable"); });

        assertTrue(missing.isEmpty());
        assertTrue(broken.isEmpty());
    }

    @Test
    void resolverCachesPositiveAndNegativeLookupsAndReloadInvalidatesThem() {
        CastPresentationResources.invalidate();
        int[] lookups = {0};
        var kind = CastAudiovisualOrchestration.Kind.RESULT_FAILED;

        assertTrue(CastPresentationResources.resolveSoundEvent(kind, ignored -> {
            lookups[0]++;
            return true;
        }).isPresent());
        assertTrue(CastPresentationResources.resolveSoundEvent(kind, ignored -> {
            lookups[0]++;
            return false;
        }).isPresent(), "cached positive lookup must remain stable until reload");
        assertEquals(1, lookups[0]);
        assertEquals(1, CastPresentationResources.cachedEntryCount());

        CastPresentationResources.invalidate();
        assertEquals(0, CastPresentationResources.cachedEntryCount());
        assertFalse(CastPresentationResources.resolveSoundEvent(kind, ignored -> {
            lookups[0]++;
            return false;
        }).isPresent());
        assertEquals(2, lookups[0]);
    }

    @Test
    void soundsJsonAssetsAndProvenanceAreDurableProjectOwnedResources() throws Exception {
        Path soundsJson = ROOT.resolve("src/main/resources/assets/black_arcana/sounds.json");
        Path soundDir = ROOT.resolve("src/main/resources/assets/black_arcana/sounds/cast");
        Path provenance = ROOT.resolve("docs/architecture/casting-audiovisual-asset-provenance.md");

        assertTrue(Files.isRegularFile(soundsJson));
        String json = Files.readString(soundsJson);
        assertTrue(json.contains("cast.intent"));
        assertTrue(json.contains("cast.success"));
        assertTrue(json.contains("cast.denied"));
        assertTrue(json.contains("cast.failed"));

        for (String name : Set.of("intent.ogg", "success.ogg", "denied.ogg", "failed.ogg")) {
            Path asset = soundDir.resolve(name);
            assertTrue(Files.isRegularFile(asset), "missing original Black Arcana sound: " + name);
            assertTrue(Files.size(asset) > 64L, "sound asset must not be an empty placeholder: " + name);
        }

        assertTrue(Files.isRegularFile(provenance));
        String provenanceText = Files.readString(provenance);
        assertTrue(provenanceText.contains("procedurally generated"));
        assertTrue(provenanceText.contains("project-owned"));
        assertTrue(provenanceText.contains("Mahou Tsukai"));
        assertTrue(provenanceText.contains("Iron's"));
    }

    private static Path repositoryRoot() {
        String workspace = System.getenv("GITHUB_WORKSPACE");
        if (workspace != null && !workspace.isBlank()) return Path.of(workspace);
        Path candidate = Path.of("").toAbsolutePath();
        while (candidate != null) {
            if (Files.exists(candidate.resolve("settings.gradle")) && Files.isDirectory(candidate.resolve(".github"))) {
                return candidate;
            }
            candidate = candidate.getParent();
        }
        throw new IllegalStateException("Unable to locate repository root");
    }
}
