# HazentouveLib — 1.0.9

Status: `✅ CATALOGED / CURRENT PHYSICAL 1.0.9 / EXACT OFFICIAL SOURCE VERSION PIN / 3 IRON'S SCHOOLS + 6 SCHOOL ATTRIBUTES + HEXED + SOUL-FIRE INFRASTRUCTURE / 0 CONCRETE PROVIDER SPELLS+GLYPHS+RITUALS / STRICT SPELL-ACTION DELTA +0 / RUNTIME+CONSUMER QA SEPARATE`

## Current physical identity

Current sibling authority rechecked at `neoforge-rpg-skilltree@b9edb403c06567423d6c101d136b73a1065f2ad4`.

Canonical sibling dossier:

`PROJECT-INSTRUCTIONS/modlist/API and Library/✅-hazentouvelib v1.0.9.md`

- physical JAR: `hazentouvelib-1.0.9.jar`;
- mod id: `hazentouvelib`;
- runtime: `1.0.9`;
- Minecraft / loader: 1.21.1 / NeoForge;
- physical SHA-1: `b5d68711babb604e368b918683eb89a4d1492077`;
- confirmed physical consumer: Hazen N Stuff 1.4.0.14.

## Exact official source pin

Official repository:

`Hazentouvel/HazentouveLib`

Exact version checkpoint:

`641acf4e9e254f1af9f59b2eb2251ff0f1fcfc08`

The commit is explicitly titled `HazentouveLib 1.0.9`. At that revision `gradle.properties` declares Minecraft `1.21.1`, NeoForge `21.1.224`, mod id `hazentouvelib`, version `1.0.9` and `mod_license=Polyform Shield`.

The exact metadata requires Iron's Spells and Caelus in addition to NeoForge/Minecraft. This is an exact source-version pin, not a byte-reproducibility claim for the physical JAR.

## Provider role

HazentouveLib is not a standalone spell pack. It is a shared Hazen ecosystem library that also registers several concrete magical infrastructure/content objects consumed directly or by downstream mods.

Iron's Spells remains authority for its spell registry/casting runtime. HazentouveLib owns the schools, attributes, effects, Soul Fire state/content and reusable base classes it registers. Consumers own concrete spells/entities/items they define on top of those abstractions.

Black Arcana does not acquire provider casting authority from this library, and RPG Skill Tree remains progression-only through explicit contracts.

## Exact magic-relevant inventory

### 3 provider-owned Iron's school identities

`HLSchoolRegistry` registers exactly three `SchoolType` entries into Iron's `SCHOOL_REGISTRY_KEY`:

1. `hazentouvelib:radiance`;
2. `hazentouvelib:shadow`;
3. `hazentouvelib:cosmic`.

Each school is bound to provider power/resistance attributes and a provider magic damage type. These are real provider-owned school identities, but a school is not itself a concrete castable spell.

### 6 school attributes

`HLAttributeRegistry` registers:

- `radiance_magic_resist`;
- `shadow_magic_resist`;
- `cosmic_magic_resist`;
- `radiance_spell_power`;
- `shadow_spell_power`;
- `cosmic_spell_power`.

They are synchronized Iron's-style magic percentage attributes and are infrastructure/state, not standalone spell identities.

### Hexed effect

`HLEffects` registers one harmful mob effect: `hazentouvelib:hexed`.

The exact `HLServerEvents` listens to Iron's `SpellPreCastEvent`; when a server-side caster has Hexed, the library applies `max(1, 15% of max health)` using the provider `corrupt_magic` damage type and plays a sound for server players.

Hexed is therefore a provider-owned reactive casting penalty/effect. It modifies casts but does not register a spell.

### Soul Fire subsystem

The exact provider registers:

- block `hazentouvelib:soul_fire`;
- item `hazentouvelib:soul_igniter`;
- attachment type `hazentouvelib:soul_fire` for per-entity burn ticks;
- data/network synchronization through `SoulFireData.Payload`;
- damage type data `hazentouvelib:soul_fire`.

`SoulIgniterItem` directly places/ignites the provider Soul Fire where its placement contract allows it. The fire applies provider burn state and damage and can spread according to its block logic.

This is concrete provider gameplay/content, but it is an item/block effect system rather than a spell/glyph/ritual registration.

### Other exact provider support objects

At the exact pin the provider also establishes:

- seven registered items total: three school upgrade orbs, three school runes and Soul Igniter;
- one registered block: Soul Fire;
- five provider damage-type data identities: `radiance_magic`, `shadow_magic`, `cosmic_magic`, `corrupt_magic`, `soul_fire`;
- three packaged Iron's upgrade-orb-type data identities: `radiance_power`, `shadow_power`, `cosmic_power`;
- five client key mappings (`ability_1` through `ability_5`) used as reusable consumer input surfaces.

`HLUpgradeOrbTypeRegistry` also declares a `hydro_power` resource key, but the exact 1.0.9 tree contains no matching packaged upgrade-orb-type data definition. It is therefore not promoted as an active registered 1.0.9 identity.

## Concrete spell/glyph/ritual audit

The exact source tree contains spell-oriented helper/base classes such as `AbstractTaggedSpell`, `HLSpellDamageSource` and abstract spellcasting Enderman classes.

However:

- no `DeferredRegister<AbstractSpell>` or equivalent concrete HazentouveLib spell registry was established;
- no concrete provider spell class registration is present in the exact bootstrap;
- no provider glyph/spell-part registry is present;
- no provider ritual registry/content surface is present.

Result for the strict castable/action ledger:

- concrete provider-owned spells: **0**;
- glyphs/spell parts: **0**;
- rituals: **0**;
- strict spell/glyph/ritual delta: **+0**.

This `+0` does not erase the three schools, Hexed or Soul Fire subsystem; those are cataloged above as provider-owned magical infrastructure/content outside the strict castable-spell denominator.

## Authority and integration boundaries

- HazentouveLib owns its three schools, school attributes, Hexed effect, Soul Fire state/content and shared API/base classes.
- Iron's Spells owns Iron's casting, mana, spell execution and base school/spell contracts.
- Hazen consumers own concrete spells, mobs, armor, Curios and abilities they register.
- Black Arcana must not duplicate Hexed damage, Soul Fire settlement/state or school attributes.
- A future BA integration must use a verified version-appropriate boundary and preserve exactly-once provider effects.

## Runtime / consumer QA remains separate

Catalog closure does not claim physical runtime validation for:

- school registry sync with every installed Iron's addon;
- consumer use of `AbstractTaggedSpell`;
- Hexed pre-cast damage exactly once across all casting paths;
- Soul Fire attachment persistence/sync across death/relog/dimension transfer/server restart;
- five consumer keybind/ability routes;
- attribute modifier stacking and update compatibility;
- dedicated-server/client classloading;
- source↔physical-JAR byte equality.

These remain runtime/integration QA, not missing catalog identities.

## Current result

**✅ Cataloged.**

HazentouveLib 1.0.9 contributes real magical infrastructure/content — especially **3 schools**, **Hexed** and the **Soul Fire** subsystem — while contributing **0 concrete spells, glyphs or rituals** to the strict castable-magic denominator.
