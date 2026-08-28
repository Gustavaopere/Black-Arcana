# 02.03 — Targeting & Effect Runtime

## Objective
Provide reusable, bounded targeting/effect primitives without creating a giant universal spell DSL.

## Targeting
Self, entity, ray, block, cone, sphere/cylinder, projectile-mediated and linked targets. Server clamps range and validates line-of-sight according to each definition.

## Runtime
Effects return explicit outcomes and may enqueue bounded follow-up work. Expensive area operations use budgets/schedulers, never unbounded single-tick loops.

## Acceptance
Tests cover range spoofing, unloaded chunks, dead/invalid entities, friendly-fire policy and bounded area iteration.
