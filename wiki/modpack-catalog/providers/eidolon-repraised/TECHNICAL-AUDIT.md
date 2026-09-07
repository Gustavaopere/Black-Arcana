# Eidolon: Repraised 0.5.0.2 — Technical Audit

Status: `SOURCE-PINNED / STATIC SPELL + ACTIVE RITUAL SURFACES INVENTORIED / DATA-DRIVEN RESOURCES + RUNTIME QA PENDING`

Source authority: `Alexthw46/Eidolon-Repraised@696a47333e43970be7f697790eac0af76b6a04b8`

## Audit scope

This file tracks integration-sensitive behavior that must be proven before Black Arcana consumes Eidolon state/events.

### Confirmed provider-owned state

- mana capability;
- reputation/devotion capability;
- soul capability;
- knowledge/research capability;
- Sign registry and SignSequence resolution;
- spell registry/cache;
- ritual registry;
- chant / command-chant / chant-conversion recipes;
- deity and altar state;
- server configs per registered spell.

### Confirmed event surface

`StaticSpell.canCast(...)` posts a cancelable `SpellCastEvent.Pre` before mana/target validation returns true. `StaticSpell.cast(...)` invokes the concrete effect and then posts `SpellCastEvent.Post`.

Integration rule: Black Arcana observations must use one causal id/guard per provider cast and must not combine event observation with world-delta observation without deduplication.

## Cost/settlement model

The base class verifies that sufficient mana exists but does **not** centrally settle the cost. Concrete spell implementations are responsible for calling `IMana.expendMana(...)` when their action commits. This makes source-level per-path settlement audit mandatory.

### Verified normal/intentional paths

- `FireTouchSpell`: spends cost after successful block/entity action.
- `FrostSpell`: spends cost after successful water/entity action.
- `HealSpell`: spends cost after healing/cleanse path.
- `DarkTouchSpell` / `LightTouchSpell`: spend either recipe-defined conversion cost or fallback spell cost.
- `ZombifySpell` / `ConvertZombieSpell`: explicitly spend 20 mana after conversion path.
- `ThrallSpell`: explicitly spends a **dynamic** target-sensitive cost, not its nominal base value.
- ordinary Light/Dark `LightSpell` casts spend cost after valid placement/effect.
- ordinary `PrayerSpell` registrations can legitimately have zero mana cost; their authority is reputation/cooldown/effigy/altar state instead.

### Dynamic-cost path

`ThrallSpell` computes effective mana cost as:

`2 × getCost() × (targetHealth / targetMaxHealth)`

With default base cost 50 this becomes `100 × healthRatio`. Black Arcana must never charge the nominal 50 externally or cache a fixed cost for this spell.

## Cost/settlement anomaly queue

At source level, these paths require runtime verification:

- `SmiteSpell`: declares cost 40 but concrete `cast()` does not directly expend mana;
- `ApplyPotionSpell`: generic effect-application path does not directly expend mana;
- `SunderArmorSpell`: inherits `ApplyPotionSpell`, declares cost 50 and therefore inherits the same ambiguity;
- `LightArmorSpell` / `reinforce_armor`: inherits `ApplyPotionSpell`, declares cost 50 and inherits the same ambiguity;
- `WaterSpell`: air/source-placement path visibly spends 10 mana, but the `LiquidBlockContainer` placement branch does not visibly spend mana;
- `UndeadLureSpell`: declares cost 50, `canCast()` returns true, but the concrete `cast()` is empty; no source-visible effect or mana settlement exists in this exact build.

These are **not** classified as confirmed bugs without runtime evidence. Black Arcana must not compensate by charging mana externally, injecting missing effects or altering provider code from this documentation PR.

## Sacrifice/prayer semantics

`dark_animal_sacrifice` and `dark_villager_sacrifice` are registered using `PrayerSpell` constructors without a positive mana-cost parameter. Their transaction cost is therefore not generic mana; their verified authority is provider-native prayer readiness, target/sacrifice gates, deity reputation, altar power and prayer cooldown/state. Zero mana here must not be treated as an anomaly.

## Ritual authority findings

The active 0.5.0.2 hardcoded ritual registry contains 10 entries. Several mutate global or cross-system-sensitive state:

- `crystal`: kills eligible undead with ritual damage and emits provider Soul Shards;
- `daylight` / `moonlight`: mutate world day time directly and synchronize players;
- `absorption`: serializes weakened eligible entities into a Summoning Staff and removes them with `RemovalReason.KILLED`;
- `purify`: performs entity conversions;
- `allure` / `repelling`: inject provider movement goals into mobs.

Black Arcana must not interpret these as ordinary spell damage/mob death/time-change events without deduplication and semantic classification.

## Soul authority

`SoulImpl` stores an integer soul count and an optional master entity UUID or block position. Entity-master assignment is constrained by provider ownership semantics involving Summon Staff. Increment/decrement operations synchronize provider state to server players. The serialized form contains soul count plus optional master identity/location.

Integration rule: Eidolon soul is a separate provider resource. It must not be silently mapped to Malum spirits, Goety Soul Energy, Iron's mana, Ars Source or Black Arcana resource pools.

## Authority constraints

1. Mana settlement: Eidolon only.
2. Reputation/devotion mutation: Eidolon only.
3. Research grants: Eidolon only.
4. Soul mutation: Eidolon only unless a documented external API path exists.
5. Chant conversion selection and per-item conversion cost: Eidolon recipe manager only.
6. Prayer cooldown, altar power/capacity and effigy readiness: Eidolon only.
7. `NECROTIC`/`CONSECRATED` charge mutation: Eidolon only.
8. SignSequence matching: Eidolon only.
9. Ritual requirements/sacrifices/focus mutation: Eidolon only.
10. Entity capture/serialization by Absorption: Eidolon only.
11. Global time mutation by Daylight/Moonlight: Eidolon only.

## Runtime QA required

- verify actual mana delta for every spell class, with special focus on Smite, ApplyPotion-derived spells, WaterSpell container placement and Undead Lure;
- verify whether Undead Lure is truly inert at runtime or receives behavior from a path not visible in its concrete class;
- verify Pre/Post event count and logical side on dedicated server;
- verify no duplicate cast event when a data-driven ChantRecipe materializes a cached Spell;
- verify dynamic Enthrall cost at multiple target health ratios;
- verify prayer cooldown/reputation/mana updates are server authoritative;
- verify zero-mana sacrifice prayers do not incur a hidden external resource cost;
- verify `NECROTIC` and `CONSECRATED` charges under Epic Fight/other combat transforms in the actual pack;
- verify exact research survival unlock chain;
- verify soul production/consumption lifecycle;
- verify Crystal Soul Shard drops against modded undead and loot/progression hooks;
- verify Absorption does not accidentally trigger duplicate normal-kill rewards in the pack;
- verify Daylight/Moonlight interaction with other installed time systems;
- verify all ritual requirements, sacrifices and cleanup paths;
- verify data-driven chant/command-chant/conversion and ritual recipes present in the exact installed resources.

## Current conclusion

Eidolon is a high-authority provider. Its static spell registry and active hardcoded ritual registry are now sufficiently mapped for capability deduplication, but resource/progression interception remains unsafe until data-driven resources and runtime settlement checks are closed.