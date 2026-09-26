# Hexalia 1.3.7 — Celestial Infusion catalog

## Estado

`SOURCE-PINNED 1.3.7 / RECIPES 6/6 / CORE IMPLEMENTATION + ALL 6 RECIPE BLOBS IDENTICAL TO 1.3.6 / CHANNEL+ENVIRONMENT LIFECYCLE AUDITED / PHYSICAL-JAR BYTE EQUALITY UNPROVEN`

Source pin:

`AstralyaStudios/Hexalia@98c22aaf70e069c616fed5ad2dc56d2b37fcd283` (release commit; later same-version maintenance is not projected backward)

The 1.3.7 release commit was compared directly to the previously audited 1.3.6 release pin. `CelestialInfusion.java`, `CelestialInfusionRecipe.java`, and every one of the six generated Celestial Infusion recipe JSONs are blob-identical across the two pins. The 6/6 semantic inventory and lifecycle below therefore remain current without extrapolating from changelog prose.

## Provider-native process

Celestial Infusion is performed on a **Ritual Brazier** and is distinct from Nature's Ritual.

### Start requirements

The 1.3.7 release path, unchanged for this subsystem from the audited 1.3.6 path, requires:

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

The eight standard Hexalia `BrewItem` consumables in 1.3.7 (the previous seven plus Gravebloom; Homestead remains its separate one-shot class) check the full Moonweave set and multiply their effect duration by `1.5`.

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
