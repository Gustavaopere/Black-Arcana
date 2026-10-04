# Iron's Spellbooks KubeJS 4.0.3 — exact source coverage matrix

Status: `EXACT SOURCE FILE COVERAGE / FRAMEWORK AUDIT COMPLETE / CURRENT PACK SCRIPT CONTENT STILL UNVERIFIED`

Exact source checkpoint:

`sentwayfarer/irons_spells_js@f3c05a102707a87ac3b8f0d2df5d2ffa5ae5b6c7`

The exact tree contains 49 files. This matrix covers every **30 `src/main/java` files**, all **5 `src/main/resources` files**, and all **3 bundled `run/kubejs` development fixtures** that are relevant to framework/runtime/catalog reasoning.

Coverage here means the file's role has been inspected and assigned a catalog disposition. It does **not** prove that the current assembled modpack has any script-built spell, school, item, attribute, entity or recipe.

## Java coverage — 30/30

| # | Exact source file | Role established at 4.0.3 | Catalog disposition |
|---:|---|---|---|
| 1 | `IronsSpellsJSMod.java` | mod bootstrap; bridge config lifecycle / Iron's server-config rebuild participation | framework/runtime; no fixed semantic object |
| 2 | `IronsSpellsJSModClient.java` | Curios renderer for built `SpellBook`; Iron's staff arm pose for built `StaffItem` | client/presentation integration; +0 semantic |
| 3 | `IronsSpellsJSPlugin.java` | 6 core builders, 21 bindings, event group, 3 recipe schemas | primary KubeJS bridge surface |
| 4 | `compat/entityjs/EntityJSPlugin.java` | conditional EntityJS registration of `spellcasting` and `spell_projectile` builders | optional framework surface |
| 5 | `compat/entityjs/entity/SpellCastingMobJS.java` | script-built `PathfinderMob` implementing Iron's `IMagicEntity`, `MagicData`/cast lifecycle | optional script-built entity runtime; no fixed entity |
| 6 | `compat/entityjs/entity/SpellProjectileJS.java` | Iron's-compatible script-built spell projectile behavior | optional script-built entity runtime; no fixed entity |
| 7 | `compat/entityjs/entity/builder/SpellCastingMobBuilder.java` | EntityJS base extension with `isCasting` and `onCancelledCast` callbacks | optional builder capability |
| 8 | `compat/entityjs/entity/builder/SpellCastingMobJSBuilder.java` | concrete spellcasting-mob builder/factory and base combat attributes | optional builder capability |
| 9 | `compat/entityjs/entity/builder/SpellProjectileJSBuilder.java` | anti-magic, trail/impact particles and impact-sound hooks | optional builder capability |
| 10 | `entity/attribute/SpellAttributeBuilderJS.java` | ranged, syncable Iron's `MagicRangedAttribute` construction; boolean mode rejected | scriptable magic-attribute builder; no fixed attribute |
| 11 | `event/ChangeManaEventJS.java` | KubeJS wrapper for mana change including mutable new mana and `MagicData` | runtime event wrapper |
| 12 | `event/IronsSpellsJSEvents.java` | declares/bridges the five `ISSEvents` handlers | event bridge authority with mixin paths included |
| 13 | `event/SpellOnCastEventJS.java` | exposes cast spell/school/source and mutable level/mana cost | runtime event wrapper |
| 14 | `event/SpellPostCastEventJS.java` | post-cast wrapper posted by `AbstractSpellMixin` | runtime event wrapper |
| 15 | `event/SpellPreCastEventJS.java` | cancellable pre-cast wrapper for player/mixin-targeted entity paths | runtime event wrapper |
| 16 | `event/SpellSelectionEventJS.java` | spell-selection wrapper able to append selection options | runtime selection bridge |
| 17 | `item/CustomMagicSwordItem.java` | script-built magic sword/tier plus explicit spell-level entries | item builder/runtime; no fixed item |
| 18 | `item/CustomSpellBook.java` | script-built spellbook, slots/affinity/default spell container integration | item builder/runtime; no fixed item |
| 19 | `item/CustomStaff.java` | script-built Iron's staff/tier integration | item builder/runtime; no fixed item |
| 20 | `mixin/AbstractSpellMixin.java` | custom-spell callbacks; non-player pre-cast; targeted post-cast posting | required host bridge mixin |
| 21 | `mixin/IronsSpellbooksMixin.java` | redirects/postpones host server-config registration | required config-lifecycle mixin |
| 22 | `mixin/LivingEntityMixin.java` | implements `MagicEntityKJS` on living entities | required script-facing `MagicData` bridge |
| 23 | `mixin/PathfinderMobMixin.java` | implements Iron's `IMagicEntity` machinery on generic pathfinder mobs with guarded host behavior | required casting-runtime mixin; no new spell |
| 24 | `mixin/ServerConfigsAccessor.java` | accessor to Iron's server-config builder/create-spell-config path | required config bridge internal |
| 25 | `recipe/ISSSchemas.java` | schemas for brew/empty/fill Alchemist Cauldron recipes | recipe construction capability; no fixed recipe |
| 26 | `spell/AbstractSpellWrapper.java` | `Spell` binding helper: `of`, `ofHolder`, `exists`, `isSpell`, `checkStatus`, `isEnabled` | lookup/status scripting surface; no registration |
| 27 | `spell/CustomSpell.java` | generic script-defined `AbstractSpell` implementation and builder | primary custom-spell construction surface |
| 28 | `spell/MagicEntityKJS.java` | remapped `getMagicData()` access for living entities | script-facing magic-data helper |
| 29 | `spell/school/SchoolTypeJSBuilder.java` | script-defined Iron's school construction | custom-school builder; no fixed school |
| 30 | `util/ISSKJSUtils.java` | internal safe callback wrapper logging script exceptions | internal implementation helper; not a catalog object |

