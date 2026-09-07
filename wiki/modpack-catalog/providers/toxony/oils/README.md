# Toxony 0.10.7 — Oils

## Status

`EXACT SOURCE-VERSION REGISTRY 9/9 / EFFECT PAYLOADS AUDITED / ACQUISITION+RUNTIME QA PENDING / LICENSE CONFLICT`

Exact source checkpoint: `MrFrostyDev/Toxony_Mod@881bf7fe632659e748c279966a2bf49b99f7503f`.

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

- full 0.10.7 crafting/processing graph for all nine Oils;
- exact duration/amplifier settlement for every delivery surface;
- interaction with modded weapons/projectiles in the installed pack;
- stable supported external API for reading/applying Oil state;
- runtime QA against the installed JAR.

Source-visible implementation parameters remain factual audit evidence only while the exact source checkpoint has unresolved GPLv3/LGPLv3 licensing conflict.
