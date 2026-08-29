package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.hazard.ArcaneEquipmentSetBonus;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;

public final class ArcaneEquipmentSetBonusRegistry {
    public static final int MAX_BONUSES = 4_096;
    private static final Comparator<ArcaneEquipmentSetBonus> ORDER =
        Comparator.comparing(ArcaneEquipmentSetBonus::setId)
            .thenComparingInt(ArcaneEquipmentSetBonus::requiredPieces)
            .thenComparing(ArcaneEquipmentSetBonus::bonusId);
    private final Map<String, ArcaneEquipmentSetBonus> bonuses = new LinkedHashMap<>();

    public synchronized void register(ArcaneEquipmentSetBonus bonus) {
        ArcaneEquipmentSetBonus checked = Objects.requireNonNull(bonus, "bonus");
        if (bonuses.containsKey(checked.bonusId())) {
            throw new IllegalStateException("duplicate arcane equipment set bonus: " + checked.bonusId());
        }
        if (bonuses.size() >= MAX_BONUSES) throw new IllegalStateException("arcane equipment set bonus registry is full");
        bonuses.put(checked.bonusId(), checked);
    }

    public synchronized void replaceAll(Map<String, ArcaneEquipmentSetBonus> replacements) {
        Objects.requireNonNull(replacements, "replacements");
        if (replacements.size() > MAX_BONUSES) throw new IllegalArgumentException("too many arcane equipment set bonuses");
        LinkedHashMap<String, ArcaneEquipmentSetBonus> validated = new LinkedHashMap<>();
        for (Map.Entry<String, ArcaneEquipmentSetBonus> entry : replacements.entrySet()) {
            String id = Objects.requireNonNull(entry.getKey(), "bonus id");
            ArcaneEquipmentSetBonus bonus = Objects.requireNonNull(entry.getValue(), "bonus");
            if (!id.equals(bonus.bonusId())) throw new IllegalArgumentException("set bonus map key does not match bonus id: " + id);
            if (validated.putIfAbsent(id, bonus) != null) throw new IllegalArgumentException("duplicate set bonus: " + id);
        }
        bonuses.clear();
        bonuses.putAll(validated);
    }

    public synchronized List<ArcaneEquipmentSetBonus> resolve(Map<String, Integer> setCounts) {
        Objects.requireNonNull(setCounts, "setCounts");
        List<ArcaneEquipmentSetBonus> resolved = new ArrayList<>();
        for (ArcaneEquipmentSetBonus bonus : bonuses.values()) {
            int pieces = setCounts.getOrDefault(bonus.setId(), 0);
            if (pieces >= bonus.requiredPieces()) resolved.add(bonus);
        }
        resolved.sort(ORDER);
        return List.copyOf(resolved);
    }

    public synchronized Map<String, ArcaneEquipmentSetBonus> snapshot() { return Map.copyOf(bonuses); }
    public synchronized int size() { return bonuses.size(); }
}
