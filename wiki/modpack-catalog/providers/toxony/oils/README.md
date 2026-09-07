# Toxony 0.10.7 — Oils

## Status

`EXACT SOURCE-VERSION REGISTRY 9/9 / EFFECT PAYLOADS AUDITED / MORTAR ACQUISITION AUDITED / DELIVERY INVENTORY PARTIAL / RUNTIME QA PENDING / LICENSE CONFLICT`

Exact source checkpoint: `MrFrostyDev/Toxony_Mod@881bf7fe632659e748c279966a2bf49b99f7503f`.

Detailed processing/delivery facts: [Processing, acquisition and delivery](../processing/README.md).

## Registry — 9/9

| Oil ID | Provider effect payload | Applicability surface |
|---|---|---|
| `toxony:poison_oil` | vanilla Poison | Toxony oil-applicable item tag |
| `toxony:toxin_oil` | `toxony:toxin` | Toxony oil-applicable item tag |
| `toxony:fatigue_oil` | Slowness + Mining Fatigue + Weakness | Toxony oil-applicable item tag |
| `toxony:fire_resistance_oil` | Fire Resistance | Toxony oil-applicable item tag |
| `toxony:glowing_oil` | Glowing | vanilla `weapon_enchantable` item tag |
| `toxony:acid_oil` | `toxony:acid` | Toxony oil-applicable item tag |
| `toxony:smoke_oil` | Slowness + Blindness + Weakness | Toxony oil-applicable item tag |
| `toxony:regeneration_oil` | Regeneration + Instant Health | Toxony oil-applicable item tag |
| `toxony:witchfire_oil` | `toxony:toxin` + `toxony:flammable` | Toxony oil-applicable item tag |

## Mending Oil is not a tenth registered Oil

The provider also exposes a dedicated `mending_oil_pot` item/block and Mortar recipe. It is implemented through a special `MendingOilPotItem`/block path rather than an additional entry in the nine-entry custom Oil registry.

Therefore:

- registered Oils remain **9/9**;
- Mending Oil Pot remains a real provider capability/delivery item;
- it must not be counted as `toxony:mending_oil` unless such a registry entry is separately proven.

## Mortar acquisition for Oil/Tox delivery items

Exact 0.10.7 Mortar recipes include:

- Poison Oil Pot — Honeycomb + Poison Paste + Empty Oil Pot;
- Fire Resistance Oil Pot — Honeycomb + Magma Cream + Empty Oil Pot;
- Glowing Oil Pot — Honeycomb + Glow Ink Sac + Empty Oil Pot;
- Fatigue Oil Pot — Honeycomb + Fermented Spider Eye + Water Hemlock + Empty Oil Pot;
- Acid Oil Pot — Honeycomb + Toxic Paste + 2× Acid Slimeball + Empty Oil Pot;
- Mending Oil Pot — Honeycomb + Toxic Paste + Toxic Spit + Ocelot Mint + Empty Oil Pot;
- Toxin Tox Pot — Honeycomb + Toxin + Toxic Paste + Empty Tox Pot;
- Regeneration Tox Pot — Honeycomb + Ghast Tear + Sunspot + Empty Tox Pot;
- Smoke Tox Pot — Honeycomb + Fermented Spider Eye + Moonlight Hemlock + Empty Tox Pot;
- Acid Tox Pot — Honeycomb + Warproot + Acid Slimeball + Bog Bone + Empty Tox Pot;
- Witchfire Tox Pot — Honeycomb + Blaze Powder + Warproot + Empty Tox Pot;
- Oil Base — Honeycomb + Toxic Paste → 2 Oil Base.

This confirms acquisition is provider alchemy, not generic spell learning.

## Provider identity

Toxony Oils are not Black Arcana spell effects. The provider owns:

- what equipment accepts an Oil;
- coating state/lifetime;
- delivery through its pots, tox pots, bolts and other items;
- resulting MobEffect application;
- item durability/capacity and alchemical acquisition.

The exact source line contains dedicated delivery items including oil pots, tox pots and several effect-specific bolts. This establishes that Toxony already covers both weapon coating and projectile/throwable chemical delivery.

## Deduplication

Black Arcana must not create a parallel Oil registry or add a second copy of an already-settled Toxony effect when observing a hit.

Particularly strong overlaps:

- Poison/Toxin — direct harmful chemical damage/status;
- Acid — corrosion;
- Witchfire — toxin + flammability combination;
- Smoke/Fatigue — control/debuff mixtures;
- Regeneration — restorative coating/delivery;
- Fire Resistance — defensive alchemical preparation.

A future Witchcraft capability may consume a real Toxony Oil item or state only through a verified provider/native Minecraft boundary. Similar naming or chemistry theme is not an integration hook.

## Fields still open

- individual inventories for non-Mortar processing families;
- complete duration/amplifier/max-use table for every delivery item;
- interaction with modded weapons/projectiles in the installed pack;
- stable supported external API for reading/applying Oil state;
- runtime QA against the installed JAR.

Source-visible implementation parameters remain factual audit evidence only while the exact source checkpoint has unresolved GPLv3/LGPLv3 licensing conflict.
