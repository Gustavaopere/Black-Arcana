# Visual 05.01 — Loadout Editor Presentation

## Purpose

Own the UI/visual half of Stage 05.01 without changing the server-owned loadout contract in `plans/05-casting-ux/🟡-PENDENTE-01-input-loadouts.md`.

## Current baseline

The editor presents synchronized spell metadata, creates a local bounded draft, supports add/remove/clear/apply and paginates for small viewports. The draft is presentation/editing state only; an emitted update is not acceptance.

## Presentation backlog

### Explicit slot awareness

- show slots `1–16` clearly;
- visually distinguish slots `1–8` as eligible for direct quick-cast mappings;
- support bounded reorder affordances while preserving uniqueness;
- never visually claim acceptance until a synchronized server snapshot confirms it.

### Search and filtering

- client-side display-name search may filter only already synchronized entries;
- provider/domain/school filters are permitted only when the synchronized presentation schema exposes those fields;
- never infer categories from resource-id string patterns.

### Iconography

- render `SpellPresentationPayload.Entry.iconId` when the resource resolves safely;
- always retain a text/name fallback;
- missing art is a presentation failure, never spell unavailability;
- icon rendering remains client-only.

### Apply-state communication

Distinguish:

1. draft not submitted;
2. update sent / awaiting authoritative snapshot;
3. authoritative snapshot received.

Explicit rejection feedback, when present, must come from a bounded server result. Absence of immediate local change is not acceptance or denial.

### Draft recovery

A client-only “reset draft to synchronized state” action is allowed before apply. It must not override a newer synchronized snapshot.

## Accessibility/layout

- bounded text at small viewports and large GUI scales;
- keyboard focus must be visible;
- selected/accepted/draft-added/draft-removed states must not rely on color alone;
- translated strings must remain bounded;
- art/resource failure falls back to text without affecting the loadout.

## Validation

Visual-production QA covers small viewport/GUI scale, ordering clarity, keyboard focus, search/filter legibility, icon fallback, apply-state wording and compatibility with the assembled modpack UI stack.
