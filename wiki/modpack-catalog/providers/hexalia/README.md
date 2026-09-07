# Hexalia — filename/source release 1.3.6, installed runtime metadata 1.3.5

## Status

`EXACT PUBLIC NEOFORGE RELEASE 1.3.6 / SOURCE-PINNED RELEASE COMMIT 4952c652 / MIT / PHYSICAL FILENAME 1.3.6 / INSTALLED RUNTIME METADATA 1.3.5 / SOURCE CATALOG ADVANCED / EXACT INSTALLED-JAR EQUIVALENCE + RUNTIME QA PENDING`

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

with message `Release Hexalia 1.3.6`, also dated 2026-08-16. At that pin:

- `gradle.properties` declares `mod_version=1.3.6` and `minecraft_version=1.21.1`;
- NeoForge metadata declares `license = "MIT"`, `modId = "hexalia"` and `version = "${version}"`.

Therefore source inspection for **release-line cataloging** is permitted under the publisher's MIT declaration and is pinned to this exact commit. No upstream code/assets are copied or adapted into Black Arcana.

### Important equivalence limitation

The public release filename and source pin both say `1.3.6`, while the installed JAR reports runtime `1.3.5`. That discrepancy prevents a stronger claim that the installed binary is byte-for-byte/metadata-equivalent to the pinned 1.3.6 source build.

Consequently:

- source-derived registry/data/behavior facts below are `SOURCE-PINNED 1.3.6`;
- installed presence/filename/runtime remain `MODLIST-PINNED`;
- where the two materially affect an integration contract, **runtime/artifact QA is still required** before promotion to exact installed-runtime behavior.

## Documentation freshness

The official GitHub Wiki currently identifies its supported version as `1.3.3`. It remains useful for player-facing concepts, but source/data at the `1.3.6` release pin and the 1.3.6 publisher changelog take precedence for version-specific facts.

The 1.3.6 publisher changelog specifically records:

- Mortar & Pestle/Pestle texture fix;
- Bone Meal duplication fix for magical herbs;
- Lotus Flower duplication fix;
- missing translation/message keys;
- missing Mortar & Pestle recipes added to Verdant Grimoire;
- Ritual Brazier recipe reference fix in Verdant Grimoire;
- Nature's Ritual nearby-crop requirement made configurable from 0–32, default 8.

## Core witchcraft loop

Hexalia owns a preparation-first witchcraft loop rather than an instant spellbook loop:

1. acquire magical herbs/materials;
2. refine ingredients, including Mortar & Pestle paths;
3. prepare Small Cauldron, Nature's Ritual or Celestial Infusion content;
4. satisfy provider environmental/equipment conditions;
5. receive a provider-owned brew, ritual output, node, item or equipment effect.

Black Arcana must integrate around that identity rather than reproducing it as an instant cast system.

## Small Cauldron behavior

Official Verdant Grimoire documentation establishes the preparation model:

- fill with water;
- heat from below;
- add ingredients;
- stir with a Ladle to begin cooking;
- heat must remain present;
- invalid combinations can create a **Spoiled Mixture** with harmful/corrupted consequences;
- overcooking reduces yield;
- timing/preparation are part of the mechanic.

Exact 1.3.6 implementation details may be cataloged from the pinned MIT source, but exact installed-JAR behavior remains QA-sensitive because of the runtime-version mismatch.

## Source-pinned 1.3.6 brew catalog

The pinned 1.3.6 source/generated data expose the following eight capability-bearing brews. Their registry/data identity is source-pinned; pack-runtime equivalence is not yet promoted beyond the mismatch gate.

| ID / name | Source-pinned preparation | Source/public behavior | Dedup impact |
|---|---|---|---|
| `hexalia:brew_of_arachnid_grace` — Arachnid Grace | Spider Eye + Ghost Powder + Black Dye + String; Small Cauldron | wall-climb-oriented brew; poison protection/removal and water/rain drawback are part of provider behavior | blocks generic witch wall-climb/poison-protection brew clones |
| `hexalia:brew_of_bloodlust` — Bloodlust | Mandrake + Spirit Powder + Tree Resin + Rotten Flesh | offensive/life-restoration brew with regeneration suppression in the provider surface | overlaps offensive/lifesteal blood-adjacent witch brews; **not** a blood reservoir resource |
| `hexalia:brew_of_daybloom` — Daybloom | Sunfire Tomato + Spirit Powder + Glow Berries + Witchweed | sunlight-dependent healing/mobility behavior; source pin contains quantitative logic, runtime equivalence pending | blocks generic sunlight-heal/speed potion clones |
| `hexalia:brew_of_hollow_silence` — Hollow Silence | Feather + Ghost Powder + Chillberries + Sculk | provider documentation describes reduced/silenced presence around sound-sensitive entities with vision drawback; exact event path remains an integration QA item | blocks generic sound-stealth witch brew only at provider semantic level |
| `hexalia:brew_of_homestead` — Homestead | Tree Resin + Ender Pearl + Spirit Powder + Galeberries | one-shot safe-return/home teleport consumable with post-teleport nausea/confusion behavior in the source/public surface | blocks generic witch return-home potion |
| `hexalia:brew_of_siphon` — Siphon | Dream Paste + Siren Paste + Iron Ingot + Redstone | mining/item-attraction-oriented brew with provider exhaustion/tradeoff surface | blocks generic magnetic/item-siphon witch brew clones |
| `hexalia:brew_of_slimewalker` — Slimewalker | Slime Ball + Chillberries + Tree Resin + Feather | fall/bounce traversal brew with movement tradeoff | blocks generic fall/bounce witch brew clones |
| `hexalia:brew_of_spikeskin` — Spikeskin | Celestial Crystal + Iron Nugget + Sweet Berries + Tree Resin | armor/retaliation-oriented brew with movement penalty | blocks generic thorns/armor witch brew clones |

