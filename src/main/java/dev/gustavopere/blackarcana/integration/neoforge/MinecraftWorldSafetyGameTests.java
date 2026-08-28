package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.api.ArcanaCastContext;
import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaCost;
import dev.gustavopere.blackarcana.api.ArcanaServices;
import dev.gustavopere.blackarcana.api.ArcanaSpellDefinition;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;
import dev.gustavopere.blackarcana.core.world.ChunkRef;
import dev.gustavopere.blackarcana.core.world.TemporaryMutationKey;
import dev.gustavopere.blackarcana.core.world.WorldEffectProfile;
import dev.gustavopere.blackarcana.core.world.WorldMutationClass;
import dev.gustavopere.blackarcana.core.world.WorldMutationType;
import net.minecraft.core.BlockPos;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.world.level.block.Blocks;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

import java.util.UUID;

@GameTestHolder(BlackArcanaMod.MOD_ID)
@PrefixGameTestTemplate(false)
public final class MinecraftWorldSafetyGameTests {
    private static final ArcanaSpellId TEMPORARY_SPELL_ID =
        ArcanaSpellId.parse("black_arcana:world_safety_gametest");

    private MinecraftWorldSafetyGameTests() { }

    @GameTest(template = "foundation_empty", timeoutTicks = 40)
    public static void backendCompareAndSetPreservesBlockState(GameTestHelper helper) {
        BlockPos relative = new BlockPos(1, 2, 1);
        BlockPos absolute = helper.absolutePos(relative);
        helper.setBlock(relative, Blocks.STONE);

        MinecraftTemporaryBlockBackend backend =
            new MinecraftTemporaryBlockBackend(helper.getLevel().getServer());
        TemporaryMutationKey key = key(helper, absolute);
        String stone = backend.readLoadedState(key).orElseThrow();
        String obsidian = MinecraftTemporaryBlockBackend.encodeState(Blocks.OBSIDIAN.defaultBlockState());

        helper.assertTrue(
            backend.replaceIfCurrent(key, stone, obsidian),
            "loaded non-block-entity state must be replaceable through CAS");
        helper.assertTrue(
            helper.getLevel().getBlockState(absolute).is(Blocks.OBSIDIAN),
            "CAS replacement must reach the server level");
        helper.assertTrue(
            !backend.replaceIfCurrent(key, stone, MinecraftTemporaryBlockBackend.encodeState(Blocks.DIRT.defaultBlockState())),
            "stale expected state must not overwrite a newer block state");
        helper.succeed();
    }

    @GameTest(template = "foundation_empty", timeoutTicks = 40)
    public static void backendRefusesBlockEntityMutation(GameTestHelper helper) {
        BlockPos relative = new BlockPos(1, 2, 1);
        BlockPos absolute = helper.absolutePos(relative);
        helper.setBlock(relative, Blocks.CHEST);

        MinecraftTemporaryBlockBackend backend =
            new MinecraftTemporaryBlockBackend(helper.getLevel().getServer());
        TemporaryMutationKey key = key(helper, absolute);
        String chest = backend.readLoadedState(key).orElseThrow();
        String stone = MinecraftTemporaryBlockBackend.encodeState(Blocks.STONE.defaultBlockState());

        helper.assertTrue(
            !backend.replaceIfCurrent(key, chest, stone),
            "temporary mutation backend must reject block entities");
        helper.assertTrue(
            helper.getLevel().getBlockState(absolute).is(Blocks.CHEST),
            "rejected block-entity mutation must preserve the original block");
        helper.succeed();
    }

