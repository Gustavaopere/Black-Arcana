# Somake Spells 1.0.9 — exact registration-gate map

Status: `EXACT PHYSICAL=PUBLISHER ARTIFACT / 83 DECLARED IDS / 67 UNCONDITIONAL + 16 UNIQUE OPTIONAL-GATED / CURRENT MOD-COMPOSITION 83/83 / REACHABILITY NOT CLOSED`

## Evidence

Exact current artifact:

- `somakespells-1.0.9-1.21.1.jar`;
- CurseForge File `8867079`;
- SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`;
- physical Project Library checkpoint SHA-1: same value.

Refined NON-MERGE audit:

- HEAD `071bdd92fed50aea65ad47772f4d1fb0cb8b7536`;
- workflow run `36161117761`;
- verify job `108157871675`: SUCCESS;
- Stage 05 companion smoke job `108159016060`: SUCCESS.

The audit retains only registry IDs, field/control-flow relationships, bounded provider-presence predicates and config-definition facts required for catalog interoperability.

## Registry cardinality

Exact `ModSpells` surface:

- 83 `DeferredHolder` spell fields;
- 83 `DeferredRegister.register(...)` calls;
- 83 unique IDs;
- 0 provider `isEnabled()` overrides;
- 7 provider `allowCrafting()` overrides.

## Cached optional-registration booleans

Exact `ModSpells` initialization caches three booleans:

| Cached field | Provider predicate |
|---|---|
| `MOWZIE_LOADED` | `ModList.isLoaded("mowziesmobs")` |
| `ISS_LOADED` | `MagicFromTheEastCompat.isLoaded()` → `iss_magicfromtheeast` |
| `LEGENDARY_MONSTERS_LOADED` | `LegendaryMonstersCompat.isLoaded()` → `legendary_monsters` |

No Born in Chaos, Tunes 'n Tomes or Geomancy Plus boolean gates a `ModSpells` registration in exact 1.0.9. Those providers have compatibility checks elsewhere in the artifact.

## Exact conditional IDs

### Mowzie's Mobs only — 3

- `somakespells:blessed_connection`;
- `somakespells:guardian_connection`;
- `somakespells:cursed_connection`.

### ISS: Magic From The East only — 2

- `somakespells:mirror_strike`;
- `somakespells:symmetry_empowerment`.

### Legendary Monsters only — 9

- `somakespells:procession_of_souls`;
- `somakespells:grave_sigil`;
- `somakespells:soul_bastion`;
- `somakespells:soul_latch`;
- `somakespells:spiral_of_ruin`;
- `somakespells:soulfall_judgment`;
- `somakespells:soul_reprisal`;
- `somakespells:spectral_rondo`;
- `somakespells:winged_ruin`.

### ISS + Legendary Monsters — 2 nested gates

Both cached booleans must permit the registration block:

- `somakespells:crimson_reflection`;
- `somakespells:spirit_empowerment`.

Unique conditional IDs:

**16**

Unconditional IDs:

`83 - 16 = 67`

## Current-pack registration outcome

Current sibling authority rechecked at:

`neoforge-rpg-skilltree@af648d441441dde929cd49c5e18509347f06f09a`

Current physical provider evidence contains:

- Mowzie's Mobs `1.8.2`;
- ISS: Magic From The East `1.1.5`;
- Legendary Monsters release `2.2.2` / metadata runtime discrepancy preserved in its dossier.

Therefore all three Somake registration predicates required by the exact 1.0.9 registry are satisfied by the current mod composition.

Current-pack Somake registration outcome:

**83 / 83 declared spell identities admitted by provider registration predicates.**

This is not a universal predicate statement for other modpacks and does not establish that all 83 are enabled, craftable or survival-obtainable after effective host/provider config.

## Spell-lock config fact

Exact 1.0.9 `Config` defines:

`enableSpellLockSystem`

through NeoForge `ModConfigSpec.Builder.define(String, boolean)` with code default:

**false**

The effective deployed COMMON value remains unavailable. Default is not substituted for deployed state.

## Remaining strict-count blockers

Registration composition is no longer a blocker.

Still open:

- effective Iron's per-spell/global/datapack `enabled`;
- effective Iron's `allow_crafting`;
- deployed Somake `enableSpellLockSystem`;
- acquisition/focus/reachability, especially the seven spells with provider `allowCrafting()` overrides;
- Somake Aqua current focus/acquisition/reachability; historical Traveloptics coexistence is retired as a current blocker because sibling `d809c7c2e617f5ee14f6867af618c52922d85589` contains no Traveloptics entry;
- assembled-pack runtime/progression settlement.

Therefore Somake remains **⚠️ partial / conditioned** and contributes **+0 strict** from this checkpoint.
