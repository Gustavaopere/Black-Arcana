import java.util.function.Supplier;
/** Independent synthetic Java 21 fixture, not upstream implementation. */
final class RiteHolder<T>{}
final class Rite{}
final class MalumMod{static final String MALUM="malum";}
final class Registry<T>{}
final class DeferredRiteTypes{
 static DeferredRiteTypes create(String id){return new DeferredRiteTypes();}
 Registry<Rite> makeRegistry(Supplier<Object> o){return new Registry<>();}
 RiteHolder<Rite> register(String id,Supplier<Rite> o){return new RiteHolder<>();}
}
public class MalumRiteRegistryFixture{
 static final DeferredRiteTypes RITE_TYPES=DeferredRiteTypes.create(MalumMod.MALUM);
 static final Registry<Rite> RITE_REGISTRY=RITE_TYPES.makeRegistry(()->"registry");
 static final RiteHolder<Rite> UNDIRECTED_RITE=RITE_TYPES.register("undirected_rite",()->new Rite());
 static final RiteHolder<Rite> UNCHAINED_RITE=RITE_TYPES.register("unchained_rite",()->new Rite());
}