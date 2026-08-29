package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.content.blood.BloodPriceHealthAccess;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.level.GameType;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

@GameTestHolder(BlackArcanaMod.MOD_ID)
@PrefixGameTestTemplate(false)
public final class BloodPriceGameTests {
    private BloodPriceGameTests() { }

    @SuppressWarnings("removal")
    @GameTest(template = "foundation_empty", timeoutTicks = 60)
    public static void realHealthReservationNeverConsumesAbsorptionAndRevalidatesFloor(GameTestHelper helper) throws Exception {
        ServerPlayer caster = helper.makeMockServerPlayerInLevel();
        caster.setGameMode(GameType.SURVIVAL);
        caster.getAbilities().invulnerable = false;
        caster.getAbilities().instabuild = false;
        caster.onUpdateAbilities();
        caster.setHealth(20.0F);
        var maxAbsorption = caster.getAttribute(Attributes.MAX_ABSORPTION);
        helper.assertTrue(maxAbsorption != null, "fixture requires the vanilla max-absorption attribute");
        maxAbsorption.setBaseValue(8.0D);
        caster.setAbsorptionAmount(8.0F);
        helper.assertTrue(caster.getAbsorptionAmount() == 8.0F, "fixture must begin with eight absorption");

        MinecraftServer server = helper.getLevel().getServer();
        Class<?> implementation = Class.forName(
            "dev.gustavopere.blackarcana.integration.neoforge.NeoForgeBloodPriceHealthAccess");
        BloodPriceHealthAccess access = (BloodPriceHealthAccess) implementation
            .getConstructor(MinecraftServer.class)
            .newInstance(server);

        var reservation = access.reserve(caster.getUUID(), 4.0D, 4.0D);
        helper.assertTrue(reservation.reserved(), "four real health should be reservable above the floor");
        helper.assertTrue(caster.getHealth() == 16.0F, "Blood Price must deduct exactly four real health");
        helper.assertTrue(caster.getAbsorptionAmount() == 8.0F, "Blood Price must never consume absorption");

        reservation.refund();
        helper.assertTrue(caster.getHealth() == 20.0F, "refund must restore exactly the reserved real health");
        helper.assertTrue(caster.getAbsorptionAmount() == 8.0F, "refund must not alter absorption");

        caster.setHealth(5.0F);
        var denied = access.reserve(caster.getUUID(), 2.0D, 4.0D);
        helper.assertTrue(!denied.reserved(), "reservation crossing the minimum health floor must fail closed");
        helper.assertTrue(caster.getHealth() == 5.0F, "denied reservation must not mutate health");
        helper.assertTrue(caster.getAbsorptionAmount() == 8.0F, "denied reservation must not mutate absorption");
        helper.succeed();
    }
}