    @GameTest(template = "foundation_empty", timeoutTicks = 40)
    public static void temporaryMutationRestoresThroughRuntimeTick(GameTestHelper helper) {
        BlockPos relative = new BlockPos(1, 2, 1);
        BlockPos absolute = helper.absolutePos(relative);
        helper.setBlock(relative, Blocks.STONE);

        ArcanaServerRuntime runtime = ArcanaServerRuntime.createDefault();
        MinecraftTemporaryBlockBackend backend =
            new MinecraftTemporaryBlockBackend(helper.getLevel().getServer());
        runtime.installWorldBackend(backend, backend);
        runtime.worldEffectProfiles().register(
            TEMPORARY_SPELL_ID,
            new WorldEffectProfile(
                WorldMutationType.TEMPORARY_BLOCK,
                WorldMutationClass.TEMPORARY,
                8,
                false));

        long now = helper.getLevel().getGameTime();
        ArcanaCastRequest request = request(helper, now);
        String obsidian = MinecraftTemporaryBlockBackend.encodeState(Blocks.OBSIDIAN.defaultBlockState());

        var decision = runtime.temporaryBlockGateway().orElseThrow().replace(
            request,
            ArcanaServices.TargetResolution.resolved("world-safety-probe"),
            chunk(helper, absolute),
            key(helper, absolute),
            obsidian,
            now + 2L);

        helper.assertTrue(decision.allowed(), "safe temporary mutation must be admitted");
        helper.assertTrue(
            helper.getLevel().getBlockState(absolute).is(Blocks.OBSIDIAN),
            "temporary replacement must be visible before expiry");
        helper.assertTrue(runtime.temporaryMutations().size() == 1, "rollback record must exist before expiry");

        runtime.tick(now + 2L);

        helper.assertTrue(
            helper.getLevel().getBlockState(absolute).is(Blocks.STONE),
            "runtime tick must restore the original block after expiry");
        helper.assertTrue(runtime.temporaryMutations().size() == 0, "successful restoration must clear rollback state");
        helper.assertTrue(
            runtime.lastTemporaryRestoration().restored() == 1,
            "restoration telemetry must report the restored block");
        helper.succeed();
    }

    @GameTest(template = "foundation_empty", timeoutTicks = 40)
    public static void temporaryMutationNeverOverwritesExternalEdit(GameTestHelper helper) {
        BlockPos relative = new BlockPos(1, 2, 1);
        BlockPos absolute = helper.absolutePos(relative);
        helper.setBlock(relative, Blocks.STONE);

        ArcanaServerRuntime runtime = ArcanaServerRuntime.createDefault();
        MinecraftTemporaryBlockBackend backend =
            new MinecraftTemporaryBlockBackend(helper.getLevel().getServer());
        runtime.installWorldBackend(backend, backend);
        runtime.worldEffectProfiles().register(
            TEMPORARY_SPELL_ID,
            new WorldEffectProfile(
                WorldMutationType.TEMPORARY_BLOCK,
                WorldMutationClass.TEMPORARY,
                8,
                false));

        long now = helper.getLevel().getGameTime();
        var decision = runtime.temporaryBlockGateway().orElseThrow().replace(
            request(helper, now),
            ArcanaServices.TargetResolution.resolved("world-safety-probe"),
            chunk(helper, absolute),
            key(helper, absolute),
            MinecraftTemporaryBlockBackend.encodeState(Blocks.OBSIDIAN.defaultBlockState()),
            now + 2L);
        helper.assertTrue(decision.allowed(), "temporary mutation must be admitted before external edit");

        helper.getLevel().setBlockAndUpdate(absolute, Blocks.DIRT.defaultBlockState());
        runtime.tick(now + 2L);

        helper.assertTrue(
            helper.getLevel().getBlockState(absolute).is(Blocks.DIRT),
            "expiry must preserve a block changed by another actor");
        helper.assertTrue(runtime.temporaryMutations().size() == 0, "externally changed record must be retired");
        helper.assertTrue(
            runtime.lastTemporaryRestoration().changedByOthers() == 1,
            "restoration telemetry must record external ownership change");
        helper.succeed();
    }

    private static ArcanaCastRequest request(GameTestHelper helper, long now) {
        ArcanaSpellDefinition spell = new ArcanaSpellDefinition(
            TEMPORARY_SPELL_ID,
            "spell.black_arcana.world_safety_gametest",
            "black_arcana:textures/spell/world_safety_gametest.png",
            new ArcanaCost("black_arcana:synthetic", 1.0D),
            true);
        return new ArcanaCastRequest(
            ArcanaCastId.random(),
            spell,
            new ArcanaCastContext(
                UUID.fromString("3f30fd0d-1fe7-4491-bc40-e53a08992567"),
                now,
                helper.getLevel().dimension().location().toString()));
    }

    private static TemporaryMutationKey key(GameTestHelper helper, BlockPos absolute) {
        return new TemporaryMutationKey(
            helper.getLevel().dimension().location().toString(),
            absolute.asLong());
    }

    private static ChunkRef chunk(GameTestHelper helper, BlockPos absolute) {
        return new ChunkRef(
            helper.getLevel().dimension().location().toString(),
            absolute.getX() >> 4,
            absolute.getZ() >> 4);
    }
}
