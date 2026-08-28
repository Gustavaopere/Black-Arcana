package dev.gustavopere.blackarcana.core.progression;

import dev.gustavopere.blackarcana.api.ArcanaSpellId;

import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;
import java.util.Set;

/** Explicit rename/removal table for persisted knowledge ids. */
public final class KnowledgeMigrationTable {
    public static final int MAX_MIGRATIONS = 512;

    public record Migration(Optional<ArcanaSpellId> replacement, String reason) {
        public Migration {
            Objects.requireNonNull(replacement, "replacement");
            Objects.requireNonNull(reason, "reason");
            if (reason.isBlank() || reason.length() > 256) {
                throw new IllegalArgumentException("migration reason must be non-blank and bounded");
            }
        }
    }

    private final Map<ArcanaSpellId, Migration> migrations = new LinkedHashMap<>();

    public synchronized void replace(ArcanaSpellId oldId, ArcanaSpellId newId, String reason) {
        register(oldId, new Migration(Optional.of(Objects.requireNonNull(newId, "newId")), reason));
    }

    public synchronized void remove(ArcanaSpellId oldId, String reason) {
        register(oldId, new Migration(Optional.empty(), reason));
    }

    private void register(ArcanaSpellId oldId, Migration migration) {
        Objects.requireNonNull(oldId, "oldId");
        Objects.requireNonNull(migration, "migration");
        if (migrations.containsKey(oldId)) throw new IllegalStateException("duplicate knowledge migration: " + oldId.canonical());
        if (migrations.size() >= MAX_MIGRATIONS) throw new IllegalStateException("knowledge migration table is full");
        migrations.put(oldId, migration);
        try {
            resolve(oldId);
        } catch (RuntimeException failure) {
            migrations.remove(oldId);
            throw failure;
        }
    }

    public synchronized Optional<ArcanaSpellId> resolve(ArcanaSpellId source) {
        Objects.requireNonNull(source, "source");
        ArcanaSpellId current = source;
        Set<ArcanaSpellId> seen = new HashSet<>();
        while (true) {
            if (!seen.add(current)) throw new IllegalStateException("knowledge migration cycle at " + current.canonical());
            Migration migration = migrations.get(current);
            if (migration == null) return Optional.of(current);
            if (migration.replacement().isEmpty()) return Optional.empty();
            current = migration.replacement().orElseThrow();
        }
    }

    public synchronized Map<ArcanaSpellId, Migration> snapshot() {
        return Map.copyOf(migrations);
    }

    public static KnowledgeMigrationTable none() { return new KnowledgeMigrationTable(); }
}
