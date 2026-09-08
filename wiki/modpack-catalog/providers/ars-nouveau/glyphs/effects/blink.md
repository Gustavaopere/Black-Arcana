# Blink

- Registry ID: `ars_nouveau:glyph_blink`
- Source class: `EffectBlink`
- School: Manipulation
- Default tier: **3**
- Default mana: **50**
- Default distance config: **8** + **3.0** per amplification unit
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Source-pinned behavior

Blink supports several Ars-owned teleport paths. Self use attempts a forward teleport with safe-space checks. Entity use can consume Warp Scroll location data from the caster context/offhand, including dimension-aware provider warping where the stored data permits it. Turret/Rune caster contexts can source Warp Scroll data from adjacent inventory behavior. Entities tagged as not supporting teleport are rejected, and Ender-style teleport events can veto relevant warp paths.

Compatible augments: Amplify, Dampen.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:manipulation_essence` + `#c:ender_pearls` ×4.
- Source-default recipe XP: **160 XP** (Tier III).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Boundary

Ars Nouveau owns Blink/Warp Scroll/portal teleport semantics. Black Arcana must not duplicate generic Blink/Warp ownership; any Black Arcana displacement remains server-validated under its destination-recovery, protection and loaded-chunk contracts.

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME+CONFIG QA PENDING`.