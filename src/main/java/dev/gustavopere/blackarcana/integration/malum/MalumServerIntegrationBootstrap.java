package dev.gustavopere.blackarcana.integration.malum;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.core.ritual.BlackArcanaGrandRituals;
import dev.gustavopere.blackarcana.core.ritual.RitualCompletionKey;
import dev.gustavopere.blackarcana.core.ritual.RitualCompletionLedger;
import dev.gustavopere.blackarcana.core.ritual.RitualContext;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;
import dev.gustavopere.blackarcana.integration.rpg.RpgSkillTreeBridge;
import dev.gustavopere.blackarcana.persistence.RitualCompletionSavedData;
import net.minecraft.core.BlockPos;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.neoforged.fml.ModList;

import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;

/** Loaded reflectively only when Malum is present. */
public final class MalumServerIntegrationBootstrap {
    private MalumServerIntegrationBootstrap() { }

    public static void install(MinecraftServer server, ArcanaServerRuntime runtime) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(runtime, "runtime");

        String version = ModList.get().getModContainerById(MalumIntegrationIds.MOD_ID)
            .map(container -> container.getModInfo().getVersion().toString())
            .orElse("not-loaded");
        MalumIntegrationBridge bridge = MalumIntegrationBridge.probe(true, version, server);
        runtime.integrations().register(bridge);

        BlackArcanaMod.LOGGER.info(
            "Black Arcana integration {}: {} version={} capabilities={}{}",
            bridge.integrationId(),
            bridge.availability(),
            bridge.implementationVersion(),
            bridge.capabilities(),
            bridge.diagnostic().isBlank() ? "" : " diagnostic=" + bridge.diagnostic());

        if (!bridge.available()) return;

        Optional<RpgSkillTreeBridge> rpg = runtime.integrations()
            .find(RpgSkillTreeBridge.MOD_ID)
            .filter(RpgSkillTreeBridge.class::isInstance)
            .map(RpgSkillTreeBridge.class::cast);
        MalumSyntheticContent.install(runtime, bridge.spiritAccess(), rpg);
        installGrandRitual(server, runtime, bridge.spiritAccess());
    }

    private static void installGrandRitual(
            MinecraftServer server,
            ArcanaServerRuntime runtime,
            MalumSpiritAccess spiritAccess
    ) {
        MalumRitualSpiritComponentProvider components = new MalumRitualSpiritComponentProvider(
            spiritAccess,
            Map.of(
                BlackArcanaGrandRituals.VEIL_ANCHOR_CONSECRATION_ID,
                List.of(
                    new MalumRitualSpiritRequirement("arcane", 4),
                    new MalumRitualSpiritRequirement("wicked", 2))));

        BlackArcanaGrandRituals.install(
            runtime,
            (definition, context, nowTick) -> checkGrandRitualRequirements(server, context),
            components,
            (definition, context, nowTick) -> completeGrandRitual(server, context, nowTick));
    }

    private static ArcanaDecision checkGrandRitualRequirements(MinecraftServer server, RitualContext context) {
        if (server.getPlayerList().getPlayer(context.casterId()) == null) {
            return ArcanaDecision.deny(
                "grand_ritual_caster_offline",
                "grand ritual caster must remain online");
        }

        RitualCompletionKey completion = RitualCompletionKey.forCaster(
            BlackArcanaGrandRituals.VEIL_ANCHOR_CONSECRATION_ID,
            context.casterId());
        if (RitualCompletionSavedData.get(server).contains(completion)) {
            return ArcanaDecision.deny(
                "grand_ritual_already_completed",
                "veil anchor consecration is already recorded for this caster");
        }

        ServerLevel level = findLevel(server, context.anchor().dimensionId());
        if (level == null) {
            return ArcanaDecision.deny(
                "grand_ritual_dimension_unavailable",
                "ritual anchor dimension is not loaded");
        }
        BlockPos anchorPos = BlockPos.of(context.anchor().packedBlockPos());
        if (level.getChunkSource().getChunkNow(anchorPos.getX() >> 4, anchorPos.getZ() >> 4) == null) {
            return ArcanaDecision.deny(
                "grand_ritual_chunk_unloaded",
                "ritual anchor chunk must already be loaded");
        }
        return ArcanaDecision.allow();
    }

    private static ArcanaDecision completeGrandRitual(
            MinecraftServer server,
            RitualContext context,
            long nowTick
    ) {
        RitualCompletionLedger.CompletionResult result = RitualCompletionSavedData.get(server).complete(
            RitualCompletionKey.forCaster(
                BlackArcanaGrandRituals.VEIL_ANCHOR_CONSECRATION_ID,
                context.casterId()),
            nowTick);
        return switch (result) {
            case RECORDED -> ArcanaDecision.allow();
            case ALREADY_COMPLETED -> ArcanaDecision.deny(
                "grand_ritual_duplicate_reward",
                "veil anchor consecration completion was already recorded");
            case CAPACITY_EXCEEDED -> ArcanaDecision.deny(
                "grand_ritual_completion_capacity",
                "ritual completion ledger is full");
        };
    }

    private static ServerLevel findLevel(MinecraftServer server, String dimensionId) {
        for (ServerLevel level : server.getAllLevels()) {
            if (level.dimension().location().toString().equals(dimensionId)) return level;
        }
        return null;
    }
}
