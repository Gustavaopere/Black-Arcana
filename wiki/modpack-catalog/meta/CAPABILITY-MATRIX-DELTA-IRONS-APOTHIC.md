# Capability Matrix Delta — Iron's Apothic 2.2.2

Status: `CURRENT PHYSICAL MAGIC BRIDGE / EXACT SOURCE-PINNED SUPPORT SURFACE / RUNTIME FAIL-CLOSED`

This file records only overlap relevant to Black Arcana deduplication.

| Iron's Apothic capability | Provider-native meaning | Black Arcana consequence |
|---|---|---|
| School-filtered attribute affix | modifies magic attributes for matching schools | do not add a duplicate school-power settlement layer |
| Spell-level affix | changes effective spell level through Apothic affix state | distinguish progression/perk bonuses from item-affix authority |
| Mana-cost affix | modifies spell mana cost | never charge/refund mana twice for the same modifier |
| Spell-effect affix | reacts to spell heal/damage with mob effects | derived effect is not a new spell identity |
| Spell-trigger affix | casts a referenced Iron's spell on combat/heal/hurt triggers | dedupe by original external spell identity and affix trigger cause |
| Imbued-spell trigger affix | triggers the spell already imbued in an item | preserve item/provider ownership; no parallel imbued-spell pipeline |
| Magic Telepathic | routes drops from magic kills | do not duplicate loot relocation/magnetism settlement |
| Magic staff/spellbook reforge categories | allows Iron's gear in Apothic reforging | keep gear progression separate from spell ownership |
| External-school gem/affix resources | provider-specific school integration such as Geo | similarity of school theme is not a new Black Arcana school/bridge contract |

## Semantic boundary

The 48 spell-oriented affix definitions are support mechanics that reference or trigger external spell identities.

Strict independent spell contribution: **+0**.

## Runtime boundary

The exact source includes recursion/cooldown protections, but current assembled-pack safety remains fail-closed until runtime validation confirms exactly-once settlement across all installed spell providers and combat hooks.
