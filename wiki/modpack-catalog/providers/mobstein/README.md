# Mobstein 5.4.4 — resurrection, constructed bodies and experiment authority

## Status

`EXACT INSTALLED ARTIFACT 5.4.4 / EXACT CURSEFORGE RELEASE 8040734 / PUBLISHER GUIDE AUDITED / 10 RESURRECTED FORMS / 6 SURGERY-STRETCH TYPES / 7 FAILED EXPERIMENTS / BODY+ORGAN+SYRINGE+STRUCTURE SURFACES DOCUMENTED / 5.4.4 SABLE-COMPAT CLAIM RECORDED / ALL RIGHTS RESERVED / NO OFFICIAL PUBLIC SOURCE PIN LOCATED / REGISTRY+API+RUNTIME QA PENDING / PROVIDER-SPECIFIC IMPLEMENTATION FAIL-CLOSED`

## Runtime identity

Current physical modlist authority:

- provider: **Mobstein**;
- installed JAR: `mobstein-5.4.4-neoforge-1.21.1.jar`;
- mod id: `mobstein`;
- runtime version: `5.4.4`;
- modlist note: `MCreator mod`;
- SHA-1: `3672d88f940ddd474a5429d7066b099cd0ce0c29`;
- CurseForge/package fingerprint recorded by the modlist: `3386302902`;
- loader/game: NeoForge 1.21.1;
- role: `RESURRECTION / CONSTRUCTED-CREATURE / BODY-PART / EXPERIMENT PROVIDER`.

The modlist remains authoritative for the binary actually installed in the pack.

## Exact public release checkpoint

Official publisher surface:

- CurseForge project: **Mobstein : Revive animals and necromancy!**;
- author: **Pecsitonic**;
- project ID: `1193873`;
- exact NeoForge 1.21.1 file ID: `8040734`;
- filename: `mobstein-5.4.4-neoforge-1.21.1.jar`;
- release date: `2026-05-04`;
- channel: Release;
- project license: **All Rights Reserved**;
- environment: Client & Server.

The exact 5.4.4 release note states that Mobstein is compatible with **Sable Mod**. It does not publish a Sable version contract on that release page. The current pack uses Sable `2.0.5`, therefore exact 5.4.4↔2.0.5 behavior remains a runtime QA item rather than an inferred compatibility guarantee.

No official public source repository or exact source revision for Mobstein 5.4.4 was located during this checkpoint. Black Arcana therefore uses publisher documentation/release metadata and the installed modlist only. The Mobstein JAR is **not decompiled** for this catalog.

## Provider identity and authority

Mobstein is a supernatural gameplay provider centered on reconstructing and resurrecting bodies, creating experimental creatures and maintaining provider-owned companions. Its laboratory presentation does **not** make it a technology provider by itself.

Mobstein owns, where its public documentation establishes the behavior:

- Clinical Stretch resurrection flow;
- resurrected vanilla-creature variants and their abilities/taming;
- full bodies and harvested body parts;
- organ extraction and organ storage gameplay;
- Surgery Stretch constructed creatures;
- provider-owned `Attack`, `Health`, `Speed` and `Template` perks used by that construction flow;
- Subject Assembly Machine mannequin construction;
- failed-experiment creature family;
- Dr. Mobstenio and Igor progression;
- resurrection/utility syringes;
- Frankenstein Castle, Witherstein Ruins and Old Ruins;
- Witherstein encounter/revival flow.

Black Arcana must not create a second Mobstein corpse ledger, resurrection ownership model, experiment state, pet ownership layer or copy of Mobstein's internal construction perks merely to integrate the provider.

## Canonical subcatalogs

- [Resurrection and experiment catalog](RESURRECTION-EXPERIMENTS.md)
- [Technical/provenance audit](TECHNICAL-AUDIT.md)
- [Black Arcana integration rules](INTEGRATION-RULES.md)

## Publisher-documented capability inventory

### Clinical Stretch — 10 resurrected forms

The official guide describes night-time resurrection by placing a full body on the **Clinical Stretch**, remaining at the apparatus for approximately 15 seconds and allowing the lightning event to complete.

| Public name | Provider-owned capability summary |
|---|---|
| Axolotl Resucited | sit/bucket transport; nearby regeneration + night vision when tamed |
| Dolphin Resucited | rideable; water breathing; strong water mobility |
| Bat Resucited | flying melee attacker; sit command |
| Putrid Horse | fast/high-jump mount; approximately five cosmetic rot stages; own interface; no armor |
| Ocelot Resucited | fast pet; sit command; dyeable collar |
| Villager Resucited | kill-triggered chance to provide one of three organs |
| Silver fish Resucited | nearby cave-mining speed utility; sit command |
| Warden Resucited | powerful stationary bodyguard; no vanilla sonic boom; Reviver Syringe exclusion |
| Frankenstein Resucited | stationary bodyguard; nearby `Blacksmithstrength` effect described as granting speed; Reviver Syringe exclusion |
| Rabbit Resucited | nearby jump-boost utility; sit command |

These are publisher-facing names. Exact entity registry IDs, AI classes, attributes, effect IDs and internal formulas are **UNVERIFIED**.

### Surgery Stretch — 6 constructed creature types

The official guide exposes six constructed types:

1. Turtle;
2. Panda;
3. Polar Bear;
4. Spider;
5. Enderman;
6. SnowGolem.

It also exposes four Mobstein-owned construction `perks`:

- `Attack` — public range `0.8–2`;
- `Health` — public range `20–40`;
- `Speed` — public range `0.3–0.5`;
- `Template` — crafting input for the other provider perks.

