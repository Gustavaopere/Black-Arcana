# 03.03 — Eidolon: Repraised

## Intent
Make Eidolon the primary occult/ritual presentation layer where its public API/data model permits it.

## Investigate
Ritual registration/extensibility, signs/knowledge, altar/components, sacrifice/item conditions and progression hooks available in the exact 1.21.1 build.

## Rule
If Eidolon lacks a stable public hook for a required grand ritual, implement a Black Arcana ritual engine that consumes/recognizes Eidolon content instead of mixin-patching internals by default.

## Acceptance
Document supported versus unavailable hooks and implement one safe prototype ritual bridge without relying on private internals.
