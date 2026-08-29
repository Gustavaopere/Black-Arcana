package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDangerProfile;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDangerTier;
import dev.gustavopere.blackarcana.api.hazard.ArcaneEquipmentProfile;
import dev.gustavopere.blackarcana.api.hazard.ArcaneEquipmentSetBonus;
import dev.gustavopere.blackarcana.api.hazard.ArcaneEquipmentSlotSnapshot;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceQuery;
import dev.gustavopere.blackarcana.api.hazard.CorruptionResistanceQuery;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.UUID;
import java.util.stream.Collectors;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ArcaneEquipmentSetBonusResolverTest {
    private static final String SET = "black_arcana:veil";
    private static final UUID PLAYER = UUID.fromString("63000000-0000-0000-0000-000000000001");
    private static final ArcanaCastId CAST = ArcanaCastId.parse("63000000-0000-0000-0000-000000000002");
    private static final ArcanaSpellId SPELL = ArcanaSpellId.parse("black_arcana:set_bonus_probe");
    private static final ArcaneDangerProfile DANGER = new ArcaneDangerProfile(
        ArcaneDangerTier.DANGEROUS, 1.0D, 0.0D, 0.0D, 40L, 16, 0.0D, 0.0D, false);

    @Test
    void cumulativeThresholdsResolveFromFrozenExplicitSetComposition() {
        ArcaneEquipmentProfileRegistry profiles = profiles();
        ArcaneEquipmentSetBonusRegistry bonuses = bonuses();
        ArcaneEquipmentSnapshotService service = new ArcaneEquipmentSnapshotService(profiles, bonuses);

        var twoPiece = service.capture(List.of(
            slot("head", "black_arcana:veil_hood"),
            slot("chest", "black_arcana:veil_robe"),
            slot("legs", "minecraft:netherite_leggings")));

        assertEquals(2, twoPiece.setPieces(SET));
        assertEquals(25.0D, twoPiece.arcaneResistance(), 0.0D);
        assertEquals(13.0D, twoPiece.corruptionResistance(), 0.0D);
        assertEquals(14.0D, twoPiece.strainCapacityBonus(), 0.0D);
        assertEquals(0.3D, twoPiece.strainRecoveryPerTick(), 1.0e-9D);
        assertEquals(List.of("black_arcana:veil_2pc"), twoPiece.activeSetBonuses().stream()
            .map(resolved -> resolved.bonus().bonusId()).toList());

        var fourPiece = service.capture(List.of(
            slot("head", "black_arcana:veil_hood"),
            slot("chest", "black_arcana:veil_robe"),
            slot("legs", "black_arcana:veil_leggings"),
            slot("feet", "black_arcana:veil_boots")));

        assertEquals(4, fourPiece.setPieces(SET));
        assertEquals(56.0D, fourPiece.arcaneResistance(), 0.0D);
        assertEquals(28.0D, fourPiece.corruptionResistance(), 0.0D);
        assertEquals(32.0D, fourPiece.strainCapacityBonus(), 0.0D);
        assertEquals(0.75D, fourPiece.strainRecoveryPerTick(), 1.0e-9D);
        assertEquals(List.of("black_arcana:veil_2pc", "black_arcana:veil_4pc"), fourPiece.activeSetBonuses().stream()
            .map(resolved -> resolved.bonus().bonusId()).toList());
    }

    @Test
    void capturedSetBonusesDoNotChangeAfterRegistryReload() {
        ArcaneEquipmentSetBonusRegistry bonuses = bonuses();
        ArcaneEquipmentSnapshotService service = new ArcaneEquipmentSnapshotService(profiles(), bonuses);
        var snapshot = service.capture(List.of(
            slot("head", "black_arcana:veil_hood"),
            slot("chest", "black_arcana:veil_robe")));

        bonuses.replaceAll(Map.of());

        assertEquals(25.0D, snapshot.arcaneResistance(), 0.0D);
        assertEquals(1, snapshot.activeSetBonuses().size());
        assertEquals("black_arcana:veil_2pc", snapshot.activeSetBonuses().getFirst().bonus().bonusId());
    }

    @Test
    void providerExposesStableDiagnosticContributionPerActiveSetThreshold() {
        var snapshot = new ArcaneEquipmentSnapshotService(profiles(), bonuses()).capture(List.of(
            slot("head", "black_arcana:veil_hood"),
            slot("chest", "black_arcana:veil_robe"),
            slot("legs", "black_arcana:veil_leggings"),
            slot("feet", "black_arcana:veil_boots")));
        ArcaneEquipmentHazardResistanceProvider provider =
            new ArcaneEquipmentHazardResistanceProvider(ignored -> snapshot);

        Map<String, Double> arcane = provider.contributions(arcaneQuery()).stream()
            .collect(Collectors.toMap(contribution -> contribution.sourceId(), contribution -> contribution.amount()));
        Map<String, Double> corruption = provider.contributions(corruptionQuery()).stream()
            .collect(Collectors.toMap(contribution -> contribution.sourceId(), contribution -> contribution.amount()));

        assertEquals(40.0D, arcane.get(ArcaneEquipmentHazardResistanceProvider.SOURCE_ID), 0.0D);
        assertEquals(5.0D, arcane.get("black_arcana:veil_2pc"), 0.0D);
        assertEquals(11.0D, arcane.get("black_arcana:veil_4pc"), 0.0D);
        assertEquals(20.0D, corruption.get(ArcaneEquipmentHazardResistanceProvider.SOURCE_ID), 0.0D);
        assertEquals(3.0D, corruption.get("black_arcana:veil_2pc"), 0.0D);
        assertEquals(5.0D, corruption.get("black_arcana:veil_4pc"), 0.0D);
    }

    @Test
    void unmatchedAndUnprofiledItemsNeverActivateASetBonus() {
        ArcaneEquipmentSnapshotService service = new ArcaneEquipmentSnapshotService(profiles(), bonuses());
        var snapshot = service.capture(List.of(
            slot("head", "black_arcana:veil_hood"),
            slot("chest", "minecraft:netherite_chestplate"),
            slot("legs", "minecraft:netherite_leggings")));

        assertEquals(1, snapshot.setPieces(SET));
        assertTrue(snapshot.activeSetBonuses().isEmpty());
        assertEquals(10.0D, snapshot.arcaneResistance(), 0.0D);
    }

    private static ArcaneEquipmentProfileRegistry profiles() {
        ArcaneEquipmentProfileRegistry profiles = new ArcaneEquipmentProfileRegistry();
        profiles.register("black_arcana:veil_hood", profile("hood"));
        profiles.register("black_arcana:veil_robe", profile("robe"));
        profiles.register("black_arcana:veil_leggings", profile("leggings"));
        profiles.register("black_arcana:veil_boots", profile("boots"));
        return profiles;
    }

    private static ArcaneEquipmentProfile profile(String name) {
        return new ArcaneEquipmentProfile(
            "black_arcana:veil_" + name,
            10.0D,
            5.0D,
            6.0D,
            0.1D,
            SET,
            Set.of("black_arcana:containment"));
    }

    private static ArcaneEquipmentSetBonusRegistry bonuses() {
        ArcaneEquipmentSetBonusRegistry bonuses = new ArcaneEquipmentSetBonusRegistry();
        bonuses.register(new ArcaneEquipmentSetBonus(
            "black_arcana:veil_2pc", SET, 2, 5.0D, 3.0D, 2.0D, 0.1D,
            Set.of("black_arcana:set/veil_2pc")));
        bonuses.register(new ArcaneEquipmentSetBonus(
            "black_arcana:veil_4pc", SET, 4, 11.0D, 5.0D, 6.0D, 0.25D,
            Set.of("black_arcana:set/veil_4pc")));
        return bonuses;
    }

    private static ArcaneEquipmentSlotSnapshot slot(String slot, String item) {
        return new ArcaneEquipmentSlotSnapshot(slot, item, 100);
    }

    private static ArcaneResistanceQuery arcaneQuery() {
        return new ArcaneResistanceQuery(CAST, SPELL, PLAYER, "minecraft:overworld", 100L, DANGER);
    }

    private static CorruptionResistanceQuery corruptionQuery() {
        return new CorruptionResistanceQuery(CAST, SPELL, PLAYER, "minecraft:overworld", 100L, DANGER);
    }
}
