package dev.gustavopere.blackarcana.qa.stage05;

import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntimeManager;
import net.neoforged.fml.common.Mod;

/**
 * Removable physical-QA companion for Stage 05. This mod is deliberately
 * packaged separately from Black Arcana production content.
 */
@Mod(Stage05QaFixtureMod.MOD_ID)
public final class Stage05QaFixtureMod {
    public static final String MOD_ID = Stage05LoadoutQaFixtureContent.NAMESPACE;

    public Stage05QaFixtureMod() {
        ArcanaServerRuntimeManager.addInitializer(Stage05LoadoutQaFixtureContent::install);
    }
}
