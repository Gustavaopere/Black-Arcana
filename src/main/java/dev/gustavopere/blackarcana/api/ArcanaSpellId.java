package dev.gustavopere.blackarcana.api;

import java.util.Objects;
import java.util.regex.Pattern;

public record ArcanaSpellId(String namespace, String path) {
    private static final Pattern NAMESPACE = Pattern.compile("[a-z0-9_.-]+");
    private static final Pattern PATH = Pattern.compile("[a-z0-9/._-]+");

    public ArcanaSpellId {
        Objects.requireNonNull(namespace, "namespace");
        Objects.requireNonNull(path, "path");
        if (!NAMESPACE.matcher(namespace).matches()) {
            throw new IllegalArgumentException("Invalid spell namespace: " + namespace);
        }
        if (!PATH.matcher(path).matches()) {
            throw new IllegalArgumentException("Invalid spell path: " + path);
        }
    }

    public static ArcanaSpellId parse(String value) {
        Objects.requireNonNull(value, "value");
        int separator = value.indexOf(':');
        if (separator <= 0 || separator != value.lastIndexOf(':') || separator == value.length() - 1) {
            throw new IllegalArgumentException("Spell id must be namespace:path: " + value);
        }
        return new ArcanaSpellId(value.substring(0, separator), value.substring(separator + 1));
    }

    public String canonical() {
        return namespace + ':' + path;
    }
}
