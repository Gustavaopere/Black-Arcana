# Brew of Slimewalker

## Estado

`SOURCE-PINNED HEXALIA 1.3.6 / ITEM+EFFECT+RECIPE VERIFIED / BOUNCE CONDITION RUNTIME QA RECOMMENDED / INSTALLED-RUNTIME EQUIVALENCE PENDING`

- Provider: Hexalia
- Source pin: `AstralyaStudios/Hexalia@4952c65233bf31e9f0d3e55ff76be7fa1007ee3d`
- Item ID: `hexalia:brew_of_slimewalker`
- Effect ID: `hexalia:slimewalker`
- Acquisition: Small Cauldron
- Base duration: `4800 ticks = 240 s`
- Full Moonweave duration: `7200 ticks = 360 s`
- Base amplifier: `0`

## Receita 1.3.6

`hexalia:small_cauldron`, recipe duration `4800`:

1. `minecraft:slime_ball`
2. `hexalia:chillberries`
3. `hexalia:tree_resin`
4. `minecraft:feather`

Result: `hexalia:brew_of_slimewalker`.

## Efeito diretamente comprovado

`SlimewalkerEffect` evaluates every effect tick.

### Grounded slowdown

Whenever the entity is on the ground, it applies vanilla `Movement Slowness`:

- duration: `10 ticks`;
- amplifier: `0`.

Because the provider refreshes this while grounded, the movement penalty behaves as a continuously maintained short vanilla effect during the source path.

### Bounce path

When both conditions are true:

- `livingEntity.onGround()`;
- `livingEntity.isSuppressingBounce()`;

the provider:

- preserves X/Z velocity;
- sets Y velocity to `1.0`;
- sets `hasImpulse=true`;
- plays the slime-jump sound;
- spawns 8 slime-item particles;
- returns from the tick path.

The exact use of `isSuppressingBounce()` is preserved verbatim as a source fact. Its player-facing interpretation is counterintuitive relative to the phrase “bounce when landing”; this catalog does not reinterpret it. Runtime QA should confirm actual landing/crouch behavior in the installed pack.

### Fall-distance handling

On ticks that do not return through the bounce branch, the provider sets:

`fallDistance = 0.0`.

This is the direct source mechanism supporting fall-damage negation.

## Public description

The source-generated description says Slimewalker:

- negates fall damage;
- causes the user to bounce on landing;
- slows movement while grounded.

The first and third claims have direct paths above. The bounce behavior also has a direct source path, but the exact trigger semantics require runtime validation because of the `isSuppressingBounce()` condition.

## Deduplication / authority

Hexalia already owns a witch-brew traversal package combining fall protection, bounce and grounded slowdown. Black Arcana should not create a generic duplicate brew/spell.

Black Arcana also must not treat every grounded/bounce tick as a cast or progress event. Hexalia owns movement mutation and vanilla-effect application for this consumable.