The generated item tag and registry/data surfaces at the release pin support these brew identities. Quantitative formulas may be retained in granular source-audit notes when needed, but they are not treated as exact installed-runtime acceptance evidence until the 1.3.6/1.3.5 discrepancy is resolved.

## Related capability-bearing preparations

The source/public provider surface also contains:

- `Brambleguard Salve` — defensive salve surface, including resistance/Bleeding interaction;
- `Mender's Salve` — healing/regeneration consumable;
- `Bleeding` — provider harmful effect;
- `Overfed` — saturation/movement tradeoff effect;
- `Stunned` — harmful control/immobilization effect.

These remain Hexalia-owned effects, not Black Arcana status channels.

## Nature's Ritual — source-pinned release-line outputs

Generated data at the 1.3.6 pin expose `hexalia:natures_ritual` recipes whose player-facing outputs include:

- `Aegiflora`;
- `Astrylis`;
- `Grimshade`;
- `Lourdes`;
- `Morphora`;
- `Nautilite`;
- `Windsong`;
- `Air Node`;
- `Earth Node`;
- `Fire Node`;
- `Water Node`;
- `Rootshaper`;
- `Kelpweave Blade`;
- `Rabbage Seeds`;
- Bloomwrap armor pieces.

`debug_natures_ritual` is excluded from player-facing catalog counts.

The 1.3.6 changelog additionally proves that the nearby-crop requirement is configurable from `0–32`, default `8`.

Exact ingredient/output semantics should live in the ritual subcatalog rather than being inferred from display names.

## Celestial Infusion — source-pinned provider surface

Pinned source/data and provider documentation expose Celestial Infusion outputs including:

- Celestial Crystal;
- Galeberries;
- Moonweave Hood;
- Moonweave Mantle;
- Moonweave Bindings;
- Moonweave Footwraps.

This is real overlap with celestial presentation but does not make Hexalia a Holy/Iron's-style spell school. Any future Black Arcana Divine/Celestial design must remain semantically distinct from this existing lunar/celestial witchcraft preparation path.

## Deduplication consequences

### Witchcraft

Black Arcana Witchcraft must **integrate, not replace**, Hexalia's:

- cauldron brewing;
- herbs/material preparation;
- provider brews and salves;
- Nature's Ritual;
- Celestial Infusion;
- Mortar & Pestle processing;
- provider mutations/transformations;
- nodes/idols where mechanically relevant.

A future Black Arcana recipe may require or transform a real Hexalia preparation only through a verified boundary; it must not silently recreate the same result as a generic spell.

### Blood / Binding

`Brew of Bloodlust` is blood-themed but is **not** evidence of blood-volume storage, an external blood reservoir, blood-link authority or blood-only casting settlement. It does not occupy the planned Hematic Reservoir / typed blood-binding architecture.

### Divine / Celestial

`Daybloom` and Celestial Infusion create genuine solar/celestial overlap. Divine/Celestial identity must therefore be Holy/miracle/authority-oriented rather than merely “sun-powered buff” or celestial crafting.

### Order / Chaos

No audited Hexalia surface currently proves Black Arcana's proposed server-authoritative imposed-law or causal/probability mechanics. Individual rituals still require semantic review before those gaps can be declared free.

## Acquisition / learning authority

Hexalia progression is provider-owned through its Verdant Grimoire, recipes, advancements and preparation systems. Brews are prepared with actual ingredients/Small Cauldron rules; they are not learned as Iron's scrolls. Nature's Ritual and Celestial Infusion likewise remain provider-owned preparation systems.

## Safe integration posture

- No second Hexalia recipe engine.
- No second registry of brew effects.
- No re-settlement of a provider ritual/world mutation.
- No Mastery by continuous proximity to a node/ritual.
- Any progression event requires discrete causal evidence and deduplication.
- Source pin authorizes factual cataloging, not copying upstream code/assets into Black Arcana.
- Any provider-specific adapter must still identify a stable API/hook; source class visibility alone is not a supported integration contract.

## Open audit items

1. reconcile exact installed-JAR identity against public File ID `8658488` and explain why runtime metadata reports `1.3.5`;
2. enumerate every 1.3.6 Nature's Ritual recipe with exact inputs/output and mark which are runtime-sensitive;
3. enumerate every 1.3.6 Celestial Infusion recipe;
4. enumerate Mortar & Pestle transformations relevant to magic/deduplication;
5. trace Hollow Silence's event path and determine whether a stable public hook exists;
6. catalog mutation mechanics and capability-bearing idols/nodes;
7. identify supported integration/API surfaces rather than coupling to implementation classes;
8. perform exact pack runtime QA before promoting source-derived formulas to installed-runtime facts.

## Phase 3 gate

Hexalia is now **source-pinned at the public 1.3.6 release line**, but implementation is still `BLOCKED` until semantic coverage is complete and the installed `1.3.6 filename / 1.3.5 runtime` discrepancy is resolved for any integration contract that depends on exact binary behavior.