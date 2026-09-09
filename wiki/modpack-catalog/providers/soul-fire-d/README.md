# Soul Fire'd 6.1.0

Status: `EXACT PHYSICAL VERSION + EXACT OFFICIAL SOURCE VERSION / PROMETHEUS-BACKED SOUL-FIRE CONTENT PROVIDER / 0 SPELLS / 0 MIXINS / 2 ENCHANTMENTS / 1 FIRE TYPE + ASSOCIATED FIRE CHARGE / LICENSE-METADATA CONFLICT + FULL-PACK QA FAIL-CLOSED`

## Installed identity

- physical JAR: `soul-fire-d-neoforge-1.21-6.1.0.jar`
- mod id: `soul_fire_d`
- runtime version: `6.1.0`
- Minecraft: `1.21` / `1.21.1`
- loader: NeoForge
- physical SHA-1: `877002a5aa386f9011ebc4eb3360a7647ac359d9`
- CurseForge project/file: `662413 / 7364962`
- exact official source branch: `Crystal-Nest/soul-fire-d:1.21`
- exact source revision: `0cc7a03b950e74742eb75f51642cc7a0190c7127`

The physical modlist/JAR metadata is authority for installed presence/version/hash. The exact publisher file independently matches the installed filename and supports Minecraft 1.21/1.21.1 on NeoForge.

## Provider role after 6.0.0

Soul Fire'd must not be cataloged as the owner of a generic custom-fire framework on the installed 6.x line.

The project moved that API to **Prometheus** in 6.0.0+. The exact 6.1.0 source consumes:

- `it.crystalnest.prometheus.api.Fire`;
- `FireManager`;
- `FireRegistrar`.

The physical pack contains exact dependency versions used by this source line:

- Cobweb `1.4.0`;
- Prometheus `1.2.5`.

Therefore the authority split is:

- **Prometheus 1.2.5**: generic fire-type/component registration/runtime API;
- **Soul Fire'd 6.1.0**: the Soul Fire definition/content, its associated charge, enchantments, static datapack, loot acquisition and player-facing Soul Fire behavior;
- **Black Arcana**: BA casting, spell domains, hazards, costs, cooldowns/charges, targeting, Corruption, Strain, Arcane Danger, Backlash and `WorldEffectPolicy`.

## Exact source initialization surface

`CommonModLoader.init()` performs exactly two high-level operations:

1. loads `FireRegistry`, which registers the Soul Fire definition through Prometheus;
2. registers a Cobweb `StaticDataPack` named `soul_fire_d:enchantments` at `Pack.Position.TOP`.

The NeoForge `ModLoader` then registers Soul Fire'd's global-loot-modifier serializer.

The exact common and NeoForge mixin manifests both have empty `mixins`, `client` and `server` arrays. Current exact mixin count is therefore **0**, despite the physical metadata correctly listing the two empty config files.

## Exact Soul Fire definition

The source reuses `FireManager.SOUL_FIRE_TYPE`, which exact Prometheus 1.2.5 defines as `minecraft:soul`.

Soul Fire'd registers that fire through `FireManager.fireBuilder(...)` with:

- Prometheus default components;
- vanilla `minecraft:soul_fire_flame` particle;
- light level `10`;
- damage value `2`;
- associated fire-charge registration via `FireRegistrar.registerFireCharge(...)`.

Exact Prometheus 1.2.5 owns the generic registration helper and derives component registries from the fire type. Soul Fire'd supplies the Soul Fire-specific registration request; it does not own the generic framework.

The source resources and recipe resolve the associated item as `minecraft:soul_fire_charge`; the recipe produces 16 from gunpowder + ghast tear + coal/charcoal.

## Exact enchantment surface

The built-in static datapack contains exactly two enchantment definitions:

1. `minecraft:soul_fire_aspect`
2. `minecraft:soul_flame`

Both use the Prometheus `prometheus:ignite` effect with `fire_type: "soul"`.

`Soul Fire Aspect`:

- max level 2;
- direct post-attack victim effect;
- duration expression base `4.0`, plus `4.0` per level above first; no unit is inferred beyond the exact provider data/API contract;
- exclusive set `#prometheus:exclusive_set/fire_aspect`;
- supported items `#minecraft:enchantable/fire_aspect`.

`Soul Flame`:

- max level 1;
- projectile-spawned ignition;
- duration `100.0` in the exact effect JSON;
- exclusive set `#prometheus:exclusive_set/flame`;
- supported items `#minecraft:enchantable/bow`.

These are enchantments, not Black Arcana spells, and they do not enter BA's casting pipeline.

## Loot surface

NeoForge registers one provider-owned global loot modifier serializer:

- `soul_fire_d:chest_loot_modifier`.

The bundled `bastion_other_loot_modifier.json` targets `minecraft:chests/bastion_other` and independently gives:

- `minecraft:soul_fire_aspect` level 1 enchanted book: `0.05` chance;
- `minecraft:soul_flame` level 1 enchanted book: `0.05` chance.

The modifier clamps requested enchantment level to the enchantment's actual max level before creating the book.

## Semantic inventory result

For the exact 6.1.0 source ceiling:

- standalone spells: **0**;
- glyphs: **0**;
- rituals: **0**;
- provider mana/resource/cast pipeline: **0**;
- provider mixins: **0**;
- Soul Fire definitions supplied to Prometheus: **1** (`minecraft:soul`);
- associated Soul Fire charge: **1** (`minecraft:soul_fire_charge`);
- enchantments: **2**;
- NeoForge global-loot-modifier serializers: **1**.

No count above transfers Prometheus framework ownership to Soul Fire'd, and none should be inflated into a Black Arcana spell count.

## Black Arcana disposition

Black Arcana must not:

- recreate Prometheus's generic fire-type/component framework;
- duplicate Soul Fire'd's Soul Fire registration or enchantment datapack;
- treat `minecraft:soul_fire_aspect` / `minecraft:soul_flame` as BA spells;
- bypass BA `WorldEffectPolicy` merely because a provider fire type exists;
- infer that generic fire damage or an enchantment proc is BA Backlash/casting causality;
- route BA Backlash into normal offensive proc chains solely to trigger provider enchantment behavior;
- transfer magic runtime authority to RPG Skill Tree.

A future BA fire-domain or hazard integration may consume a **verified current Prometheus/provider boundary**, but BA remains authority over its own spell/hazard creation, bounded world effects, costs, targeting, cooldowns and safety policy.

## Catalog files

- [FIRE-RUNTIME-AND-AUTHORITY.md](FIRE-RUNTIME-AND-AUTHORITY.md)
- [ENCHANTMENTS-LOOT-AND-DATA.md](ENCHANTMENTS-LOOT-AND-DATA.md)
- [EVIDENCE-AND-PROVENANCE.md](EVIDENCE-AND-PROVENANCE.md)

## Evidence ceiling / QA

Closed semantically from exact evidence:

- physical 6.1.0 identity/hash;
- exact publisher 1.21 NeoForge file;
- exact source-version pin;
- exact dependency baselines and physical dependency match;
- generic-fire authority migration to Prometheus;
- exact Soul Fire registration values;
- exact two enchantment definitions;
- exact NeoForge loot-modifier serializer/data;
- exact zero-mixin result.

Still fail-closed:

- byte-for-byte source/JAR reproducibility;
- full-pack Soul Fire behavior against every other fire/combat mod;
- dedicated multiplayer regression of provider interactions;
- compatibility claims for optional integrations not proven from exact hooks in this phase;
- source-vs-publisher license metadata reconciliation for any reuse beyond factual interoperability analysis.
