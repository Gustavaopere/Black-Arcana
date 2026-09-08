# Ars Additions 21.3.0 — Glyphs

Status: `3/3 SOURCE-PINNED / RUNTIME QA PENDING`

Source checkpoint: `Jarva/Ars-Additions@91f102a90dc058cf40e4eac5a67a881e48b856b4`.

`ArsNouveauRegistry.registerGlyphs()` registers exactly three spell parts:

1. [Retaliate](retaliate.md) — Form / cast method, Tier III, default mana 25.
2. [Mark](mark.md) — Effect, Tier III, default mana 25.
3. [Recall](recall.md) — Form / cast method, Tier III, default mana 50.

All three declare no compatible augments in their own classes. Mark is hard-limited to one occurrence per spell. Recall declares Mark as an invalid combination and has explicit Spell Turret behavior registered by the addon.

Ars Nouveau remains authority for composition, mana calculation, resolver execution and learning/config semantics. These pages catalog only the additional provider primitives.
