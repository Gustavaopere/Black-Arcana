package dev.gustavopere.blackarcana.client;

import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import org.junit.jupiter.api.Test;

import java.lang.reflect.Method;
import java.util.List;
import java.util.Locale;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assertions.fail;

class LoadoutCatalogSearchTest {
    @Test
    void emptyQueryReturnsFullCatalogInStableInputOrder() {
        ArcanaSpellId a = spell("a");
        ArcanaSpellId b = spell("b");
        ArcanaSpellId c = spell("c");
        List<ArcanaSpellId> catalog = List.of(c, a, b);

        assertEquals(catalog, filter(catalog, Map.of(a, "Alpha", b, "Beta", c, "Gamma"), ""));
        assertEquals(catalog, filter(catalog, Map.of(a, "Alpha", b, "Beta", c, "Gamma"), "   "));
    }

    @Test
    void matchesDisplayNameCaseInsensitivelyWithLocaleRoot() {
        ArcanaSpellId iris = spell("iris");
        ArcanaSpellId beta = spell("beta");
        Locale previous = Locale.getDefault();
        try {
            Locale.setDefault(Locale.forLanguageTag("tr-TR"));
            assertEquals(List.of(iris), filter(
                    List.of(iris, beta),
                    Map.of(iris, "IRIS", beta, "Beta"),
                    "iris"));
        } finally {
            Locale.setDefault(previous);
        }
    }

    @Test
    void canonicalIdMatchIsSupportedWithoutDisplayMetadata() {
        ArcanaSpellId blood = ArcanaSpellId.parse("black_arcana:blood_lance");
        ArcanaSpellId veil = ArcanaSpellId.parse("black_arcana:void_veil");

        assertEquals(List.of(blood), filter(
                List.of(blood, veil),
                Map.of(),
                "BLOOD_LANCE"));
        assertEquals(List.of(veil), filter(
                List.of(blood, veil),
                Map.of(),
                "black_arcana:void"));
    }

    @Test
    void duplicateDisplayNamesRemainDistinctBySpellIdentity() {
        ArcanaSpellId first = ArcanaSpellId.parse("black_arcana:first");
        ArcanaSpellId second = ArcanaSpellId.parse("black_arcana:second");

        assertEquals(List.of(first, second), filter(
                List.of(first, second),
                Map.of(first, "Shared Name", second, "Shared Name"),
                "shared"));
    }

    @Test
    void noMatchReturnsEmptyWithoutMutatingDraftOrderOrMembership() {
        ArcanaSpellId a = spell("a");
        ArcanaSpellId b = spell("b");
        LoadoutDraft draft = new LoadoutDraft(List.of(b, a));

        assertTrue(filter(List.of(a, b), Map.of(a, "Alpha", b, "Beta"), "missing").isEmpty());
        assertEquals(List.of(b, a), draft.snapshot());
        assertEquals(List.of(a, b), filter(List.of(a, b), Map.of(a, "Alpha", b, "Beta"), ""));
        assertEquals(List.of(b, a), draft.snapshot());
    }

    @SuppressWarnings("unchecked")
    private static List<ArcanaSpellId> filter(
            List<ArcanaSpellId> catalog,
            Map<ArcanaSpellId, String> displayNames,
            String query
    ) {
        try {
            Class<?> type = Class.forName("dev.gustavopere.blackarcana.client.LoadoutCatalogSearch");
            Method method = type.getDeclaredMethod("filter", List.class, Map.class, String.class);
            return (List<ArcanaSpellId>) method.invoke(null, catalog, displayNames, query);
        } catch (ReflectiveOperationException exception) {
            return fail("LoadoutCatalogSearch.filter(...) is missing or invalid", exception);
        }
    }

    private static ArcanaSpellId spell(String path) {
        return ArcanaSpellId.parse("black_arcana:" + path);
    }
}
