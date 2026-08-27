# 03.06 — Optional Dependency & Fallback Matrix

## Objective
Define exactly what happens for every integration combination.

## Matrix fields
mod present? compatible API? content enabled? replacement cost/provider? recipe/ritual hidden? datapack condition? startup behavior?

## Rules
- Never crash because an optional mod is absent.
- Never silently make a spell free because its cost provider is absent.
- Disable unavailable content with actionable diagnostics.
- Keep client/server mod-list expectations explicit.

## Acceptance
Automated smoke profiles cover core-only and representative integration combinations chosen by the release dependency policy.
