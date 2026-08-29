package dev.gustavopere.blackarcana.content.forbidden;

import java.util.Objects;
import java.util.Optional;
import java.util.function.Predicate;

public final class DomainReturnSelector {
    private DomainReturnSelector() { }

    public static Optional<DomainReturnPoint> choose(
        DomainReturnPoint origin,
        DomainReturnPoint fallback,
        Predicate<DomainReturnPoint> loadedAndSafe
    ) {
        Objects.requireNonNull(origin, "origin");
        Objects.requireNonNull(fallback, "fallback");
        Objects.requireNonNull(loadedAndSafe, "loadedAndSafe");
        if (loadedAndSafe.test(origin)) return Optional.of(origin);
        if (loadedAndSafe.test(fallback)) return Optional.of(fallback);
        return Optional.empty();
    }
}
