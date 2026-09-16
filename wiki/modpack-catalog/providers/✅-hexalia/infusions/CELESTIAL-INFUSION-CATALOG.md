# Hexalia 1.3.6 — Celestial Infusion catalog

## Estado

`SOURCE-PINNED 1.3.6 / RECIPES 6/6 / CHANNEL+ENVIRONMENT LIFECYCLE AUDITED / INSTALLED-RUNTIME EQUIVALENCE PENDING`

Source pin:

`AstralyaStudios/Hexalia@4952c65233bf31e9f0d3e55ff76be7fa1007ee3d`

## Provider-native process

Celestial Infusion is performed on a **Ritual Brazier** and is distinct from Nature's Ritual.

### Start requirements

The exact 1.3.6 path requires:

- a non-empty Ritual Brazier containing a recipe input;
- `hexalia:hex_focus` in main hand or offhand to initiate;
- open sky above the brazier;
- at least three `Celestial Bloom` or `Withered Celestial Bloom` blocks found within horizontal radius `3` on the brazier's Y level;
- a valid `hexalia:celestial_infusion` recipe for the stored item.

The Celestial Infusion start path **does not check `RitualBrazierBlock.SALTED`**. Salt can be applied to the brazier by the shared interaction code, but it is not an admission requirement for this infusion in the audited source.

### Channel duration

`CHANNEL_DURATION = 120 ticks = 6 s`.

During every server tick of the channel:

- the brazier input must remain present;
- a pending output must remain valid;
- `SunlightCheck.canSeeSun(...)` must remain true;
- the three captured bloom positions must remain valid Celestial/Withered Celestial Blooms.

Any failure cancels the channel and clears the pending output/captured bloom state.

### Completion and bloom cost

On success:

- the stored input is replaced by one copy of the recipe output;
- each of the three captured blooms degrades exactly one stage:
  - `Celestial Bloom -> Withered Celestial Bloom`;
  - `Withered Celestial Bloom -> Dead Bush`.

This degradation is provider-owned world mutation and must not be repeated by Black Arcana.

## Recipe inventory — 6/6

| Recipe ID | Input | Output |
|---|---|---|
| `hexalia:galeberries_from_celestial_infusion` | `minecraft:glow_berries` | `hexalia:galeberries` |
| `hexalia:celestial_crystal_from_celestial_infusion` | `minecraft:amethyst_shard` | `hexalia:celestial_crystal` |
| `hexalia:moonweave_hood_from_celestial_infusion` | `hexalia:silkweave_hood` | `hexalia:moonweave_hood` |
| `hexalia:moonweave_mantle_from_celestial_infusion` | `hexalia:silkweave_mantle` | `hexalia:moonweave_mantle` |
| `hexalia:moonweave_bindings_from_celestial_infusion` | `hexalia:silkweave_bindings` | `hexalia:moonweave_bindings` |
| `hexalia:moonweave_footwraps_from_celestial_infusion` | `hexalia:silkweave_footwraps` | `hexalia:moonweave_footwraps` |

## Moonweave interaction with brews

The seven standard Hexalia `BrewItem` consumables check the full Moonweave set and multiply their effect duration by `1.5`.

Therefore Celestial Infusion is not merely cosmetic gear progression: it produces an equipment set that directly extends Hexalia brew lifecycle. This relation remains Hexalia-owned and should not be duplicated as a Black Arcana potion-duration subsystem.

## Celestial / Divine deduplication

Hexalia already occupies a concrete **celestial infusion** identity involving:

- sunlight/open-sky gating;
- Celestial Bloom environmental resources;
- celestial crystal production;
- lunar/celestial armor upgrading;
- downstream brew-duration empowerment.

This does not make Hexalia a Holy miracle/spell authority, but it eliminates novelty claims based only on “use moon/sun/celestial energy to infuse equipment”. Black Arcana Divine/Celestial content must retain a distinct Holy/authority/miracle contract if approved after full provider deduplication.

## Authority / world safety

Hexalia owns:

- admission checks;
- six-second channel state;
- recipe matching;
- output replacement;
- Celestial Bloom degradation;
- cancellation semantics.

Black Arcana must not run a second channel, consume a second environmental cost, re-degrade blooms, or treat channel ticks as repeated casts. If Black Arcana independently performs a world mutation in a future bridge, its own `WorldEffectPolicy` still applies to Black Arcana-owned mutation without retroactively taking authority over Hexalia's native process.
