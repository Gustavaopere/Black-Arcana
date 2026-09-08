# Ars Nouveau — Delay

Status: `SOURCE-PINNED 5.13.1 / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_delay`
- Display name: Delay
- School: Manipulation
- Default tier: 1
- Default mana cost: 0
- Compatible augments: Extend Time, Reduce Time (`glyph_duration_down`), Randomize
- Source default base delay: 20 ticks
- Source default Extend Time increment: 20 ticks per augment
- Source default Reduce Time decrement: 10 ticks per augment
- Source default Randomize amplitude: 25% per Randomize count

## Provider-native behavior

Delay suspends resolution of all spell parts to its right by creating a `DelayedSpellEvent`, storing it in Ars' server event queue and synchronizing a client delay effect. Randomize varies the resulting duration around the calculated delay.

## Authority / deduplication

This is an Ars spell-composition scheduler primitive, not merely a visual delay. Black Arcana must not reuse or replace Ars' delayed resolution queue for its own canonical cast pipeline, and must not insert a second settlement path around Ars spells.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectDelay`).
