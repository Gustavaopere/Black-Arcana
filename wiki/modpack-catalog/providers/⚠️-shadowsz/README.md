# ShadowsZ — 1.1.9

Status: `⚠️ PARTIAL / PHYSICAL IDENTITY CLOSED / PUBLISHER LOWER BOUND 6 / COMPLETE ACTION INVENTORY OPEN / +0 STRICT`

## Current physical authority

- sibling checkpoint: `neoforge-rpg-skilltree@ac23fc1c67937deeffe982ae971c21d4f3561bc5`;
- physical row: `#500`;
- JAR: `shadowsz-1.1.9.jar`;
- mod id: `shadowsz`;
- runtime: `1.1.9`;
- physical SHA-1: `f946eb3a8181e1964279f163f430ccbba6c4edcd`;
- required host: Iron's Spells 'n Spellbooks `3.16.3`.

## Exact publisher release line

Current official CurseForge project:

- project: `ShadowsZ`;
- project ID: `1582485`;
- license: All Rights Reserved;
- environment: Client & Server;
- current NeoForge 1.21.1 file: `shadowsz-1.1.9.jar`;
- current NeoForge file ID: `8626238`;
- upload date: 2026-08-11;
- publisher size: 247.9 KB;
- release type: Release.

Official project:
`https://www.curseforge.com/minecraft/mc-mods/shadowsz`

Exact NeoForge 1.21.1 file:
`https://www.curseforge.com/minecraft/mc-mods/shadowsz/files/8626238`

The physical filename/runtime line matches the publisher release line, but this audit has not established physical-JAR ↔ publisher-JAR byte equality. No matching public source repository was identified during this audit. Therefore no `COUNTED_EXACT` or source-pinned completeness claim is made.

## Confirmed publisher lower-bound actions

The current official project description documents six player-facing supernatural actions with distinct causal identities:

| # | Provider action | Surface | Semantic disposition |
|---:|---|---|---|
| 1 | Shadow Eyes | keybind reveals nearby fallen-entity shadows | confirmed lower-bound action |
| 2 | Shadow Arising | player attempts to raise/claim a fallen shadow, using current Mana/target difficulty | confirmed lower-bound action |
| 3 | Position Swap | player instantly exchanges position with one owned shadow, subject to cooldown | confirmed lower-bound action |
| 4 | Miasma | Umbral spell | confirmed lower-bound spell |
| 5 | Umbral Bond | Umbral spell binding a shadow as guardian to another creature | confirmed lower-bound spell |
| 6 | Aura of the Monarch | Umbral spell | confirmed lower-bound spell |

The Umbral school and its spell-power/resistance attributes are taxonomy/stat infrastructure and are not counted as additional actions.

Current semantic evidence therefore establishes:

- **3 named provider-owned Umbral spells**;
- **3 additional publisher-documented supernatural player actions**;
- **lower bound = 6**;
- **strict contribution = +0** until the complete current 1.1.9 inventory and active-surface gates are closed.

## Controls intentionally not promoted yet

The same publisher documentation exposes additional player controls/systems, but this catalog does not currently promote them into the semantic lower bound without implementation-level classification:

- attack-order hotkey;
- Summon All;
- Dismiss All;
- Despawn Wild Shadows;
- individual summon hotkeys;
- group summon/dismiss hotkeys;
- army behavior/stance controls;
- permanent release;
- Shadow Fusion;
- Shadow Equipment;
- Progress Mode/title progression;
- Claiming/accepting the power itself.

Reasons differ by surface:

- some are roster/army-management controls rather than independent supernatural abilities;
- some are progression/config state;
- Fusion, Equipment and Progress Mode are documented as optional/off by default;
- the publisher states that major systems can be switched on/off through config;
- exact implementation/registry ownership is not available from a matching public source.

Admin commands such as `/shadowsz grant`, `revoke`, `levelplayer` and `levelshadows` are administrative tooling and excluded from semantic action counting.

## 1.1.9 release delta

The exact 1.1.9 publisher changelog documents fixes/compatibility for:

- shadow texture/rank coloration;
- max shadow count config;
- semi-compatibility with Bosses Rise, Monster Expansion, Mowzie's Mobs and L_Ender's Cataclysm;
- optimization;
- inventory-button incompatibility;
- Tyros;
- RestrictPowers/revoke tools;
- vanilla mob transforms;
- Maledictus grab;
- Frostmaw friendly freeze.

That changelog does **not** provide a complete semantic registry. It cannot be used to prove that the six confirmed actions are the only actions in 1.1.9.

## Ownership boundary

- ShadowsZ owns Shadow Eyes/Arising, its army/roster/storage/progression state, Position Swap, Umbral integration and provider-native actions.
- Iron's Spells owns host mana, spell infrastructure and generic spell-runtime contracts.
- External mob mods retain authority for their own entity/boss semantics.
- Black Arcana must not duplicate ShadowsZ roster, shadow lifecycle, mana settlement, teleport execution or Umbral spell execution.
- RPG Skill Tree remains sibling authority only for progression/attributes/Mastery/perks/gates exposed through verified contracts.

## Current config uncertainty

The official description states that major systems are configurable and specifically documents toggles/options for progression, fusion, equipment and Progress Mode plus numerical settings for arising, mana difficulty/cost, teleport cooldown and related surfaces.

The deployed pack config has not been authoritatively read in this catalog closure. Therefore the current **active** semantic surface remains fail-closed even for documented actions where config can alter reachability/availability.

## Closure gate

Promote ShadowsZ beyond `LOWER_BOUND 6 / +0 STRICT` only after authoritative evidence closes both:

1. **complete 1.1.9 action inventory**
   - exact matching public source;
   - exact legally inspectable physical/publisher artifact facts;
   - or deterministic complete assembled registry/action evidence;

2. **effective active-surface state**
   - deployed config/gamerules where they can disable or materially gate provider actions.

The closure must separately classify:

- Umbral spells;
- supernatural keybind/actions;
- army-management controls;
- optional progression systems;
- admin commands;
- passive/stat/title effects;
- downstream shadow/entity behavior.

## Runtime QA remains separate

Catalog evidence does not certify:

- dedicated-server compatibility with Iron's 3.16.3;
- roster/storage persistence;
- chunk-ticket cleanup;
- Position Swap safety;
- multiplayer ownership isolation;
- modded-boss conversion;
- exactly-once loot/XP/state settlement;
- performance with large shadow armies.

## Result

**⚠️ Partial — publisher-bounded lower bound 6.**

Confirmed current-version semantic lower bound: **6 provider-owned supernatural player actions**, including three Umbral spells.

Strict global delta: **+0** until exact-current completeness and active-state gates are closed.
