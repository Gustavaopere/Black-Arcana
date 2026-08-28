package dev.gustavopere.blackarcana.client;

import net.neoforged.neoforge.common.ModConfigSpec;

/** Client-only presentation preferences. None of these values participate in gameplay validation. */
public final class BlackArcanaClientConfig {
    public enum RadialBehavior { TOGGLE, HOLD }
    public enum FeedbackLevel { MINIMAL, STANDARD, VERBOSE }

    private static final ModConfigSpec.Builder BUILDER = new ModConfigSpec.Builder();

    public static final ModConfigSpec.BooleanValue CONTEXTUAL_HUD = BUILDER
            .comment("Show Black Arcana contextual cast feedback. No permanent resource bar is rendered.")
            .translation("config.black_arcana.contextual_hud")
            .define("contextualHud", true);
    public static final ModConfigSpec.DoubleValue HUD_SCALE = BUILDER
            .comment("Scale of contextual Black Arcana HUD elements.")
            .translation("config.black_arcana.hud_scale")
            .defineInRange("hudScale", 1.0D, 0.5D, 2.0D);
    public static final ModConfigSpec.EnumValue<HudLayout.Anchor> HUD_ANCHOR = BUILDER
            .comment("Anchor used by the contextual HUD.")
            .translation("config.black_arcana.hud_anchor")
            .defineEnum("hudAnchor", HudLayout.Anchor.BOTTOM_CENTER);
    public static final ModConfigSpec.IntValue SELECTION_DURATION_TICKS = BUILDER
            .comment("How long a selected spell remains visible after selection or cast input.")
            .translation("config.black_arcana.selection_duration_ticks")
            .defineInRange("selectionDurationTicks", 60, 0, 400);
    public static final ModConfigSpec.IntValue FEEDBACK_DURATION_TICKS = BUILDER
            .comment("How long authoritative cast results remain visible.")
            .translation("config.black_arcana.feedback_duration_ticks")
            .defineInRange("feedbackDurationTicks", 80, 0, 400);
    public static final ModConfigSpec.EnumValue<FeedbackLevel> FEEDBACK_LEVEL = BUILDER
            .comment("MINIMAL shows denials only; STANDARD also shows selection; VERBOSE includes success feedback.")
            .translation("config.black_arcana.feedback_level")
            .defineEnum("feedbackLevel", FeedbackLevel.STANDARD);
    public static final ModConfigSpec.EnumValue<RadialBehavior> RADIAL_BEHAVIOR = BUILDER
            .comment("TOGGLE keeps the radial open until selection/close. HOLD closes it when the radial key is released.")
            .translation("config.black_arcana.radial_behavior")
            .defineEnum("radialBehavior", RadialBehavior.TOGGLE);
    public static final ModConfigSpec.DoubleValue PARTICLE_DENSITY = BUILDER
            .comment("Client-side multiplier reserved for Black Arcana particles. It never changes server effects.")
            .translation("config.black_arcana.particle_density")
            .defineInRange("particleDensity", 1.0D, 0.0D, 1.0D);
    public static final ModConfigSpec.BooleanValue REDUCED_MOTION = BUILDER
            .comment("Reduce future Black Arcana camera/screen motion effects on this client.")
            .translation("config.black_arcana.reduced_motion")
            .define("reducedMotion", false);
    public static final ModConfigSpec.BooleanValue REDUCED_FLASHES = BUILDER
            .comment("Reduce future Black Arcana flashing effects on this client.")
            .translation("config.black_arcana.reduced_flashes")
            .define("reducedFlashes", false);

    public static final ModConfigSpec SPEC = BUILDER.build();

    private BlackArcanaClientConfig() { }
}
