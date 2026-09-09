# Backported Spellbooks — content, worldgen and proc boundary

## Registry surface

At the May 28 official source ceiling, explicit provider registration/data surfaces close as follows:

- 15 explicit non-block item registrations;
- 4 provider blocks, each also registered with a block item;
- total item-registry objects: 19;
- 5 entity types;
- 4 mob effects;
- 2 particles;
- 1 fluid + 1 fluid type;
- 19 recipe JSONs;
- 2 configured ore features;
- 2 placed ore features;
- 2 NeoForge biome modifiers.

This count is a source-registry/data inventory, not a claim of byte-for-byte physical-JAR parity.

## Explicit non-block items

Observed item registrations:

- `pale_observer_helmet`;
- `pale_observer_chestplate`;
- `pale_observer_leggings`;
- `pale_observer_boots`;
- `slime_boots`;
- `eyebloosom_staff`;
- `miasma_staff`;
- `garden_rapier`;
- `pale_guide_spell_book`;
- `quicksilver_spell_book`;
- `resin_vial`;
- `pale_amber`;
- `raw_quicksilver`;
- `quicksilver_ingot`;
- `corroded_fossil`.

The four registered blocks also receive block items through the provider registration helper.

Resource filenames such as affinity-ring/scroll/model assets are not counted as items unless a registration surface exists.

## Blocks and worldgen

Registered blocks:

- `backportedspellbooks:corroded_fossil_ore`;
- `backportedspellbooks:quicksilver_ore`;
- `backportedspellbooks:raw_quicksilver_block`;
- `backportedspellbooks:quicksilver_block`.

Worldgen data provides placed/configured ore feature families for Corroded Fossil and Quicksilver.

Both exact NeoForge biome modifiers:

- use `neoforge:add_features`;
- target `minecraft:sulfur_caves`;
- inject at `underground_ores`.

Feature IDs:

- `backportedspellbooks:corroded_fossil_ore_placed`;
- `backportedspellbooks:quicksilver_ore_placed`.

This matches the publisher's exact 0.1.2 changelog. Vanilla Backport remains authority for the host Sulfur Caves content referenced by the provider source.

Black Arcana must not duplicate these ore placements, create substitute Sulfur Caves worldgen, or run global/per-tick scans to emulate provider acquisition.

## Entity/effect support

Observed entity types:

- `pale_thorn`;
- `resin_spray`;
- `sulfur_bomb`;
- `sulfur_field`;
- `sulfur_cloud`.

Observed effects:

- `paranoia`;
- `resin_poison`;
- `slime_aspect`;
- `sulfuric_poison`.

Observed particles:

- `resin`;
- `resin_bubble`.

These are support/content registry objects. Entity/effect/particle counts do not inflate the spell count.

## Fluid/data-processing surface

The provider registers one Resin fluid and one FluidType. Source data includes alchemist-cauldron and ordinary crafting/cooking/smithing recipes around resin, quicksilver, equipment and armor.

Recipe execution/resource settlement belongs to the corresponding recipe host/framework. Black Arcana does not create a parallel recipe or fluid settlement path.

## Miasma Staff proc

The source defines Miasma Staff as an Iron's staff object and observes it from a server-side post-damage hook.

Observed policy:

- qualifying Nature/Hydro magic damage can trigger the provider effect path;
- the proc applies provider `sulfuric_poison`;
- item cooldown handling uses the player/item cooldown container;
- source defines a 10-second passive cooldown constant.

Iron's/Ace's own the host damage classifications/attributes they expose. Backported owns the equipment proc. BA must not duplicate the poison proc or cause BA Backlash to enter it intentionally.

## Garden Rapier proc

The provider Garden Rapier is an Iron's magic-sword object with provider-specific server post-damage behavior. The source embeds/uses Iron's Oakskin-related spell capability and triggers provider nature/resin behavior after qualifying damage.

Backported owns this equipment proc. Iron's owns its host spell/damage infrastructure. BA must not execute a second blastwave/poison settlement for the same hit.

## Slime Boots fall behavior

The server hook cancels `LivingFallEvent` for a player wearing the provider Slime Boots. This is provider equipment behavior, not a spell cast.

Static QA discrepancy retained: the item class contains cooldown-related tooltip/state language, while the inspected fall-event hook does not visibly test or set that cooldown before canceling the fall. Live physical behavior remains runtime-QA pending; the catalog does not invent a missing condition.

## Spellbooks and host attributes

Quicksilver Spellbook is an Iron's `SpellBook` with eight slots and source-defined modifiers to Iron's casting move speed, cast-time reduction, mana regeneration and max mana.

Pale Guide Spellbook is an Iron's `SpellBook` with twelve slots and source-defined Nature/Eldritch power plus Ace's mana-steal/max-mana-related modifiers.

These modifiers remain host/provider attributes. They do not become BA casting speed, BA mana, BA cooldown or RPG Skill Tree authority automatically.

## Dependency/failure boundary

The source directly imports Iron's, Vanilla Backport and selected Ace's APIs, while exact NeoForge metadata formally declares only NeoForge and Minecraft.

Consequences:

- these are undeclared code-level/source expectations;
- physical presence in the current pack satisfies presence, not compatibility proof;
- BA must not register fallback classes/items/biomes/effects when one is missing;
- future integration must fail closed if a provider contract cannot be proven.

## World safety

Provider worldgen is bounded by datapack biome modifiers. Provider spell/projectile world effects remain provider-owned.

Any future Black Arcana destructive mutation triggered by a BA-native mechanic must still pass through `WorldEffectPolicy`. The existence of provider ores, sulfur entities or nature magic does not authorize BA to bypass its canonical world-safety policy.