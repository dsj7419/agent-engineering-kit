package example.order;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.UUID;

/** Owns an order's line items, lifecycle and monetary invariants.
 * Amounts are integer minor units in one currency fixed by the caller's domain.
 * Instances are mutable, single-owner aggregates; they are not thread-safe.
 */
public final class Order {
    public enum Status { DRAFT, CONFIRMED, CANCELLED }

    public record Line(String sku, int quantity, long unitPrice) {
        public Line {
            if (sku == null || sku.isBlank()) {
                throw new IllegalArgumentException("SKU is required");
            }
            if (quantity <= 0 || unitPrice < 0) {
                throw new IllegalArgumentException("Invalid quantity or price");
            }
            Math.multiplyExact(quantity, unitPrice);
        }

        public long subtotal() {
            return Math.multiplyExact(quantity, unitPrice);
        }

        private Line withQuantity(int newQuantity) {
            return new Line(sku, newQuantity, unitPrice);
        }
    }

    public record Snapshot(UUID id, Status status, List<Line> lines,
                           long subtotal, long discount, long total) {
        public Snapshot {
            lines = List.copyOf(lines);
        }
    }

    private final UUID id;
    private final Map<String, Line> lines = new LinkedHashMap<>();
    private Status status = Status.DRAFT;
    private long discount;

    public Order(UUID id) {
        this.id = Objects.requireNonNull(id, "id");
    }

    public UUID id() {
        return id;
    }

    public Status status() {
        return status;
    }

    public List<Line> lines() {
        return List.copyOf(lines.values());
    }

    public boolean contains(String sku) {
        return lines.containsKey(sku);
    }

    public int distinctItems() {
        return lines.size();
    }

    public long subtotal() {
        long sum = 0;
        for (Line line : lines.values()) {
            sum = Math.addExact(sum, line.subtotal());
        }
        return sum;
    }

    public long discount() {
        return discount;
    }

    public long total() {
        return Math.subtractExact(subtotal(), discount);
    }

    public Snapshot snapshot() {
        long sum = subtotal();
        return new Snapshot(id, status, lines(), sum, discount, sum - discount);
    }

    public void addItem(String sku, int quantity, long unitPrice) {
        requireDraft();
        Line added = new Line(sku, quantity, unitPrice);
        if (contains(sku)) {
            throw new IllegalArgumentException("SKU already present");
        }
        long proposedSubtotal = Math.addExact(subtotal(), added.subtotal());
        validateDiscount(discount, proposedSubtotal);
        lines.put(sku, added);
    }

    public void changeQuantity(String sku, int quantity) {
        requireDraft();
        Line previous = requireLine(sku);
        Line replacement = previous.withQuantity(quantity);
        long remaining = Math.subtractExact(subtotal(), previous.subtotal());
        long proposedSubtotal = Math.addExact(remaining, replacement.subtotal());
        validateDiscount(discount, proposedSubtotal);
        lines.put(sku, replacement);
    }

    public void removeItem(String sku) {
        requireDraft();
        Line previous = requireLine(sku);
        long proposedSubtotal = Math.subtractExact(subtotal(), previous.subtotal());
        validateDiscount(discount, proposedSubtotal);
        lines.remove(sku);
    }

    public void applyDiscount(long amount) {
        requireDraft();
        validateDiscount(amount, subtotal());
        discount = amount;
    }

    public void clearDiscount() {
        applyDiscount(0);
    }

    public void confirm() {
        requireDraft();
        if (lines.isEmpty()) {
            throw new IllegalStateException("Cannot confirm an empty order");
        }
        status = Status.CONFIRMED;
    }

    public void cancel() {
        if (status == Status.CANCELLED) {
            throw new IllegalStateException("Order already cancelled");
        }
        status = Status.CANCELLED;
    }

    private void requireDraft() {
        if (status != Status.DRAFT) {
            throw new IllegalStateException("Only draft orders may be changed");
        }
    }

    private Line requireLine(String sku) {
        Line line = lines.get(sku);
        if (line == null) {
            throw new IllegalArgumentException("Unknown SKU");
        }
        return line;
    }

    private static void validateDiscount(long amount, long subtotal) {
        if (amount < 0 || amount > subtotal) {
            throw new IllegalArgumentException("Discount outside subtotal");
        }
    }
}
