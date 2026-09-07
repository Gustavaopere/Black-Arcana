# Blood Brand

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:blood_brand`
- **Iron's school:** Blood
- **Levels:** 1–5
- **Minimum rarity:** Rare
- **Cast type:** Instant
- **Cooldown:** 4 s
- **Resource:** Iron's mana
- **Introduced/explicitly called out:** public 0.9.7.1 changelog
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 100`
- `spellPowerPerLevel = 75`
- `baseManaCost = 35`
- `manaCostPerLevel = 10`
- `castTime = 0`
- burst radius: `5 blocks`

## Initial hit

Exact raw projectile damage:

`1 + spellPower / 100`

then multiplied by server config `DamageMultiplierKey.BLOOD_BRAND`.

The source comment explicitly characterizes the initial damage as intentionally low because the debuff/brand is the main mechanic.

## Death burst

Exact raw burst damage seeded by the spell:

`8 * spellPower / 100`

then multiplied by the same Blood Brand server damage multiplier.

The provider guide states:

- the projectile brands a damaged mob;
- when the branded mob dies, blood magic bursts against nearby mobs;
- healing equals **50% of health actually lost to the burst**;
- a killing blow from Higanbana causes a stronger burst;
- walls block the blood magic;
- the burst fails if the brand loses connection to its caster.

The precise stronger-Higanbana multiplier and brand lifecycle are owned by the provider's downstream entity/effect implementation and remain separate detailed QA items unless needed for a future bridge.

## Causality

Blood Brand is a particularly important deduplication case because one cast produces a delayed death-triggered effect. Correct causal identity is:

`Blood Brand cast -> branded victim -> qualifying death -> provider burst/heal`

Black Arcana must not treat the downstream burst as a second independent cast or generate normal offensive proc chains twice from the initial kunai plus death burst unless an explicit future integration contract defines that behavior.

## Acquisition

Uses Iron's spell registry/scroll infrastructure. Exact 0.9.7.1 acquisition distribution remains pending data audit.

## Confidence

`SOURCE-PINNED SPELL CONFIG + DAMAGE FORMULAS + SERVER PROJECTILE SPAWN + PROVIDER GUIDE / DOWNSTREAM BRAND ENTITY LIFECYCLE AND PACK CONFIG QA PENDING`