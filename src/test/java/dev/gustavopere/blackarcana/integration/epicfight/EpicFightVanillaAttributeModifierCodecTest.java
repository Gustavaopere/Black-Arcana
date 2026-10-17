package dev.gustavopere.blackarcana.integration.epicfight;

import net.minecraft.nbt.CompoundTag;
import net.minecraft.nbt.NbtOps;
import net.minecraft.world.entity.ai.attributes.AttributeModifier;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * Compatibility evidence for the Minecraft 1.21.1 codec Epic Fight's adjacent
 * source references. This test does not load Epic Fight and must not be used to
 * claim that an installed provider has applied any modifier or skill datapack.
 */
class EpicFightVanillaAttributeModifierCodecTest {
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
