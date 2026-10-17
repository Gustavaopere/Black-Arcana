package dev.gustavopere.blackarcana.integration.epicfight;

import net.minecraft.nbt.CompoundTag;
import net.minecraft.nbt.NbtOps;
import net.minecraft.world.entity.ai.attributes.AttributeModifier;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * Compatibility evidence for the Minecraft 1.21.1 codec Epic Fight's adjacent
 * source references. This test does not load Epic Fight and must not be used to
 * claim that an installed provider has applied any modifier or skill datapack.
 */
class EpicFightVanillaAttributeModifierCodecTest {
    private record LegacyModifierRow(
        String skill, String name, String uuid, String operation, double amount
    ) {}

    // All eight attribute_modifier rows from the FIVE packaged legacy-shaped
    // Epic Fight 21.17.3.1 skill JSONs were checked by the SHA-pinned
    // docs/qa/epicfight_211731_perk_binary.py gate. This fixture encodes only
    // the factual data shape, not proprietary source or class implementation.
    private static final List<LegacyModifierRow> LEGACY_ROWS = List.of(
        new LegacyModifierRow("adaptive_skin", "adaptive_skin_skill_stat",
            "e9cd15f0-72cc-474b-bfee-66276d06157d", "addition", 6.0D),
        new LegacyModifierRow("adrenaline_fiend", "adrenaline_skill_stat",
            "678cff5d-dc70-492d-b960-f01241d1a0f9", "multiply_total", 0.1D),
        new LegacyModifierRow("adrenaline_fiend", "adrenaline_skill_stat",
            "678cff5d-dc70-492d-b960-f01241d1a0f9", "multiply_total", 0.075D),
        new LegacyModifierRow("catharsis", "bloodlust_skill_stat",
            "0c6efd18-199e-48a6-aa1b-51a1c1f9f613", "addition", 0.15D),
        new LegacyModifierRow("catharsis", "bloodlust_skill_stat",
            "0c6efd18-199e-48a6-aa1b-51a1c1f9f613", "multiply_total", 0.1D),
        new LegacyModifierRow("bonebreaker", "bonebreaker_skill_stat",
            "06212e76-6dbe-4d4b-a875-562829bb6db4", "multiply_total", 0.15D),
        new LegacyModifierRow("vengeance", "vengeance_skill_stat",
            "bcb1f110-c987-412e-9e40-5831c62eba2e", "addition", 3.0D),
        new LegacyModifierRow("vengeance", "vengeance_skill_stat",
            "bcb1f110-c987-412e-9e40-5831c62eba2e", "multiply_total", 0.075D)
    );

    @Test
    void allEightPhysicallyAuditedLegacyRowsFailVanillaCodecParsing() {
        assertTrue(LEGACY_ROWS.size() == 8, "eight exact JSON modifier rows are required");
        assertTrue(LEGACY_ROWS.stream().map(LegacyModifierRow::skill).distinct().count() == 5,
            "five distinct legacy-bearing skill resource IDs are required");
        for (LegacyModifierRow row : LEGACY_ROWS) {
            CompoundTag raw = new CompoundTag();
            raw.putString("name", row.name());
            raw.putString("uuid", row.uuid());
            raw.putDouble("amount", row.amount());
            raw.putString("operation", row.operation());
            assertFalse(AttributeModifier.MAP_CODEC.codec().parse(NbtOps.INSTANCE, raw)
                    .result().isPresent(), "raw legacy modifier parsed unexpectedly: " + row.skill());
        }
    }

    @Test
    void modernIdCannotRescueLegacyOperationNames() {
        for (String legacyOperation : List.of("addition", "multiply_total")) {
            CompoundTag raw = new CompoundTag();
            raw.putString("id", "epicfight:legacy_operation_control");
            raw.putDouble("amount", 0.15D);
            raw.putString("operation", legacyOperation);
            assertFalse(AttributeModifier.MAP_CODEC.codec().parse(NbtOps.INSTANCE, raw)
                    .result().isPresent(), "legacy operation unexpectedly accepted: " + legacyOperation);
        }
    }

    @Test
    void modernOperationsCannotRescueMissingIdWithLegacyNameUuid() {
        for (String modernOperation : List.of("add_value", "add_multiplied_total")) {
            CompoundTag raw = new CompoundTag();
            raw.putString("name", "legacy_field_control");
            raw.putString("uuid", "12345678-1234-1234-1234-123456789012");
            raw.putDouble("amount", 0.15D);
            raw.putString("operation", modernOperation);
            assertFalse(AttributeModifier.MAP_CODEC.codec().parse(NbtOps.INSTANCE, raw)
                    .result().isPresent(), "legacy field shape unexpectedly accepted: " + modernOperation);
        }
    }

    @Test
    void bothModernOperationsDecodeWithIdPositiveControls() {
        for (String modernOperation : List.of("add_value", "add_multiplied_total")) {
            CompoundTag raw = new CompoundTag();
            raw.putString("id", "epicfight:modern_operation_control");
            raw.putDouble("amount", 0.15D);
            raw.putString("operation", modernOperation);
            assertTrue(AttributeModifier.MAP_CODEC.codec().parse(NbtOps.INSTANCE, raw)
                    .result().isPresent(), "modern operation must pass with modern id: " + modernOperation);
        }
    }

    @Test
    void exactLegacyNameUuidAdditionShapeDoesNotDecodeAsModernAttributeModifier() {
        CompoundTag raw = new CompoundTag();
        raw.putString("name", "adaptive_skin_skill_stat");
        raw.putString("uuid", "e9cd15f0-72cc-474b-bfee-66276d06157d");
        raw.putDouble("amount", 6.0D);
        raw.putString("operation", "addition");

        assertFalse(
            AttributeModifier.MAP_CODEC.codec().parse(NbtOps.INSTANCE, raw).result().isPresent(),
            "legacy name/uuid/addition must not be promoted to an applied attribute bonus");
    }

    @Test
    void modernIdAndAddValueControlDecodesWithTheSameCodec() {
        CompoundTag raw = new CompoundTag();
        raw.putString("id", "epicfight:catalog_codec_control");
        raw.putDouble("amount", 6.0D);
        raw.putString("operation", "add_value");

        assertTrue(
            AttributeModifier.MAP_CODEC.codec().parse(NbtOps.INSTANCE, raw).result().isPresent(),
            "positive control must demonstrate codec is usable in the test environment");
    }

    @Test
    void LegacyNameUuidMultiplyTotalIsAlsoRejected() {
        CompoundTag raw = new CompoundTag();
        raw.putString("name", "adrenaline_skill_stat");
        raw.putString("uuid", "678cff5d-dc70-492d-b960-f01241d1a0f9");
        raw.putDouble("amount", 0.1D);
        raw.putString("operation", "multiply_total");

        assertFalse(
            AttributeModifier.MAP_CODEC.codec().parse(NbtOps.INSTANCE, raw).result().isPresent(),
            "legacy multiply_total is serialized text, not proven loaded attribute state");
    }
}
