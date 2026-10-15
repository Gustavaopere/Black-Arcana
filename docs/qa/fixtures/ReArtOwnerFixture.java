import java.util.function.Supplier;

/** Synthetic Java 21 switch and LambdaMetafactory fixture; no provider implementation. */
public class ReArtOwnerFixture {
    public static class HatItem { public HatItem() {} }
    public static class ToolItem { public ToolItem() {} }
    public static class FoodItem { public FoodItem() {} }

    private static Object register(String name, Supplier<?> supplier) { return supplier.get(); }
    private static Object wearableItem(String name, Supplier<?> supplier) { return supplier.get(); }

    private static Object redirectWearableItem(String name, Supplier<?> original) {
        return switch (name) {
            case "plastic_drinking_hat", "novelty_drinking_hat" -> register(name, HatItem::new);
            case "snorkel" -> register(name, ToolItem::new);
            default -> wearableItem(name, original);
        };
    }

    private static Object redirectRegister(String name, Supplier<?> original) {
        return switch (name) {
            case "eternal_steak" -> register(name, FoodItem::new);
            default -> register(name, original);
        };
    }
}
