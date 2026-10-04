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

### 1A. Magic attribute builder

`irons_spells_js:spell` is the addon builder type registered under the vanilla attribute registry. `SpellAttributeBuilderJS` specializes KubeJS `AttributeBuilder` for Iron's `MagicRangedAttribute`:

- boolean attribute mode is explicitly unsupported;
- a ranged/default numeric definition is required before object creation;
- successful construction returns an Iron's `MagicRangedAttribute` using the configured default/min/max range.

This lets scripts define spell-related power/resistance-style attributes, but the builder itself contributes no fixed attribute identity to the pack.

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

### Official source development fixtures — syntax evidence only

The exact 4.0.3 source checkpoint contains three development scripts under `run/kubejs/*/test/test.js`. They are **not packaged modpack definitions** and must never be counted as current-pack content.

The startup fixture demonstrates the provider's intended KubeJS invocation forms:

- `StartupEvents.registry("attribute", ...)` with `event.create(..., "spell")`;
- `StartupEvents.registry("irons_spellbooks:schools", ...)` with default school builder creation;
- `StartupEvents.registry("irons_spellbooks:spells", ...)` with default custom-spell builder creation;
- `StartupEvents.registry("item", ...)` with `event.create(..., "spellbook")`, `"staff"` and `"magic_sword"`.

The server fixture exercises all five declared `ISSEvents` names, including `spellPostCast`, plus the three Alchemist Cauldron recipe schemas.

These fixtures validate exact 4.0.3 scripting syntax and informed the bounded deployed-evidence marker tests. They do not establish any semantic object in the user's assembled pack.

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

Verified bridge behavior across the exact event class **and required mixins**:

- `changeMana` subscribes to Iron's `ChangeManaEvent`; its wrapper exposes old/new mana, `setNewMana(...)` and `MagicData`;
- `spellPreCast` subscribes to Iron's `SpellPreCastEvent` for player casts, is targeted to player entity type and propagates cancellation; `AbstractSpellMixin` separately injects at `AbstractSpell.checkPreCastConditions` for non-player living entities, posts the same targeted KubeJS handler by entity type and can force the pre-cast check to `false` when cancelled;
- `spellOnCast` subscribes to Iron's `SpellOnCastEvent`; its wrapper exposes and can mutate spell level and mana cost while retaining original values plus school/cast source;
- `spellPostCast` is targeted by entity type and **does have a verified emission path**: `AbstractSpellMixin` injects at the head of `AbstractSpell.onServerCastComplete`, builds `SpellPostCastEventJS` and posts the KubeJS handler when listeners exist for that entity type;
- `spellSelection` subscribes to `SpellSelectionManager.SpellSelectionEvent` and can append selection options.

The previous event-class-only audit incorrectly left `spellPostCast` fail-closed because its emission does not live in `IronsSpellsJSEvents`; it lives in the required `AbstractSpellMixin`. At the exact 4.0.3 pin, all **5 declared handlers now have a verified subscription or posting path**.

## 6A. Required host mixin surfaces

`irons_spells_js.mixins.json` is required and lists exactly five common mixins with no client-only mixins:

1. `AbstractSpellMixin`;
2. `IronsSpellbooksMixin`;
3. `LivingEntityMixin`;
4. `PathfinderMobMixin`;
5. `ServerConfigsAccessor`.

Magic-relevant behavior established by those mixins:

