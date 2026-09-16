package dev.gustavopere.blackarcana.qa;

import org.junit.jupiter.api.Test;

import java.lang.reflect.Constructor;
import java.lang.reflect.Method;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;
import java.util.UUID;
import java.util.function.Predicate;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assertions.fail;

class Stage05LoadoutQaFixtureTest {
    private static final String FIXTURE_CLASS =
            "dev.gustavopere.blackarcana.qa.stage05.Stage05LoadoutQaFixtureContent";
    private static final String LOADOUT_SERVICE_CLASS =
            "dev.gustavopere.blackarcana.core.cast.LoadoutUpdateService";

    @Test
    void companionFixtureMakesAllSixteenCanonicalSlotsServerAcceptable() throws Exception {
        Class<?> fixtureClass;
        try {
            fixtureClass = Class.forName(FIXTURE_CLASS);
        } catch (ClassNotFoundException missingFixture) {
            fail("Stage 05 QA companion fixture content is missing");
            return;
        }

        Method install = Arrays.stream(fixtureClass.getMethods())
                .filter(method -> method.getName().equals("install") && method.getParameterCount() == 1)
                .findFirst()
                .orElseThrow(() -> new AssertionError("fixture install method is missing"));
        Class<?> fixtureRuntimeType = install.getParameterTypes()[0];
        Object runtime = fixtureRuntimeType.getMethod("createDefault").invoke(null);
        install.invoke(null, runtime);

        @SuppressWarnings("unchecked")
        List<Object> fixtureSpells = (List<Object>) fixtureClass.getField("SPELL_IDS").get(null);
        assertEquals(16, fixtureSpells.size());
        assertEquals(16, fixtureSpells.stream().map(Object::toString).distinct().count());

        Object registry = fixtureRuntimeType.getMethod("spells").invoke(runtime);
        Object loadouts = fixtureRuntimeType.getMethod("loadouts").invoke(runtime);
        Method resolve = Arrays.stream(registry.getClass().getMethods())
                .filter(method -> method.getName().equals("resolve") && method.getParameterCount() == 1)
                .findFirst()
                .orElseThrow();
        Method hasInstalledEngine = Arrays.stream(fixtureRuntimeType.getMethods())
                .filter(method -> method.getName().equals("hasInstalledEngine") && method.getParameterCount() == 1)
                .findFirst()
                .orElseThrow();

        for (Object spellId : fixtureSpells) {
            Optional<?> resolved = (Optional<?>) resolve.invoke(registry, spellId);
            assertTrue(resolved.isPresent(),
                    () -> "fixture spell must be live in the authoritative registry: " + spellId);
            assertTrue((Boolean) hasInstalledEngine.invoke(runtime, spellId),
                    () -> "fixture spell must have an installed execution engine: " + spellId);
        }

        ClassLoader fixtureLoader = fixtureClass.getClassLoader();
        Class<?> loadoutServiceClass = Class.forName(LOADOUT_SERVICE_CLASS, true, fixtureLoader);
        Constructor<?> constructor = Arrays.stream(loadoutServiceClass.getConstructors())
                .filter(candidate -> candidate.getParameterCount() == 3)
                .findFirst()
                .orElseThrow();
        Predicate<Object> executable = spellId -> {
            try {
                return (Boolean) hasInstalledEngine.invoke(runtime, spellId);
            } catch (ReflectiveOperationException exception) {
                throw new IllegalStateException(exception);
            }
        };
        Object service = constructor.newInstance(registry, loadouts, executable);

        UUID casterId = UUID.fromString("166d17f8-9dd1-4d5b-bbd8-bf6d812d55f0");
        Method apply = Arrays.stream(loadoutServiceClass.getMethods())
                .filter(method -> method.getName().equals("apply") && method.getParameterCount() == 2)
                .findFirst()
                .orElseThrow();
        Object result = apply.invoke(service, casterId, fixtureSpells);
        Object decision = result.getClass().getMethod("decision").invoke(result);
        boolean allowed = (Boolean) decision.getClass().getMethod("allowed").invoke(decision);
        String detail = (String) decision.getClass().getMethod("detail").invoke(decision);
        assertTrue(allowed, detail);

        @SuppressWarnings("unchecked")
        List<Object> acceptedLoadout = (List<Object>) result.getClass().getMethod("loadout").invoke(result);
        Method getLoadout = Arrays.stream(loadouts.getClass().getMethods())
                .filter(method -> method.getName().equals("getLoadout") && method.getParameterCount() == 1)
                .findFirst()
                .orElseThrow();
        @SuppressWarnings("unchecked")
        List<Object> persistedLoadout = (List<Object>) getLoadout.invoke(loadouts, casterId);

        assertEquals(fixtureSpells, acceptedLoadout);
        assertEquals(fixtureSpells, persistedLoadout);
    }
}