## Resource coverage — 5/5

| Exact resource | Coverage result |
|---|---|
| `META-INF/accesstransformer.cfg` | empty at the exact 4.0.3 pin; establishes no additional access-transformer contract |
| `META-INF/neoforge.mods.toml` | required NeoForge/Minecraft/Iron's/KubeJS dependency metadata; mixin config declared |
| `icon.png` | presentation asset only |
| `irons_spells_js.mixins.json` | exactly five common required mixins; no client-only mixin entries |
| `kubejs.plugins.txt` | core `IronsSpellsJSPlugin` plus `EntityJSPlugin` conditional on `entityjs` |

## Bundled KubeJS development fixtures — 3/3

| Fixture | Evidence role |
|---|---|
| `run/kubejs/startup_scripts/test/test.js` | validates exact 4.0.3 registration syntax for attributes, schools, spells and magic items; also exercises `ISSEvents.spellSelection` and `Spell` lookup helpers; **not current-pack content** |
| `run/kubejs/server_scripts/test/test.js` | exercises `changeMana`, `spellPreCast`, `spellOnCast`, `spellPostCast` and all three Alchemist Cauldron schemas; **not current-pack content** |
| `run/kubejs/client_scripts/test/test.js` | development/client scripting fixture; **not current-pack content** |

## Coverage conclusion

At the exact 4.0.3 source pin, no runtime-relevant Java/resource/fixture file remains unclassified for catalog purposes.

This closes **framework source coverage**, not current-pack semantic closure:

- fixed provider-owned spells: **0 established**;
- fixed provider-owned schools: **0 established**;
- fixed provider-owned script-created items/entities/attributes/recipes: **0 established**;
- pack-defined semantic objects: **UNKNOWN until authoritative current assembled scripts/provenance are audited**;
- provider status remains **⚠️ PARTIAL / CONDITIONAL**.

Repository/source completeness must never be substituted for the missing authoritative current `kubejs/` tree.
