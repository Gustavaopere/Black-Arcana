# Black Arcana — Visual Production

This directory is the canonical planning area for Black Arcana presentation work that is intentionally separated from the numbered runtime-engineering stages.

## Scope

This area owns mod-specific presentation requirements for:

- UI screens and information architecture;
- contextual HUD and tooltips;
- iconography and texture/resource resolution;
- models and render-only representation;
- animations and camera/presentation motion;
- particles, VFX, shaders and telegraphs;
- sound/audio feedback;
- visual accessibility, contrast, reduced-motion/reduced-flash and low-particle presentation;
- presentation-only onboarding/help and visual validation.

It does **not** own gameplay authority. Casting, networking, persistence, costs, cooldowns, targeting, progression, Arcane Danger, ritual settlement, world mutation and provider causality remain in the numbered Black Arcana engineering plans.

## Runtime/presentation boundary

A numbered engineering plan may require a bounded server/client contract such as “emit a cast-result event”, “expose a synchronized icon id”, “provide a render-safe projection identity” or “support a cosmetic fallback”. That requirement remains in the engineering plan because runtime correctness depends on it.

The visual-production plan owns how that legitimate state is communicated: layout, art, icon, texture, model, animation, particle, shader, sound, wording hierarchy and presentation QA.

Presentation must never become a second gameplay authority. Missing or broken presentation assets fail visually safe and do not change cast validity or server state.

## Relationship to minecraft-mod-factory

`Gustavaopere/minecraft-mod-factory` is the source of truth for reusable mod/asset production infrastructure, standards, schemas, validators, templates, tooling, CI and source-art pipeline rules.

Black Arcana remains the source of truth for Black Arcana-specific product requirements and runtime-facing presentation contracts.

In practical terms:

- Black Arcana specifies **what must be communicated and which runtime state is available**;
- minecraft-mod-factory specifies **how reusable assets/pipelines are authored, validated and integrated**;
- source formats such as `.bbmodel` and reusable art tooling belong to the Factory boundary;
- final Black Arcana runtime resources remain subject to Black Arcana clean-room/provenance and release rules.

No asset, model, sound, animation or protected third-party presentation may be copied from Mahou Tsukai or another provider without separately verified compatible rights and recorded provenance.

## Scheduling rule

`visual-production/` is intentionally not a numbered stage. Its backlog does not block the numerical runtime implementation sequence merely because presentation polish is unfinished.

A numbered stage is blocked only by presentation work when a reviewed runtime contract explicitly requires that presentation for safety, accessibility of a gameplay-critical telegraph, or release acceptance. Otherwise, presentation remains a deferred visual-production tranche.

## Structure

- `05-casting-ux/` — UI/HUD/input-surface presentation, iconography, targeting presentation, inspection, audiovisual feedback and onboarding.
- `05a-arcane-danger/` — danger/resistance/corruption/strain presentation.
- `06-rituals/` — ritual visual/audio production requirements when they exist.
- `07-spell-domains/` — spell-family models/textures/VFX/audio/animation requirements when they are specified.
- `07a-arcane-polarity-fusion-metamagic/` — sigils, ritual presentation and polarity/fusion presentation.

See `MIGRATION-MAP.md` for the extraction audit and source-to-destination mapping.
