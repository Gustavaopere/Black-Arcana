# Catch Flame

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:catch_flame`
- **Iron's school:** Fire
- **Levels:** 1–8
- **Minimum rarity:** Uncommon
- **Cast type:** Long
- **Cooldown:** 0.5 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 800`
- `spellPowerPerLevel = 75`
- `baseManaCost = 10`
- `manaCostPerLevel = 3`
- `castTime = 10 ticks`
- fixed range: **3 blocks**
- effect half-size around impact: **0.5 block**

Raw damage:

`spellPower / 100`

then multiplied by `DamageMultiplierKey.CATCH_FLAME`.

Burn duration:

`max((spellLevel - 1) * 20, 10)` ticks.

## Entity-hit behavior

The spell resolves a short-range raycast and builds a small impact AABB. Valid combat targets must intersect the impact volume and have line of sight from the resolved impact origin.

If a target is already burning, Catch Flame selects its dedicated penetrating damage type; otherwise it uses the standard Catch Flame damage type. On successful damage, remaining fire ticks are raised to at least the spell's burn duration.

## Block/world interaction

Catch Flame can ignite a targeted block surface and has a dedicated interaction for the provider's **Essence Smoker**.

Important world-safety facts from exact source:

- block ignition is gated by provider server config;
- Spell Dispenser casting has a separate ignition permission toggle;
- remote-owner and non-player casts are resolved separately;
- real-player interaction permissions are checked before ignition;
- `mayInteract` / `mayUseItemAt` checks are preserved;
- ordinary block ignition is routed through a Flint and Steel `useOn` flow so loader/land-protection events can deny it;
- Essence Smoker ignition executes only after provider hook/protection checks.

This is significant for Black Arcana: the addon owns these local Fire world effects. A bridge must not bypass provider protection checks or route the same ignition through Black Arcana `WorldEffectPolicy` a second time after the provider has already settled it.

## What it does

Provider guide semantics: kindles fire at close range; already-burning targets can be struck through normal invulnerability-frame behavior; it can ignite an Essence Smoker or place fire on a block surface. The implementation explicitly preserves land-protection/interact hooks.

## Acquisition

Registered through Iron's spell registry. Exact 0.9.7.1 scroll/loot/recipe availability remains in the provider-wide acquisition audit.

## Deduplication

Occupies the **short-range Fire strike + burn + protected block ignition / Essence Smoker utility** niche. Black Arcana should not recreate the same convenience ignition spell or bypass these provider-owned checks.

## Confidence

`SOURCE-PINNED SPELL + TARGETING + IGNITION PATH / PACK CONFIG VALUES + FULL MODPACK LAND-PROTECTION QA PENDING`