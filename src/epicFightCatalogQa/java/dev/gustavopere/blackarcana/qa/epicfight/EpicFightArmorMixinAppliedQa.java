package dev.gustavopere.blackarcana.qa.epicfight;

import com.mojang.logging.LogUtils;
import net.minecraft.world.entity.LivingEntity;
import org.slf4j.Logger;

import java.lang.reflect.Method;

/**
 * Read-only opt-in class-transformation observation in an actual NeoForge server.
 *
 * The emitted PASS requires a compiler-generated Mixin handler on the loaded
 * LivingEntity target with the expected source, amount and CallbackInfoReturnable
 * signature. It proves handler installation, not handler invocation, armor
 * reduction, combat damage, player patch lifecycle or real client behavior.
 *
 * No Epic Fight source/code is copied or executed by this observer.
 */
final class EpicFightArmorMixinAppliedQa {
    private static final Logger LOG = LogUtils.getLogger();
    private static final String PREFIX = "[BLACK_ARCANA_EPICFIGHT_ARMOR_MIXIN_QA]";
    private static final String EXPECTED_FRAGMENT = "epicfight$getDamageAfterArmorAbsorb";

    private EpicFightArmorMixinAppliedQa() {
    }

    static void inspectLoadedTarget() {
        int matching = 0;
        int mismatched = 0;
        try {
            // This is the target class loaded by the running NeoForge server,
            // NOT the publisher's untransformed Mixin classfile from its JAR.
            for (Method method : LivingEntity.class.getDeclaredMethods()) {
                String name = method.getName();
                if (!name.contains(EXPECTED_FRAGMENT)) continue;
                Class<?>[] params = method.getParameterTypes();
                boolean expected = name.startsWith("handler$")
                    && method.getReturnType() == Void.TYPE
                    && params.length == 3
                    && params[0].getName().equals("net.minecraft.world.damagesource.DamageSource")
                    && params[1] == Float.TYPE
                    && params[2].getName().equals(
                        "org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable");
                if (expected) {
                    matching++;
                } else {
                    mismatched++;
                }
            }
            if (matching == 1 && mismatched == 0) {
                LOG.info("{} type=result status=TRANSFORMED_HANDLER_PRESENT handler_count=1 "
                    + "handler_invoked=false damage_tested=false client_connected=false "
                    + "mastery_tested=false", PREFIX);
            } else {
                LOG.warn("{} type=result status=HANDLER_SIGNATURE_NOT_EXACT "
                    + "matching={} mismatched={} handler_invoked=false "
                    + "damage_tested=false client_connected=false", PREFIX,
                    matching, mismatched);
            }
        } catch (LinkageError | RuntimeException error) {
            LOG.warn("{} type=result status=REFLECTION_OR_LINKAGE_UNAVAILABLE exception={} "
                + "handler_invoked=false damage_tested=false client_connected=false",
                PREFIX, error.getClass().getName());
        }
    }
}
