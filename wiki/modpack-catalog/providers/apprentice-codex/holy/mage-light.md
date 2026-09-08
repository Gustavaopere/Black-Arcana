# Mage Light

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:mage_light`
- **Iron's school:** Holy
- **Levels:** 1
- **Minimum rarity:** Uncommon
- **Cast type:** Instant
- **Cooldown:** 0.5 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 100`
- `spellPowerPerLevel = 25`
- `baseManaCost = 20`
- `manaCostPerLevel = 0`
- `castTime = 0`
- Chargecast Staffbow incompatible.

Normal placement range:

`max(0, min(8 * spellPower / 100, configuredMaxRange))`

The hard maximum is provider server config, mirrored client-side through the provider's Mage Light config state. The exact pack config value remains runtime/config QA.

## Placement authority

The spell validates a block target before cast, stores the resolved placement position in cast data and then attempts placement through the provider's `BlockTools.tryPlaceBlockByEntity(...)` path.

The source respects replacement/survival checks and does not simply trust client coordinates. A successful cast places `MAGE_LIGHT_TORCH`, plays placement audio and emits particles.

Provider guide semantics: summons and places a magical torch that lights the area and does not require an ordinary supporting block.

## Integration/world safety

This is an Apprentice's Codex world effect settled by provider placement helpers. Black Arcana must not place a duplicate torch or charge a second world-effect transaction after observing the provider cast. Black Arcana-originated world effects remain governed by its own `WorldEffectPolicy`.

## Acquisition

Registered through Iron's spell registry. Exact 0.9.7.1 scroll/loot availability remains in the provider-wide acquisition audit.

## Deduplication

Occupies the **cheap magical light placement** niche. A second generic BA light-orb/torch spell needs a materially different persistent/domain role to justify itself.

## Confidence

`SOURCE-PINNED SPELL + SERVER PLACEMENT / PACK MAX-RANGE CONFIG + FULL PROTECTION-MOD QA PENDING`