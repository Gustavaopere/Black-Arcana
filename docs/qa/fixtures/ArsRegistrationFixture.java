class SpellPart {}
class RitualPart {}
class MethodProjectile extends SpellPart { static final MethodProjectile INSTANCE=new MethodProjectile(); }
class EffectHarm extends SpellPart { static final EffectHarm INSTANCE=new EffectHarm(); }
class RitualFlight extends RitualPart {}
class RitualBinding extends RitualPart {}
public class ArsRegistrationFixture {
    public static void registerSpell(SpellPart part) {}
    public static void registerRitual(RitualPart ritual) {}
    public static void setup() {
        registerSpell(MethodProjectile.INSTANCE);
        registerSpell(EffectHarm.INSTANCE);
        registerRitual(new RitualFlight());
        registerRitual(new RitualBinding());
    }
}
