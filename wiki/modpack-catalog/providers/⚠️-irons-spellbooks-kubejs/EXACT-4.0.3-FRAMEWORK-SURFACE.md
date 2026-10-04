# Iron's Spellbooks KubeJS 4.0.3 — exact framework surface catalog

Status: `SOURCE-CLOSED / EXACT 4.0.3 PIN / FRAMEWORK CAPABILITIES ONLY / DOES NOT PROVE CURRENT PACK SCRIPT CONTENT`

Exact source checkpoint:

`sentwayfarer/irons_spells_js@f3c05a102707a87ac3b8f0d2df5d2ffa5ae5b6c7`

This file catalogs the bridge-owned surfaces established by that exact 4.0.3 source. It deliberately does **not** attribute any custom spell, school, item, entity or recipe to the current modpack unless a pack script or assembled-runtime provenance establishes it.

## 1. KubeJS registry builders

`IronsSpellsJSPlugin.registerBuilderTypes` registers six core builder entries:

1. Iron's spell registry -> `CustomSpell.Builder` (default builder);
2. Iron's school registry -> `SchoolTypeJSBuilder` (default builder);
3. vanilla attribute registry -> `irons_spells_js:spell` / `SpellAttributeBuilderJS`;
4. item registry -> `irons_spells_js:magic_sword` / `CustomMagicSwordItem.Builder`;
5. item registry -> `irons_spells_js:staff` / `CustomStaff.Builder`;
6. item registry -> `irons_spells_js:spellbook` / `CustomSpellBook.Builder`.

These are construction surfaces. Their presence is not a provider-owned content roster.

## 2. Custom spell builder

`CustomSpell` is a generic script-defined `AbstractSpell`. Its builder can configure:

- resource identity;
- school;
- minimum rarity;
- maximum level;
- cooldown;
- cast type and cast time;
- base mana and mana-per-level;
- base spell power and power-per-level;
- cast start/finish sounds;
- server `onCast` and `onPreCast` callbacks;
- client `onClientCast` and `onPreClientCast` callbacks;
- looting eligibility;
- learning requirement;
- player crafting predicate;
- unique tooltip/info callback;
- cast start/finish animations;
- pre-cast predicate/targeting condition.

The exact builder defaults are framework defaults, not cataloged spells: `COMMON`, Blood school, max level 10, cooldown 20 seconds, `INSTANT`, base mana 40, mana-per-level 20, base spell power 0, power-per-level 1, cast time 0, looting false and learning false.

## 3. Custom school builder

`SchoolTypeJSBuilder` can define:

- school resource ID;
- focus item tag;
- explicit focus items and focus tags;
- display component/name;
- power attribute;
- resistance attribute;
- default cast sound;
- damage type;
- learning requirement;
- looting permission.

Its data generator writes the custom focus tag into Iron's `irons_spellbooks:tags/item/school_focus` aggregation and generates the custom school-focus item tag from the configured items/tags.

Again, the builder does not establish a fixed built-in custom school.

## 4. Magic item builders

### Spellbook

`CustomSpellBook.Builder` supports:

- max spell slots;
- default spell entries with explicit levels;
- default spellbook attributes;
- affinity spell;
- unique-spellbook behavior when default spells are supplied.

The exact 4.0.3 builder constructor automatically adds the `curios:spellbook` tag. Initialization creates the Iron's spell container and injects configured default spells/affinity when present.

### Staff

`CustomStaff.Builder` supports custom enchantment value and a custom/derived `StaffTier` with damage, speed and additional attributes. It can inherit from Iron's known staff tiers. The ordinary KubeJS item `use` callback is explicitly unsupported for this staff builder and emits a startup warning.

### Magic sword

`CustomMagicSwordItem.Builder` supports a custom/derived extended weapon tier plus explicit spell+level entries. Its tier builder exposes uses, damage, speed, enchantment value, incorrect-block tag, repair ingredient and additional attributes, with optional inheritance from Iron's weapon tiers.

## 5. KubeJS bindings

The exact plugin exposes 21 named bindings:

