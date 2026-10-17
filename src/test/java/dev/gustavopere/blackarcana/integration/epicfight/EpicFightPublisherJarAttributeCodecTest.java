package dev.gustavopere.blackarcana.integration.epicfight;

import com.google.gson.JsonElement;
import com.google.gson.JsonParser;
import com.mojang.serialization.Codec;
import com.mojang.serialization.JsonOps;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.nbt.ListTag;
import net.minecraft.nbt.NbtOps;
import net.minecraft.nbt.Tag;
import net.minecraft.world.entity.ai.attributes.AttributeModifier;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.condition.EnabledIfEnvironmentVariable;

import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.security.MessageDigest;
import java.util.HexFormat;
import java.util.List;
import java.util.Map;
import java.util.zip.ZipEntry;
import java.util.zip.ZipFile;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertInstanceOf;
import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * Opt-in, exact-publisher fixture-only test, never part of the production mod.
 * The workflow supplies the SHA-verified downloaded JAR via an env variable.
 * No Epic Fight classes are loaded; the actual physical resource JSON is parsed
 * using Minecraft's own NbtOps/AttributeModifier codec under the pack NeoForge
 * version. Runtime skill load, hooks, events and applied attributes remain
 * explicitly out of scope.
 */
@EnabledIfEnvironmentVariable(named = "EPICFIGHT_PUBLISHER_JAR", matches = ".+")
class EpicFightPublisherJarAttributeCodecTest {
    private static final String SHA1 = "fb199b7bbea2fc402da28ab586e73f47e32f8fc0";
    private static final String SHA256 = "8b882554cf10086398340fbdc741819ee72a801a3adce516c7f4768326a39526";
    private static final Map<String, Integer> LEGACY_ROWS = Map.of(
        "adaptive_skin", 1,
        "adrenaline_fiend", 2,
        "catharsis", 2,
        "bonebreaker", 1,
        "vengeance", 2
    );

    private static Path publisherJar() throws Exception {
        Path jar = Path.of(System.getenv("EPICFIGHT_PUBLISHER_JAR")).toAbsolutePath();
        assertTrue(Files.isRegularFile(jar), "exact publisher JAR must be mounted explicitly");
        byte[] bytes = Files.readAllBytes(jar);
        assertEquals(SHA1, hash("SHA-1", bytes), "physical SHA-1 mismatch");
        assertEquals(SHA256, hash("SHA-256", bytes), "physical SHA-256 mismatch");
        return jar;
    }

    private static String hash(String algorithm, byte[] bytes) throws Exception {
        return HexFormat.of().formatHex(MessageDigest.getInstance(algorithm).digest(bytes));
    }

    private static ListTag actualModifierList(ZipFile zip, String skill) throws Exception {
        String path = "data/epicfight/skill_parameters/" + skill + ".json";
        ZipEntry entry = zip.getEntry(path);
        assertTrue(entry != null, "missing exact publisher resource: " + path);
        try (var reader = new InputStreamReader(zip.getInputStream(entry), StandardCharsets.UTF_8)) {
            JsonElement json = JsonParser.parseReader(reader);
            Tag nbt = JsonOps.INSTANCE.convertTo(NbtOps.INSTANCE, json);
            CompoundTag parameters = assertInstanceOf(CompoundTag.class, nbt);
            Tag modifiers = parameters.get("attribute_modifiers");
            return assertInstanceOf(ListTag.class, modifiers,
                "physical resource must contain a compound modifier list: " + skill);
        }
    }

    @Test
    void allEightActualPublisherLegacyModifierRowsRejectVanillaMapCodec() throws Exception {
        int count = 0;
        try (ZipFile zip = new ZipFile(publisherJar().toFile())) {
            for (var expected : LEGACY_ROWS.entrySet()) {
                ListTag modifiers = actualModifierList(zip, expected.getKey());
                assertEquals(expected.getValue().intValue(), modifiers.size(),
                    "number of physical modifier rows drifted: " + expected.getKey());

                for (int i = 0; i < modifiers.size(); i++) {
                    CompoundTag row = assertInstanceOf(CompoundTag.class, modifiers.get(i));
                    assertTrue(row.contains("attribute"), "attribute identity must remain present");
                    assertTrue(row.contains("name") && row.contains("uuid"), "legacy identity shape changed");
                    assertFalse(row.contains("id"), "legacy raw record unexpectedly gained modern id");
                    assertTrue(row.getString("operation").equals("addition")
                            || row.getString("operation").equals("multiply_total"),
                        "expected legacy operation on physical row");
                    assertFalse(AttributeModifier.MAP_CODEC.codec()
                            .parse(NbtOps.INSTANCE, row).result().isPresent(),
                        "physical legacy row unexpectedly decoded: " + expected.getKey() + "[" + i + "]");
                    count++;
                }
                assertFalse(Codec.list(AttributeModifier.MAP_CODEC.codec())
                        .parse(NbtOps.INSTANCE, modifiers).result().isPresent(),
                    "physical legacy list unexpectedly decoded: " + expected.getKey());
            }
        }
        assertEquals(8, count, "all eight exact physical rows must be examined");
    }

    @Test
    void controlsBasedOnActualAmountsDecodeWithModernIdAndOperations() throws Exception {
        int count = 0;
        try (ZipFile zip = new ZipFile(publisherJar().toFile())) {
            for (var expected : LEGACY_ROWS.entrySet()) {
                ListTag physical = actualModifierList(zip, expected.getKey());
                ListTag convertedControls = new ListTag();
                for (int i = 0; i < physical.size(); i++) {
                    CompoundTag legacy = assertInstanceOf(CompoundTag.class, physical.get(i));
                    CompoundTag control = new CompoundTag();
                    control.putString("id", "epicfight:publisher_codec_control_" + count);
                    control.putDouble("amount", legacy.getDouble("amount"));
                    control.putString("operation", legacy.getString("operation").equals("addition")
                        ? "add_value" : "add_multiplied_total");
                    assertTrue(AttributeModifier.MAP_CODEC.codec()
                            .parse(NbtOps.INSTANCE, control).result().isPresent(),
                        "modern positive codec control must decode: " + expected.getKey());
                    convertedControls.add(control);
                    count++;
                }
                var result = Codec.list(AttributeModifier.MAP_CODEC.codec())
                    .parse(NbtOps.INSTANCE, convertedControls).result();
                assertTrue(result.isPresent(), "modern control list must decode: " + expected.getKey());
                assertEquals(physical.size(), result.get().size(),
                    "modern control list count changed: " + expected.getKey());
            }
        }
        assertEquals(8, count, "all physical amounts must be exercised in modern positive controls");
    }
}
