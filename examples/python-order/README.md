# Python order context — runnable example

A deliberately small example of the kit's inward dependency rules, immutable value objects, a consumer-owned port, adapter, composition root and behavior tests. Python 3.9+; no dependencies. Run from this directory:

```sh
python -m order.main
python -m unittest discover -s tests -v
```

The first command prints `700`. The second checks domain invariants, integration behavior and a small AST import allowlist. `domain.py` owns pricing; `application.py` orchestrates an order; `infrastructure.py` implements the store; `main.py` composes them. The in-memory adapter is synchronous, single-process demo code; no durability, authentication, transactions or concurrency guarantees are claimed. The import check is intentionally narrow: it cannot detect dynamic imports, arbitrary nested package structures or semantic coupling. Use appropriate production analyzers for larger projects.

This is not a recommendation to add DDD layers to every script. The example is small to make the boundaries inspectable. See the repository's benchmark task for a controlled extension exercise.
