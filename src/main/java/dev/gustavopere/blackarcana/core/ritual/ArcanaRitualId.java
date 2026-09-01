package dev.gustavopere.blackarcana.core.ritual;

import java.util.Objects;
import java.util.regex.Pattern;

public record ArcanaRitualId(String namespace, String path) {
    private static final Pattern NAMESPACE = Pattern.compile("[a-z0-9_.-]+");
    private static final Pattern PATH = Pattern.compile("[a-z0-9/._-]+");

    public ArcanaRitualId {
        Objects.requireNonNull(namespace, "namespace");
        Objects.requireNonNull(path, "path");
        if (namespace.length() > 64 || !NAMESPACE.matcher(namespace).matches()) {
            throw new IllegalArgumentException("invalid ritual namespace: " + namespace);
        }
        if (path.length() > 160 || !PATH.matcher(path).matches()) {
            throw new IllegalArgumentException("invalid ritual path: " + path);
        }
    }

    public static ArcanaRitualId parse(String value) {
        Objects.requireNonNull(value, "value");
        int separator = value.indexOf(':');
        if (separator <= 0 || separator != value.lastIndexOf(':') || separator == value.length() - 1) {
            throw new IllegalArgumentException("ritual id must be namespace:path: " + value);
        }
        return new ArcanaRitualId(value.substring(0, separator), value.substring(separator + 1));
    }

    public String canonical() {
        return namespace + ':' + path;
    }
}
