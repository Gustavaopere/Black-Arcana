# Host capability map — NeoForge 1.21.1

Accessed: 2026-08-27

This map exists to avoid duplicating systems already provided by the pack. Installed/upstream version reconciliation is recorded separately in `runtime-host-baseline.md`. This is not an adapter implementation plan; Stage 03 must confirm concrete, version-compatible APIs before integration code is written.

## Iron's Spells 'n Spellbooks

Installed/runtime baseline: `1.21.1-3.16.3`.
Latest public 1.21.1 release checked: `1.21.1-3.16.3` (2026-08-18).
Public developer documentation: https://iron.wiki/developers/

Confirmed planning facts:
- NeoForge 1.21+ has a published compile API artifact.
- The current developer guide calls `io.redspace.ironsspellbooks.api` the stable API surface; full-mod/internal packages may break between releases.
- Third-party mods can register spells through the documented spell registry/DeferredRegister path; the developer documentation also covers custom schools.
- Spell definitions are config-driven for values including school, cooldown and max level.
- Iron's already owns generic active-spell concerns such as mana/spell power/cooldown attributes and spellbook-oriented presentation.

Black Arcana role:
- Preferred host for active combat casts that benefit from Iron's spell lifecycle, scaling and spell equipment.
- Good fit: spectral/rift armaments, gaze attacks, barriers, vector control and selected offensive forbidden spells.
- Default to the stable `api` classifier. Any use of non-API packages requires an explicit Stage 03 compatibility justification and dedicated tests.
- Iron's mana is one optional `CostProvider`, never a hard dependency of Black Arcana core.

## Ars Nouveau

Installed/runtime baseline: `1.21.1-5.13.0`.
Latest public 1.21.1 release checked: `1.21.1-5.13.1` (2026-08-24).
Public guide: https://ars.guide/1.21.1/

Confirmed overlap:
- `Blink` already teleports the caster and can warp entities with Warp Scrolls.
- Warp Scrolls and Warp Portals already implement recorded-location travel; stabilized scrolls cover cross-dimensional travel.
- Ritual of Warping moves nearby entities to a scroll location.
- Ars has a mature familiar system obtained through a Binding ritual, with player-bound familiar selection/summoning.
- Ars is explicitly designed around composable glyphs and has a large 1.21.1 addon ecosystem.

Black Arcana role:
- Do not recreate generic blink, generic point-to-point portals, generic warp-scroll travel or generic familiar ownership.
- Prefer Ars integration for spatial utility where Black Arcana adds a forbidden constraint/augmentation rather than a duplicate transport system.
- Candidate unique spatial mechanics remain: projectile-anchor recall, reciprocal transposition, astral severance, namescrying and domain travel, because their gameplay contracts differ materially from normal Warp/Blink.
- If an Ars glyph would only duplicate an existing Ars effect, disposition should be `MERGE` or `DROP` rather than creating a Black Arcana clone.
- Stage 03 targets installed `5.13.0` first. The newer `5.13.1` is not treated as equivalent until the chosen extension seam is tested against both or the pack is updated.

## Eidolon: Repraised

Installed/runtime baseline: `1.21.1-0.5.0.2`.
Latest public 1.21.1 release checked: `1.21.1-0.5.0.2` (2026-05-09), NeoForge; CurseForge lists LGPLv3.
Public 1.21.1 changelogs confirm rituals, chants, progression/spellcasting events, mana/soul-heart state and necrotic/undeath-themed mechanics.

Black Arcana role:
- Preferred thematic host for prepared occult acts, covenants, curses, bargains, necrotic rites and grand rituals when its supported extension surface can express them.
- The mere existence of Eidolon rituals does **not** mean Black Arcana may inject arbitrary ritual behavior through a stable API. Stage 03 must inspect/document the actual supported extension points.
- Routine combat casts should not be forced into Eidolon ritual UX.

## Malum

Installed/runtime baseline: `1.21.1-1.8.2`.
Latest public 1.21.1 release checked: `1.21.1-1.8.2` (2025-12-08), NeoForge; project description centers soul magic / spirit arcana and CurseForge lists LGPLv3.

Important version signal:
- Malum 1.7.3 removed the old Spirit Ritual system that used the Ritual Plinth.
- Malum 1.8 reworked Spirit Rites and introduced the current Rite-oriented model.

Black Arcana role:
- Natural provider/host for spirit costs, soul harvesting, spirit-infused effects and soul-bound equipment where supported.
- Good thematic fit: Black Pyre/soul burn, Mortal Ledger/Soul Anchor, sympathetic wounds, spirit sight and sacrificial weapon ascension.
- Do not design against the removed Ritual Plinth system.
- Stage 03 must target the current 1.8.x registry/data model or a Black Arcana adapter that fails safely when Malum is absent.

## RPG Skill Tree

Black Arcana's own project policy reserves attributes/mastery/perks as progression gates and scaling inputs, not as a casting host. The RPG adapter should answer Black Arcana-owned questions such as `has mastery`, `attribute value`, `perk present` and `record mastery use` without leaking RPG implementation types into the core.

## Host selection rule

Choose the host that already owns the player's mental model:

- Active spell lifecycle -> Iron's when its stable API is sufficient.
- Composable utility/teleport/familiar magic -> Ars when not uniquely forbidden.
- Prepared occult bargains/rites -> Eidolon when supported.
- Souls/spirit economy -> Malum when supported.
- Progression/scaling -> RPG Skill Tree adapter.
- Cross-cutting safety, covenants, domains, persistent IDs and fallback execution -> Black Arcana core.

No host selection is final until Stage 03 verifies a stable integration path for the exact installed 1.21.1 version recorded in `runtime-host-baseline.md`.
