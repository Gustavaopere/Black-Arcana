# Ars Controle 1.6.15 — integration and deduplication rules

Status: `SOURCE-PINNED AUTHORITY MAP / NO BLACK ARCANA ADAPTER APPROVED`

## Authority split

### Ars Nouveau

Retains authority for:

- player mana and Source primitives;
- spell grammar/resolver/cast lifecycle;
- `EntityProjectileSpell` semantics;
- base glyph/augment validation;
- Warp Scroll and Portal infrastructure;
- Ritual Brazier, ritual identity, Source and ritual effects;
- Dominion Wand/IWandable base concepts.

### Ars Controle

Owns:

- its 9 registered spell parts;
- its 4 blocks/6 items and their provider state;
- Warping Spell Prism target/routing/additional Source/chunk-ticket behavior;
- Scryer's Linkage remote reference/capability/redstone delegation;
- Temporal Stability Sensor signal;
- Scroll Holder frame/activation behavior;
- Remote connection state/modes;
- Portable Brazier Relay association/context substitution;
- its C2S/S2C provider packets and optional CC peripherals.

### Black Arcana

Retains authority for:

- one canonical Black Arcana cast pipeline and `ArcanaCastId`;
- Black Arcana cost/replay/cooldown/charges;
- Black Arcana target admission;
- `WorldEffectPolicy`, claims/protection and mutation budgets for Black Arcana effects;
- Arcane Danger, Backlash, Corruption and Strain;
- Black Arcana Stage 06 ritual orchestration;
- Stage 07.04 destination safety/teleport contracts;
- Stage 07.07 Noetic/privacy/observation contracts;
- RPG Skill Tree interaction only through its real sibling boundary.

## Capability dispositions

| Surface | Disposition |
|---|---|
| projectile relocation / cross-dimensional routing | `PROVIDER-OWNED / DO NOT DUPLICATE`; same Ars causal projectile/resolver |
| provider chunk ticket from Warping Spell Prism | `PROVIDER-OWNED EXCEPTION`; never inherit as Black Arcana force-load permission |
| remote block/entity reference storage | `PROVIDER-OWNED`; persisted target is not Black Arcana authorization |
| remote block capabilities/redstone | `PROVIDER-OWNED / UNDERLYING PROVIDER AUTHORITY`; no duplicate item/fluid/energy processing |
| Warp Scroll portal construction | `COMPLEMENTARY TO ARS NOUVEAU`; not a Black Arcana portal provider |
| logical/conditional spell filters | `PROVIDER-OWNED ARS GRAMMAR`; do not create parallel Black Arcana filter grammar from these objects |
| probabilistic Random filter | `PROVIDER-OWNED`; separate from Black Arcana Chaos identity unless Black Arcana proves a distinct semantic delta |
| Precise Delay scheduling | `PROVIDER-OWNED ARS CONTINUATION`; delayed child/continuation remains same causal cast |
| portable ritual relocation | `PROVIDER-OWNED ORIGINAL-RITUAL RELAY`; never double-settle ritual costs/effects/Mastery |
| performance/lag sensing | `PROVIDER-OWNED OBSERVABILITY`; not time magic or Arcane Danger telemetry |
| Remote multiple-area connection | `PROVIDER-OWNED / SAFETY RISK`; no reuse as Black Arcana target enumeration |
| CC peripheral target/telemetry | `OPTIONAL / CURRENTLY ABSENT`; not available as current pack authority |

## Causal rules

1. A Warping Spell Prism redirect is one Ars cast/projectile history. Do not create a second Black Arcana success/kill/Mastery/cooldown/danger event at the exit.
2. Precise Delay schedules continuation inside Ars event/SpellContext machinery. Do not treat the delayed continuation as a new root cast.
3. A Portable Brazier Relay uses the same Ars ritual object while suppressing its normal brazier tick. Do not create a second ritual identity or second Source transaction.
4. Scryer's Linkage delegates the remote capability; the remote provider remains owner of its item/fluid/energy/etc. state.
5. Remote stored endpoints are configuration references, not security/claim facts.

## Safety rules

- Provider force-loading never weakens Black Arcana D019/D032/no-force-load boundaries.
- Black Arcana destructive effects still route through `WorldEffectPolicy` even if invoked near an Ars Controle portal/link/prism.
- Client presentation packets and Remote UI state never become Black Arcana gameplay authority.
- Do not perform global/per-tick Black Arcana scans for Ars Controle targets, relays or links.
- Optional integration absence must fail locally without synthetic replacement behavior.
- No API/hook is assumed safe merely because the implementation class is public.

## Known fail-closed questions

- installed-JAR Source charging for entity-target Warping Spell Prism redirects;
- effective Scryer's Linkage chunk-loading behavior versus declared `load_time` config;
- Remote multi-selection practical bounds under the full pack;
- mixin/event ordering against Ars Nouveau 5.13.1 and sibling Ars addons;
- exact effective server configs/datapacks;
- client and dedicated-server full-modpack behavior.

Until those are tested, no runtime Black Arcana adapter should depend on those semantics.
