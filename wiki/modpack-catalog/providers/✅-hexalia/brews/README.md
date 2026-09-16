# Hexalia 1.3.6 — Brews

## Estado

`SOURCE-PINNED RELEASE-LINE CATALOG 8/8 ITEMS / RECIPES 8/8 / CORE EFFECT PATHS AUDITED / INSTALLED-RUNTIME EQUIVALENCE PENDING`

Source authority for this subcatalog:

`AstralyaStudios/Hexalia@4952c65233bf31e9f0d3e55ff76be7fa1007ee3d` — publisher commit `Release Hexalia 1.3.6`, MIT.

The physical modpack JAR is `hexalia-neoforge-1.3.6.jar`, but its runtime metadata reports `1.3.5`. Therefore **8/8 here means complete against the pinned public 1.3.6 brew item/tag/source surface, not exact installed-JAR runtime validation**.

## Catalog

| Brew | Item ID | Consumption | Base duration | 1.3.6 source status |
|---|---|---|---:|---|
| [Arachnid Grace](arachnid-grace.md) | `hexalia:brew_of_arachnid_grace` | MobEffect brew | 240 s | wall climb + Poison removal + water/rain Weakness source-confirmed; documented cobweb immunity runtime-unverified |
| [Bloodlust](bloodlust.md) | `hexalia:brew_of_bloodlust` | MobEffect brew | 240 s | regeneration-effect suppression source-confirmed; advertised lifesteal/strength path not located |
| [Daybloom](daybloom.md) | `hexalia:brew_of_daybloom` | MobEffect brew | 240 s | 5 s sunlight pulses, heal/damage/speed formula source-confirmed |
| [Hollow Silence](hollow-silence.md) | `hexalia:brew_of_hollow_silence` | MobEffect brew | 240 s | registered effect class is inert; advertised sound/vision behavior path not located |
| [Homestead](homestead.md) | `hexalia:brew_of_homestead` | one-shot custom consumable | instant | interdimensional respawn-return path + 30 s Confusion source-confirmed |
| [Siphon](siphon.md) | `hexalia:brew_of_siphon` | MobEffect brew | 240 s | item attraction/pickup + attack-speed modifier source-confirmed; advertised mining speed/exhaustion path not located |
| [Slimewalker](slimewalker.md) | `hexalia:brew_of_slimewalker` | MobEffect brew | 240 s | fall-distance reset + grounded Slowness + bounce path source-confirmed; exact bounce trigger needs runtime QA |
| [Spikeskin](spikeskin.md) | `hexalia:brew_of_spikeskin` | MobEffect brew | 240 s | attribute registrations/override source-confirmed; effective values + advertised damage reflection require QA |

## Shared BrewItem contract

The seven MobEffect brews use Hexalia's common `BrewItem` path:

- server applies the bound MobEffect;
- base duration `4800 ticks = 240 s`;
- amplifier `0`;
- full Moonweave armor multiplies duration by `1.5`, yielding `7200 ticks = 360 s` for these base brews;
- consumed item returns a `hexalia:rustic_bottle`.

Homestead is intentionally excluded from that duration contract because it uses `HomesteadBrewItem` and performs a one-shot teleport instead of applying one of the seven brew MobEffects.

## Recipe completeness

The exact generated 1.3.6 data includes one `hexalia:small_cauldron` recipe for each of the eight brew items. Every individual fiche records the exact four ingredients found at the source pin.

This closes the **1.3.6 brew item/recipe inventory**. It does not close all Hexalia witchcraft content: salves, Nature's Ritual, Celestial Infusion, Mortar & Pestle, mutations, nodes/idols and other capability-bearing systems remain separate catalog surfaces.

## QA blockers discovered by source audit

The audit intentionally distinguishes provider text from executable paths:

1. **Arachnid Grace** — cobweb immunity is documented, but no matching source path was located.
2. **Bloodlust** — heal-from-damage/strength is documented, while the directly located class removes regeneration-like effects; the advertised lifesteal path was not found.
3. **Hollow Silence** — the registered MobEffect subclass has no custom behavior and no separate effect-specific hook was located.
4. **Siphon** — mining-speed/exhaustion behavior is documented, but the located implementation proves item attraction and attack-speed modification instead.
5. **Slimewalker** — the bounce branch explicitly requires `isSuppressingBounce()`; actual player-facing landing/crouch behavior must be tested.
6. **Spikeskin** — source contains raw armor/movement templates plus a custom modifier-adjustment override; exact applied values and the advertised incoming-damage reflection need runtime/API validation.

These are provider QA findings, not Black Arcana defects and not permission for Black Arcana to patch Hexalia implicitly.

## Black Arcana rule

A persistent brew effect is not a repeated cast. Do not award mastery, Arcane Danger, Corruption, Strain or other Black Arcana settlement per effect tick. Any bridge must consume a discrete causal event through a verified boundary and preserve Hexalia's item/effect authority.
