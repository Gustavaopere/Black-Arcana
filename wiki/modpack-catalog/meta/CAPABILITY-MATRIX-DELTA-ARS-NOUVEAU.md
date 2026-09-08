# Capability Matrix Delta — Ars Nouveau 5.13.1

Status: `PHASE 2P / SOURCE-PINNED PROVIDER DELTA / RUNTIME QA PENDING`

Provider authority in this file is restricted to `ars_nouveau` core at exact source pin `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`. Addons remain separate providers.

| Capability surface | Ars Nouveau evidence | Disposition for Black Arcana |
|---|---|---|
| compositional spell grammar | 5 Forms + 67 Effects + 13 Augments; provider `SpellContext`/resolver execution | `EXISTING PROVIDER AUTHORITY`; do not build a second Ars grammar/cast pipeline |
| player spell resource | Ars player mana, equipment modifiers and provider spell costs | `EXISTING PROVIDER AUTHORITY`; no second mana charge/conversion by Black Arcana |
| world/automation resource | Source is distinct from player mana | `EXISTING PROVIDER AUTHORITY`; do not conflate Source with player mana or Black Arcana resources |
| glyph acquisition/learning | 85/85 provider-generated recipes, tier/default recipe XP and server-owned learning path cataloged | `EXISTING PROVIDER AUTHORITY`; no duplicate unlock ledger |
| persistent/child spell execution | Linger, Wall, Orbit, Reset, Delay/Rewind and related continuations create provider-owned child/delayed contexts | `CAUSALITY BOUNDARY`; one root provider cast must not fan out into duplicate costs/mastery/danger settlements |
| world mutation | Break, Place Block, Conjure Water, Freeze, Evaporate, Exchange, Intangible, Fell/Harvest/Grow and other block/fluid Effects | `EXISTING PROVIDER AUTHORITY`; observe provider result only; independent Black Arcana destruction remains behind `WorldEffectPolicy` |
| force/control/fields | Pull, Gust/Knockback, Launch, Gravity, Snare, Rune, Bubble, Wall, Burst and related Effects | `STRONG OVERLAP`; future Order/control content requires a distinct law/seal/contract mechanic, not generic immobilization/geometry |
| randomness/chaos | core `Randomize` augment | `OVERLAP`; generic randomness is not a unique Chaos identity |
| time/space | Blink, Exchange, Rewind, Delay and provider continuations | `STRONG OVERLAP`; future time/space magic requires a materially different bounded contract |
| divination/sensing | Sense Magic | `OVERLAP`; future Black Arcana divination must exceed generic magical detection without stealing provider state |
| healing/abjuration | Heal, Dispel, Slowfall/Invisibility support and related primitives | `OVERLAP`; no generic heal/dispel duplication without a distinct forbidden-magic identity |
| curse/death | Hex, Wither, Summon Undead, Summon Vex and combat summons | `OVERLAP`; Black Arcana Souls & Death must preserve its own soul/corruption/ritual contracts rather than relabel Ars summons/debuffs |
| fire/infernal | Ignite, Flare, Firework plus elemental interactions | `OVERLAP`; future Infernal content needs mechanics beyond ordinary ignition/fire burst |
| mobility | Leap, Glide, Blink, Bounce, Slowfall, Launch | `OVERLAP`; movement magic must not be duplicated solely by presentation |
| ritual system | 24/24 source-cataloged rituals | `EXISTING PROVIDER AUTHORITY`; ritual execution/resources/state remain Ars-owned |
| familiar system | 6/6 source-cataloged familiar mechanics | `EXISTING PROVIDER AUTHORITY`; do not treat Ars familiars as Black Arcana soul/familiar ownership without a real bridge |
| Threads/perks | 20/20 perks/Threads + 12/12 armor slot providers | `EXISTING PROVIDER AUTHORITY`; RPG Skill Tree/Black Arcana must not duplicate provider Threads or modifier settlement |

## Cross-provider rules

1. Namespace/provider ownership is preserved: Ars addon glyphs are not promoted to `ars_nouveau` core merely because the official guide displays them together.
2. Provider VFX/particles are presentation evidence only; they do not establish Black Arcana spell provenance or gameplay authority.
3. A future adapter may classify/observe a provider cast only through a real exact-version seam. It must not replay effects, consume provider resources twice or convert child contexts into independent casts.
4. Failure to prove the relevant provider hook is fail-closed for the integration; it is not permission to infer state from items, visuals or names.

## Remaining validation

Runtime/config values, claim/protection interactions, cross-mod event ordering, client presentation and full 612-entry dedicated-server/modpack QA remain separate from this source-catalog delta.
