package dev.gustavopere.blackarcana.core.cost;

import dev.gustavopere.blackarcana.api.ArcanaServices;

import java.util.Objects;
import java.util.regex.Pattern;

/**
 * A transactional cost provider that owns exactly one canonical namespaced resource id.
 *
 * <p>The id is authority metadata only. It does not select a provider for any spell and
 * does not imply a fallback when the requested resource is unavailable.</p>
 */
public interface ResourceCostProvider extends ArcanaServices.CostProvider {
    Pattern NAMESPACE = Pattern.compile("[a-z0-9_.-]+");
    Pattern PATH = Pattern.compile("[a-z0-9/._-]+");

    String resourceId();

    static String requireResourceId(String resourceId) {
        Objects.requireNonNull(resourceId, "resourceId");
        int separator = resourceId.indexOf(':');
        if (separator <= 0 || separator != resourceId.lastIndexOf(':') || separator == resourceId.length() - 1) {
            throw new IllegalArgumentException("resource id must be namespace:path: " + resourceId);
        }
        String namespace = resourceId.substring(0, separator);
        String path = resourceId.substring(separator + 1);
        if (!NAMESPACE.matcher(namespace).matches() || !PATH.matcher(path).matches()) {
            throw new IllegalArgumentException("invalid resource id: " + resourceId);
        }
        return resourceId;
    }
}
