# ShadowsZ — 1.1.9

Status: `✅ CATALOGED / EXACT 1.1.9 SEMANTIC INVENTORY 10 / COMPLETE 10-ROOT OBJECT CATALOG / 9 CORE + 1 FUSION-CONDITIONAL / DEPLOYED ATTUNEMENT POLICY OPEN / +0 STRICT`

> Folder-prefix rule (2026-09-29): **✅ means the current semantic/action denominator is fully cataloged and materialized.** Deployed config, reachability or runtime QA may still keep individual identities conditional or outside the strict numerator; those conditions remain documented here and do not make the folder structurally partial.

## Current physical authority

Current sibling authority at `neoforge-rpg-skilltree@7028524829b5589ee377cd980aa8298cf95cf5c7` records:

- physical row: **#500**;
- JAR: `shadowsz-1.1.9.jar`;
- mod id: `shadowsz`;
- runtime: `1.1.9`;
- physical SHA-1: `f946eb3a8181e1964279f163f430ccbba6c4edcd`;
- category: Addons + Magic + Mobs;
- required host: Iron's Spells 'n Spellbooks `3.16.3`.

The sibling dossier explicitly states that the local ShadowsZ config was not read and that optional systems must not be presumed active.

## Exact publisher artifact closure

Official publisher release:

- CurseForge project `1582485`;
- NeoForge 1.21.1 File `8626238`;
- Modrinth version `Z5VFhs8D`;
- file: `shadowsz-1.1.9.jar`;
- license: All Rights Reserved.

NON-MERGE audit PR **#443** materialized the exact Modrinth publisher artifact and required SHA-1 equality with the physical pack digest before inspection.

Final reinforced audit evidence:

- audit HEAD: `2ea4f054a2cecc487bc27d629824a865a502e4dd`;
- exact audit run: `36430580803` — GREEN;
- audit artifact: `10973381572`;
- audit artifact digest: `sha256:fc7094ce04ef92d420a28fcae4c1c7bb18fa99f77442c59a8a37f1d55925b0d9`;
- downloaded/publisher SHA-1: `f946eb3a8181e1964279f163f430ccbba6c4edcd`;
- physical SHA-1: `f946eb3a8181e1964279f163f430ccbba6c4edcd`;
- exact metadata mod id/version: `shadowsz` / `1.1.9`;
- exact provider classes: **86**.

See [EXACT-1.1.9-ARTIFACT-AUDIT.md](EXACT-1.1.9-ARTIFACT-AUDIT.md).

## Exact semantic denominator

The exact hash-matched artifact closes three unconditional Iron's-spell registrations and the complete player action router.

### Registered Umbral spells

| # | Spell ID | Disposition |
|---:|---|---|
| 1 | `miasma` | semantic root |
| 2 | `umbral_bond` | semantic root |
| 3 | `aura_of_the_monarch` | semantic root |

The registry has exactly **3** spell fields, exactly those **3** IDs, and **0** conditional branches in the spell static registration path.

### Provider supernatural actions

The exact `ShadowActionC2S` router exposes 20 individual action codes and `ShadowGroupC2S` exposes 5 group codes. Implementation-level classification closes the independent supernatural roots as:

| # | Action | Exact evidence | Disposition |
|---:|---|---|---|
| 4 | Shadow Eyes | `toggleShadowEyes` toggles provider supernatural sight state with provider feedback | semantic root |
| 5 | Shadow Arising | `ShadowEvents.tryAbsorb` converts a fallen shadow into owned roster state using Iron's mana/difficulty inputs | semantic root |
| 6 | Summon Shadow | `summon` spends Iron's mana and manifests a stored shadow with provider portal/teleport effects | semantic root |
| 7 | Dismiss Shadow | `dismissInternal` persists current shadow state and demanifests the entity with provider portal/teleport effects | semantic root |
| 8 | Position Swap | `teleportSwap` exchanges player/shadow positions and owns its cooldown | semantic root |
| 9 | Despawn Wild Shadows | `despawnWildShadows` performs player-invoked portal banishment of wild shadow entities | semantic root |
| 10 | Shadow Fusion | `fuseShadows` performs a distinct sacrificial merge and reads `FUSION_ENABLED` | **conditional semantic root** |

Together with the three registered spells, the complete current 1.1.9 semantic denominator is therefore **10 distinct provider-owned supernatural actions**.

