# Warping Spell Prism

State: `SOURCE-PINNED 1.6.15 / ENTITY-COST PATH DIVERGENCE / RUNTIME QA PENDING`

Registry id: `ars_controle:warping_spell_prism`
Block entity: `ars_controle:warping_spell_prism` -> `WarpingSpellPrismTile`
Source checkpoint: `Vonr/Ars-Controle@ecbb83ba512bc9ca7a025556fb9c62dbd32b6430`

## Acquisition

Enchanting Apparatus:

- reagent: `ars_nouveau:spell_prism`;
- 4 × tag `c:ender_pearls`;
- 4 × `minecraft:popped_chorus_fruit`;
- recipe `sourceCost`: `0`.

Operational routing may still consume Ars Source; the zero crafting cost is not a zero-use-cost guarantee.

## Target state

The tile stores exactly one provider-owned target at a time:

- block target: attachment `ars_controle:block_target` as `GlobalPos`;
- entity target: attachment `ars_controle:entity_target` as UUID.

Setting one removes the other. Block targets resolve a server level from the stored dimension. Entity targets resolve through the provider cache by UUID.

Provider interaction can link blocks or living entities. Linking another player is denied for non-creative users by default unless `warping_spell_prism.allow_linking_other_players=true`; linking self remains available.

## Projectile routing

`WarpingSpellPrismBlock.onHit` acts on Ars `EntityProjectileSpell`.

The executable path:

1. rejects/discards a projectile with no resolver;
2. resolves the configured target and target level;
3. requests/validates destination chunk availability according to provider config;
4. when the target level differs, creates a replacement projectile in that level and copies the original resolver plus projectile state such as redirect count, age, pierce/sensitive counters and delta movement;
5. removes the old projectile as `CHANGED_DIMENSION`;
6. resolves the same provider spell at/near the routed destination rather than starting a new Ars cast.

Black Arcana must therefore preserve the original causal cast identity if it ever observes this path. A routed projectile is not a second cast and must not incur a second Black Arcana cooldown, Mastery grant, Arcane Danger activation or host-mana settlement.

## Destination chunk behavior

Default `warping_spell_prism.load_time = 600` ticks.

When `load_time > 0`, the provider adds a region ticket named `warping_spell_prism` for the destination chunk at ticket level/radius argument `3`. When `load_time <= 0`, an unloaded destination causes the projectile to be discarded instead.

This is a provider-owned force-loading exception. It does **not** relax Black Arcana's no-force-load and already-loaded-destination contracts.

## Source cost formula

Defaults:

- `max_cost = -1` -> no configured maximum;
- `cost_min_distance = 1024`;
- `cost_per_block = 0.03125`;
- `dimension_cost = 2000`.

For a resolved hit, the source helper computes squared distance from prism to target. Let `D2` be that squared distance, `M = 1024`, `P = 0.03125`, and `Cdim` be `2000` cross-dimension or `0` same-dimension.

If `D2 > M²`, source-required is the non-negative integer truncation/cap of:

`Cdim + sqrt(D2 - M²) * P`

Otherwise source-required is `max(0, Cdim)`.

The exact formula is not `distance - 1024`; the implementation uses `sqrt(distance² - 1024²)`.

## Source-path divergence for entity targets

`getSourceRequired()` explicitly supports both block and entity hit results. However, in the audited `onHit` implementation, the entity-target branch posts the projectile-hit event, resolves the effect and returns **before** the later Source-deduction block used by the block-target path.

Therefore the catalog does not claim that entity-target routing actually pays the calculated Source cost in runtime 1.6.15. This is `RUNTIME QA REQUIRED` and must not be normalized by inference.

## Optional ComputerCraft surface

Only when mod id `computercraft` is loaded, Ars Controle registers a CC peripheral for the prism. The peripheral can set block targets, inspect the current target and query `sourceNeeded()`.

CC:Tweaked/ComputerCraft is not present as a top-level JAR in the current physical modlist, so this surface is `OPTIONAL / CURRENTLY ABSENT` for the pack.

## Boundary

- Ars Nouveau owns spell/resolver/projectile and Source semantics.
- Ars Controle owns target attachments, redirection, its region ticket and additional Source routing rule.
- Black Arcana must not replay the spell at the destination.
- Provider force-loading is not inherited by Black Arcana Space & Displacement.
- A stored target is not Black Arcana target authorization.

## QA pending

1. Verify installed-JAR block-target and entity-target Source settlement, especially the source-path divergence.
2. Verify target persistence after restart/chunk unload.
3. Exercise same-dimension and cross-dimensional redirects with `load_time=600` and `0`.
4. Validate event ordering with other Ars projectile/prism addons.
5. Confirm other-player linking policy in the effective server config.
