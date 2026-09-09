package dev.gustavopere.blackarcana.client;

import dev.gustavopere.blackarcana.api.ArcanaSpellId;

import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Objects;

/** Client-only filtering over the already synchronized presentation catalog. */
public final class LoadoutCatalogSearch {
    private LoadoutCatalogSearch() {}

    public static List<ArcanaSpellId> filter(
            List<ArcanaSpellId> catalog,
            Map<ArcanaSpellId, String> displayNames,
            String query
    ) {
        Objects.requireNonNull(catalog, "catalog");
        Objects.requireNonNull(displayNames, "displayNames");
        Objects.requireNonNull(query, "query");

        String normalizedQuery = query.strip().toLowerCase(Locale.ROOT);
        if (normalizedQuery.isEmpty()) return List.copyOf(catalog);

        return catalog.stream()
                .filter(spell -> matches(spell, displayNames.get(spell), normalizedQuery))
                .toList();
    }

    private static boolean matches(ArcanaSpellId spell, String displayName, String normalizedQuery) {
        String canonical = spell.canonical().toLowerCase(Locale.ROOT);
        if (canonical.contains(normalizedQuery)) return true;
        return displayName != null && displayName.toLowerCase(Locale.ROOT).contains(normalizedQuery);
    }
}
