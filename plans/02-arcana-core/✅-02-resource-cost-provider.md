# 02.02 — Resource & Cost Providers

## Objective
Avoid a mandatory second mana system.

## Providers
Support abstract costs such as mana, health, items, durability, spirits/souls, cooldown-only and composite costs. External mods supply adapters rather than leaking types into core.

## Requirements
- `canAfford`, reserve/commit/refund semantics when applicable.
- Atomic composite payment to prevent partial consumption.
- Configurable percent-of-max costs for high-tier magic.
- Creative/admin policy explicit.
- No negative/overflow values.

## Acceptance
Fake providers prove atomicity; integration providers later pass identical contract tests.
