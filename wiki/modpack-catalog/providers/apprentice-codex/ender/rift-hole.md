# Rift Hole

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:rift_hole`
- **Iron's school:** Ender
- **Levels:** 1–3
- **Minimum rarity:** Epic
- **Cast type:** Instant
- **Cooldown:** 10 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 100`
- `spellPowerPerLevel = 25`
- `baseManaCost = 150`
- `manaCostPerLevel = 50`
- source field `castTime = 30 ticks` while `getCastType()` returns `INSTANT`; exact player-facing timing should therefore be confirmed in runtime rather than assuming the field is consumed
- open duration: `200 ticks = 10 s`
- recast count: `2`
- tunnel radius on the plane: `1`, producing a potential **3×3** cross-section
- targeting range: `8 + 8 * spellPower / 100`
- tunnel depth: `floor(range)`, minimum 1

At default unmodified spell power, nominal ranges are **16 / 18 / 20 blocks** for levels 1–3.

## Server-authoritative world mutation

The provider requires a server-validated block target and rejects disallowed dimensions. It constructs a tunnel plan, applying a provider safety predicate before replacing each eligible block.

For every replaced position it stores the original block state in the provider `RiftHoleBlockEntity`, plus caster/tunnel identity and expiry time. Recast or timeout closes the tunnel by restoring only provider blocks belonging to the matching tunnel UUID.

This is a bounded temporary world mutation with an explicit restore path; it is not a permanent excavation spell.

## Safety boundary

`RIFT_HOLE_TUNNEL_DENYLIST` exists in the exact provider tag registry, and `RiftHoleBlockSafety` remains provider authority for what may be replaced.

Black Arcana must not reapply this mutation or restoration through a second `WorldEffectPolicy` transaction after the provider has settled it. A Black Arcana-originated portable-hole mechanic would still require its own policy and must demonstrate a real semantic gap.

## Causality

Opening, active recast state and closing belong to one provider tunnel lifecycle. Closing/restoration is cleanup, not a new spell/progression event.

## Acquisition

Registered through Iron's spell registry. Exact survival acquisition remains provider-wide audit work.

## Deduplication

Occupies the **temporary bounded portable tunnel with stateful block restoration** niche.

## Confidence

`SOURCE-PINNED SPELL / EXACT RANGE+DURATION+CROSS-SECTION+RESTORE IDENTITY / CAST-TYPE-vs-CAST-TIME RUNTIME UX + DENYLIST CONTENT + PACK QA PENDING`