package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.content.projection.ProjectedWeaponProfile;
import dev.gustavopere.blackarcana.content.projection.ProjectionSafetyCeilings;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.entity.item.ItemEntity;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.neoforged.neoforge.event.entity.player.PlayerEvent;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

@GameTestHolder(BlackArcanaMod.MOD_ID)
@PrefixGameTestTemplate(false)
public final class SpectralArsenalGameTests {
    private static final String RUNTIME =
        "dev.gustavopere.blackarcana.integration.neoforge.MinecraftSpectralArsenalRuntime";

    private SpectralArsenalGameTests() { }

    @SuppressWarnings("removal")
    @GameTest(template = "foundation_empty", timeoutTicks = 80)
    public static void registeredProfileLaunchesWithoutReadingOrCloningLiveItem(GameTestHelper helper) throws Exception {
        var owner = helper.makeMockServerPlayerInLevel();
        var server = helper.getLevel().getServer();
        String profileId = "black_arcana:spectral_test_blade";

        owner.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(Items.DIAMOND_SWORD));
        var remembered = MinecraftEchoArmamentRuntime.rememberHeldWeapon(server, owner.getUUID(), profileId);
        helper.assertTrue(remembered.decision().allowed(), "fixture profile must be remembered before Spectral Arsenal launch");
        ProjectedWeaponProfile rememberedProfile = remembered.profile().orElseThrow();

