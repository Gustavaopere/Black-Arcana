# Eidolon: Repraised — Black Arcana Integration Rules

## Mandatory rules

1. **Provider-native cost first.** Never debit Eidolon mana from Black Arcana for a cast already accepted/settled by Eidolon.
2. **Provider-native progression first.** Reputation, research, soul and altar state remain Eidolon authority.
3. **Single causal cast.** `SpellCastEvent.Pre/Post` observations must deduplicate against world/effect observations for the same cast.
4. **Fail closed on settlement ambiguity.** If source inspection does not prove cost settlement, do not assume free cast and do not patch it externally.
5. **No effect replay.** Do not reapply provider effects such as Chilled, Vulnerable, Necrotic or Consecrated.
6. **No SignSequence reinterpretation.** The provider resolves spell identity from signs and recipes.
7. **No prayer flattening.** Prayer is a deity/effigy/altar/cooldown transaction, not a generic spell cast.
8. **No implicit resource unification.** Eidolon mana, soul and reputation remain distinct from Iron's mana, Ars Source, Goety Soul Energy, Malum spirits and Black Arcana resources.
9. **Respect data-driven chants/conversions.** Recipe-manager resolution is canonical.
10. **Dedicated-server validation required** before using any client-visible effect as authoritative progression evidence.

## Safe observation candidates

Subject to runtime validation, the cleanest provider-native hook for ordinary static spell observation is the Eidolon `SpellCastEvent.Post`, paired with a per-cast deduplication guard. For canceled/attempted casts, `SpellCastEvent.Pre` is available but should not be counted as a completed action.

Prayer/resource/progression integrations may require observing post-state instead of deriving deltas from spell identity alone, because altar power, capacity, reputation and config can change the outcome.