# Born in Chaos — 1.7.6

Status: `✅ CATALOGED / EXACT PHYSICAL=PUBLISHER ARTIFACT / PLAYER-MAGIC SURFACES EXHAUSTIVELY CLASSIFIED / 17 COUNTED_EXACT / RUNTIME QA SEPARATE`

## Current physical identity

Current sibling physical authority:

- row: **#84**;
- JAR: `born_in_chaos_[Neoforge]_1.21.1_1.7.6.jar`;
- mod id: `born_in_chaos_v1`;
- runtime: `1.7.6`;
- physical SHA-1: `73704f38ac368c03716f9cc8f537470d3b352fa2`;
- Minecraft / loader: 1.21.1 / NeoForge.

Born in Chaos is primarily a mobs/encounters/equipment provider, but the exact installed build also owns a bounded set of deliberate player-facing supernatural artifact/staff actions. Those actions are cataloged here without reclassifying every magical-looking effect, mob ability, weapon proc or consumable as a spell.

## Exact publisher-artifact closure

NON-MERGE evidence PR **#501** audits CurseForge project/file `686437 / 8268280` and hard-gates the downloaded artifact against the physical pack fingerprint.

Final evidence checkpoint:

- audit HEAD: `7e0fb1d74e543661926fe053f7085f2136aa8205`;
- exact-artifact run: `36919074090` — **SUCCESS**;
- Black Arcana CI: **#4041** — **SUCCESS**;
- evidence artifact: `11190708455`;
- artifact digest: `sha256:37e2646bec350a0dce723445b5a58b86e9e45c2532b3f8a8c256675c6b47c8d0`;
- publisher SHA-1: `73704f38ac368c03716f9cc8f537470d3b352fa2`;
- publisher SHA-256: `a0271a24db8622434d9573c5e789d451a05c9211173885049284e1911e2499c7`;
- bytes: `11,842,184`.

The exact artifact contains **4,364 archive entries**, **1,550 classes**, **212 item classes**, **514 procedure classes** and **618 provider data paths**. The audit narrows that large surface to player-action-shaped item methods, linked procedures, global item-interaction procedures and provider-native acquisition data.

See [`EXACT-1.7.6-ARTIFACT-ACTION-AUDIT.md`](EXACT-1.7.6-ARTIFACT-ACTION-AUDIT.md).

## Exact semantic-magic inventory — 17 actions

The canonical metric counts a discrete supernatural player action, not every item, status effect, mob spell, projectile or passive proc.

Exact current counted roots:

1. Bone Heart — Bone Barrier activation;
2. Charm of Endurance — supernatural Endurance buff activation;
3. Charm of Fury — supernatural Fury/Rampage activation;
4. Charm of Strength — supernatural Strength activation;
5. Charm of Resistance — supernatural Resistance activation;
6. Charm of Stealth — supernatural Invisibility activation;
7. Dark Atrium — Dark Ward activation;
8. Dark Ritual Dagger — Sacrifice;
9. Ethereal Spirit — Pumpkin Spirit animation/transformation;
10. Bonescaller Staff — controlled skeleton/spiritual-assistant summoning;
11. Fel Lamp — Felsteed summoning;
12. Lord Pumpkinhead's Lamp — Lord's Felsteed summoning;
13. Frostbitten Blade / Icy Sweetness — one shared Icy Splash action;
14. Pumpkin Staff — one magical staff action whose projectile result can explode on entities or summon the provider-controlled Mr. Pumpkin on block impact;
15. Staff of Magic Arrows — Magic Arrow casting/shooting action;
16. Stormcaller's Horn — Snow Storm invocation;
17. Transmuting Elixir — one transmutation action across its provider-supported block/entity targets.

All 17 are `COUNTED_EXACT`: identity/control flow and a current provider-native acquisition route are directly closed in the hash-matched artifact.

Object-level cards:

