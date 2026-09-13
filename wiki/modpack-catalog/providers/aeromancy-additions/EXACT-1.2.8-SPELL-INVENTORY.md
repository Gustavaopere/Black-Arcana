# SnackPirate's Aeromancy Additions 1.2.8 — exact spell inventory

Status: `10 / 10 ACTIVE PROVIDER SPELL REGISTRATIONS CLOSED AT EXACT SOURCE PIN`

Source authority: `snackerpirater/aero-additions@ae282b32d25ad76ef8d01c637ec05566a767ae4c`
Registry authority: `AASpells` / Iron's `SpellRegistry`
Provider school: `aero_additions:wind`

Active registered IDs:

- `aero_additions:wind_charge`
- `aero_additions:updraft`
- `aero_additions:airstep`
- `aero_additions:asphyxiate`
- `aero_additions:feather_fall`
- `aero_additions:wind_shield`
- `aero_additions:airblast`
- `aero_additions:wind_blade`
- `aero_additions:flush`
- `aero_additions:dash`

The exact registry source also contains commented-out registrations for Tornado, Thunderclap, Summon Breeze, Telelink and Shapeshift. They are not active registry identities and contribute zero to the strict semantic count at this pin.

`AASpells` owns the provider spell register and registers exactly the ten active objects above. `Aeromancy` registers it directly on the mod event bus. No provider-side conditional configuration path controlling creation/removal of these identities was found.

Wind uses the host-native Scroll Forge route through Breeze Rod as school focus. The exact provider source also registers a NeoForge global loot modifier for the normal Trial Chamber reward table; it appends a provider loot table containing Breeze Rod. Updraft Tome and Wind Sword independently embed Updraft and Wind Blade. These acquisition/support surfaces are not additional semantic spells.

Source-pinned semantic delta candidate: **+10 `COUNTED_SOURCE_PINNED`**.
