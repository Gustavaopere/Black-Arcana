package dev.gustavopere.blackarcana.config;

import com.google.gson.JsonElement;
import com.google.gson.JsonParser;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDangerTier;
import net.minecraft.resources.ResourceLocation;
import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

import static org.junit.jupiter.api.Assertions.assertEquals;

class Stage05RealClientFixtureTest {
    private static final Path ROOT = Path.of("docs", "qa", "fixtures", "stage05-real-client");

    @Test
    void targetsMinecraft1211DatapackFormat() throws IOException {
        var pack = read(ROOT.resolve("pack.mcmeta")).getAsJsonObject().getAsJsonObject("pack");
        assertEquals(48, pack.get("pack_format").getAsInt());
    }

    @Test
    void publishesDangerousIronAndNormalArsControls() throws IOException {
        var ironSpell = ArcanaSpellDataReloadListener.parseDefinition(
            id("irons_integration_probe"),
            data("spells/irons_integration_probe.json"));
        var arsSpell = ArcanaSpellDataReloadListener.parseDefinition(
            id("ars_integration_probe"),
            data("spells/ars_integration_probe.json"));
        assertEquals("black_arcana:irons_integration_probe", ironSpell.id());
        assertEquals("black_arcana:ars_integration_probe", arsSpell.id());

        var ironHazard = ArcaneDangerDataReloadListener.parseDefinition(
            id("irons_integration_probe"),
            data("hazards/irons_integration_probe.json"));
        assertEquals(ArcaneDangerTier.DANGEROUS, ironHazard.tier());
        assertEquals(10.0D, ironHazard.minimumArcaneResistance());
        assertEquals(30.0D, ironHazard.recommendedArcaneResistance());

        var arsHazard = ArcaneDangerDataReloadListener.parseDefinition(
            id("ars_integration_probe"),
            data("hazards/ars_integration_probe.json"));
        assertEquals(ArcaneDangerTier.NORMAL, arsHazard.tier());
        assertEquals(0.0D, arsHazard.minimumArcaneResistance());
        assertEquals(0.0D, arsHazard.recommendedArcaneResistance());
    }

    @Test
    void resistanceFixturesProduceFifteenAndThirtyPointControls() throws IOException {
        var stick = ArcaneEquipmentDataReloadListener.parseDefinition(
            id("qa_resistance_stick"),
            data("equipment_profiles/qa_resistance_stick.json"));
        var blazeRod = ArcaneEquipmentDataReloadListener.parseDefinition(
            id("qa_resistance_blaze_rod"),
            data("equipment_profiles/qa_resistance_blaze_rod.json"));

        assertEquals("minecraft:stick", stick.itemId());
        assertEquals("minecraft:blaze_rod", blazeRod.itemId());
        assertEquals(15.0D, stick.profile().arcaneResistance());
        assertEquals(15.0D, blazeRod.profile().arcaneResistance());
        assertEquals(30.0D, stick.profile().arcaneResistance() + blazeRod.profile().arcaneResistance());
    }

    @Test
    void alternateReloadProfileChangesTierVersionAndThresholds() throws IOException {
        var alternate = ArcaneDangerDataReloadListener.parseDefinition(
            id("irons_integration_probe"),
            read(ROOT.resolve("alternates/irons_integration_probe.reload.json")));

        assertEquals(2, alternate.profileVersion());
        assertEquals(ArcaneDangerTier.FORBIDDEN, alternate.tier());
        assertEquals(20.0D, alternate.minimumArcaneResistance());
        assertEquals(40.0D, alternate.recommendedArcaneResistance());
    }

    private static ResourceLocation id(String path) {
        return ResourceLocation.fromNamespaceAndPath("black_arcana", path);
    }

    private static JsonElement data(String relative) throws IOException {
        return read(ROOT.resolve("data/black_arcana/black_arcana").resolve(relative));
    }

    private static JsonElement read(Path path) throws IOException {
        return JsonParser.parseString(Files.readString(path));
    }
}
