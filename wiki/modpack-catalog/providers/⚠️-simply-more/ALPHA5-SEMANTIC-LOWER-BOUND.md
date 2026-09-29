# Simply More 1.3.0 Alpha 5 — historical release-correlated semantic lower bound

Checkpoint: 2026-09-27

> **SUPERSEDED FOR CURRENT DENOMINATOR PURPOSES.** The exact physical-artifact audit in [EXACT-ALPHA5-ARTIFACT-AUDIT.md](EXACT-ALPHA5-ARTIFACT-AUDIT.md) closes the current Simply More action denominator at **24** while deployed reachability remains open. This file is retained as provenance for the earlier conservative 9-action lower bound.

## Evidence class

`HISTORICAL / EXACT_PHYSICAL_PUBLISHER_FILE / RELEASE_CORRELATED_SOURCE / LOWER_BOUND 9 PLAYER_ACTIONS / SUPERSEDED BY EXACT CURRENT DENOMINATOR 24`

## Metric boundary

The canonical semantic-magic ledger counts one discrete provider-owned magical action identity only when it is a standalone spell, glyph primitive, ritual/rite, or equivalent **player-invoked supernatural action**.

It excludes items, gear, equipment proc frameworks, passive gear effects, status/effect machinery and downstream consequences.

This boundary is decisive for Simply More: passive on-hit mechanics and weapon implicits are documented provider behavior, but they are not added to the semantic action count.

## Physical / publisher authority

Sibling physical row #502 at
`neoforge-rpg-skilltree@51d590653d927538f23ba6f1643576dc6cc49859`:

- physical JAR: `simplymore-forge-1.3.0_alpha.jar`;
- mod id: `simplymore`;
- runtime: `1.3.0_alpha`;
- SHA-1: `51636477cd5c378f42d9700e1fe35cd952c8f4f1`.

The sibling dossier reconciles that SHA-1 to CurseForge File `8736778`:

- publisher title: Simply More 1.3.0 ALPHA 5;
- NeoForge 1.21.1;
- publisher filename: `simplymore-neoforge-1.3.0_alpha5+1.21.1.jar`;
- embedded/file name reported by publisher: `simplymore-forge-1.3.0_alpha.jar`;
- upload date: 2026-08-26.

Alpha 5 contains crash fixes and does not claim a wholesale ability rewrite relative to the initial 1.3 Alpha line.

## Initial Alpha semantic boundary

The initial 1.3 Alpha release explicitly states that some uniques marked for rework had functionality removed and could currently do nothing. It also introduces weapon-type implicits and limits new Iron's Spellbooks compatibility to reworked uniques.

Consequently:

- 10 weapon types are not 10 semantic actions;
- 33 Unique Weapons are not 33 semantic actions;
- item registry presence cannot prove a live player action;
- passive/proc behavior is not counted by the semantic-magic metric;
- reworked/current active surfaces can provide a positive lower bound without implying completeness.

## Release-correlated source

Source checkpoint:
`jay-jay0101/Simply-More@55977c5e6a4fdaf4281781d9c4475a52286b3184`.

Reason for correlation:

- commit date: 2026-08-26;
- follows the dedicated-server registration fixes;
- precedes the later September development series;
- source still declares `1.3.0_alpha` / Minecraft 1.21.1;
- changed surfaces include client/server separation and Soulfracture/Blade-of-the-Grotesque-adjacent crash-sensitive paths consistent with Alpha-5 release notes.

No physical-JAR ↔ source-build byte-equality claim is made.

## Nine confirmed player-invoked roots

Publisher Alpha notes and release-correlated source positively establish player-invoked active ability surfaces for these nine current/reworked families:

| # | Unique | Countable player action |
|---:|---|---|
| 1 | Magmaseep | Volcanic Vent |
| 2 | Moundshifter | excavation/drill activation |
| 3 | Grandfrost | Snow Prison |
| 4 | Lustrous Moxie | Heavensent Ray |
| 5 | Soulfracture | fragment-control activation |
| 6 | Black Pearl | cannonball activation |
| 7 | The Blood Harvester | Harvest activation |
| 8 | Ruyi Jingu Bang | charged enlarged strike |
| 9 | Blade of the Grotesque | statue transformation |

Conservative rule: multiple consequences or follow-up modes inside one activation remain one causal action root unless a separate player invocation is independently established.

Semantic lower bound: **9**.

## Provider behavior documented but excluded

### Reworked-Unique passive/proc surfaces

The same nine families also expose passive/on-hit/aura behavior. These are equipment/passive proc mechanics rather than player-selected supernatural actions and are excluded from the semantic count.

### Weapon implicits

`ImplicitRegistry` defines four Simply More-owned implicits:

- `simplymore:grandsword_sunder`;
- `simplymore:friendship`;
- `simplymore:disarm`;
- `simplymore:stun`.

Other Simply More weapon types route to existing Simply Swords definitions or reuse the same Simply More implicit root.

All four remain **+0 semantic** under the current metric because they are weapon/equipment proc mechanics.

## Explicit non-promotions

Not counted yet:

- older/legacy active uniques not included in the positive rework set;
- incomplete/rework placeholders;
- deprecated/removed redirect items;
- Mimicry forms as separate actions;
- passive/proc behavior;
- effects, entities, HUD states, cooldowns and components;
- Simply Swords-owned implicits reused by Simply More;
- Iron's Spellbooks scaling/compatibility as separate provider actions;
- Reforming Remnant without further player-action classification.

The source contains examples of unfinished/inert surfaces, so the remaining inventory must be classified object-by-object.

## Clean-room boundary

Upstream license is All Rights Reserved.

Only public factual metadata, names/IDs, behavior-level semantics, source structure and causal ownership are retained for catalog/interoperability purposes.

## Result

- physical/publisher artifact identity: **closed**;
- release-correlated source checkpoint: **established**;
- confirmed semantic lower bound: **9 player-invoked actions**;
- documented excluded provider surfaces: **9 passive/proc surfaces + 4 implicits**;
- complete Alpha-5 active-action denominator: **open**;
- strict contribution: **+0**;
- provider status: **⚠️**.