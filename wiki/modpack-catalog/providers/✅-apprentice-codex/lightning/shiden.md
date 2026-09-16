# Shiden

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:shiden`
- **Iron's school:** Lightning
- **Levels:** 1–5
- **Minimum rarity:** Rare
- **Cast type:** Long
- **Cooldown:** 10 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 1600`
- `spellPowerPerLevel = 400`
- `baseManaCost = 50`
- `manaCostPerLevel = 15`
- `castTime = 30 ticks`

Raw slash damage is `spellPower / 100`, then multiplied by `DamageMultiplierKey.SHIDEN`.

Damage multiplier when the slash penetrates block obstruction:

`clamp(20 + spellLevel * 5, 10, 90)%`

For the actual 1–5 level range, this produces **25%, 30%, 35%, 40%, 45%** of normal damage through the provider's block-penetration path.

The ideal range is delegated to `ShidenKatanaEntity.getAttackDepth()`; this catalog does not invent a numeric distance without auditing that entity constant.

## Cast lifecycle

The katana is summoned during the long cast. Before the attack, current spell power and penetration multiplier are refreshed so completion-time provider/Focus Staffbow modifiers are reflected.

The weapon enters its standby animation/state using a speed scale derived from base vs actual cast duration. Cancelling releases the weapon; successful completion executes exactly one provider-owned slash.

## What it does

Provider guide semantics: summons a magical katana and swiftly slashes upward. Blocks do not completely stop the slash, but obstruction reduces its damage and impact.

## Causality

The partially penetrating hit remains one Shiden slash. Black Arcana must not treat the unobstructed and through-block portions as separate attack/proc identities.

## Acquisition

Registered through Iron's spell registry. Exact 0.9.7.1 scroll/loot availability remains in the provider-wide acquisition audit.

## Deduplication

Occupies the **charged Lightning katana rising slash with reduced block penetration** niche.

## Confidence

`SOURCE-PINNED SPELL / EXACT ATTACK DEPTH + KATANA COLLISION DETAILS + PACK CONFIG MULTIPLIER QA PENDING`