These are **not RPG Skill Tree perk nodes**. Black Arcana and the RPG progression provider must not mirror them into a second progression ledger.

### Subject Assembly Machine

The publisher guide states that this machine builds a mannequin from head/torso/pants and allows any game head, including a custom player head produced through the Head Creator flow. It explicitly states that these assembled mannequins have no special abilities.

No FE, Create stress, AE2 network, Oritech power or other technology-resource contract is documented for this machine. Visual laboratory machinery is insufficient evidence for a technology bridge.

### Failed experiments — 7 public variants

The current official guide names:

- Experiment 097;
- Experiment 062;
- Experiment 067;
- Experiment 077;
- Experiment 091;
- Experiment 012;
- Experiment 007.

Their public behavior is cataloged in [RESURRECTION-EXPERIMENTS.md](RESURRECTION-EXPERIMENTS.md). Exact registry identities and internal AI/state contracts remain unverified.

### Special NPC/provider progression

- **Dr. Mobstenio** — found in Frankenstein Castle, revived using the Mobstenio Blood Syringe and tamed with Wither Spores obtained from the Witherstein progression; the public guide says the revived NPC wanders rather than follows.
- **Igor** — summoned from an Igor Spawner, not tameable, and used with Igor's table plus Suspicious Syringes to create random failed experiments; the official guide excludes experiments 062 and 097 from this creation route.

### Syringe family

The official guide documents:

1. Empty Syringe;
2. Reviver Syringe;
3. Mobstenio Blood Syringe;
4. Lightningbolt Syringe;
5. Suspicious Syringe.

The Reviver Syringe is also the documented trigger for reviving the Witherstein skeleton. The same public guide states that Resurrected Warden and Frankenstein cannot be revived by the Reviver Syringe.

### Structures and boss progression

Publicly documented structures:

- Frankenstein Castle — Swamp;
- Witherstein Ruins — Jungle;
- Old Ruins — Jungle.

The Witherstein encounter starts by using the Reviver Syringe on the skeleton in Witherstein Ruins and is described as having **three stages**, with Wither Skeleton spawning in the later stages.

Exact structure registry IDs, placement weights, boss statistics, loot tables and encounter state-machine internals are **UNVERIFIED**.

## Body, organ and material loop

The official guide describes body/material acquisition from vanilla creatures and a provider-owned organ loop:

- full bodies can be placed on a support and removed with shears;
- the Organ Extractor uses tweezers and a full body to yield one of three organs randomly;
- the Resurrected Villager offers an alternate organ-farming route through its kills;
- a Jar is used to store organs;
- several mob-specific body parts are publicly documented, including Piglin chop, Polar Bear/Panda leather, Villager nose, Spider legs, Dolphin tail, Horse leather, Axolotl gill and Bat wings/fangs.

These are Mobstein acquisition/material semantics, not Black Arcana corruption or soul currency.

## Semantic overlap with Black Arcana and other providers

Mobstein materially occupies:

- physical-body resurrection;
- creature reconstruction;
- tameable resurrected companions/bodyguards;
- corpse/body-part/organ processing;
- laboratory-style constructed creatures;
- conditional creature revival exclusions;
- a three-stage resurrected boss encounter.

This overlaps thematically with Souls & Death, rituals, familiars and resurrection, but thematic overlap does not transfer authority.

Required separation:

- Mobstein resurrection state ≠ Black Arcana Corruption/Strain/Backlash;
- Mobstein organs/bodies ≠ Malum spirits;
- Mobstein resurrection ≠ Goety Soul Energy/servant ownership;
- Mobstein resurrection ≠ Eidolon ritual/soul-shard state;
- Mobstein undead/experiment state ≠ Enshrouded Shroud corruption;
- Mobstein construction `perks` ≠ RPG Skill Tree perks;
- Mobstein laboratory blocks ≠ Create/AE2/Oritech authority.

## Safe integration posture

- provider-native resurrection and companion ownership first;
- do not re-award or re-settle damage/kill/organ outcomes already owned by Mobstein;
- no Mastery for a resurrected companion merely remaining alive or near the player;
- any progression reward requires a discrete, deduplicable causal action;
- no per-tick scan of all Mobstein companions/corpses/structures;
- no provider-specific adapter until a supported external boundary is actually demonstrated;
- Sable compatibility is a runtime/physics compatibility claim, not permission for Black Arcana to own Sable transformation or Mobstein entity physics.

## Remaining open gates

1. runtime-validate the exact installed 5.4.4 JAR in the current pack;
2. validate the public Sable compatibility claim against current Sable `2.0.5`;
3. identify a supported public Mobstein integration/API boundary, if one exists, without decompilation;
4. runtime-check Clinical/Surgery Stretch ownership, cleanup and duplicate-prevention behavior;
5. verify exact entity/effect/item/block/structure IDs only through supported/public/runtime-observable means;
6. validate multiplayer ownership/friendly-fire/death/revival semantics before consuming any companion or resurrection event;
7. validate the Witherstein lifecycle, repeatability and reward/loot semantics before using it as a progression milestone;
8. verify special exclusions and edge cases such as Warden/Frankenstein Reviver behavior and day/night resurrection routes.

## Phase 3 gate

Mobstein has a strong publisher-documented **semantic** catalog, but provider-specific integration remains:

`BLOCKED / FAIL-CLOSED`

until a supported boundary and exact-pack runtime behavior are demonstrated. Public gameplay documentation establishes what Mobstein owns; it does not establish an external API contract.