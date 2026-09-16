# Precise Delay

State: `SOURCE-PINNED 1.6.15 / RUNTIME QA PENDING`

- Registry id: `ars_controle:glyph_precise_delay`
- Kind: Effect
- Tier: II
- School: Manipulation
- Base mana: 0
- Scribe XP: 55

## Acquisition

Ars glyph recipe inputs:

- `ars_nouveau:manipulation_essence`
- `minecraft:clock`
- `minecraft:comparator`

## Executable behavior

If there is still spell content after this part, it schedules the remainder through Ars Nouveau's `DelayedSpellEvent` / server `EventQueue`.

Delay duration is:

`1 << ExtendTimeCount`

That is `2^n` ticks for `n` Extend Time augments. The addon allows Extend Time up to 20 on this glyph and overrides its augment mana contribution to 0. A provider client packet presents the delay effect nearby; that packet is presentation, not authority.

If the spell is already at its end, the glyph returns without scheduling additional work.

## Boundary

The delayed continuation remains the same Ars spell causal chain. Black Arcana must not charge a second resource/cooldown/Mastery/Arcane Danger settlement when the delayed event resumes.
