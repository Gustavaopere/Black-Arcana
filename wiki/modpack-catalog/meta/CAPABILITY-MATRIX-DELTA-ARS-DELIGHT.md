# Capability Matrix Delta — Ars Nouveau's Flavors & Delight 2.2.2

Status: `SOURCE-PINNED PROVIDER DELTA / CURRENT-HOST RUNTIME QA PENDING`

| Capability | Current Ars Delight coverage | Black Arcana consequence |
|---|---|---|
| Ars-themed food progression | 42 base `ADFood` entries convert Ars ingredients/mobs/fruits into food, drinks, jams and dishes | generic magical food that merely reproduces Ars buffs is occupied; BA food needs a distinct forbidden-magic consequence or ritual identity |
| Wilden/Chimera harvesting | provider global-loot modifiers add meat/horn rewards for exact mob/tool conditions | do not duplicate the same loot settlement through a BA death observer |
| Heal → mana | `flourishing` converts confirmed healing into Ars mana through Ars `CapabilityRegistry` | Ars mana remains authority; BA must not mirror/refund a second mana gain for the same heal |
| Heal → absorption | `synchronized_shield` converts healing into bounded absorption under provider config | do not replay the same heal as a second BA shield proc |
| Spell damage → freezing | `freezing_spell` reacts to Ars `SpellDamageEvent.Post` | the freezing child effect is a descendant of that Ars damage event, not a second independent BA cast/proc |
| Wilden spell amplification | `wilden` changes Ars spell damage, max mana and mana regeneration through Ars events | no parallel BA copy of these Ars statistics or multiplicative duplicate around the same provider calculation |
| Enchanter's Knife | Farmer's Delight knife + Ars caster-tool behavior casts a scribed touch spell on melee hit | melee + provider spell settlement must remain one provider-native causal action; BA may observe only through a real boundary |
| Ars spells on Cutting Board | `EffectResolveEvent.Pre` maps Cut/Crush/Fell/Break to Farmer's Delight board processing and cancels the handled effect | respect provider cancellation; never replay the original Ars effect after the board transaction settles |
| Jelly projectile infusion | Ars spell projectiles can pick up provider jelly context; `EffectInfuse` consumes that attachment as potion contents | spell context/potion settlement remains Ars/provider-owned; no BA duplicate attachment or potion serializer |
| Drygmy farming tools | mixin lends an adjacent pedestal tool to Ars `ANFakePlayer`, optionally damages the source stack, then removes the fake-player item | do not create a second Drygmy/tool-durability settlement or depend on this internal mixin as a BA integration hook |
| Farmer's Delight feasts/pies/cabinet | provider blocks reuse FD serving/bite/cabinet contracts | FD/provider block state and loot are authoritative; no parallel BA servings ledger |
| Ars Elemental optional content | conditional Flashpine content and `lightning_curse` react through Ars Elemental when loaded | provider-owned optional content may be observed only when the exact provider is present/compatible |
| Thirst optional bridge | source can register Ars Delight drinks through the legacy Thirst API when enabled | current `thirst` implementation must be runtime-validated; mod-id similarity alone does not prove API compatibility |

## Semantic disposition

Ars Delight materially occupies **Ars Nouveau × Farmer's Delight magical cuisine, Wilden/Chimera food progression, Ars-aware culinary processing and its own food-driven spell/heal modifiers**. Recoloring food, changing names or adding darker particles does not create a Black Arcana gap.

Black Arcana remains free to implement forbidden consumables or ritual meals only when they have a genuinely Black Arcana-owned causal identity — for example explicit Corruption/Strain/Backlash contracts or ritual preparation — without taking ownership of Ars mana, Farmer's Delight serving state, Ars spell resolution or provider loot.

## Authority/dedup rules

- Ars mana, spell resolution and Ars spell events settle once through Ars/provider paths.
- Farmer's Delight food, feast, cutting-board and cabinet state settles once through FD/provider paths.
- Ars Delight owns only the crossover content/effects it registers; it is not a general progression or casting authority.
- Provider child effects from heal/spell-damage events remain descendants of their originating event and are not independent BA proc opportunities.
- RPG Skill Tree may gate/progress through a real contract but does not become Ars Delight, Ars or Farmer's Delight runtime authority.
- Black Arcana must not couple to Ars Delight mixin internals as an interoperability API.
