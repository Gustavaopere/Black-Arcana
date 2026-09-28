# Simply More 1.3.0 Alpha 5 — release-correlated semantic lower bound

Checkpoint: 2026-09-27

## Evidence class

`EXACT_PHYSICAL_PUBLISHER_FILE / RELEASE_CORRELATED_SOURCE / LOWER_BOUND 22 / LEGACY_INVENTORY_OPEN`

## Physical / publisher authority

Sibling physical row #502 at
`neoforge-rpg-skilltree@107ce395d9b37f908ad0ba39ef6ea6a01e5f27b2`:

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

Alpha 5 itself contains three crash fixes and does not claim a wholesale ability rewrite relative to Alpha 4.

## Initial Alpha semantic boundary

The initial 1.3 Alpha release explicitly states that some uniques marked for rework had functionality removed and could currently do nothing. It also introduces weapon-type implicits and limits new Iron's Spellbooks compatibility to reworked uniques.

Consequently:

- 10 weapon types are not 10 semantic actions;
- 33 Unique Weapons are not 33 semantic actions;
- item registry presence cannot prove live ability identity;
- reworked/current surfaces can provide a positive lower bound without implying completeness.

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

## Four provider-owned implicits

`ImplicitRegistry` defines four Simply More-owned implicit definitions:

| ID | Owner/type | Causal identity |
|---|---|---|
| `simplymore:grandsword_sunder` | Grandsword | armor sunder / shield interaction |
| `simplymore:friendship` | Lance | mounted damage bonus |
| `simplymore:disarm` | Khopesh | attack-speed reduction chance |
| `simplymore:stun` | Pernach | stun chance |

Other Simply More weapon types route to existing Simply Swords weapon-type definitions or reuse one of the roots above. They do not increase the provider-owned implicit count.

Subtotal: **4**.

## Nine reworked Unique families

The initial Alpha changelog and release-correlated source positively establish active/passive ability surfaces for these nine current/reworked families:

| Unique | Passive causal root | Active causal root |
|---|---|---|
| Magmaseep | Hellfire hit eruption | Volcanic Vent |
| Moundshifter | pressure → earthquake / carried-block combat state | excavation/drill |
| Grandfrost | hit freeze | Snow Prison |
| Lustrous Moxie | light-orb accumulation/detonation | Heavensent Ray |
| Soulfracture | soul-fragment fracture/harvest | fragment-control activation |
| Black Pearl | effect theft | cannonball |
| The Blood Harvester | lifesteal | Harvest |
| Ruyi Jingu Bang | weapon growth | charged enlarged strike |
| Blade of the Grotesque | hostile aura/held passive | statue transformation |

Each row contributes two distinct causal roots. Downstream projectiles/entities/effects or multiple consequences inside one activation are not separately counted.

Subtotal: **18**.

## Lower-bound arithmetic

`18 reworked-Unique roots + 4 provider-owned implicits = 22`.

This is a **lower bound**, not a final denominator.

## Explicit non-promotions

Not counted yet:

- older/legacy uniques not included in the positive rework set;
- incomplete/rework placeholders;
- deprecated/removed redirect items;
- Mimicry forms as separate actions;
- effects, entities, HUD states, cooldowns and components;
- Simply Swords-owned implicits reused by Simply More;
- Iron's Spellbooks scaling/compatibility as separate provider actions;
- Reforming Remnant as a magic-action root without further semantic classification.

The source contains examples of unfinished/inert surfaces, so the remaining inventory must be classified object-by-object.

## Clean-room boundary

Upstream license is All Rights Reserved.

Only public factual metadata, names/IDs, behavior-level semantics, source structure and causal ownership are retained for catalog/interoperability purposes.

## Result

- physical/publisher artifact identity: **closed**;
- release-correlated source checkpoint: **established**;
- confirmed semantic lower bound: **22**;
- complete Alpha-5 denominator: **open**;
- strict contribution: **+0**;
- provider status: **⚠️**.
