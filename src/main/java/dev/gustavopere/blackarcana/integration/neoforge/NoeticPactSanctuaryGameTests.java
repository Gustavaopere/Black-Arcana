package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.content.noetic.FamiliarOwnershipProvider;
import dev.gustavopere.blackarcana.content.noetic.FamiliarOwnershipRegistry;
import dev.gustavopere.blackarcana.content.noetic.PactSanctuarySpec;
import net.minecraft.core.BlockPos;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.server.MinecraftServer;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.Mob;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

import java.util.Set;
import java.util.UUID;

@GameTestHolder(BlackArcanaMod.MOD_ID)
@PrefixGameTestTemplate(false)
public final class NoeticPactSanctuaryGameTests {
    private NoeticPactSanctuaryGameTests() { }

    @GameTest(template = "foundation_empty", timeoutTicks = 100)
    public static void ownedFamiliarSuppressesOnlyExplicitMemberTarget(GameTestHelper helper) {
        MinecraftServer server = helper.getLevel().getServer();
        LivingEntity owner = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(1, 2, 2));
        LivingEntity familiar = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(2, 2, 2));
        LivingEntity member = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(2, 2, 3));
        LivingEntity outsider = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(2, 2, 1));
        Mob memberAttacker = helper.spawnWithNoFreeWill(EntityType.ZOMBIE, new BlockPos(3, 2, 2));
        Mob outsiderAttacker = helper.spawnWithNoFreeWill(EntityType.ZOMBIE, new BlockPos(3, 2, 3));

        FamiliarOwnershipRegistry ownership = ownershipFor(owner.getUUID(), familiar.getUUID());
        MinecraftPactSanctuaryRuntime runtime = new MinecraftPactSanctuaryRuntime(ownership);
        PactSanctuarySpec spec = new PactSanctuarySpec(3, 200, 1);

        memberAttacker.setTarget(member);
        outsiderAttacker.setTarget(outsider);
        ArcanaDecision activation = runtime.activate(
                server,
                owner.getUUID(),
                familiar.getUUID(),
                spec,
                Set.of(member.getUUID()));

        helper.assertTrue(activation.allowed(), "explicitly owned familiar must activate Pact Sanctuary");
        helper.assertTrue(runtime.activeSanctuaries(server) == 1, "activation must create exactly one bounded sanctuary");

        int suppressed = runtime.tick(server);
        helper.assertTrue(suppressed == 1, "one eligible hostile target must be suppressed");
        helper.assertTrue(memberAttacker.getTarget() == null, "explicit sanctuary member must be protected from the current hostile target");
        helper.assertTrue(outsiderAttacker.getTarget() == outsider, "non-member targeting must remain untouched");

        helper.assertTrue(runtime.clearEntity(server, familiar.getUUID()) == 1, "clearing the familiar must close its sanctuary once");
        helper.assertTrue(runtime.clearEntity(server, familiar.getUUID()) == 0, "sanctuary cleanup must be idempotent");
        helper.assertTrue(runtime.activeSanctuaries(server) == 0, "cleanup must leave no active sanctuary");
        helper.succeed();
    }

    @GameTest(template = "foundation_empty", timeoutTicks = 100)
    public static void foreignOrUnsupportedFamiliarFailsClosed(GameTestHelper helper) {
        MinecraftServer server = helper.getLevel().getServer();
        LivingEntity owner = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(1, 2, 2));
        LivingEntity familiar = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(2, 2, 2));

        FamiliarOwnershipRegistry foreign = new FamiliarOwnershipRegistry(1);
        foreign.register(new FamiliarOwnershipProvider() {
            @Override
            public String providerId() {
                return "gametest:foreign";
            }

            @Override
            public Result ownership(UUID ownerId, Object candidate) {
                return Result.NOT_OWNED;
            }
        });

        MinecraftPactSanctuaryRuntime runtime = new MinecraftPactSanctuaryRuntime(foreign);
        ArcanaDecision denied = runtime.activate(
                server,
                owner.getUUID(),
                familiar.getUUID(),
                new PactSanctuarySpec(3, 200, 1),
                Set.of(owner.getUUID()));
        helper.assertTrue(!denied.allowed(), "foreign familiar must fail closed");
        helper.assertTrue("pact_sanctuary_foreign_familiar".equals(denied.code()), "foreign ownership denial must remain explicit");
        helper.assertTrue(runtime.activeSanctuaries(server) == 0, "denied activation must not leak sanctuary state");

        MinecraftPactSanctuaryRuntime unsupported = new MinecraftPactSanctuaryRuntime(new FamiliarOwnershipRegistry(1));
        ArcanaDecision unsupportedDecision = unsupported.activate(
                server,
                owner.getUUID(),
                familiar.getUUID(),
                new PactSanctuarySpec(3, 200, 1),
                Set.of(owner.getUUID()));
        helper.assertTrue(!unsupportedDecision.allowed(), "unknown ownership must fail closed");
        helper.assertTrue("pact_sanctuary_ownership_unsupported".equals(unsupportedDecision.code()), "unsupported ownership denial must remain explicit");
        helper.assertTrue(unsupported.activeSanctuaries(server) == 0, "unsupported activation must not leak sanctuary state");
        helper.succeed();
    }

    private static FamiliarOwnershipRegistry ownershipFor(UUID ownerId, UUID familiarId) {
        FamiliarOwnershipRegistry registry = new FamiliarOwnershipRegistry(1);
        registry.register(new FamiliarOwnershipProvider() {
            @Override
            public String providerId() {
                return "gametest:owned";
            }

            @Override
            public Result ownership(UUID requestedOwner, Object candidate) {
                if (!(candidate instanceof LivingEntity living)) return Result.UNSUPPORTED;
                return requestedOwner.equals(ownerId) && living.getUUID().equals(familiarId)
                        ? Result.OWNED
                        : Result.NOT_OWNED;
            }
        });
        return registry;
    }
}