- `AbstractSpellMixin` provides the non-player targeted `spellPreCast` bridge and the targeted `spellPostCast` emission described above;
- `LivingEntityMixin` makes `LivingEntity` implement `MagicEntityKJS`, exposing `irons_spells_js$getMagicData()` as a script-facing route to Iron's `MagicData`;
- `PathfinderMobMixin` targets `PathfinderMob` and implements Iron's `IMagicEntity`. For mobs that are not already `AbstractSpellCastingMob`, it initializes/synchronizes `MagicData`/`SyncedSpellData`, persists casting state, supports cancel/complete/tick cast lifecycle and potion-drinking state, and performs host-specific cast-data setup for Iron's Teleport/Frost Step/Blood Step/Burning Dash behaviors. This expands which mobs can participate in Iron's casting; it does **not** register new spell identities;
- `IronsSpellbooksMixin` redirects the host server-config registration during Iron's initialization so the bridge can postpone it;
- `ServerConfigsAccessor` exposes Iron's server-config builder/create-spell-config internals to `IronsSpellsJSMod.runIronSpellsConfig`, which later creates config entries for KubeJS-registered spell objects and registers the rebuilt server config.

These mixins are runtime bridge capabilities, not semantic spell/school objects. They must not be added to the global magic denominator, but they are relevant to exactly-once casting/event/config interoperability.

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

### Spell-casting mob

`SpellCastingMobBuilder` adds addon-specific `isCasting(...)` and `onCancelledCast(...)` script callbacks on top of EntityJS pathfinder-mob construction.

The resulting `SpellCastingMobJS` extends `PathfinderMob` and implements Iron's `IMagicEntity`. It owns `MagicData` plus `SyncedSpellData`, persists/reloads casting state, supports cancel/complete/initiate cast lifecycle, advances cast duration server-side, calls Iron's `onServerCastTick` / `onCast` with `CastSource.MOB`, and carries the same host-specific teleport/dash cast-data handling needed by several Iron's spells.

### Spell projectile

`SpellProjectileJSBuilder` adds addon-specific callbacks/configuration for:

- `onAntiMagic(...)`;
- trail particles;
- impact particles;
- impact sound.

`SpellProjectileJS` extends Iron's `AbstractMagicProjectile`, implements EntityJS projectile integration plus Iron's `AntiMagicSusceptible`, exposes mutable projectile damage, and persists that damage through entity save/load.

These are optional scripted-entity construction/runtime surfaces. They do not prove that the current pack defines any such custom entity or projectile.

### 8A. Client presentation integration

`IronsSpellsJSModClient` is a client-only event subscriber that reuses Iron's native presentation for KubeJS-built magic items:

- during client setup, KubeJS item objects that are `SpellBook` instances receive Iron's `SpellBookCurioRenderer` through Curios;
- during client-extension registration, KubeJS item objects that are `StaffItem` instances receive an `IClientItemExtensions` arm-pose implementation returning Iron's native `StaffArmPose`.

This is presentation interoperability only. It does not create spell/item semantic identities and does not grant client authority over casting.

## 9. Config integration

`IronsSpellsJSMod.runIronSpellsConfig` iterates KubeJS `RegistryObjectStorage` for Iron's spell registry and asks Iron's server-config builder to create spell config entries for the registered script-built spell objects before registering the resulting Iron's server config.

This exact 4.0.3 path is sufficient to establish bridge-to-host server-config participation. Do **not** backport later-upstream `SpellConfigManagerMixin` / `CustomSpellConfigEntriesJS` behavior into this pin: those files were not present at the exact 4.0.3 checkpoint audited here.

## 10. Catalog disposition

- provider-owned fixed spell identities: **0 established**;
- provider-owned fixed school identities: **0 established**;
- core builder types: **6 established**;
- conditional EntityJS builder types: **2 established**;
- conditional EntityJS runtime capabilities: spell-casting mob lifecycle and anti-magic-capable spell projectile surfaces **verified**;
- client presentation reuse: native Iron's spellbook Curios renderer and staff arm pose **verified for matching script-built item instances**;
- named KubeJS bindings: **21 established**;
- declared KubeJS event handlers: **5**, with **5 verified subscription/posting paths when the required exact mixins are included**;
- Alchemist Cauldron schemas: **3 established**;
- current pack script-defined semantic objects: **UNKNOWN until current assembled scripts/provenance are audited**.

These framework counts are capability counts and must not be added to the global magic semantic denominator.
