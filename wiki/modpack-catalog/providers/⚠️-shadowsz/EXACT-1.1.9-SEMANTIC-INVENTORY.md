# ShadowsZ 1.1.9 — Exact Semantic Inventory

Status: `EXACT PHYSICAL=PUBLISHER ARTIFACT / SEMANTIC DENOMINATOR 10 / 9 COUNTED_EXACT + 1 CONDITIONAL`

## Authority

- current physical row: #500;
- physical JAR: `shadowsz-1.1.9.jar`;
- physical SHA-1: `f946eb3a8181e1964279f163f430ccbba6c4edcd`;
- latest sibling revalidation: `neoforge-rpg-skilltree@7028524829b5589ee377cd980aa8298cf95cf5c7`;
- NON-MERGE exact-artifact PR: #443;
- final audit HEAD: `9628dc7d90f17afbac94372a52cd704740473e86`;
- exact audit run: `36422402267` — GREEN;
- audit artifact: `10970337207`;
- artifact digest: `sha256:aebc421c6f4855e84abb5be6e5442d9cb3f4089093fe7fdbf1595b075bfeba3c`;
- publisher artifact source: Modrinth version `Z5VFhs8D`;
- downloaded SHA-1 = physical SHA-1.

CurseForge independently identifies NeoForge 1.21.1 File `8626238` as ShadowsZ 1.1.9.

## Clean-room boundary

ShadowsZ is All Rights Reserved. The audit retained only bounded interoperability/catalog facts:

- hashes and metadata;
- archive/class/resource identities;
- localization keys;
- signature/constant facts;
- exact C2S action codes and case→method routing;
- exact spell registration IDs;
- bounded method call/field/string sets needed to distinguish semantic roots from aliases/management.

The audit does not retain the JAR, protected assets, localization prose wholesale, full bytecode disassembly or decompiled method bodies.

## Exact spell registry

`ModSpells` closes exactly three registrations:

1. `miasma`
2. `umbral_bond`
3. `aura_of_the_monarch`

Registry initializer branch count: **0**.

## Exact player-action surface

`ShadowActionC2S` exposes 20 exact action codes:

- SUMMON
- DISMISS
- RENAME
- BEHAVIOR
- REMOVE
- TELEPORT
- ASSIGN_SLOT
- TOGGLE_SLOT
- TOGGLE_EYES
- ATTACK_TARGET
- DISMISS_ALL
- OPEN_STORAGE
- TOGGLE_PICKUP
- SUMMON_ALL
- AGGRO
- SPEND_POINT
- DESPAWN_WILD
- OPEN_MOUNT
- FUSE
- OPEN_EQUIPMENT

`ShadowGroupC2S` exposes five exact codes:

- SAVE
- DELETE
- SUMMON
- DISMISS
- TOGGLE

Additional player-facing C2S surfaces include attunement choice and party management. Shadow Arising is reached through direct entity interaction rather than a dedicated C2S action code.

## Semantic classification

| Root | Exact disposition | Reason |
|---|---|---|
| Shadow Eyes | `COUNTED_EXACT` | provider-native supernatural sensing toggle |
| Shadow Arising | `COUNTED_EXACT` | mana/difficulty-based conversion of fallen shadow into owned shadow |
| Position Swap | `COUNTED_EXACT` | explicit player↔shadow teleport action |
| Summon Shadow | `COUNTED_EXACT` | spends Iron's mana and manifests stored shadow with portal/teleport effects |
| Dismiss Shadow | `COUNTED_EXACT` | persists summoned entity state and demanifests it with portal/teleport effects |
| Banish Wild Shadows | `COUNTED_EXACT` | player-invoked portal banishment of wild shadows |
| Miasma | `COUNTED_EXACT` | exact provider spell registration |
| Umbral Bond | `COUNTED_EXACT` | exact provider spell registration |
| Aura of the Monarch | `COUNTED_EXACT` | exact provider spell registration |
| Shadow Fusion | `CONDITIONAL` | exact player action exists but reads `FUSION_ENABLED`; deployed value unavailable |

## Aliases and non-semantic controls

Not counted as additional roots:

- Summon All, group summon and summon hotkeys — aliases/batching of Summon Shadow;
- Dismiss All, group dismiss and group hotkeys — aliases/batching of Dismiss Shadow;
- attack order/stand-down — AI command;
- rename, behavior, aggro stance, pickup, slots/groups — roster/AI management;
- permanent release — roster deletion;
- storage/mount/equipment screens — inventory/UI;
- level-point spending, titles, Progress Mode — progression/stat state;
- attunement acceptance — one-time consent/gate;
- party controls — social grouping;
- admin commands — administration;
- `bindGuardian` — downstream Umbral Bond behavior;
- `tryAuraConvert` — downstream Aura of the Monarch behavior.

## Config/gamerule facts

Exact Boolean defaults:

- `progressMode=true`
- `levelingEnabled=true`
- `blackTexture=true`
- `fusionEnabled=false`
- `equipmentEnabled=false`

Exact gamerule default:

- `shadowszRestrictPowers=false`

No provider Boolean enable field exists for the nine strict-counted roots.

## Result

Exact semantic denominator: **10**

- strict: **9 `COUNTED_EXACT`**
- conditional: **1 Shadow Fusion**
- strict delta: **+9**
- remaining catalog gate: deployed `fusionEnabled`
