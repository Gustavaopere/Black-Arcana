# Ars Creo 5.4.0 — integration and deduplication rules

Status: `SOURCE-PINNED AUTHORITY MAP / NO BLACK ARCANA ADAPTER APPROVED`

1. Create owns contraption identity, movement/actors, kinetic/stress and display/fluid infrastructure.
2. Ars Nouveau owns spell grammar/resolution, Source accounting, turret spell data, portal teleport semantics, ritual identity/effects and Potion Jar contents.
3. Ars Creo owns only the bridge translating those provider states into moving Create behavior.
4. A moving turret spell is one Ars spell action. Do not create a Black Arcana root cast, second cost, cooldown, Mastery, Arcane Danger, Corruption or Strain settlement from the same action.
5. `ContraptionCaster` reports caster type `OTHER`; do not assign player ownership/Mastery from proximity, interaction history or contraption ownership without an explicit causal contract.
6. Source on a contraption remains Ars Source. Do not mirror, convert or settle it in a Black Arcana resource ledger.
7. Creative Source Jar behavior remains provider-owned infinite Source and must not authorize infinite Black Arcana resources.
8. Moving Portal behavior delegates to Ars `PortalTile`; do not replay teleport or infer that a destination is valid for a Black Arcana displacement spell.
9. Moving Ritual behavior uses the same serialized Ars ritual identity/state and a stand-in brazier. Do not duplicate ritual effects/procs; compatibility is per ritual and QA-gated.
10. Potion Jar FluidHandler exposes Ars contents to Create transport. Do not duplicate fill/drain operations based on observed fluid change.
11. Display Sources are observational/presentation surfaces, never gameplay authority.
12. Registered S2C packets are client-state surfaces; no Black Arcana authority is inferred from them.
13. Aeronautics/Sable/moving-sublevel interoperability requires the actual provider boundary; thematic compatibility with Create contraptions is insufficient.
14. Black Arcana destructive/world-changing effects still use `WorldEffectPolicy`; provider movement or ritual support is not an exemption.
15. Any future adapter must bind to an exact-version supported seam and fail closed if that seam is absent or ambiguous.