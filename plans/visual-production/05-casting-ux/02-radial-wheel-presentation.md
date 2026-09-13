# Visual 05.02 — Radial Wheel Presentation

## Goal

Provide a compact combat selector without permanent screen occupation. Runtime selection authority remains in Stage 05.

## Current presentation baseline

Normal viewports use bounded cards around the ring with slot number, short display name, selected/hovered emphasis, center title, synchronized hazard/preflight context and a page indicator. Compact viewports may reduce cards to slot identity and expose focused spell identification separately.

## Geometry requirements

Normal viewport:

- maximum eight visible sectors per page;
- readable center;
- no card overlap;
- hit regions visually agree with sector/card placement;
- text stays inside the viewport.

Small viewport:

- preserve slot identity, selected/focused feedback, usable hit regions, focused spell identification and close/page/select affordances;
- reduce decoration/text density before shrinking hit targets beyond usability.

Ultrawide:

- keep the radial centered and bounded rather than scaling radius with total monitor width.

## Presentation backlog

- resolve synchronized spell icons with text fallback;
- compact cooldown/readiness affordance only after valid synchronized spell→cooldown-group mapping exists;
- concise danger marker plus text/symbol redundancy;
- provider resource/cost only from an approved bounded server/provider presentation contract;
- visually explicit page state and selected-page continuity;
- keyboard focus/selection presentation without turning selection into casting;
- no nested hierarchy unless evidence shows two-page paging is insufficient and hierarchy metadata is server-authored.

## Semantic state

Keep independent visual roles for selected, focused/hovered, ready/cooldown, dangerous, preview unavailable and missing art. Do not collapse them into one color code.

## Accessibility

Important state must use shape/icon/text/outline in addition to color. Reduced motion and low-particle preferences may simplify decoration but cannot obscure gameplay-critical telegraphs.

## Visual QA

Validate at 854×480, 1920×1080 and 3440×1440 plus supported GUI scales, both toggle/hold interaction styles, both pages, mouse/keyboard navigation, missing-art fallback and color-independent state distinction.
