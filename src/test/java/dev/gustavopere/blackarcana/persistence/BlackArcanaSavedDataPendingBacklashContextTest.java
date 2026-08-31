package dev.gustavopere.blackarcana.persistence;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.hazard.ArcanaDamageInstanceId;
import dev.gustavopere.blackarcana.api.hazard.ArcaneEmergencyProtectionSnapshot;
import dev.gustavopere.blackarcana.core.hazard.PendingBacklashDebt;
import dev.gustavopere.blackarcana.core.hazard.PendingBacklashRegistry;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.nbt.ListTag;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;

class BlackArcanaSavedDataPendingBacklashContextTest {
    private static final UUID PLAYER = UUID.fromString("62000000-0000-0000-0000-000000000001");
    private static final ArcanaCastId ROOT = ArcanaCastId.parse("62000000-0000-0000-0000-000000000021");
    private static final ArcanaDamageInstanceId DAMAGE = new ArcanaDamageInstanceId(
        UUID.fromString("62000000-0000-0000-0000-000000000011"));

    @Test
    void contextualDebtRoundTripKeepsRootDamageIdentityAndFrozenProtectionSnapshot() {
        ArcaneEmergencyProtectionSnapshot frozen = new ArcaneEmergencyProtectionSnapshot(List.of(
            new ArcaneEmergencyProtectionSnapshot.Candidate(
                "black_arcana:sealed_hood",
                "black_arcana:sealed_hood",
                8.0D,
                120L)));
        PendingBacklashDebt debt = PendingBacklashDebt.contextual(18.0D, ROOT, DAMAGE, true, frozen);
        PendingBacklashRegistry source = new PendingBacklashRegistry(16, 1_000.0D);
        assertTrue(source.accrue(PLAYER, debt));

        BlackArcanaSavedData saved = new BlackArcanaSavedData();
        saved.capturePendingBacklash(source);
        CompoundTag root = saved.save(new CompoundTag(), null);
        BlackArcanaSavedData loaded = BlackArcanaSavedData.load(root, null);

        PendingBacklashRegistry restored = new PendingBacklashRegistry(16, 1_000.0D);
        loaded.restorePendingBacklash(restored);
        PendingBacklashDebt restoredDebt = assertSingle(restored.drainDebts(PLAYER));
        assertEquals(debt, restoredDebt);
        assertEquals(ROOT, restoredDebt.rootCastId().orElseThrow());
        assertEquals(DAMAGE, restoredDebt.damageInstanceId().orElseThrow());
    }

    @Test
    void legacyAmountOnlyNbtRestoresAsExplicitlyUnprotectedDebt() {
        CompoundTag root = new CompoundTag();
        root.putInt("schema", 1);
        CompoundTag legacyDebt = new CompoundTag();
        legacyDebt.putUUID("player", PLAYER);
        legacyDebt.putDouble("amount", 11.0D);
        ListTag legacy = new ListTag();
        legacy.add(legacyDebt);
        root.put("pending_backlash", legacy);

        BlackArcanaSavedData loaded = BlackArcanaSavedData.load(root, null);
        PendingBacklashRegistry restored = new PendingBacklashRegistry(16, 1_000.0D);
        loaded.restorePendingBacklash(restored);

        PendingBacklashDebt debt = assertSingle(restored.drainDebts(PLAYER));
        assertEquals(11.0D, debt.amount(), 0.0D);
        assertTrue(debt.rootCastId().isEmpty());
        assertTrue(debt.damageInstanceId().isEmpty());
        assertFalse(debt.protectionAllowed());
        assertTrue(debt.emergencyProtectionSnapshot().candidates().isEmpty());
    }

    @Test
    void malformedContextualNbtFailsClosedToUnprotectedLegacyDebt() {
        CompoundTag root = new CompoundTag();
        root.putInt("schema", 1);

        CompoundTag malformed = new CompoundTag();
        malformed.putUUID("player", PLAYER);
        malformed.putDouble("amount", 13.0D);
        malformed.putBoolean("contextual", true);
        malformed.putBoolean("protection_allowed", true);
        ListTag contextual = new ListTag();
        contextual.add(malformed);
        root.put("pending_backlash_debts", contextual);

        BlackArcanaSavedData loaded = BlackArcanaSavedData.load(root, null);
        PendingBacklashRegistry restored = new PendingBacklashRegistry(16, 1_000.0D);
        loaded.restorePendingBacklash(restored);

        PendingBacklashDebt debt = assertSingle(restored.drainDebts(PLAYER));
        assertEquals(13.0D, debt.amount(), 0.0D);
        assertTrue(debt.rootCastId().isEmpty());
        assertTrue(debt.damageInstanceId().isEmpty());
        assertFalse(debt.protectionAllowed());
        assertTrue(debt.emergencyProtectionSnapshot().candidates().isEmpty());
    }

    private static <T> T assertSingle(List<T> values) {
        assertEquals(1, values.size());
        return values.getFirst();
    }
}