`SpellRarity`, `SchoolRegistry`, `CastType`, `IronsSpellsParticleHelper`, `SpellRegistry`, `ItemTags`, `Player`, `SpellData`, `Spell`, `ISSAnimationHolder`, `ISSUtils`, `TargetEntityCastData`, `Potions`, `ISSPotionRegistry`, `WizardAttackGoal`, `WarlockAttackGoal`, `WizardRecoverGoal`, `WizardSupportGoal`, `SpellBarrageGoal`, `GustDefenseGoal`, `WispAttackGoal`.

Bindings are scripting access surfaces; they do not add semantic objects on their own.

## 6. Event bridge

`IronsSpellsJSEvents` declares the KubeJS event group `ISSEvents` with five handler names:

- server `changeMana`;
- targeted server `spellPreCast`;
- server `spellOnCast`;
- targeted server `spellPostCast`;
- startup `spellSelection`.

Verified bridge behavior in the exact event class:

- `changeMana` subscribes to Iron's `ChangeManaEvent`; its wrapper exposes old/new mana, `setNewMana(...)` and `MagicData`;
- `spellPreCast` subscribes to Iron's `SpellPreCastEvent`, is targeted to player entity type and propagates cancellation; its wrapper exposes entity, spell ID, level, school and cast source;
- `spellOnCast` subscribes to Iron's `SpellOnCastEvent`; its wrapper exposes and can mutate spell level and mana cost while retaining original values plus school/cast source;
- `spellSelection` subscribes to `SpellSelectionManager.SpellSelectionEvent` and can append selection options.

Important fail-closed nuance: although `spellPostCast` and `SpellPostCastEventJS` are declared in the exact 4.0.3 source, the inspected `IronsSpellsJSEvents` class contains no corresponding `@SubscribeEvent`/`post(...)` path for that handler. It must therefore **not** be treated as a verified emitted KubeJS runtime event without additional provider evidence.

## 7. Alchemist Cauldron recipe schemas

The plugin registers three schemas under namespace `irons_spellbooks`:

- `alchemist_cauldron_brew`: `results`, `input`, `base_fluid`, optional `byproduct`;
- `alchemist_cauldron_empty`: `result`, `input`, `fluid`, optional `sound`;
- `alchemist_cauldron_fill`: `fluid`, `input`, `result`, optional/default-true `mustFitAll`, optional `sound`.

These schemas permit scripts to define recipes; the schemas themselves do not prove any current pack recipe.

## 8. Conditional EntityJS surface

`kubejs.plugins.txt` loads `EntityJSPlugin` conditionally on `entityjs`. At the exact pin, that plugin registers two entity-type builder IDs:

- `irons_spells_js:spellcasting` -> `SpellCastingMobJSBuilder`;
- `irons_spells_js:spell_projectile` -> `SpellProjectileJSBuilder`.

This establishes optional EntityJS interoperability. It does not prove that the current pack defines any such custom entity.

## 9. Config integration

`IronsSpellsJSMod.runIronSpellsConfig` iterates KubeJS `RegistryObjectStorage` for Iron's spell registry and asks Iron's server-config builder to create spell config entries for the registered script-built spell objects before registering the resulting Iron's server config.

This exact 4.0.3 path is sufficient to establish bridge-to-host server-config participation. Do **not** backport later-upstream `SpellConfigManagerMixin` / `CustomSpellConfigEntriesJS` behavior into this pin: those files were not present at the exact 4.0.3 checkpoint audited here.

## 10. Catalog disposition

- provider-owned fixed spell identities: **0 established**;
- provider-owned fixed school identities: **0 established**;
- core builder types: **6 established**;
- conditional EntityJS builder types: **2 established**;
- named KubeJS bindings: **21 established**;
- declared KubeJS event handlers: **5**, of which **4 have a verified posting/subscription path in the inspected exact event class** and `spellPostCast` remains fail-closed;
- Alchemist Cauldron schemas: **3 established**;
- current pack script-defined semantic objects: **UNKNOWN until current assembled scripts/provenance are audited**.

These framework counts are capability counts and must not be added to the global magic semantic denominator.
