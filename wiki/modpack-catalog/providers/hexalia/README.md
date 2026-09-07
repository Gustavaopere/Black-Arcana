# Hexalia — filename/source release 1.3.6, installed runtime metadata 1.3.5

## Status

`EXACT PUBLIC NEOFORGE RELEASE 1.3.6 / SOURCE-PINNED RELEASE COMMIT 4952c652 / MIT / PHYSICAL FILENAME 1.3.6 / INSTALLED RUNTIME METADATA 1.3.5 / BREWS 8/8 / NATURE'S RITUAL 19/19 PLAYER-FACING / CELESTIAL INFUSION 6/6 / MUTATION 21/21 / MORTAR & PESTLE 12/12 / CENSER 10/10 / IDOLS AUDITED / EXACT INSTALLED-JAR EQUIVALENCE + RUNTIME/API QA PENDING`

## Runtime identity

The current physical modlist remains authority for what actually loads in the pack:

- provider: **Hexalia**;
- installed JAR: `hexalia-neoforge-1.3.6.jar`;
- mod id: `hexalia`;
- runtime version reported by the installed JAR: `1.3.5`;
- mixin config: `hexalia-neoforge.mixins.json`;
- loader/game: NeoForge 1.21.1;
- role: `RITUAL / BREWING / WITCHCRAFT PROVIDER`.

The filename/runtime mismatch is real and must remain visible. Black Arcana must not normalize `1.3.6` and `1.3.5` into one unqualified version string.

## Exact public release + source pin

CurseForge publishes the NeoForge 1.21.1 artifact as:

- project ID `962878`;
- file ID `8658488`;
- file name `hexalia-neoforge-1.3.6.jar`;
- release date `2026-08-16`;
- release line `Hexalia 1.3.6-1.21.1 - NeoForge`;
- license `MIT`.

The official source repository `AstralyaStudios/Hexalia` contains commit:

`4952c65233bf31e9f0d3e55ff76be7fa1007ee3d`

with message `Release Hexalia 1.3.6`, also dated 2026-08-16. At that pin `gradle.properties` declares `mod_version=1.3.6` and `minecraft_version=1.21.1`, while NeoForge metadata declares MIT licensing, `modId = "hexalia"` and `version = "${version}"`.

Source inspection for release-line cataloging is therefore pinned and license-permitted. No upstream code/assets are copied or adapted into Black Arcana.

### Important equivalence limitation

The public release filename and source pin say `1.3.6`, while the installed JAR reports runtime `1.3.5`. That prevents a stronger claim that the installed binary is byte-for-byte/metadata-equivalent to the pinned source build.

Consequently:

- source-derived registry/data/behavior facts are `SOURCE-PINNED 1.3.6`;
- installed presence/filename/runtime remain `MODLIST-PINNED`;
- exact installed-runtime behavior remains QA-gated where integration depends on it.

## Documentation freshness

The official GitHub Wiki currently identifies its supported version as `1.3.3`; it is useful for player-facing concepts, but 1.3.6 pinned source/data and the publisher changelog take precedence for version-specific facts.

The 1.3.6 changelog records, among other fixes, Mortar & Pestle recipe/documentation corrections and makes Nature's Ritual nearby-crop requirement configurable `0–32`, default `8`.

## Canonical subcatalogs

### Small Cauldron brews — 8/8

- [Brew catalog](brews/README.md)

The source-pinned 1.3.6 catalog contains Arachnid Grace, Bloodlust, Daybloom, Hollow Silence, Homestead, Siphon, Slimewalker and Spikeskin. All eight source recipes are cataloged individually.

Provider descriptions and located executable paths do not agree perfectly for several brews. Bloodlust, Hollow Silence, Siphon, Slimewalker and Spikeskin retain explicit runtime/behavior QA blockers rather than having missing semantics inferred.

### Nature's Ritual — 19/19 player-facing

