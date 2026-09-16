# Brew of Arachnid Grace

## Estado

`SOURCE-PINNED HEXALIA 1.3.6 / ITEM+EFFECT+RECIPE VERIFIED / INSTALLED-RUNTIME EQUIVALENCE PENDING`

- Provider: Hexalia
- Source pin: `AstralyaStudios/Hexalia@4952c65233bf31e9f0d3e55ff76be7fa1007ee3d`
- Item ID: `hexalia:brew_of_arachnid_grace`
- Effect ID: `hexalia:arachnid_grace`
- Acquisition: Small Cauldron
- Base effect duration: `4800 ticks = 240 s`
- Full Moonweave duration: `7200 ticks = 360 s`
- Base amplifier: `0`
- Cooldown: none established; this is a prepared consumable, not a spell cast

The source/release line is 1.3.6/MIT. The installed JAR filename is 1.3.6 but reports runtime metadata 1.3.5, so exact pack-runtime equivalence remains a separate QA gate.

## Receita 1.3.6

`hexalia:small_cauldron`, recipe duration `4800`:

1. `minecraft:spider_eye`
2. `hexalia:ghost_powder`
3. `minecraft:black_dye`
4. `minecraft:string`

Result: `hexalia:brew_of_arachnid_grace`.

## Efeito diretamente comprovado no source

`ArachnidGraceEffect` executes every effect tick.

### Wall climbing

When the affected entity has a horizontal collision and is **not crouching**:

- the current horizontal velocity is preserved as the basis;
- vertical velocity is set to `0.2`;
- the resulting vector is scaled by `0.96`.

This is the direct wall-climb mechanic of the effect.

### Poison removal

If vanilla `Poison` is active, the effect removes it.

This source path proves active poison cleansing while Arachnid Grace is ticking; it should not be generalized into immunity to arbitrary poison-like mod effects.

### Water/rain/bubble drawback

When the entity is in water, rain or a bubble column, Arachnid Grace applies vanilla `Weakness`:

- duration: `40 ticks`;
- amplifier: `0`.

The effect re-evaluates this every tick.

## Public-description delta

Hexalia's player-facing description also attributes **cobweb immunity** to Arachnid Grace. A repo-wide audit at the exact 1.3.6 pin did not locate an additional Arachnid Grace implementation path that proves that behavior; the effect class itself does not implement cobweb handling.

Therefore:

`COBWEB IMMUNITY = PUBLIC DESCRIPTION / SOURCE PATH NOT LOCATED / RUNTIME QA REQUIRED`.

Do not promote it to an integration contract until the exact runtime path is demonstrated.

## Black Arcana deduplication

Hexalia already owns the preparation-based witchcraft capability for:

- wall climbing;
- active Poison cleansing;
- environmental water/rain drawback;
- publicly claimed cobweb traversal/protection, pending runtime proof.

Black Arcana must not add a generic witch brew or spell whose identity is merely this package under another name. Any future traversal magic must have a distinct causal/resource/gameplay contract.

## Authority

Hexalia owns item consumption, effect lifecycle and movement/status mutation. Black Arcana must not reapply, settle or extend the brew through its cast pipeline. RPG/Black Arcana progress should only observe a discrete provider action when a safe causal boundary exists; effect ticks are not repeated casts or mastery events.
