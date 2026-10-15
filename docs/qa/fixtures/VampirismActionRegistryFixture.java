import java.util.function.Supplier;
interface IEventBus {}
final class VampirismRegistries {
    static final class Keys { static final Object ACTION = new Object(); }
}
final class REFERENCE { static final String MODID = "vampirism"; }
final class DeferredRegister {
    static DeferredRegister create(Object registry, String modid) { return new DeferredRegister(); }
    Object register(String id, Supplier<?> supplier) { return supplier.get(); }
    void register(IEventBus bus) {}
}
final class BatVampireAction { BatVampireAction() {} }
final class FreezeVampireAction { FreezeVampireAction() {} }
public final class VampirismActionRegistryFixture {
    public static final DeferredRegister ACTIONS =
        DeferredRegister.create(VampirismRegistries.Keys.ACTION, REFERENCE.MODID);
    public static final Object BAT = ACTIONS.register("bat", BatVampireAction::new);
    public static final Object FREEZE = ACTIONS.register("freeze", FreezeVampireAction::new);
    public static void register(IEventBus bus) { ACTIONS.register(bus); }
}
