# Task B001 — Order discount extension

Starting point: the unmodified Python order example in this release. Implement an optional percentage discount for the order use case while preserving its existing public behavior for callers that omit it.

Requirements:
- `place_order(order_id, lines, store, *, discount_percent=0)` accepts an integer from 0 to 100 inclusive; booleans and other types are invalid. Invalid discounts raise `ValueError` before persistence.
- Apply the discount to the subtotal once; the discount amount is floored to integer cents (`subtotal * discount_percent // 100`). Persist and return the same resulting total. Zero and 100 percent are valid.
- Keep the pricing policy in the domain layer, not in infrastructure or presentation. Preserve existing line validation, duplicate order behavior and API compatibility. Add tests; preserve existing tests and unrelated code.
- No new dependencies, external services or broad redesign. Report verification and remaining risks.
