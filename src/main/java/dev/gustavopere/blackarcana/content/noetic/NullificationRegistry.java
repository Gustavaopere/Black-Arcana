package dev.gustavopere.blackarcana.content.noetic;

import net.minecraft.resources.ResourceLocation;

import java.util.ArrayList;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Objects;
import java.util.Set;

/**
 * Bounded allowlist for effects that Noetic nullification is explicitly permitted to remove.
 * Unknown effect ids always fail closed.
 */
public final class NullificationRegistry {
    private final int maxEffectTypes;
    private final Set<ResourceLocation> nullifiable = new LinkedHashSet<>();

    public NullificationRegistry(int maxEffectTypes) {
        if (maxEffectTypes <= 0 || maxEffectTypes > NoeticSafetyCeilings.MAX_NULLIFIABLE_EFFECT_TYPES) {
            throw new IllegalArgumentException("Nullifiable effect limit exceeds the hard Noetic ceiling");
        }
        this.maxEffectTypes = maxEffectTypes;
    }

    public synchronized boolean register(ResourceLocation effectId) {
        Objects.requireNonNull(effectId, "effectId");
        if (nullifiable.contains(effectId) || nullifiable.size() >= maxEffectTypes) {
            return false;
        }
        return nullifiable.add(effectId);
    }

    public synchronized boolean isNullifiable(ResourceLocation effectId) {
        Objects.requireNonNull(effectId, "effectId");
        return nullifiable.contains(effectId);
    }

    public synchronized int size() {
        return nullifiable.size();
    }

    public List<ResourceLocation> selectNullifiable(List<ResourceLocation> activeEffectIds) {
        Objects.requireNonNull(activeEffectIds, "activeEffectIds");

        final Set<ResourceLocation> allowlist;
        synchronized (this) {
            allowlist = Set.copyOf(nullifiable);
        }

        List<ResourceLocation> selected = new ArrayList<>(NoeticSafetyCeilings.MAX_NULLIFICATIONS_PER_ACTION);
        Set<ResourceLocation> seen = new LinkedHashSet<>();
        for (ResourceLocation effectId : activeEffectIds) {
            if (effectId == null || !allowlist.contains(effectId) || !seen.add(effectId)) {
                continue;
            }
            selected.add(effectId);
            if (selected.size() >= NoeticSafetyCeilings.MAX_NULLIFICATIONS_PER_ACTION) {
                break;
            }
        }
        return List.copyOf(selected);
    }
}
