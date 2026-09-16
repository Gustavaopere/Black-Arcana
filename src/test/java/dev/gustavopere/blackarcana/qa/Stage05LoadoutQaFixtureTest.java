package dev.gustavopere.blackarcana.qa;

import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.core.cast.LoadoutUpdateService;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;
import org.junit.jupiter.api.Test;

import java.lang.reflect.Method;
import java.util.List;
import java.util.UUID;
import java.util.stream.IntStream;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assertions.fail;

class Stage05LoadoutQaFixtureTest {
    private static final String FIXTURE_CLASS =
            "dev.gustavopere.blackarcana.qa.stage05.Stage05LoadoutQaFixtureContent";

    @Test
    void companionFixtureMakesAllSixteenCanonicalSlotsServerAcceptable() throws Exception {
        ArcanaServerRuntime runtime = ArcanaServerRuntime.createDefault();
        Class<?> fixtureClass;
        try {
            fixtureClass = Class.forName(FIXTURE_CLASS);
        } catch (ClassNotFoundException missingFixture) {
            fail("Stage 05 QA companion fixture content is missing");
            return;
        }

        Method install = fixtureClass.getMethod("install", ArcanaServerRuntime.class);
        install.invoke(null, runtime);

        List<ArcanaSpellId> fixtureSpells = IntStream.rangeClosed(1, 16)
                .mapToObj(slot -> ArcanaSpellId.parse(
                        "black_arcana_stage05_qa:slot_%02d".formatted(slot)))
                .toList();

        assertEquals(16, fixtureSpells.stream().distinct().count());
        for (ArcanaSpellId spellId : fixtureSpells) {
            assertTrue(runtime.spells().resolve(spellId).isPresent(),
                    () -> "fixture spell must be live in the authoritative registry: " + spellId);
            assertTrue(runtime.hasInstalledEngine(spellId),
                    () -> "fixture spell must have an installed execution engine: " + spellId);
        }

        UUID casterId = UUID.fromString("166d17f8-9dd1-4d5b-bbd8-bf6d812d55f0");
        LoadoutUpdateService service = new LoadoutUpdateService(
                runtime.spells(), runtime.loadouts(), runtime::hasInstalledEngine);
        LoadoutUpdateService.Result result = service.apply(casterId, fixtureSpells);

        assertTrue(result.decision().allowed(), result.decision().detail());
        assertEquals(fixtureSpells, result.loadout());
        assertEquals(fixtureSpells, runtime.loadouts().getLoadout(casterId));
    }
}
