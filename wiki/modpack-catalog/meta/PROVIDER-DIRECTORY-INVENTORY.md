# Provider Directory Inventory

Checkpoint: 2026-10-06

Current structural authority:
- Black Arcana base for this batch: `main@4d6ff1f63bda925836af0b1b1c0a2702c7cbdf3a`;
- current sibling physical/modlist authority: `neoforge-rpg-skilltree@de80b186357cad20ba5b81892a8682777e96e35a`.

## Current structural count

The canonical tree `wiki/modpack-catalog/providers/` now contains:

- **164** top-level provider directories;
- **162 ✅ cataloged**;
- **2 ⚠️ partial / conditioned**;
- **0 ❌**;
- **0 🟡**;
- **0 ⛔**.

The two current ⚠️ directories are:

1. Traveloptics;
2. Deeper and Darker.

Iron's Spellbooks KubeJS is now ✅ cataloged at **+0** semantic identities under exact-source + owner-attestation evidence; deployed-instance script parity is retained as QA and can reopen the catalog if contradictory current scripts are found.

The current physical-`Magic` category reconciliation remains **97/97 mapped**. See [PHYSICAL-MAGIC-RECONCILIATION-2026-10-05.md](./PHYSICAL-MAGIC-RECONCILIATION-2026-10-05.md).

Folder prefixes track **catalog completeness**, not whether every deployed config/reachability/runtime gate has passed. A ✅ provider can therefore retain explicit runtime/config conditions inside its dossier.

## 06/10 cross-domain zero-semantic batch 1

Four new current physical providers outside the physical-`Magic` category subtotal are now materialized:

- `✅-create-dragons-plus` — `ZERO_SEMANTIC_CREATE_PROCESSING_COMPAT_INFRA`;
- `✅-immersive-portals-true-immersion` — `ZERO_SEMANTIC_PORTAL_INTERACTION_BRIDGE`;
- `✅-yungs-better-witch-huts` — `ZERO_SEMANTIC_STRUCTURE_WORLDGEN_LOOT`;
- `✅-snow-real-magic` — `ZERO_SEMANTIC_SNOW_WORLDSTATE`;

All four new providers contribute **+0 strict**. `efiscompat` 3.1.0 is already represented once by canonical `✅-efiscompat` and contributes no new structural row. The physical-`Magic` subtotal remains **97/97 mapped** and the strict reconstructible semantic minimum remains **1849**.

See [CROSS-DOMAIN-REBASE-2026-10-06-BATCH-1.md](./CROSS-DOMAIN-REBASE-2026-10-06-BATCH-1.md).

## 06/10 cross-domain zero-semantic batch 2

Three additional current physical cross-domain providers are now materialized:

- `✅-sky-aesthetics` — `ZERO_SEMANTIC_CLIENT_SKY_RENDER_API`;
- `✅-northstar-redux` — `ZERO_SEMANTIC_CREATE_SPACE_TECH_TRAVEL`;
- `✅-yungs-better-end-island` — `ZERO_SEMANTIC_END_WORLDGEN_DRAGON_FIGHT_OVERLAY`.

All three contribute **+0 strict**. The physical-`Magic` subtotal remains **97/97 mapped**, the strict reconstructible semantic minimum remains **1849**, and the only catalog-partial providers remain Traveloptics and Deeper and Darker.

Cold Sweat: Altitude 0.7.0 remains outside the current physical structural count because the sibling dossier explicitly lacks post-install physical revalidation. Amplified Nether and Chunky remain pure worldgen/pregeneration infrastructure and are not materialized as magic-provider directories in this batch.

See [CROSS-DOMAIN-REBASE-2026-10-06-BATCH-2.md](./CROSS-DOMAIN-REBASE-2026-10-06-BATCH-2.md).

## Historical 01/10 structural checkpoint

The detailed cross-domain sequence below documents the historical 01/10-era expansion, where the tree reached **154 = 151 ✅ + 3 ⚠️** before later closures/additions. Its per-provider evidence remains valid; only the structural total and current-open-folder list are superseded by the 05/10 snapshot.

