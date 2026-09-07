# Otherworld Lens

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:otherworld_lens`
- **Iron's school:** Eldritch
- **Levels:** 1
- **Minimum rarity:** Legendary
- **Cast type:** Continuous
- **Cooldown:** 5 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source config

- `baseManaCost = 35`
- `manaCostPerLevel = 0`
- `baseSpellPower = 0`
- `spellPowerPerLevel = 0`
- `castTime = 300 ticks`
- fixed targeting/placement range: **8 blocks**
- marked incompatible with the provider's Chargecast Staffbow path.

## Server-authoritative placement/session

The spell only accepts a `ServerPlayer`. Before casting it:

1. resolves a pending block target within 8 blocks;
2. requires a valid hit block + face and air at the placement side;
3. runs `OtherworldLensTargetSafety.validate(...)`;
4. stores validated target data as cast data.

During server pre-cast, the target is validated again before the temporary lens block is placed. A provider session UUID then links player, lens position and viewed target.

Every server cast tick validates the active session. The spell cancels if the player is too far away, the lens disappears, the lens is replaced, or another provider validation fails. Cast completion always closes the session with a provider-owned end reason.

## What it does

Provider guide semantics: conjures an unstable crystal lens from another world. Looking through it reveals the world as though viewed from behind the lens surface. The lens only persists while concentration is maintained, and obstructions can prevent a valid placement/session.

This is a temporary, validated remote-viewing surface—not a persistent portal.

## Authority and deduplication

This directly overlaps Black Arcana Divination. Black Arcana must not create a second camera/session state or independently place/remove the same lens. A future bridge should observe the provider session only through a legitimate boundary and preserve its server-validated target and cleanup rules.

## Acquisition

Registered through Iron's spell registry. Exact 0.9.7.1 scroll/loot acquisition remains in the provider-wide acquisition audit.

## Confidence

`SOURCE-PINNED SPELL + SERVER TARGET/SESSION LIFECYCLE / CLIENT VIEW RENDER + FULL MODPACK QA PENDING`