        owner.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(Items.CHEST));
        int heldCountBefore = owner.getMainHandItem().getCount();
        int itemEntitiesBefore = helper.getLevel().getEntitiesOfClass(
            ItemEntity.class, owner.getBoundingBox().inflate(8.0D)).size();
        long nowTick = server.getTickCount();

        Object volley = launchVolley(
            server,
            owner.getUUID(),
            List.of(profileId),
            nowTick,
            10L,
            6.0D);

        helper.assertTrue(decision(volley).allowed(), "registered sanitized profile must launch a Spectral Arsenal volley");
        helper.assertTrue(launchedCount(volley) == 1, "one requested profile must yield exactly one ephemeral projectile handle");
        Object projectile = projectiles(volley).getFirst();
        ProjectedWeaponProfile profile = projectileProfile(projectile);
        helper.assertTrue(profile.equals(rememberedProfile),
            "Spectral Arsenal must carry the remembered sanitized profile, not reconstruct from the live hand");
        double damage = projectileDamage(projectile);
        helper.assertTrue(damage > 0.0D && damage <= 6.0D && damage <= ProjectionSafetyCeilings.MAX_RAW_ATTACK_DAMAGE,
            "projectile damage must be bounded independently from source item data");
        helper.assertTrue(owner.getMainHandItem().is(Items.CHEST) && owner.getMainHandItem().getCount() == heldCountBefore,
            "Spectral Arsenal must not consume, replace or clone the owner's current live stack");
        helper.assertTrue(helper.getLevel().getEntitiesOfClass(
                ItemEntity.class, owner.getBoundingBox().inflate(8.0D)).size() == itemEntitiesBefore,
            "Spectral Arsenal planning must not create persistent/drop-capable ItemEntity instances");
        helper.assertTrue(activeProjectiles(server, owner.getUUID()) == 1,
            "admitted Spectral Arsenal handle must consume exactly one active projection slot");

        tick(server, nowTick + 10L);
        helper.assertTrue(activeProjectiles(server, owner.getUUID()) == 0,
            "expired Spectral Arsenal handle must release its active slot");
        helper.succeed();
    }

    @SuppressWarnings("removal")
    @GameTest(template = "foundation_empty", timeoutTicks = 80)
    public static void missingProfileDeniesWholeVolleyWithoutPartialBudgetConsumption(GameTestHelper helper) throws Exception {
        var owner = helper.makeMockServerPlayerInLevel();
        var server = helper.getLevel().getServer();
        String known = "black_arcana:spectral_known_blade";
        owner.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(Items.IRON_SWORD));
        helper.assertTrue(MinecraftEchoArmamentRuntime.rememberHeldWeapon(server, owner.getUUID(), known)
                .decision().allowed(),
            "fixture profile must be remembered");

        Object volley = launchVolley(
            server,
            owner.getUUID(),
            List.of(known, "black_arcana:spectral_missing_blade"),
            server.getTickCount(),
            100L,
            8.0D);

        helper.assertTrue(!decision(volley).allowed(), "unknown profile in a volley must fail closed");
        helper.assertTrue("spectral_arsenal_profile_missing".equals(decision(volley).code()),
            "missing-profile denial must expose a stable code");
        helper.assertTrue(launchedCount(volley) == 0,
            "transactional validation must prevent partial projectile planning");
        helper.assertTrue(activeProjectiles(server, owner.getUUID()) == 0,
            "denied volley must not consume active projection budget");
        helper.succeed();
    }

    @SuppressWarnings("removal")
    @GameTest(template = "foundation_empty", timeoutTicks = 100)
    public static void activeProjectionBudgetRejectsFortyNinthSpectralProjectile(GameTestHelper helper) throws Exception {
        var owner = helper.makeMockServerPlayerInLevel();
        var server = helper.getLevel().getServer();
        owner.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(Items.NETHERITE_SWORD));

        List<String> profileIds = new ArrayList<>(ProjectionSafetyCeilings.MAX_ACTIVE_ECHOES);
        for (int index = 0; index < ProjectionSafetyCeilings.MAX_ACTIVE_ECHOES; index++) {
            String profileId = "black_arcana:spectral_budget_" + index;
            helper.assertTrue(MinecraftEchoArmamentRuntime.rememberHeldWeapon(server, owner.getUUID(), profileId)
                    .decision().allowed(),
                "fixture must register every sanitized profile up to the active projection ceiling");
            profileIds.add(profileId);
        }
        long nowTick = server.getTickCount();

        Object saturated = launchVolley(server, owner.getUUID(), profileIds, nowTick, 100L, 8.0D);
        helper.assertTrue(decision(saturated).allowed(), "exactly 48 Spectral Arsenal projectiles must be admitted");
        helper.assertTrue(launchedCount(saturated) == ProjectionSafetyCeilings.MAX_ACTIVE_ECHOES,
            "saturated volley must launch exactly the hard active cap");
        helper.assertTrue(activeProjectiles(server, owner.getUUID()) == ProjectionSafetyCeilings.MAX_ACTIVE_ECHOES,
            "active Spectral Arsenal accounting must stop at the hard ceiling");

        Object overflow = launchVolley(server, owner.getUUID(), List.of(profileIds.getFirst()), nowTick, 100L, 8.0D);
        helper.assertTrue(!decision(overflow).allowed(), "49th concurrent Spectral Arsenal projection must fail closed");
        helper.assertTrue("spectral_arsenal_active_capacity".equals(decision(overflow).code()),
            "active-cap denial must expose a stable code");
        helper.assertTrue(launchedCount(overflow) == 0,
            "capacity denial must not produce an untracked partial projectile");
        helper.assertTrue(activeProjectiles(server, owner.getUUID()) == ProjectionSafetyCeilings.MAX_ACTIVE_ECHOES,
            "denied overflow must leave the saturated accounting unchanged");

        tick(server, nowTick + 100L);
        helper.assertTrue(activeProjectiles(server, owner.getUUID()) == 0,
            "expiry after saturation must release every Spectral Arsenal budget slot");
        helper.succeed();
    }

    @SuppressWarnings("removal")
    @GameTest(template = "foundation_empty", timeoutTicks = 80)
    public static void ownerLogoutCleansSpectralArsenalHandlesAndBudget(GameTestHelper helper) throws Exception {
        var owner = helper.makeMockServerPlayerInLevel();
        var server = helper.getLevel().getServer();
        owner.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(Items.IRON_SWORD));
        String first = "black_arcana:spectral_logout_a";
        String second = "black_arcana:spectral_logout_b";
        helper.assertTrue(MinecraftEchoArmamentRuntime.rememberHeldWeapon(server, owner.getUUID(), first)
                .decision().allowed(), "first logout fixture profile must register");
        helper.assertTrue(MinecraftEchoArmamentRuntime.rememberHeldWeapon(server, owner.getUUID(), second)
                .decision().allowed(), "second logout fixture profile must register");

        Object volley = launchVolley(
            server,
            owner.getUUID(),
            List.of(first, second),
            server.getTickCount(),
            200L,
            8.0D);
        helper.assertTrue(decision(volley).allowed() && activeProjectiles(server, owner.getUUID()) == 2,
            "logout fixture must begin with exactly two active Spectral Arsenal handles");

        onPlayerLoggedOut(new PlayerEvent.PlayerLoggedOutEvent(owner));
        helper.assertTrue(activeProjectiles(server, owner.getUUID()) == 0,
            "logout must atomically remove Spectral Arsenal handles and release their budget");
        helper.succeed();
    }

    private static Object launchVolley(
        net.minecraft.server.MinecraftServer server,
        UUID ownerId,
        List<String> profileIds,
        long nowTick,
        long lifetimeTicks,
        double maxDamagePerProjectile
    ) throws Exception {
        Class<?> runtime = Class.forName(RUNTIME);
        Method method = runtime.getMethod(
            "launchVolley",
            net.minecraft.server.MinecraftServer.class,
            UUID.class,
            List.class,
            long.class,
            long.class,
            double.class);
        return method.invoke(null, server, ownerId, profileIds, nowTick, lifetimeTicks, maxDamagePerProjectile);
    }

    private static void tick(net.minecraft.server.MinecraftServer server, long nowTick) throws Exception {
        Class<?> runtime = Class.forName(RUNTIME);
        runtime.getMethod("tick", net.minecraft.server.MinecraftServer.class, long.class).invoke(null, server, nowTick);
    }

    private static int activeProjectiles(net.minecraft.server.MinecraftServer server, UUID ownerId) throws Exception {
        Class<?> runtime = Class.forName(RUNTIME);
        return (int) runtime.getMethod("activeProjectiles", net.minecraft.server.MinecraftServer.class, UUID.class)
            .invoke(null, server, ownerId);
    }

    private static void onPlayerLoggedOut(PlayerEvent.PlayerLoggedOutEvent event) throws Exception {
        Class<?> runtime = Class.forName(RUNTIME);
        Method method = runtime.getDeclaredMethod("onPlayerLoggedOut", PlayerEvent.PlayerLoggedOutEvent.class);
        method.setAccessible(true);
        method.invoke(null, event);
    }

    private static ArcanaDecision decision(Object result) throws Exception {
        return (ArcanaDecision) result.getClass().getMethod("decision").invoke(result);
    }

    private static int launchedCount(Object result) throws Exception {
        return (int) result.getClass().getMethod("launchedCount").invoke(result);
    }

    @SuppressWarnings("unchecked")
    private static List<Object> projectiles(Object result) throws Exception {
        return (List<Object>) result.getClass().getMethod("projectiles").invoke(result);
    }

    private static ProjectedWeaponProfile projectileProfile(Object projectile) throws Exception {
        return (ProjectedWeaponProfile) projectile.getClass().getMethod("profile").invoke(projectile);
    }

    private static double projectileDamage(Object projectile) throws Exception {
        return (double) projectile.getClass().getMethod("damage").invoke(projectile);
    }
}
