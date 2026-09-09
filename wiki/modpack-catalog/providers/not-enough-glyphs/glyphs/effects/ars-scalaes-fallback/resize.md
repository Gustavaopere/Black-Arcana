# Resize

- Registry: `ars_scalaes:resize`
- Class: NEG `EffectResize`
- Current NEG source registers this fallback unconditionally; Ars Scalaes itself is absent from the physical pack.
- Tier: **II**; default mana: **100**; school: Manipulation
- Semantics: Amplify grows, Dampen shrinks and reset/no-amplification paths manipulate provider grow/shrink state using vanilla `Attributes.SCALE`.
- Acquisition: Manipulation Essence + Abjuration Essence + Brown Mushroom.
- Config duration helper semantics remain inherited/provider-owned where the source arguments/literals are not safely reinterpretable.
- Boundary: external resize capability; no BA duplicate scale authority.