# Acolyte 1.0.3

Status: `EXACT PUBLISHER-RELEASE STRUCTURAL AUDIT / ZERO OWN SEMANTIC SPELLS / IRON'S SPELLCASTER CONTENT CATALOGED / ASSEMBLED-PACK QA PENDING`

## Current physical identity

Sibling physical authority at `neoforge-rpg-skilltree@49d9910ca0abfb9c0608c2730ab3ae8cefc59a9a` records:

- physical order: **#4**;
- JAR: `acolyte-1.0.3.jar`;
- mod id: `acolyte`;
- runtime version: `1.0.3`;
- Minecraft: `1.21.1`;
- required magic host: Iron's Spells 'n Spellbooks;
- current pack host line documented by the sibling: Iron's `1.21.1-3.16.3`.

The sibling dossier classifies Acolyte as mobs + structures + temporary recruitment + magic economy over Iron's. It publishes 18 structure variants, Human/Demon Mage/Warrior/Archer families, a Lieutenant miniboss, Horn Merchant trading and temporary emerald-paid recruitment.

## Exact publisher release

CurseForge project `1534642`, file `8098233` is the release `acolyte-1.0.3.jar` for NeoForge 1.21.1.

A bounded NON-MERGE audit downloaded that exact publisher file and measured:

- SHA-1: `ad0abc821f3f8a6573ac19a50970fc1bc46b4275`;
- SHA-256: `73fe745bbb0016fbc00af9ba14c0ecfe0a1d8a7d72a7892557739182b3486256`;
- total classes: **93**;
- provider classes: **93**.

The current sibling authority does not preserve an independent hash for the physical local JAR, so this catalog does **not** claim byte-for-byte hash equality between the publisher download and the installed copy. Identity is release-bounded by exact filename/mod id/runtime version plus the exact publisher file.

## Semantic classification

Acolyte does **not** establish provider-owned spell identities in the audited 1.0.3 release.

Exact structural evidence:

- provider classes whose superclass chain reaches Iron's `AbstractSpell`: **0**;
- provider classes with an Iron's spell superclass: **0**;
- provider-owned spell resource paths under `assets/acolyte` or `data/acolyte`: **0**;
- provider localization roots matching spell semantics: **0**;
- one localization key contains the word `spells`, `gui.acolyte.recruit.stat.spells`, but it is a recruit UI stat label rather than a spell registry identity;
- one provider class name contains `Spell`: `SingleUseSpellGoal`; it is an AI goal surface, not an `AbstractSpell` implementation.

Therefore Acolyte contributes:

**+0 semantic magic objects**

under the Black Arcana semantic ledger. Iron's remains the semantic owner of spells cast, traded or selected by Acolyte.

## Iron's host usage

The exact release clearly consumes Iron's spell infrastructure rather than creating a second registry.

Observed code-level host references include:

- `SpellRegistry.BLOOD_STEP_SPELL`;
- `SpellRegistry.STOMP_SPELL`;
- `SpellRegistry.getSpell(ResourceLocation)`;
- `SpellFilter.getRandomSpell(RandomSource)`;
- `IMagicEntity.initiateCastSpell(AbstractSpell, level)`;
- Iron's wizard/warlock attack-goal APIs.

The packaged Acolyte resources also contain 29 explicit Iron's spell resource IDs. Combined with the two direct `SpellRegistry` fields above, **31 explicitly named host spell identities** are observed in the exact release.

These 31 are cataloged in [EXACT-1.0.3-HOST-SPELL-REFERENCES.md](./EXACT-1.0.3-HOST-SPELL-REFERENCES.md).

They are **references**, not Acolyte-owned spells, and are not added again to the semantic numerator.

## Exhaustiveness boundary

The 31 explicit references are not claimed to be a complete runtime spell loadout for every Acolyte archetype.

The exact release also references dynamic Iron's selection surfaces such as `SpellFilter.getRandomSpell` and `SpellRegistry.getSpell(ResourceLocation)`. Therefore:

- explicit host references can be listed exactly;
- per-archetype active pools, weights, levels and biome-variant differences require direct config/data/runtime mapping;
- dynamic selection must not be converted into invented fixed loadouts;
- no additional semantic identities are minted by those dynamic paths because Iron's owns the selected spell.

## Gameplay surfaces relevant to the magic catalog

Acolyte adds magical gameplay around host spells without owning a new spell registry:

- Human Mage and Demon Mage spellcasters;
- biome variants for mage/warrior/archer families;
- Horn Merchant conversion of Demon Horns into scrolls/magic loot;
- temporary recruit system;
- Lieutenant demon miniboss;
- 18 published structures used as encounter/economy surfaces.

These are provider gameplay mechanics and acquisition/context surfaces. They do not become new spells solely because they interact with Iron's spells.

## Authority boundary

- **Iron's Spells 'n Spellbooks** owns spell identities, schools, mana, cast resolution, generic cooldown and host scroll semantics.
- **Acolyte** owns its mobs, AI composition, structures, recruitment, Demon Horn economy, merchant policy and provider-local encounter behavior.
- **Black Arcana** records the catalog and may integrate only through verified contracts; it does not duplicate Iron's spell registry or reconstruct Acolyte proprietary implementation.
- **RPG Skill Tree** remains progression/Mastery/perk/gate authority only through real boundaries.

## Clean-room / license boundary

The publisher marks Acolyte **All Rights Reserved**.

The audit therefore retains only bounded interoperability/catalog facts:

- release identity and hashes;
- class/superclass metadata;
- registry/API references;
- resource-location identities;
- presence/absence of spell registry surfaces.

No method bodies, assets, formulas, recipes, model data or proprietary implementation are copied into Black Arcana.

## Runtime state — fail-closed

Still unverified in the exact assembled pack:

- physical JAR hash equality with publisher file `8098233`;
- dedicated-server boot of Acolyte 1.0.3 against the exact current host set;
- effective Acolyte config/gamerules;
- exact per-archetype spell pools, weights and levels;
- biome-variant spell differences;
- Horn Merchant live trade pool and scroll tiers;
- recruitment persistence/ownership/dimension behavior;
- exactly-once combat/cast settlement with Black Arcana observers;
- Epic Fight/animation coexistence;
- multiplayer and protection behavior.

These open runtime gates do not reopen the semantic ownership result.

## Result

**✅ Cataloged at exact publisher-release structural level: Acolyte 1.0.3 owns 0 independent semantic spells.**

The exact release uses Iron's-owned spells and dynamic spellcasting infrastructure; those host identities remain counted only under Iron's.