The 01/10 cross-domain structural deltas are `✅-ignis-soulfires`, `✅-artifacts`, `✅-cataclysm`, `✅-betterend`, `✅-weapons-of-miracles`, `✅-born-in-chaos`, `✅-bosses-rise`, `✅-portable-hole`, `✅-legendary-monsters`, `✅-alexs-caves-continued`, `✅-alexs-mobs-continued`, `✅-ice-and-fire-dread-land` and `✅-bosses-of-mass-destruction`. None is a new row in the physical `Magic` category subtotal. Ignis exact-artifact PR #491 / run `36832733575` closes eight discrete supernatural player actions. Artifacts exact-artifact PR #493 / run `36834282003` closes 49 item entries and the base item-ability component surface as +0 independent semantic identities under current-stack deduplication with Reliquified Artifacts. L_Ender's Cataclysm exact-artifact PR #495 / run `36893767327` closes 24 discrete supernatural item/equipment actions plus 3 deliberate summoning rituals = **+27 `COUNTED_EXACT`**. BetterEnd exact-artifact PR #497 / run `36901757754` closes 48 `betterend:infusion` ritual identities plus one Eternal Portal Ritual = **+49 `COUNTED_EXACT`**. Weapons of Miracles exact-artifact PR #499 / run `36905999133` closes the exact 64-ID skill registry and dispositions it to **12 `COUNTED_EXACT` supernatural actions + 1 `CONDITIONAL` + 51 excluded**. Born in Chaos exact-artifact PR #501 / run `36919074090` closes **17 deliberate supernatural player actions = +17 `COUNTED_EXACT`**, with passive/on-hit gear, ordinary consumables, primary projectile modes, loot/debug surfaces and mob-native magic excluded. Bosses'Rise exact-artifact PR #503 / run `36932226075` closes **8 deliberate supernatural player actions = +8 `COUNTED_EXACT`**, with reactive/on-hit effects, primary weapon collision/firing modes, roll, passives, boss-native attacks and decor/debug surfaces excluded. Portable Hole exact-artifact PR #505 / run `36935857689` closes **1 magical traversal action = +1 `COUNTED_EXACT`**, with tunnel depth, temporary blocks, restoration lifecycle and feedback excluded as separate identities. Legendary Monsters exact-artifact PR #507 / run `36940087686` closes **22 deliberate supernatural player actions = +22 `COUNTED_EXACT`**, with primary firing/throwing modes, Withered Scythe charge, locators, passive/reactive gear, summon-management follow-ups and mob-native powers excluded. Alex's Caves Continued exact-artifact PR #509 / run `36947136917` closes **8 supernatural/magical player actions = +8 `COUNTED_EXACT`** after exhaustive 42-item interaction inspection plus exact Conversion Crucible/Beholder block seams; primary weapons, technology, consumables, vehicles, setup items and mob-native magic are excluded. Alex's Mobs Continued exact-artifact PR #511 / run `36949047824` closes **3 supernatural roots** after exhaustive 26-item + 11-block interaction inspection: Item Transmutation contributes **+1 `COUNTED_EXACT`**, while Void Worm Summoning and Dimensional Carver remain `CONDITIONAL` on current summon/reachability config. Ice And Fire: Dread Land exact-artifact PR #513 / run `36953394134` closes **1 Dreadland Key → Dread Portal Activation = +1 `COUNTED_EXACT`**, with realm keys treated as setup/progression and portal travel as downstream lifecycle. Bosses of Mass Destruction exact-artifact PR #515 / run `36955037836` closes **5 supernatural roots = 3 `COUNTED_EXACT` + 2 `CONDITIONAL`**, with the Lich summon-mechanic deployment state kept fail-closed. Deeper and Darker publisher-baseline PR #517 / run `36959073485` closes three public-release supernatural roots but proves all official 1.4.1 publisher bytes differ from physical SHA-1 `83f7edd0a8516b2767c2cda7a3b2402f9e290d88`; it therefore remains `⚠️ OTHER_VERIFIED / +0 strict`. Protection Pixel exact-artifact PR #520 / run `36962672381` proves physical SHA-1 equals publisher File `7549821` and closes the provider as **`ZERO_SEMANTIC_TECH_GEAR` / +0 strict**. BetterNether exact-artifact PR #522 / run `36965947196` proves physical SHA-1 equals publisher File `8615740` and closes altar/portal/pedestal/brewing/equipment surfaces as **`ZERO_SEMANTIC_WORLDGEN_BREWING_EQUIPMENT` / +0 strict**. Grapplemod Skybound exact-artifact PR #524 / run `36967140184` proves physical SHA-1 equals publisher File `8176552` and closes Ender Staff/forcefield/rocket/motor/magnet/rope-hook surfaces as **`ZERO_SEMANTIC_TRAVERSAL_PHYSICS` / +0 strict**. Dimensional Sable exact-artifact PR #526 / run `37003723918` proves physical SHA-1 equals Modrinth version `l9l5j4Zh` and closes `/sable dimension_set` plus sublevel warping as **`ZERO_SEMANTIC_DIMENSION_TRANSFER_INFRA` / +0 strict**. Create Teleporters Remastered exact-artifact PR #528 / final run `37011387498` proves physical SHA-1 equals CurseForge File `8010045` and closes Pocket Dimension Remote, TP Links, Custom/Quantum Portal and Entity/Item/Block Teleporters as **`ZERO_SEMANTIC_TECH_TELEPORT_INFRA` / +0 strict**. Create: Chromatic Return exact-artifact PR #530 / run `37012907385` proves physical SHA-1 equals CurseForge File `8578225` and closes three Infused Book enchantment-application branches plus charm/Creative Flight gear state as **`ZERO_SEMANTIC_ENCHANT_GEAR_INFRA` / +0 strict**. Create: Deep Dark exact-artifact PR #532 / run `37015531955` proves physical SHA-1 equals CurseForge File `7624342`; exhaustive 37-class activation inspection closes Echo armor tick buffs, Echo Sword damage-event debuffs and Molten Echo collision effects as **`ZERO_SEMANTIC_PASSIVE_ECHO_GEAR_PROCESSING` / +0 strict**. Create: Mechanical Spawner exact-artifact PR #534 / run `37016899558` proves physical SHA-1 equals CurseForge File `8418593`; 52-class/97-recipe inspection closes 28 spawner recipes, Loot Collector and KubeJS recipe support as **`ZERO_SEMANTIC_KINETIC_MOB_SPAWN_INFRA` / +0 strict**. Create: Fantasizing Again exact-artifact PR #536 / run `37018144292` proves physical SHA-1 equals CurseForge File `8585611`; 175-class/105-data-path inspection closes Warden conversion, batch tools, engines, Transporter, storage and Chromatic processing as **`ZERO_SEMANTIC_CREATE_AUTOMATION_TOOLS_INFRA` / +0 strict**. Create: More Features exact-artifact PR #538 / run `37020906917` proves physical SHA-1 equals CurseForge File `8325313`; 145-class/108-data-path inspection closes professions, mechanisms, boxes/devices and recipes as **`ZERO_SEMANTIC_CREATE_AUTOMATION_VILLAGER_INFRA` / +0 strict**. Create: Mobile Packages exact-artifact PR #540 / run `37022104060` proves physical SHA-1 equals CurseForge File `8502329`; 130-class/13-data-path inspection closes Bee Port, Robo Bee, Stock Ticker, Mobile Packager and network/package delivery as **`ZERO_SEMANTIC_CREATE_LOGISTICS_INFRA` / +0 strict**. Dragon Care 1.3.1 then adds one ✅ version-declared-source closure, **`ZERO_SEMANTIC_HUSBANDRY_SUPPORT` / +0 strict**: care/bond/items/effects/tracking/loot/data/config are provider-owned support surfaces, while passive bond rewards and husbandry/QTE/sensor/phone interactions do not form a semantic magic roster. Pufferfish's Skills 0.19.0 then adds one exact-current ✅ framework closure, **`ZERO_SEMANTIC_SKILL_TREE_FRAMEWORK` / +0 strict**: exact physical/publisher File `8792775` equality closes 426 entries / 334 classes / 92 resources, zero `data/puffish_skills/**` provider data and zero packaged provider-tree JSON definitions; rewards/tree/XP/exchange surfaces remain generic progression infrastructure. Pufferfish's Attributes 0.8.3 then adds one exact-current ✅ attribute-framework closure, **`ZERO_SEMANTIC_ATTRIBUTE_FRAMEWORK` / +0 strict**: exact physical/publisher File `8610466` equality closes 42 attribute IDs, while Magic Damage/Resistance and other stats remain numeric primitives rather than player actions. Pufferfish's Unofficial Additions 2.2.8 then adds one exact-current ✅ bridge closure, **`ZERO_SEMANTIC_SKILL_XP_REWARD_BRIDGE` / +0 strict**: exact File `7389968` equality closes three XP sources, one configurable effect reward and Iron's spell/school observer/filter infrastructure without creating a new spell roster. Create: More Automation 0.5.2 then adds one exact-current ✅ processing closure, **`ZERO_SEMANTIC_CREATE_RECIPE_AUTOMATION` / +0 strict**: exact Modrinth `en1TN4J7` equality closes 73 entries / 6 classes / 19 provider-data paths, zero magic-semantic paths, zero player-action overrides and fourteen valid Create/vanilla processing recipes. Create: Ender Transmission 2.1.1 then adds one exact-current ✅ transport closure, **`ZERO_SEMANTIC_REMOTE_TRANSFER_CHUNK_INFRA` / +0 strict**: exact Modrinth `eI9pk5JC` equality closes 107 entries / 32 classes / 14 provider-data paths; transmitter interactions are configuration UI/network endpoints and the chunk loader is kinetic server infrastructure.

