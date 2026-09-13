# SnackPirate's Aeromancy Additions 1.2.8 — exact spell inventory

Status: `10 / 10 ACTIVE PROVIDER SPELL REGISTRATIONS CLOSED AT EXACT SOURCE PIN`

Source authority: `snackerpirater/aero-additions@ae282b32d25ad76ef8d01c637ec05566a767ae4c`
Registry authority: `AASpells` / Iron's `SpellRegistry`
Provider school: `aero_additions:wind`

| Registry id | Provider class | Registry state | Catalog disposition |
|---|---|---|---|
| `aero_additions:wind_charge` | `WindChargeSpell` | active | `COUNTED_SOURCE_PINNED` |
| `aero_additions:updraft` | `UpdraftSpell` | active | `COUNTED_SOURCE_PINNED` |
| `aero_additions:airstep` | `AirstepSpell` | active | `COUNTED_SOURCE_PINNED` |
| `aero_additions:asphyxiate` | `AsphyxiateSpell` | active | `COUNTED_SOURCE_PINNED` |
| `aero_additions:feather_fall` | `FeatherFallSpell` | active | `COUNTED_SOURCE_PINNED` |
| `aero_additions:wind_shield` | `WindShieldSpell` | active | `COUNTED_SOURCE_PINNED` |
| `aero_additions:airblast` | `AirblastSpell` | active | `COUNTED_SOURCE_PINNED` |
| `aero_additions:wind_blade` | `WindBladeSpell` | active | `COUNTED_SOURCE_PINNED` |
| `aero_additions:flush` | `FlushSpell` | active | `COUNTED_SOURCE_PINNED` |
| `aero_additions:dash` | `DashSpell` | active | `COUNTED_SOURCE_PINNED` |

## Excluded source identities

The exact `AASpells` registry source also contains commented-out registrations for:

- `TornadoSpell`
- `ThunderclapSpell`
- `SummonBreezeSpell`
- `TelelinkSpell`
- `ShapeshiftSpell`

Their class files and/or support assets do not promote them into active registry identities. They contribute **0** to the strict semantic count at this pin.

## Registration closure

`AASpells` owns a single `DeferredRegister<AbstractSpell>` under `aero_additions` and registers exactly the ten active objects above. `Aeromancy` registers `AASpells` directly on the mod event bus. No provider-side conditional configuration path controlling registration was found.

Each active object resolves its own `getSpellResource()` in the provider namespace. `feather_fall` and `wind_shield` were checked directly in their classes; the remaining IDs were checked through their classes/source search plus the active registry list.

## Acquisition closure

Wind uses the host-native Scroll Forge route. Provider data marks Breeze Rod as a Wind school focus and as an Iron's school focus. Iron's 3.16.3 enumerates the school's spells for a matching focus, applying host enabled/crafting/learning gates. The audited provider does not override those gates, and host defaults are enabled/craftable while the Wind school does not require learning.

`Updraft Tome` and `Wind Sword` independently embed Updraft and Wind Blade respectively. These routes strengthen reachability evidence but do not add semantic spell identities.

## Counting result

Source-pinned semantic delta candidate: **+10**.

School identity, armor, staff/sword/tome items, effects, projectiles/entities, upgrade orbs, recipes, focus tags and acquisition loot are support/content surfaces and are not double-counted as extra spells under the current metric.
