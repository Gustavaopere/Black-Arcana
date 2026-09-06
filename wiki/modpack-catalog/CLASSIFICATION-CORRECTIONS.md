# Phase 2 Provider Classification Corrections

Status: `CANONICAL CORRECTION OVERLAY FOR THE PR #62 BASELINE REGISTRY`

`PROVIDERS.md` is the Phase 2 inventory baseline created by PR #62. Granular provider verification can reveal that a baseline class was too broad. Until the registry table is regenerated, the corrections below take precedence **only for the Phase 2 class and granular-catalog columns**. Presence, JAR identity and runtime version continue to come from the current modlist/registry.

| Baseline row | Provider | PR #62 baseline class | Correct Phase 2 class | Granular capability catalog | Evidence basis |
|---:|---|---|---|---|---|
| 9 | Ars Creo 5.4.0 | `ARS GLYPH / SYSTEM PROVIDER` | `BRIDGE / COMPAT / PROGRESSION` | `NO / CONDITIONAL` | Current 5.4.0 public surface is Create-contraption integration: Starbuncle Wheel, contraption spell turrets/Source Jars and ritual support; no current glyph inventory was proven. |
| 12 | Ars Elemancy 1.18.3 | `ARS GLYPH / SYSTEM PROVIDER` | `GEAR / ENCHANT / SUPPORT CONTENT` | `NO / CONDITIONAL` | Current 1.18.3 public surface is elemental armor/foci specializations and gear/compat behavior; no separate glyph inventory was proven. |
| 16 | Ars 'n' Spells 3.2.4 | `ARS GLYPH / SYSTEM PROVIDER` | `BRIDGE / COMPAT / PROGRESSION` | `YES` | Current provider is an Ars Nouveau ↔ Iron's bridge for mana, progression, equipment, spellbooks/casting plus discrete bridge rituals. |
| 20 | Ars Polymorphia 1.0.3 | `ARS GLYPH / SYSTEM PROVIDER` | `BRIDGE / COMPAT / PROGRESSION` | `NO / CONDITIONAL` | Current public function is Polymorph compatibility for Ars Nouveau Storage Lecterns; no spell/glyph system is exposed. |

## Why this matters

Phase 2 answers two separate questions:

1. Is the component magic-relevant?
2. Does it itself provide discrete gameplay capabilities that must be compared against proposed Black Arcana spells/systems?

A compatibility mod can be highly relevant without being a spell provider. Inflating every Ars addon into `ARS GLYPH / SYSTEM PROVIDER` would create false coverage, false deduplication and false implementation requirements.

## Provider pages supporting this overlay

- `providers/ars-creo.md`
- `providers/ars-elemancy.md`
- `providers/ars-n-spells.md`
- `providers/ars-polymorphia.md`

## Gate

These corrections do not authorize Phase 3. They improve the accuracy of the Phase 2 inventory only. New Black Arcana implementation remains blocked until the relevant capability rows have enough provider evidence to establish a real semantic gap.
