package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.hazard.ArcaneEquipmentSetBonus;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;
import org.junit.jupiter.api.Test;

import java.util.Map;
import java.util.Set;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ArcaneEquipmentSetBonusRuntimeStoreTest {
    @Test
    void reloadPublishesAtomicallyToExistingAndFutureRuntimes() {
        ArcanaServerRuntime firstRuntime = ArcanaServerRuntime.createDefault();
        ArcanaServerRuntime secondRuntime = ArcanaServerRuntime.createDefault();
        try {
            ArcaneEquipmentSetBonus firstBonus = bonus("black_arcana:first", 2, 5.0D);
            ArcaneEquipmentSetBonusRuntimeStore.reload(Map.of(firstBonus.bonusId(), firstBonus));

            ArcaneEquipmentSetBonusRegistry first = ArcaneEquipmentSetBonusRuntimeStore.forRuntime(firstRuntime);
            assertEquals(ListIds.of("black_arcana:first"), ListIds.from(first.resolve(Map.of("black_arcana:veil", 2))));

            ArcaneEquipmentSetBonus secondBonus = bonus("black_arcana:second", 3, 9.0D);
            ArcaneEquipmentSetBonusRuntimeStore.reload(Map.of(secondBonus.bonusId(), secondBonus));

            assertTrue(first.resolve(Map.of("black_arcana:veil", 2)).isEmpty());
            assertEquals(ListIds.of("black_arcana:second"), ListIds.from(first.resolve(Map.of("black_arcana:veil", 3))));
            ArcaneEquipmentSetBonusRegistry second = ArcaneEquipmentSetBonusRuntimeStore.forRuntime(secondRuntime);
            assertEquals(ListIds.of("black_arcana:second"), ListIds.from(second.resolve(Map.of("black_arcana:veil", 3))));
        } finally {
            ArcaneEquipmentSetBonusRuntimeStore.remove(firstRuntime);
            ArcaneEquipmentSetBonusRuntimeStore.remove(secondRuntime);
            ArcaneEquipmentSetBonusRuntimeStore.reload(Map.of());
        }
    }

    private static ArcaneEquipmentSetBonus bonus(String id, int pieces, double arcane) {
        return new ArcaneEquipmentSetBonus(
            id, "black_arcana:veil", pieces, arcane, 0.0D, 0.0D, 0.0D, Set.of());
    }

    private record ListIds(java.util.List<String> values) {
        static ListIds of(String... ids) { return new ListIds(java.util.List.of(ids)); }
        static ListIds from(java.util.List<ArcaneEquipmentSetBonus> bonuses) {
            return new ListIds(bonuses.stream().map(ArcaneEquipmentSetBonus::bonusId).toList());
        }
    }
}
