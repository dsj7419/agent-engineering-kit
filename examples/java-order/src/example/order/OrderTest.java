package example.order;

import java.util.UUID;

/** Dependency-free executable checks; no JVM assertion flag required. */
public final class OrderTest {
    public static void main(String[] args) {
        totalsAndSnapshots();
        discountAndAtomicity();
        lifecycle();
        invalidInputsAndOverflow();
        System.out.println("4 Java example scenarios passed");
    }

    private static Order order() {
        return new Order(UUID.fromString("00000000-0000-0000-0000-000000000001"));
    }

    private static void totalsAndSnapshots() {
        Order order = order();
        order.addItem("A", 2, 300);
        order.addItem("B", 1, 200);
        check(order.contains("A") && order.distinctItems() == 2, "items");
        check(order.subtotal() == 800, "subtotal");
        Order.Snapshot old = order.snapshot();
        order.changeQuantity("A", 3);
        order.removeItem("B");
        check(order.total() == 900 && old.total() == 800, "snapshot isolation");
        expect(UnsupportedOperationException.class, () -> order.lines().clear());
        expect(UnsupportedOperationException.class, () -> old.lines().clear());
    }

    private static void discountAndAtomicity() {
        Order order = order();
        order.addItem("A", 2, 500);
        order.applyDiscount(750);
        Order.Snapshot old = order.snapshot();
        expect(IllegalArgumentException.class, () -> order.changeQuantity("A", 1));
        expect(IllegalArgumentException.class, () -> order.removeItem("A"));
        expect(IllegalArgumentException.class, () -> order.applyDiscount(1001));
        expect(IllegalArgumentException.class, () -> order.applyDiscount(-1));
        check(order.snapshot().equals(old), "failed mutations must be atomic");
        check(order.total() == 250, "discount total");
        order.clearDiscount();
        order.removeItem("A");
        check(order.total() == 0, "clear discount then remove");
    }

    private static void lifecycle() {
        Order order = order();
        expect(IllegalStateException.class, order::confirm);
        order.addItem("A", 1, 500);
        order.confirm();
        check(order.status() == Order.Status.CONFIRMED, "confirmation");
        expect(IllegalStateException.class, () -> order.applyDiscount(1));
        expect(IllegalStateException.class, () -> order.changeQuantity("A", 2));
        expect(IllegalStateException.class, () -> order.removeItem("A"));
        expect(IllegalStateException.class, () -> order.addItem("B", 1, 1));
        order.cancel();
        check(order.status() == Order.Status.CANCELLED, "cancellation");
        expect(IllegalStateException.class, order::cancel);
        expect(IllegalStateException.class, order::confirm);
    }

    private static void invalidInputsAndOverflow() {
        Order order = order();
        expect(IllegalArgumentException.class, () -> order.addItem("", 1, 1));
        expect(IllegalArgumentException.class, () -> order.addItem("A", 0, 1));
        expect(IllegalArgumentException.class, () -> order.addItem("A", 1, -1));
        expect(ArithmeticException.class, () -> order.addItem("A", 2, Long.MAX_VALUE));
        order.addItem("A", 1, Long.MAX_VALUE);
        Order.Snapshot old = order.snapshot();
        expect(ArithmeticException.class, () -> order.addItem("B", 1, 1));
        expect(ArithmeticException.class, () -> order.changeQuantity("A", 2));
        expect(IllegalArgumentException.class, () -> order.addItem("A", 1, 1));
        expect(IllegalArgumentException.class, () -> order.removeItem("missing"));
        check(order.snapshot().equals(old), "overflow must not mutate state");
    }

    private static void check(boolean condition, String message) {
        if (!condition) {
            throw new AssertionError(message);
        }
    }

    private static void expect(Class<? extends RuntimeException> type, Runnable operation) {
        try {
            operation.run();
        } catch (RuntimeException error) {
            if (type.isInstance(error)) {
                return;
            }
            throw new AssertionError("Unexpected exception", error);
        }
        throw new AssertionError("Expected " + type.getSimpleName());
    }
}
