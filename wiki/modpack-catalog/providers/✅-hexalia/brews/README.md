# Hexalia 1.3.7 — Brews

## Estado

`RELEASE-SOURCE-PINNED 1.3.7 / ITEMS 9/9 / RECIPES 9/9 / GRAVEBLOOM DELTA AUDITED / PREVIOUS EFFECT QA BLOCKERS PRESERVED / ASSEMBLED RUNTIME QA SEPARATE`

Source authority for this subcatalog:

`AstralyaStudios/Hexalia@98c22aaf70e069c616fed5ad2dc56d2b37fcd283` — release commit `Hexalia 1.3.7`.

Physical provider: `hexalia-neoforge-1.3.7.jar` / SHA-1 `ca90edf1664cf6d44fe7e5318c71069050499c7e`. Source-build byte equality is not claimed.

## Catalog

| Brew | Item ID | Consumption | Base duration | Current source status |
|---|---|---|---:|---|
| [Arachnid Grace](arachnid-grace.md) | `hexalia:brew_of_arachnid_grace` | MobEffect brew | 240 s | wall climb + Poison removal + water/rain Weakness source-confirmed; documented cobweb immunity runtime-unverified |
| [Bloodlust](bloodlust.md) | `hexalia:brew_of_bloodlust` | MobEffect brew | 240 s | regeneration-effect suppression source-confirmed; advertised lifesteal/strength path not located |
| [Daybloom](daybloom.md) | `hexalia:brew_of_daybloom` | MobEffect brew | 240 s | 5 s sunlight pulses, heal/damage/speed formula source-confirmed |
| [Gravebloom](gravebloom.md) | `hexalia:brew_of_gravebloom` | MobEffect brew | 90 s | player-killed Monsters trigger provider moss/plant growth around the death position |
| [Hollow Silence](hollow-silence.md) | `hexalia:brew_of_hollow_silence` | MobEffect brew | 240 s | registered effect class is inert; advertised sound/vision behavior path not located |
| [Homestead](homestead.md) | `hexalia:brew_of_homestead` | one-shot custom consumable | instant | interdimensional respawn-return path + 30 s Confusion source-confirmed |
| [Siphon](siphon.md) | `hexalia:brew_of_siphon` | MobEffect brew | 240 s | item attraction/pickup + attack-speed modifier source-confirmed; advertised mining speed/exhaustion path not located |
| [Slimewalker](slimewalker.md) | `hexalia:brew_of_slimewalker` | MobEffect brew | 240 s | fall-distance reset + grounded Slowness + bounce path source-confirmed; exact bounce trigger needs runtime QA |
| [Spikeskin](spikeskin.md) | `hexalia:brew_of_spikeskin` | MobEffect brew | 240 s | attribute registrations/override source-confirmed; effective values + advertised damage reflection require QA |

## Shared BrewItem contract

Eight current MobEffect brews use Hexalia's common `BrewItem` path. Seven retained brews have base duration `4800 ticks = 240 s`; Gravebloom is the 1.3.7 exception at **1800 ticks = 90 s**. All use amplifier `0` and return `hexalia:rustic_bottle` on consumption.

Full Moonweave multiplies generic `BrewItem` duration by `1.5`: the seven 240-second brews become 360 seconds, while Gravebloom becomes **2700 ticks = 135 s**. Homestead remains excluded because `HomesteadBrewItem` performs a one-shot teleport rather than applying a MobEffect.

## Recipe completeness

The 1.3.7 release data contains one `hexalia:small_cauldron` recipe for each of the nine brew items. The new Gravebloom recipe uses Spirit Powder, Rotten Flesh, Witchweed and Tree Resin.

This closes the **current 1.3.7 brew item/recipe inventory**. It does not close all Hexalia witchcraft content: salves, Nature's Ritual, Celestial Infusion, Mortar & Pestle, mutations, nodes/idols and other capability-bearing systems remain separate catalog surfaces.

## QA blockers discovered by source audit

The audit intentionally distinguishes provider text from executable paths:

1. **Arachnid Grace** — cobweb immunity is documented, but no matching source path was located.
2. **Bloodlust** — heal-from-damage/strength is documented, while the directly located class removes regeneration-like effects; the advertised lifesteal path was not found.
3. **Hollow Silence** — the registered MobEffect subclass has no custom behavior and no separate effect-specific hook was located.
4. **Siphon** — mining-speed/exhaustion behavior is documented, but the located implementation proves item attraction and attack-speed modification instead.
5. **Slimewalker** — the bounce branch explicitly requires `isSuppressingBounce()`; actual player-facing landing/crouch behavior must be tested.
6. **Spikeskin** — source contains raw armor/movement templates plus a custom modifier-adjustment override; exact applied values and the advertised incoming-damage reflection need runtime/API validation.
7. **Gravebloom** — current source closes its death-triggered moss/plant mutation, but final assembled world-protection/datapack interaction remains runtime QA.

These are provider QA findings, not Black Arcana defects and not permission for Black Arcana to patch Hexalia implicitly.

## Black Arcana rule

A persistent brew effect is not a repeated cast. Do not award mastery, Arcane Danger, Corruption, Strain or other Black Arcana settlement per effect tick. Any bridge must consume a discrete causal event through a verified boundary and preserve Hexalia's item/effect authority.
