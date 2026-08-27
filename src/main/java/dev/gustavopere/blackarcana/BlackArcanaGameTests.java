package dev.gustavopere.blackarcana;

import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

@GameTestHolder(BlackArcanaMod.MOD_ID)
@PrefixGameTestTemplate(false)
public final class BlackArcanaGameTests {
    private BlackArcanaGameTests() {
    }

    @GameTest(template = "foundation_empty", timeoutTicks = 20)
    public static void foundationLoadsOnDedicatedGameTestServer(GameTestHelper helper) {
        helper.assertTrue("black_arcana".equals(BlackArcanaMod.MOD_ID), "canonical mod id must remain stable");
        helper.succeed();
    }
}
