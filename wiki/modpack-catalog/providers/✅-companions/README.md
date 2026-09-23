# Companions! — 1.3.4

Status: `COUNTED_SOURCE_PINNED / +9 SEMANTIC MAGIC-BOOK ACTIONS / CATALOG ✅ / RUNTIME QA FAIL-CLOSED`

## Current physical identity

The current sibling physical dossier at `neoforge-rpg-skilltree@39d358ec8de20d647cecbfe4e8c0a0181cc6b12f` confirms:

- physical order: `#104`;
- JAR: `companions-neoforge-1.21.1-1.3.4.jar`;
- mod id: `companions`;
- runtime version: `1.3.4`;
- physical SHA-1: `23f6e4f27a457a8d016412e495e417c0b36fdcc1`;
- Minecraft: 1.21.1;
- physical KnightLib line: 2.0.1.

The exact public source checkpoint used for the semantic catalog is:

`Xylonity/Companions@95c9445e1514648418064ea90b5c373e81375d2f`

That commit is the provider-owned `🔼 Bump version` commit that changes project version `1.3.3 -> 1.3.4`; `gradle.properties` declares Minecraft 1.21.1 and mod id `companions`.

This is a version-correlated source pin. It does **not** prove byte-for-byte equivalence between a locally built source artifact and the separately SHA-pinned physical JAR, so the semantic inventory is `COUNTED_SOURCE_PINNED`, not `COUNTED_EXACT`.

## Provider classification

Companions! is a mixed content provider. For the semantic-magic metric, its relevant player-facing surface is the provider-owned **Magic Book** system.

The exact 1.3.4 item registry contains exactly nine `AbstractMagicBook` registrations:

- `companions:book_ice_shard`;
- `companions:book_ice_tornado`;
- `companions:book_fire_mark`;
- `companions:book_heal_ring`;
- `companions:book_stone_spikes`;
- `companions:book_brace`;
- `companions:book_magic_ray`;
- `companions:book_black_hole`;
- `companions:book_naginata`.

Each item has its own concrete Magic Book class and its own provider-owned cast/action behavior. The same nine books are also the accepted equipment type for the Soul Mage's three book slots; Soul Mage AI has a dedicated attack goal for each identity.

The nine identities are cataloged in [SOURCE-1.3.4-MAGIC-BOOK-INVENTORY.md](./SOURCE-1.3.4-MAGIC-BOOK-INVENTORY.md).

## Registration/config closure

The nine books are registered directly and unconditionally in `CompanionsItems`; no mod-presence or config branch wraps those registrations in the pinned source.

The exact 1.3.4 `Magic Books` config section controls numerical/behavioral settlement such as:

- world griefing permission for explosive spells;
- damage/healing/radius values;
- per-book cooldowns.

It does not expose an enable/disable registration switch for any of the nine identities.

Therefore deployed numerical values remain runtime/config QA, but the source-level semantic inventory is not conditional on a provider spell-registration toggle.

## Survival acquisition closure

All nine identities have provider-owned survival routes in the exact source:

| Route | Magic Books |
|---|---|
| tamed Minion, Overworld variant + Copper Coin | Ice Shard or Ice Tornado |
| tamed Minion, Nether variant + Nether Coin | Fire Mark or Brace |
| tamed Minion, End variant + End Coin | Heal Ring or Stone Spikes |
| vanilla chest-table injection | Black Hole and Magic Ray |
| provider recipe | Naginata |

The Minion routes use provider-owned random-success interactions and then choose between the two listed books. The Black Hole/Magic Ray entries are added to Minecraft chest loot-table modification with provider-owned conditions. Naginata has a dedicated provider recipe.

This closes catalog-level survival reachability for all nine identities without treating JEI or creative-tab visibility as authority.

## Semantic catalog consequence

Companions! contributes:

- **+9 `COUNTED_SOURCE_PINNED` semantic magic actions**;
- no extra count for the nine item containers beyond their one-to-one action identities;
- no extra count for the Soul Mage AI reusing those same nine books;
- no extra count for projectiles, status effects, coins, armor, summons, companion abilities or other provider content unless a later audit establishes a separate qualifying player action.

The previously reconstructed strict semantic minimum of **1382** therefore becomes **1391**.

## Authority boundary

- Companions! owns its Magic Book identities, item use, projectiles/effects, cooldown configuration, acquisition routes and Soul Mage consumption of those books.
- Soul Mage reuse does not create a second spell identity.
- Black Arcana does not copy/reimplement Companions! spell bodies or settlement formulas.
- RPG Skill Tree remains progression/Mastery/perk authority only through real integration boundaries.

## Clean-room / license boundary

The official source repository declares the Java code under GPLv3. This catalog records factual registry, configuration-shape, acquisition and behavior ownership facts from the exact version-correlated source.

Provider assets/localization are not copied into Black Arcana. Display names are treated as identifying factual metadata only; implementation bodies, asset files and provider creative expression are not imported.

## Runtime state — fail-closed

Still unverified in the exact assembled modpack:

- dedicated-server/client boot with the physical 1.3.4 JAR and KnightLib 2.0.1;
- live item-registry parity against the source-pinned nine-book set;
- effective deployed config values;
- each acquisition path under the assembled pack's loot/recipe/datapack state;
- player casts for all nine books;
- Soul Mage three-slot persistence and all nine AI actions;
- damage/heal/projectile attribution and exactly-once settlement;
- block-grief/protection behavior;
- multiplayer owner/team interactions;
- restart/reload/chunk/dimension behavior.

These runtime gates do not erase the source-pinned semantic catalog; they prevent claiming assembled-pack compatibility or Black Arcana integration.

## Result

**✅ Cataloged at source-pinned semantic level: 9/9 provider-owned Magic Book action identities.**

Runtime/provider integration remains fail-closed until direct assembled-pack evidence exists.
