# Fantasy Armor — 1.2.4-1.21.1

Status: `CATALOGED / PHYSICAL SHA-PINNED / EXACT SOURCE-PINNED GEAR-EFFECT PROVIDER / ZERO SPELL-RITUAL-ACTION REGISTRY / +0 STRICT SEMANTIC MAGIC / RUNTIME QA FAIL-CLOSED`

## Current physical identity

Current sibling authority:

`neoforge-rpg-skilltree@d7c99d23ef1b38fe62c86a362ec521ced8861f96`

Certified dossier:

`PROJECT-INSTRUCTIONS/modlist/Adventure and RPG + Armor, Tools, and Weapons + Cosmetic + Magic/✅-fantasy-armor v1.2.4-1.21.1.md`

Physical identity:

- JAR: `fantasy_armor-neoforge-1.2.4-1.21.1.jar`;
- mod id: `fantasy_armor`;
- runtime: `1.2.4-1.21.1`;
- Minecraft 1.21.1 / NeoForge;
- physical SHA-1: `2b103680ca80a1d617dcae74630c4df8e93d3c55`.

## Exact publisher release

CurseForge project: `1083998`.

Exact NeoForge 1.21.1 file:

- file ID: `7850813`;
- filename: `fantasy_armor-neoforge-1.2.4-1.21.1.jar`;
- uploaded: 2026-03-31;
- release channel: Release;
- environment: Client & Server;
- published change: Turkish-i locale fix.

Publisher page:

`https://www.curseforge.com/minecraft/mc-mods/fantasy-armor/files/7850813`

The publisher describes Fantasy Armor as armor content where each set grants configurable effects and bonus characteristics.

## Exact source pin

Official repository:

`kend1e/FANTASY-ARMOR`

Exact 1.2.4 release-correlated pin:

`0d58f07346fd7fffc08fac907aa908e5e4295667`

That commit:

- is dated 2026-03-31;
- is titled `Fixed turkish i issue`;
- bumps the NeoForge 1.21.1 project from `1.2.3-1.21.1` to `1.2.4-1.21.1`;
- applies the locale-safe lower-case fix to armor-set naming;
- remains the repository's current `master` at this audit checkpoint.

The source pin is therefore directly version-correlated to the installed release. Physical-JAR byte equality to a locally rebuilt source artifact is not claimed.

## Exact magic-relevant source surface

The exact NeoForge 1.21.1 source tree contains **19 Java classes**.

The gameplay surface is structurally narrow:

- main mod entrypoint;
- armor/item registration;
- armor-set enum/factories;
- armor attributes/config;
- armor MobEffect config/application;
- render/model client code;
- creative tab;
- Moon Crystal item.

The entrypoint registers:

- `fantasy_armor-common.toml`;
- `fantasy_armor-armor_attributes.toml`;
- `fantasy_armor-armor_effects.toml`;
- items;
- armor items;
- creative tab.

No spell, ritual, cast, active ability or keybinding registry is established by the exact source.

## Armor roster

The exact source and sibling dossier enumerate **29 armor sets**.

Each set yields four standard armor pieces, giving **116 armor pieces** under the provider's armor registration surface.

The provider also registers Moon Crystal as a normal item used in the equipment progression/crafting surface.

These item identities are equipment content, not semantic spell/action identities.

## Full-set effects

The exact source defines default full-set effect configuration entries for all 29 sets.

Observed default effects are drawn from vanilla MobEffect identities:

- Jump Boost;
- Water Breathing;
- Night Vision;
- Fire Resistance;
- Regeneration;
- Haste;
- Luck;
- Strength;
- Resistance.

The full-set handler checks whether the player wears four pieces of the same Fantasy Armor set and refreshes the configured MobEffects.

Consequences:

- the effects are passive equipment state;
- the MobEffect identities are Minecraft-owned;
- Fantasy Armor does not mint provider-owned spell identities for them;
- config may replace the defaults, so current deployed values remain runtime/config evidence rather than immutable catalog facts.

## Semantic accounting

Provider-owned spells: **0**.

Provider-owned rituals/rites: **0**.

Provider-owned discrete active magical-action registry: **0**.

Armor items, vanilla MobEffects and attribute modifiers remain outside the Black Arcana spell/ritual/action numerator.

Strict semantic delta:

**+0**

This is a valid zero-semantic closure, not an absence of magical flavor or gameplay effects.

## Authority boundary

Fantasy Armor owns:

- its armor item identities;
- its armor-set definitions;
- provider-configured equipment attributes;
- provider-configured full-set MobEffect application;
- armor assets/rendering.

Minecraft/NeoForge owns the base equipment slots, attributes and MobEffect registries.

Epic Fight, Cosmetic Armor Reworked, FirstPerson and other render/combat systems remain external authorities over their own behavior.

Black Arcana must not reinterpret Fantasy Armor passive equipment effects as casts or duplicate their application.

## Runtime QA remains fail-closed

Catalog closure does not prove:

- exact installed config values;
- full-set effect refresh/removal under every lifecycle edge;
- stale modifiers after unequip/death;
- config reload behavior;
- Epic Fight coexistence;
- Cosmetic Armor visual/functional slot behavior;
- FirstPerson/player-model rendering;
- dedicated-server/full-pack behavior;
- resource-pack/model compatibility;
- byte equality between installed JAR and a source build.

## Result

**✅ Cataloged:** exact physical 1.2.4 identity, SHA, publisher file and exact source pin are established; the magic-relevant runtime is equipment attributes + passive full-set MobEffects, with no provider-owned spell/ritual/active-action registry.

Strict semantic contribution: **+0**.