The 02/10 semantic-ledger normalization adds **no structural provider directories**: Ars Morph and Woodwalkers SpellBooks were already ✅ cataloged and now contribute +8 and +1 strict respectively; Vampiric Ageing was already ✅ cataloged and now has its nine provider-owned actions explicitly recorded as conditional. The subsequent Protection Pixel closure adds one exact-current ✅ provider with `ZERO_SEMANTIC_TECH_GEAR`; BetterNether then adds one exact-current ✅ `ZERO_SEMANTIC_WORLDGEN_BREWING_EQUIPMENT` provider; Grapplemod Skybound adds one exact-current ✅ `ZERO_SEMANTIC_TRAVERSAL_PHYSICS` provider; Dimensional Sable adds one exact-current ✅ `ZERO_SEMANTIC_DIMENSION_TRANSFER_INFRA` provider; Create Teleporters Remastered then adds one exact-current ✅ `ZERO_SEMANTIC_TECH_TELEPORT_INFRA` provider; Create: Chromatic Return adds one exact-current ✅ `ZERO_SEMANTIC_ENCHANT_GEAR_INFRA` provider; Create: Deep Dark then adds one exact-current ✅ `ZERO_SEMANTIC_PASSIVE_ECHO_GEAR_PROCESSING` provider; Create: Mechanical Spawner adds one exact-current ✅ `ZERO_SEMANTIC_KINETIC_MOB_SPAWN_INFRA` provider; Create: Fantasizing Again then adds one exact-current ✅ `ZERO_SEMANTIC_CREATE_AUTOMATION_TOOLS_INFRA` provider. Structural count therefore becomes **154 = 151 ✅ + 3 ⚠️** after the exact-current Pufferfish's Skills, Pufferfish's Attributes, Pufferfish's Unofficial Additions, Create: More Automation, Create: Ender Transmission, Create Mechanical Companion, Create: Enchantable Machinery, Creating Space, Create: Dreams n' Desires, Epic Fight, Cold Sweat and Create: Cold Sweat closures.

