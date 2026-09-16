# Overgrowth

Status: `SOURCE-PINNED 5.13.1 / GROWTH RITUAL`

- Registry id: `ars_nouveau:ritual_overgrowth`
- Class: `RitualOvergrowth`
- Source cost declaration: `500`
- Processing cadence: every `200` game ticks
- Working radius: `5` blocks
- Exact release checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Provider-native behavior

Without a modifier, Overgrowth scans a bounded 11×3×11 block volume around the ritual every 200 ticks. Candidate farm/bonemealable positions are adjusted to their crop position; each candidate has a `1/25` random chance to receive vanilla bonemeal through an Ars fake player. If at least one bonemeal application succeeds, the ritual marks that work cycle as needing Source.

With exactly one consumed Bone Block, the ritual switches modes: it scans `AgeableMob` entities inside radius 5, skips the provider blacklist, and advances baby animals by `500` age ticks. A successful cycle requests Source.

## Authority / Black Arcana boundary

Crop growth, animal age advancement, random selection and Source settlement are Ars Nouveau authority. Black Arcana must not replay successful growth operations or duplicate Source costs.

The Bone Block modifier selects a provider-native mode; it is not a Black Arcana progression gate.

## QA

Source is pinned to 5.13.1. Effective Source debit timing and compatibility with modded bonemeal/growth hooks remain runtime QA.