## Fichas canônicas

As 10 raízes exatas estão materializadas objeto-a-objeto em [ACTION-CARDS-1.1.9.md](ACTION-CARDS-1.1.9.md). As fichas preservam a distinção entre identidade semântica já fechada e reachability implantado ainda condicionado; nenhuma delas promove o strict sem a evidência exigida em [DEPLOYED-STATE-CHECKLIST.md](DEPLOYED-STATE-CHECKLIST.md).

## Exact exclusions and aliases

The following exact router/control surfaces do **not** mint additional semantic roots under the Black Arcana metric:

- `summonAll`, `dismissAll`, group summon, group dismiss and group hotkey toggle — batch/alias surfaces of Summon/Dismiss;
- attack order — AI command/target management;
- rename, behavior, aggro, slots, pickup toggle, group save/delete — roster/army management;
- permanent release — roster deletion/lifecycle management;
- storage, mount inventory and equipment UI — inventory/gear management;
- spend point, leveling, Progress Mode and title bonuses — progression/stat systems;
- `grantPowers` / `revokePowers` — attunement/admin progression control;
- Umbral school and spell power/resistance — taxonomy/attributes;
- `bindGuardian` — downstream implementation of `umbral_bond`;
- `tryAuraConvert` and Aura helper state — downstream implementation of `aura_of_the_monarch`;
- spawned entities, particles, sounds, buffs, AI state and other downstream consequences — effects, not second action identities.

Shadow Equipment is an optional management system, not a separate supernatural action identity in this ledger.

## Reachability gate — why strict remains +0

Exact artifact guard facts establish that current player-facing power use is attunement-gated:

- all three registered Umbral spells call `ShadowSummoner.isAttuned` in pre-cast validation;
- the player action C2S handler calls `ShadowSummoner.isAttuned` before routing the action surface;
- accepting attunement calls `ModGameRules.canAttune`;
- publisher documentation states that before attunement every ShadowsZ keybind, menu and spell remains inactive;
- publisher documentation states that `/gamerule shadowszRestrictPowers true` restricts power acquisition to operators.

The exact artifact default for `shadowszRestrictPowers` is `false`, but a default is not substituted for the effective deployed world gamerule.

The exact artifact also exposes:

- `fusionEnabled=false` default;
- `equipmentEnabled=false` default;
- `progressMode=true` default;
- `levelingEnabled=true` default;
- `blackTexture=true` default.

Only `fusionEnabled` changes the semantic denominator directly: Fusion is the tenth action and remains conditional until the deployed value is captured. The other booleans control progression/presentation/management systems rather than minting additional semantic roots.

Therefore:

- exact semantic inventory: **10**;
- current strict contribution: **+0**;
- provider catalog state: **✅ cataloged**; deployed reachability remains conditioned;
- closure requires the effective current-world `shadowszRestrictPowers` value and deployed `fusionEnabled` value.

See [DEPLOYED-STATE-CHECKLIST.md](DEPLOYED-STATE-CHECKLIST.md).

## Ownership boundary

- ShadowsZ owns attunement, Shadow Eyes/Arising, roster/lifecycle, Summon/Dismiss, Position Swap, Despawn Wild, Fusion and the three Umbral spell identities.
- Iron's Spells owns host mana, generic spell infrastructure and spell-runtime contracts.
- External mob mods retain authority for their own entity/boss semantics.
- Black Arcana must not duplicate ShadowsZ roster, persistence, mana settlement, teleport execution, Fusion settlement or Umbral spell execution.
- RPG Skill Tree remains sibling authority only for progression/attributes/Mastery/perks/gates exposed through real contracts.

## Runtime QA remains separate

Catalog denominator closure does not certify:

- dedicated-server compatibility with Iron's 3.16.3;
- roster/storage persistence;
- chunk-ticket cleanup;
- Position Swap destination safety;
- multiplayer ownership isolation;
- modded-boss conversion;
- exactly-once loot/XP/state settlement;
- Fusion atomicity when enabled;
- performance with large shadow armies.

## Result

**✅ Catalog complete — exact 10-root inventory closed; deployed attunement/Fusion state remains conditional.**

Current exact semantic inventory: **10 provider-owned supernatural action identities**.

Strict global delta remains **+0** until effective deployed attunement/restriction policy and Fusion state are captured.