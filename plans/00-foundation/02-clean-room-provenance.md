# 00.02 — Clean-room Provenance

## Objective
Make it auditable that Black Arcana is an independent implementation.

## Rules
- Do not decompile or copy Mahou Tsukai implementation/source/assets.
- Reference observable mechanics through public descriptions, gameplay, documentation and user-authored specifications.
- Record each derived concept as: reference behavior → desired Black Arcana behavior → original implementation notes.
- Original names, textures, particles, sounds, models and UI are required.
- Third-party APIs may be used according to their licenses/documentation.

## Deliverables
- `docs/provenance/README.md` template.
- Source/reference ledger format with URL/date/type and what was learned.
- Explicit prohibited-input list for contributors/agents.

## Acceptance
A new contributor can implement a Stage 07 spell from the Black Arcana specification without accessing Mahou Tsukai code/assets.
