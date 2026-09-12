# Farmer's Spell 'n Spellbooks 1.0.5.1 — Exact spell inventory

Status: `6 / 6 REGISTERED PROVIDER SPELL IDENTITIES CLOSED AT EXACT SOURCE PIN`

Source authority: `GLDYM/Farmers-Spell-n-Spellbook@b7cbb40316a9ccbbc2ce2b56b3023647261ce569`
Registry authority: `ModSpells` / Iron's `SpellRegistry`
Provider school: `farmers_spell:gluttony`

| Registry id | Display name in provider locale | Cast profile observed from provider class/config | Catalog disposition |
|---|---|---|---|
| `farmers_spell:goodberry` | Goodberry | server-side item conjuration; instant/minion cast profile | `COUNTED_EXACT` |
| `farmers_spell:phantom_loot` | Ubiquitous | channelled provider/Foodgeist interaction surface | `COUNTED_EXACT` |
| `farmers_spell:seal_coat` | Grease Coating | long-duration provider status/defensive food interaction surface | `COUNTED_EXACT` |
| `farmers_spell:bad_apple` | Rotten Apple | instant provider projectile surface | `COUNTED_EXACT` |
| `farmers_spell:chaos_slash` | Chaotic Pastry Slash | instant provider slash/projectile attack surface | `COUNTED_EXACT` |
| `farmers_spell:preserve_circle` | Brining Ritual | long-cast provider area-effect/entity surface | `COUNTED_EXACT` |

## Registration closure

`ModSpells` creates one `DeferredRegister<AbstractSpell>` under the provider namespace and registers exactly the six IDs above. `FarmersSpell` registers that spell register on the mod event bus without a mod-loaded/config branch around registration.

Provider common config contains per-spell `SpellConfig` entries and a separate behavior toggle for blood-magic interaction. Those settings do not create or remove any of the six registry identities in the exact source path audited here. Numerical runtime values are provider balance, not Black Arcana-owned constants.

No seventh provider spell registration was found in the complete source tree. Spell-like localization or support items are not promoted without a registry identity.

## School handling

All six belong to the provider-owned `farmers_spell:gluttony` school. The school is not counted as a separate semantic action under the current metric, matching the catalog treatment of other Iron's addon schools.

The school declares `requiresLearning=false` and `allowLooting=false`. Therefore generic random Iron's scroll loot is not used as reachability proof.

## Host-native acquisition route

Provider data defines Gluttony focus as both `#minecraft:foods` and `farmers_spell:foodgeist_seasoning`. The public Iron's 3.16.3 source-line Scroll Forge contract identifies a school from a matching focus and enumerates its spells subject to `allowCrafting`, `isEnabled` and `canBeCraftedBy` gates.

No Farmer's Spell override of those three gates was found for the six registered classes. Foodgeist Seasoning additionally has provider-owned survival reward/loot surfaces. This is sufficient for catalog-level provider/host-native reachability while leaving assembled-pack behavior, probabilities and runtime compatibility for direct QA.

## Counting result

Exact semantic delta candidate: **+6**.

No cooking recipe, food, gear item, status effect, school identity, projectile/entity implementation or acquisition recipe is double-counted as an additional spell merely because it supports one of the six actions.
