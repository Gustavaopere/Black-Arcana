# Clean-room provenance

Black Arcana is implemented from Black Arcana-owned specifications, public API documentation, and observable/publicly documented behavior. Mahou Tsukai is a design reference only.

## Allowed inputs

- User-authored Black Arcana design specifications and decisions.
- Public mod documentation, public changelogs, public API documentation and public gameplay descriptions.
- Clean-room observation of behavior such as costs, targeting shape, timing, progression role, and player-visible effects.
- Third-party APIs and source code only where their license permits the intended use, with attribution/notice requirements recorded before reuse.

## Prohibited inputs

- Decompiling or copying Mahou Tsukai implementation code.
- Copying Mahou Tsukai textures, models, sounds, particles, GUI artwork, localization text, spell prose, or other assets.
- Copying strongly derivative proprietary names when an original Black Arcana identity is required.
- Treating a compatible implementation found in another mod as automatically reusable without license review.

## Required provenance entry

Before implementation derived from an external reference, add a row to `REFERENCE_LEDGER.md` containing: date accessed, source URL/project, reference type, what was learned, what Black Arcana specification resulted, whether source code/assets were consulted, and applicable license/notice notes.

A Stage 07 spell must be implementable from the Black Arcana specification and this ledger without requiring Mahou Tsukai code or assets.
