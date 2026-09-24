# Create: Wizardry 1.21.1-0.5.1-pre1 — source-pinned magic-surface audit

## Evidence identity

Physical authority:

- sibling: `neoforge-rpg-skilltree@4767f5c637c02c6d91ccb43a86ea1539f42a2e9b`;
- physical order: #166;
- JAR: `create_wizardry-1.21.1-0.5.1-pre1.jar`;
- mod id: `create_wizardry`;
- runtime: `1.21.1-0.5.1-pre1`.

Source authority used for semantic classification:

- repository: `TTZPlayz/Create-Wizardry`;
- exact commit: `9c4e53aad0ee9477187487443b597b77ef06f323`;
- source tree: `3397ac8702555f502f1990b046293cf3a1004dc2`;
- commit message: `CW 0.5.1 - Pre-Release 1`;
- project metadata version: `1.21.1-0.5.1-pre1`.

No independent physical hash is preserved in the sibling row, so this audit is `SOURCE_PINNED`, not `COUNTED_EXACT`.

## Bounded spell-identity checks

| Check | Result |
|---|---:|
| Java source files | 75 |
| `src/main/resources/` files | 328 |
| provider-owned spell resource paths | 0 |
| `registerSpell` search hits | 0 |
| `SpellRegistry` search hits | 0 |
| `DeferredRegister<AbstractSpell>` search hits | 0 |
| `Registries.SPELL` search hits | 0 |
| `SPELLS.register` search hits | 0 |
| `spell.create_wizardry` identity/localization hits | 0 |

The provider has Java types whose filenames contain `Spellcasting` and a mixin named `AbstractSpellCastingMobMixin`. Those names describe host spell handling and do not establish provider spell registrations.

## Provider registration surface

The exact source entrypoint registers:

- fluids;
- blocks;
- block entities;
- items;
- mob effects;
- particles;
- creative tabs;
- triggers/advancements.

No provider-owned spell registrar is registered by the entrypoint.

Two provider effects are directly registered:

- `create_wizardry:mana_depletion`;
- `create_wizardry:siphon_lock`.

They are status/effect state, not independent spell identities.

## Host spell use

Blaze Caster reads Iron's `SpellData`, obtains the host `AbstractSpell`, and invokes the host spell cast pipeline as a mob-source cast. Mana Siphon also reads host spell containers and manipulates host mana/casting state.

The provider therefore has a **spell automation surface** without owning the spell identity being automated.

Semantic ownership rule:

`automated Iron's spell != new Create: Wizardry spell`

## Explicit Blaze Caster exclusion policy

The exact source pin contains 31 host spell path names in its Blaze Caster blacklist:

`echoing_strikes`, `flaming_strike`, `shadow_slash`, `volt_strike`, `divine_smite`, `touch_dig`, `heartstop`, `wall_of_fire`, `teleport`, `recall`, `blood_step`, `frost_step`, `burning_dash`, `thunder_step`, `evasion`, `charge`, `ascension`, `angel_wing`, `portal`, `summon_ender_chest`, `summon_horse`, `summon_polar_bear`, `sacrifice`, `invisibility`, `haste`, `spider_aspect`, `heal`, `greater_heal`, `ice_tomb`, `healing_circle`, `fortify`.

The blacklist uses host spell path names and does not transfer identity ownership to Create: Wizardry.

## Semantic conclusion

Classification:

`BRIDGE / MAGIC AUTOMATION / ZERO_SEMANTIC_HOST_SPELL_AUTOMATION`

Counted provider-owned spells/glyphs/rituals/equivalent discrete magical actions: **0**.

Create: Wizardry remains important to runtime interoperability because it can automate existing spells and alter resource/casting conditions. That importance does not justify duplicating host spell identities in the semantic catalog.

## Fail-closed boundary

This source audit does not prove:

- source-build byte equality to the installed JAR;
- deployed config values;
- full addon-spell compatibility;
- runtime blacklist effectiveness;
- exact automated-cast resource/cooldown settlement;
- multiplayer ownership or protection behavior;
- persistence/reload behavior;
- absence of runtime-generated registrations outside the inspected source shape.

Those require direct assembled-pack/runtime evidence.
