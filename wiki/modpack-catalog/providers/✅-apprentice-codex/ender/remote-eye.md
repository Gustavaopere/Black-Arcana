# Remote Eye

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:remote_eye`
- **Iron's school:** Ender
- **Levels:** 1–3
- **Minimum rarity:** Epic
- **Cast type:** Instant
- **Cooldown:** 30 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 100`
- `spellPowerPerLevel = 30`
- `baseManaCost = 80`
- `manaCostPerLevel = 25`
- `castTime = 0`

Duration:

`40 + round(40 * spellPower / 100)` ticks.

At default unmodified spell power this is approximately **80 / 92 / 104 ticks** for levels 1–3, but actual duration responds to spell-power modifiers.

Persisted-state repair uses an explicit maximum active repair window of `20 * 30 = 600 ticks` for old state lacking active-duration metadata.

## Server-owned observation state

The server rejects dimensions not allowed by the provider config, then stores:

- active-until game time;
- active duration;
- anchor XYZ;
- anchor yaw/pitch.

For a `ServerPlayer`, that state is synchronized to the client. The provider guide describes a detached/free-look observation mode in which the physical caster remains vulnerable and the view cannot simply pass through walls.

The gameplay observation/camera experience is therefore a provider-owned remote-view system, not a Black Arcana `Borrowed Sight` session.

## Divination overlap

This is a direct semantic overlap with Black Arcana Familiars & Divination. A Black Arcana remote-observation spell needs a demonstrable distinction—such as target ownership/privacy semantics or a different noetic contract—rather than reproducing Remote Eye with different VFX.

Black Arcana must not consume client camera state as provider authority. Any future cross-provider progression integration would require a server-observable causal boundary.

## Acquisition

Registered through Iron's spell registry. Exact survival acquisition remains provider-wide audit work.

## Deduplication

Occupies the **temporary detached remote-eye/free-look observation** niche.

## Confidence

`SOURCE-PINNED SPELL / EXACT SERVER STATE+DURATION FORMULA+DIMENSION GATE / CLIENT CAMERA COLLISION+INPUT UX+FULL-PACK QA PENDING`