## 30/09 physical-Magic coverage correction

The latest sibling organization is audited by the **category directory** under `PROJECT-INSTRUCTIONS/modlist/`, not by matching the word `Magic` inside a mod name. This matters because names such as `Snow! Real Magic!` are not themselves proof that the dossier belongs to the magic-provider taxonomy.

At sibling `d1659e7abadcf03c386d17b1886a473dc6541195`:

- current physical dossiers whose **category directory** contains `Magic`: **97**;
- mapped into Black Arcana after ownership/alias normalization: **97/97**;
- before this correction: **96/97**;
- sole missing provider: **StarbuncleMania 1.5.8**;
- unmapped rows after materialization: **0**.

StarbuncleMania physical row #527 is `starbunclemania-1.21.1-1.5.8.jar`, mod id `starbunclemania`, runtime `1.5.8`, SHA-1 `6af8bc4f9dc24c9ff4d49367ca37fd914822ceb6`. NON-MERGE PR #476 proved exact equality with publisher File `8778598` and closed exactly two provider-owned Ars glyph identities: `starbunclemania:glyph_place_fluid` and `starbunclemania:glyph_pickup_fluid`.

The previous 84/84 physical-Magic result is preserved as a historical 27/09 checkpoint. The later sibling catalog organization and this stricter taxonomy pass expand the current physical-category subtotal to 97 without implying that all 13 newly surfaced rows are new semantic providers; twelve already mapped to existing Black Arcana ownership records.

## Duplicate resolved

The historical duplicate Vampiric Ageing records remain consolidated:

- canonical: `✅-vampiric-ageing`;
- legacy material: `✅-vampiric-ageing/legacy-vampiricageing/`.

Both identify mod id `vampiricageing`, installed JAR `vampiricageing-1.21-1.4.21.jar`, and the same source lineage. The current **138** count does not reintroduce that duplicate.

## Metric boundary

**164 is not the current technical cross-domain denominator.** It is the current structural count of top-level catalog directories. The historical `68/100` technical-component fraction used a different component model and remains historical; the current technical denominator is still `PENDING REBASE`.

Likewise, **164 is not the semantic-magic denominator**. The current strict reconstructible semantic minimum is **1849**. The prior **1858** checkpoint included Ars Morph (+8) and Woodwalkers SpellBooks (+1); current physical reconciliation excludes both because their JARs are absent from the current snapshot. The cross-domain zero-semantic closures, including the four 06/10 Batch 1 additions, do not change that numerator. Traveloptics and Deeper and Darker retain genuine current-physical/provenance blockers, while Iron's Spellbooks KubeJS is catalog-closed at +0 with deployed-instance parity retained as separate QA.

See [PHYSICAL-MAGIC-RECONCILIATION-2026-10-05.md](./PHYSICAL-MAGIC-RECONCILIATION-2026-10-05.md) for the current snapshot and [PHYSICAL-MAGIC-RECONCILIATION-2026-09-30.md](./PHYSICAL-MAGIC-RECONCILIATION-2026-09-30.md) for the historical StarbuncleMania correction.