- [Nature's Ritual catalog](rituals/NATURES-RITUAL-CATALOG.md)
- [Ritual output capability audit](rituals/RITUAL-OUTPUT-CAPABILITIES.md)

`debug_natures_ritual` exists at the source pin but is deliberately excluded from player-facing counts.

The source-pinned lifecycle uses a Ritual Table, Hex Focus, cardinal Ritual Braziers two blocks from the table, salt on each used brazier and a configurable mature-crop requirement. Default crop requirement is `8` in radius `8`; consumed mature crops are reset to age 0 on successful completion.

Duration is `40 ticks × number of used braziers`: two-brazier recipes complete in 80 ticks and four-brazier recipes in 160 ticks.

Capability-bearing outputs include Aegiflora, Astrylis, Grimshade, Lourdes, Morphora, Nautilite, Windsong, four elemental nodes, Rootshaper, Kelpweave Blade, Sage Pendant, Rabbage Seeds and the four Bloomwrap armor pieces.

Important source-level examples:

- Aegiflora intercepts Creeper-sourced explosions within radius 8 and has a two-charge wither/destroy lifecycle;
- Grimshade performs skeleton/wither conversions and provides a timed non-player Wither/Weakness field;
- Nautilite provides aquatic Conduit Power/Mining Fatigue cleansing and damages Drowned/Guardians before self-destruction at expiry;
- Windsong destroys nearby projectiles while active, then destroys itself;
- Lourdes periodically removes harmful effects and maintains Regeneration on players/animals;
- Morphora executes provider `hexalia:mutation` recipes across a horizontal radius fixed at 3 in the located path;
- Rootshaper provides provider-owned adaptive pickaxe/shovel behavior plus shift-triggered 3×3 mining;
- Kelpweave Blade has water/rain dash, Slowness-on-hit and probabilistic water repair;
- Sage Pendant modifies XP-orb pickup value while in offhand and consumes durability;
- Bloomwrap pieces provide separate knockback, reflection, regeneration and movement behaviors.

### Celestial Infusion — 6/6

- [Celestial Infusion catalog](infusions/CELESTIAL-INFUSION-CATALOG.md)

The six source-pinned transformations are Galeberries, Celestial Crystal and four Silkweave→Moonweave armor upgrades.

The located provider lifecycle requires a valid item in a Ritual Brazier, Hex Focus, open sky/sun visibility and three Celestial/Withered Celestial Blooms in radius 3. Channel duration is 120 ticks; invalid sky/bloom state cancels. On completion the three blooms degrade one stage. Salting is not checked by the audited Celestial Infusion start path.

### Mutation — 21/21

- [Mutation catalog](mutations/MUTATION-CATALOG.md)

The source pin registers 21 `hexalia:mutation` recipes: 11 vanilla→vanilla transmutations plus 10 transformations into Hexalia plants/saplings/content.

Morphora/Mutavis remain provider authority for this transformation graph. A config field `morphoraRadius` defaults to 6, but the located Morphora activation path uses fixed `MUTATION_RADIUS = 3`; this mismatch remains a provider/runtime QA item rather than being silently reconciled.

### Mortar & Pestle — 12/12

- [Mortar & Pestle catalog](processing/MORTAR-AND-PESTLE-CATALOG.md)

The source-pinned recipe type is shapeless with 1–3 ingredients. The block entity has three unit input slots and requires three completed 20-tick spins before output settlement. A player may trigger valid spins manually, and a neighbor redstone signal may also start them.

The 12 cataloged recipes include mundane conversions plus Hexalia Salt, Mutavis, Siren Paste, Dream Paste, Spirit Powder, Ghost Powder, Fragrant Nectar, Brambleguard Salve and Mender's Salve.

Brambleguard and Mender's both use a 60-tick salve application and apply their effect for 1800 ticks. Both clear canonical `hexalia:bleeding` at application. Brambleguard then additionally removes active effects every tick when their registry path contains `bleed` or `bleeding`, regardless of namespace; Mender's applies vanilla Regeneration and does not supply that ongoing generic purge.

### Censer — 10/10 combinations

- [Censer effect catalog](censer/CENSER-EFFECT-CATALOG.md)

The source-pinned Censer is a persistent provider-owned two-herb effect engine. Default effect radius is 16, default burn duration is 7200 ticks and handlers pulse on a 40-tick interval. Player ignition and dispenser ignition are both supported paths.

The 10 registered combinations cover Tidewarden, Ethereal Grazing, Tide's Memory, Miner's Respite, Phantom Drift, Undead Veil, Withering Calm, Hollow Aura, Blighted Bloom and Tidal Pull.

This is a high-impact cross-domain surface: it can buff players, breed animals, spawn items, repair anvils, relocate items, calm undead/mobs, apply Wither, purge all MobEffects, mutate local blocks/Mushroom Cows and pull animals/monsters/items. Black Arcana must not reinterpret the repeating provider pulses as casts or double-settle their effects.

`Hollow Aura` is particularly relevant to interoperability because the source removes every active MobEffect from each LivingEntity in range without namespace/category filtering. `Blighted Bloom` is world-mutating provider behavior and must not be silently routed through Black Arcana's cast pipeline; any pack-wide protection bridge requires an explicit verified contract.

### Idols

- [Idols and capability-bearing items](items/IDOLS-AND-CAPABILITY-ITEMS.md)

Source-pinned derived idols:

- Clarity Idol — server weather set to clear with provider duration 6000;
- Rainfall Idol — rain with provider duration 6000;
- Tempest Idol — rain + thunder with provider duration 6000;
- Purity Idol — removes enchantments tagged as vanilla curses from the item in the opposite hand and is consumed only when removal succeeds.

The four elemental nodes are registered as ordinary items/reagents; their names do not prove an autonomous elemental-resource runtime.

## Core witchcraft loop

Hexalia owns a preparation-first witchcraft loop rather than an instant spellbook loop:

1. acquire magical herbs/materials;
2. refine ingredients through provider processing such as Mortar & Pestle;
3. prepare Small Cauldron, Nature's Ritual, Celestial Infusion or Censer content;
4. satisfy provider environmental/equipment conditions;
5. receive provider-owned brews, ritual outputs, mutations, fields, items or equipment effects.

Black Arcana integrates around that identity rather than reproducing it as an instant cast system.

## Deduplication consequences

### Witchcraft

Black Arcana Witchcraft must integrate, not replace, Hexalia's cauldron brewing, herbs/material preparation, salves, Nature's Ritual, Celestial Infusion, Mortar & Pestle, Censer, mutations and capability-bearing idols/equipment.

### Blood / Binding

`Brew of Bloodlust` is blood-themed but is not evidence of blood-volume storage, an external blood reservoir, blood-link authority or blood-only casting settlement. It does not occupy the planned Hematic Reservoir / typed blood-binding architecture.

### Souls / spirits

`hexalia:spirit_powder` is a concrete Hexalia reagent produced by its Mortar & Pestle graph. It is not Malum's spirit economy, Eidolon soul state or a Black Arcana soul resource.

### Divine / Celestial

Daybloom and Celestial Infusion create genuine solar/celestial overlap. Divine/Celestial Black Arcana identity must remain materially distinct from this preparation/lunar/crafting path.

### Persistent fields / wards / environmental effects

Aegiflora, Windsong, Grimshade, Nautilite, Lourdes and especially the Censer demonstrate that Hexalia already owns multiple persistent local-effect fields. A Black Arcana field/domain must preserve its own identity, bounded execution and `WorldEffectPolicy` requirements instead of cloning these witchcraft utilities.

### Weather / environment

Hexalia already owns consumable clear/rain/thunder weather idols. A generic duplicate weather-control spell is therefore poor deduplication. Any Black Arcana grand-weather mechanic would still need distinct forbidden identity, hazards, budgets and canonical `WorldEffectPolicy` handling.

### Curse / status cleansing

Purity Idol already owns straightforward removal of vanilla curse-tagged enchantments from an opposite-hand item. Censer Hollow Aura additionally owns a broad local MobEffect purge. Neither behavior owns Black Arcana Corruption, Arcane Strain or Arcane Backlash unless those channels are deliberately represented through an overlapping provider surface, which current architecture does not require.

### Order / Chaos

No audited Hexalia source-pinned surface proves Black Arcana's proposed server-authoritative imposed-law or causal/probability mechanics. The current catalog does not reserve those identities for Hexalia.

## Safe integration posture

- No second Hexalia recipe engine.
- No second registry of brew/salve/Censer effects.
- No re-settlement of a provider ritual, mutation, weather action, Censer pulse or item consumption.
- No Mastery from continuous proximity to a node/plant/ritual/Censer or from redstone/dispenser automation.
- Any progression event requires discrete causal evidence and deduplication; automated provider paths must not invent a player owner.
- Do not create duplicate resources for Hexalia reagents.
- Source pin authorizes factual cataloging, not copying upstream code/assets into Black Arcana.
- Source class visibility alone is not a supported integration/API contract.

## Remaining open audit items

1. reconcile exact installed-JAR identity against public File ID `8658488` and explain why runtime metadata reports `1.3.5`;
2. retain explicit runtime QA for brew description/source discrepancies, especially Hollow Silence, Bloodlust, Siphon, Slimewalker and Spikeskin;
3. identify supported/stable integration API or event surfaces; do not couple to implementation classes merely because they are visible;
4. perform exact pack runtime QA for brews, rituals, Celestial Infusion, mutations, Mortar & Pestle, salves, Censer and idols before promoting source-derived formulas to installed-runtime facts;
5. run cross-mod interaction QA where provider behavior is deliberately broad, especially Brambleguard bleed-path removal, Censer Hollow Aura, Blighted Bloom and weather/world-changing items.

## Phase 3 gate

Hexalia now has granular source-pinned semantic coverage across its major witchcraft preparation and persistent-effect systems, but implementation remains `BLOCKED / FAIL-CLOSED FOR PROVIDER-SPECIFIC HOOKS` until stable integration boundaries and the installed `1.3.6 filename / 1.3.5 runtime` equivalence question are resolved where required. Source catalog completion is not installed-runtime validation.
