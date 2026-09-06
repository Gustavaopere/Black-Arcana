# Casos de teste candidatos

- `NO_BLOOD` Iron Golem yields 0 mB.
- UNKNOWN entity fails closed.
- reservation prevents double-spend across simultaneous casts.
- failed cast refunds exact reservation only.
- source death between quote/commit invalidates settlement safely.
- reservoir resize cannot duplicate blood.
- chunk unload does not create/lose/duplicate blood.
- broken link removes source from available total.
- PvP source requires policy/consent.
- normal mana full + zero blood => Blood spell denied.
- zero normal mana + sufficient blood => Blood spell may pass resource gate.
- multiple sources follow deterministic server-owned priority.
- reconnect/restart preserves stored/reserved state according to explicit transaction recovery rules.
