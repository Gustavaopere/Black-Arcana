# Apprentice's Codex — Ender school

Exact source checkpoint: `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`.

Installed provider: `apprentice_codex-0.9.7.1+mc1.21.1.jar` / `apprenticecodex` / `0.9.7.1`.

The exact 0.9.7.1 `SpellRegistry` registers **15/15** Apprentice's Codex spells into Iron's canonical **Ender** school:

1. [Arcane Blast](arcane-blast.md) — direct arcane hit + Arcane Charge.
2. [Arcane Beam](arcane-beam.md) — continuous 32-block piercing beam consuming Arcane Charge at completion.
3. [Personal Shelf](personal-shelf.md) — temporary personal storage/block interface.
4. [Assist Wings](assist-wings.md) — bounded jump/air-mobility utility.
5. [Manifestation Grimoire](manifestation-grimoire.md) — item-only legendary grimoire manifestation.
6. [Mantis Leap](mantis-leap.md) — uninterruptible leap + summoned blade slash.
7. [Auto Magnet](auto-magnet.md) — toggled item/XP collection familiar.
8. [Remote Eye](remote-eye.md) — server-owned remote-view state.
9. [Mana Slash](mana-slash.md) — item-tied weapon-damage-scaled mana slash.
10. [Long Stride](long-stride.md) — item-only sustained mobility channel.
11. [Rift Hole](rift-hole.md) — bounded temporary tunnel that restores original blocks.
12. [Demi-creator Wings](demicreator-wings.md) — bounded-area temporary creative flight.
13. [Mirage Avoidance](mirage-avoidance.md) — 25-tick evasive movement state with 15-tick invulnerability.
14. [Anchor Blink](anchor-blink.md) — item-tied dagger anchor/teleport setup.
15. [Servant Gaze](servant-gaze.md) — long-lived owner-bound autonomous staff turret.

## Authority

These remain Apprentice's Codex/Iron's provider casts. Iron's owns standard mana/cast/cooldown semantics; Apprentice's Codex owns the concrete Ender spell state/entities/blocks/recasts.

Black Arcana must not duplicate provider mana, damage, healing, movement, world mutation or summon settlement. Provider world effects such as Rift Hole restoration remain provider-owned; they are not retroactively routed through Black Arcana `WorldEffectPolicy`.

## High-overlap Black Arcana families

- **Divination:** Remote Eye materially overlaps remote observation.
- **Binding/storage:** Personal Shelf and Auto Magnet occupy convenience/ownership-adjacent niches.
- **Mobility:** Assist Wings, Mantis Leap, Long Stride, Demi-creator Wings, Mirage Avoidance and Anchor Blink occupy multiple movement/evasion niches.
- **Summoned autonomous objects:** Servant Gaze and Manifestation Grimoire reduce novelty space for generic magical attendants.
- **World traversal:** Rift Hole is a temporary provider-owned tunnel mechanic and blocks a trivial duplicate portable-hole spell.

Phase 3 remains blocked pending global semantic deduplication; this directory is a factual provider catalog, not implementation approval.