- aggregate: [`actions/SUPERNATURAL-ACTION-CARDS.md`](actions/SUPERNATURAL-ACTION-CARDS.md);
- [Bone Heart — Bone Barrier](actions/bone-heart-bone-barrier.md);
- [Charm of Endurance](actions/charm-endurance.md);
- [Charm of Fury](actions/charm-fury.md);
- [Charm of Strength](actions/charm-strength.md);
- [Charm of Resistance](actions/charm-resistance.md);
- [Charm of Stealth](actions/charm-stealth.md);
- [Dark Atrium — Dark Ward](actions/dark-atrium-dark-ward.md);
- [Dark Ritual Dagger — Sacrifice](actions/dark-ritual-dagger-sacrifice.md);
- [Ethereal Spirit — Pumpkin Spirit Animation](actions/ethereal-spirit-pumpkin-spirit.md);
- [Bonescaller Staff — Controlled Summon](actions/bonescaller-staff-controlled-summon.md);
- [Fel Lamp — Summon Felsteed](actions/fel-lamp-summon-felsteed.md);
- [Lord Pumpkinhead's Lamp — Summon Lord's Felsteed](actions/lord-pumpkinheads-lamp-summon.md);
- [Icy Splash](actions/icy-splash.md);
- [Pumpkin Staff — Arcane Pumpkin Shot](actions/pumpkin-staff-arcane-shot.md);
- [Staff of Magic Arrows — Magic Arrow](actions/staff-magic-arrows.md);
- [Stormcaller's Horn — Snow Storm](actions/stormcallers-horn-snow-storm.md);
- [Transmuting Elixir — Transmutation](actions/transmuting-elixir.md).

Individual-card checkpoint: [`INDIVIDUAL-ACTION-CARDS-CHECKPOINT.md`](INDIVIDUAL-ACTION-CARDS-CHECKPOINT.md).

## Important deduplications

- Frostbitten Blade and Icy Sweetness invoke the same exact Icy Splash procedure; they are two owners of **one semantic action root**, not two spells.
- Pumpkin Staff's projectile/explosion and block-hit controlled-Mr.-Pumpkin result are downstream branches of one causal staff activation.
- Transmuting Elixir has separate block and entity event paths, but both implement the same provider-owned transmutation action and are counted once.
- Filled/empty Fel Lamp capture/refill interactions are preparation/state settlement for the already-counted summoning actions, not extra roots.

## Explicit exclusions

The exact artifact also contains many magic-adjacent surfaces that add zero semantic identities under the current metric:

- **Dark Charge / Staff of Blindness:** both use the same `StaffofBlindnessProjectileEntity` shot family. Dark Charge is a normal reachable weak blinding projectile; Staff of Blindness has no provider recipe/loot/tag route and is exposed as a debug-style alternate firing surface. This shared primary projectile family is not counted as an independent spell root.
- **Pumpkin Pistol:** provider-described magical ranged weapon, but its ordinary primary firing mode remains a weapon mode rather than a separate magical action root.
- **Intoxicating/Stimulating/Phantom bombs and Easter Eggs:** ordinary throwable/projectile item modes; their explosions/effects are downstream payloads.
- **Bottle of Magical Energy, ordinary elixirs, food/candy/gingerbread:** ordinary consume-to-status/economy surfaces; the status effects themselves are not spell identities.
- **Death Totem, Missionary Hat, Nightmare armor and similar equipment:** reactive/passive behavior without an independent player cast.
- **Nightmare Scythe, Soul Saber/Soulbane, Spider Bite and other on-hit equipment effects:** proc behavior attached to ordinary attacks.
- **loot containers** such as Krampus's Bag, Creepy Gift and Glutton Fish Stomach;
- **debug structure-spawn items** and ordinary spawn eggs;
- **mob-native spells/teleports/summons** such as Missionary, Bonescaller and boss abilities; the semantic ledger catalogs player-owned magic, not every supernatural mob attack.

## Exact acquisition closure

The exact provider data index records **202 Born in Chaos item IDs across 455 recipe/loot/tag acquisition rows**.

Relevant current routes include:

- Bone Heart, Dark Atrium, Dark Ritual Dagger, Bonescaller Staff, Fel Lamp, Frostbitten Blade, Icy Sweetness, Lord Pumpkinhead's Lamp, Stormcaller's Horn and Transmuting Elixir — exact provider recipes;
- all five Charms — exact `missioner` and `missionary_raider` loot tables, also present in provider rare-loot tags;
- Ethereal Spirit — exact provider loot from multiple spirit mobs;
- Fel Lamp and Lord Pumpkinhead's Lamp — additional exact provider mob-loot routes;
- Pumpkin Staff — exact `pumpkinhead` loot;
- Staff of Magic Arrows — exact Bonescaller/Supreme Bonescaller loot plus a packaged provider recipe.

Therefore no counted root is promoted from documentation alone.

## Ownership boundary

Born in Chaos remains authority for item availability, Magic Depletion, effects, summoned minions/mounts, projectile/entity lifecycle, cooldowns, durability/consumption and interaction settlement. Black Arcana must observe/deduplicate these provider actions rather than replay them, charge a second cost, or turn downstream effects/entities into separate spell identities.

RPG Skill Tree remains sibling authority only for progression/attributes/Mastery/perks/gates through verified contracts.

## Runtime QA remains separate

Catalog closure is not an assembled-pack runtime PASS. Later QA still includes current-world gamerules/config, Epic Fight coexistence, multiplayer owner assignment for controlled summons, cooldown/effect settlement, loot overrides, KubeJS/datapack changes and restart/chunk lifecycle.

## Result

**✅ Cataloged — 17 exact-current provider-owned supernatural player actions.**

Strict semantic contribution: **+17 `COUNTED_EXACT`**.
