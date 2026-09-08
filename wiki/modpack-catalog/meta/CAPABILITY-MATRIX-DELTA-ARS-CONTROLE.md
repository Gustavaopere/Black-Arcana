# Capability Matrix Delta — Ars Controle 1.6.15

Status: `PHASE 2R / SOURCE-PINNED PROVIDER DELTA / RUNTIME+PACK QA PENDING`

Provider authority in this file is restricted to installed `ars_controle` 1.6.15 and factual source pin `Vonr/Ars-Controle@ecbb83ba512bc9ca7a025556fb9c62dbd32b6430`.

| Capability surface | Ars Controle evidence | Disposition for Black Arcana |
|---|---|---|
| logical/conditional spell grammar | 8 registered filters extend Ars `AbstractFilter`; validator mixin enforces unary/binary filter structure | `PROVIDER-OWNED / DO NOT DUPLICATE`; these remain Ars spell grammar, not a parallel Black Arcana grammar |
| probabilistic spell control | Filter Random resolves at 50% base and scales through Ars Amplify/Dampen stats | `PROVIDER-OWNED`; generic randomness is already occupied and does not define Black Arcana Chaos identity |
| delayed continuation | Precise Delay schedules the remaining Ars spell through `DelayedSpellEvent`/`SpellContext.delay` | `PROVIDER-OWNED CAUSAL CONTINUATION`; delayed resolution is not a new Black Arcana root cast |
| projectile relocation / cross-dimensional routing | Warping Spell Prism preserves the Ars resolver/projectile state while recreating the projectile in another level when needed | `PROVIDER-OWNED / DO NOT DUPLICATE`; no second cast/cost/Mastery/Arcane Danger settlement |
| provider force loading | Warping Spell Prism adds a destination region ticket when configured `load_time>0`, default 600 ticks | `PROVIDER-OWNED EXCEPTION`; Black Arcana no-force-load rules remain unchanged |
| routed Source cost | Prism computes distance/dimension Source requirement; entity-hit execution appears to return before later deduction | `UNKNOWN / FAIL-CLOSED` for entity-target charging until runtime verified; never synthesize a compensating Black Arcana charge |
| remote block reference | Scryer's Linkage persists a `GlobalPos` target and Remote can persist block/entity references | `PROVIDER-OWNED`; persisted endpoint state is not Black Arcana target/claim authorization |
| remote block capabilities | Linkage delegates NeoForge block capabilities through `BlockCapabilityCache` with class blacklists and recursion guard | `UNDERLYING PROVIDER AUTHORITY`; no duplicate item/fluid/energy/resource processing |
| remote redstone/comparator | Linkage forwards signal/direct/analog/connectivity and contextual comparator behavior | `PROVIDER-OWNED`; not a magical observation/privacy seam for Stage 07.07 |
| remote chunk loading via Linkage | config declares `load_time=600`, but audited 1.6.15 Linkage paths do not show the Prism-style ticket operation | `UNKNOWN / FAIL-CLOSED`; do not claim force loading or inherit permission |
| Warp Scroll portal formation | Scroll Holder creates Ars `PortalBlock`/`PortalTile` from valid Ars Warp Scroll data and charges provider Source on fresh activation | `COMPLEMENTARY TO ARS NOUVEAU`; Black Arcana Stage 07.04 remains independent authority |
| server performance sensing | Temporal Stability Sensor maps average server tick time to analog output every 10 ticks | `PROVIDER-OWNED OBSERVABILITY`; not time magic, cooldown authority or Arcane Danger telemetry |
| provider configuration Remote | Remote stores lock/selection modes and endpoint references; C2S mode packets mutate server-side main-hand Remote only | `PROVIDER-OWNED`; client UI/config state never becomes Black Arcana authority |
| Remote multiple-area connection | source iterates `BlockPos.betweenClosed` between corners without an explicit visible volume cap | `PROVIDER-OWNED / SAFETY RISK`; Black Arcana must use its own bounded targeting contracts |
| portable ritual execution | Portable Brazier Relay suppresses normal brazier tick and recontextualizes the same Ars ritual object to the carrier | `PROVIDER-OWNED ORIGINAL-RITUAL RELAY`; never duplicate ritual identity, Source, Mastery or proc settlement |
| ritual worldgen exclusion | relay blocks ConjureBiome/Structure/FeaturePlacement ritual classes plus provider blacklist tag | `PROVIDER SAFETY BOUNDARY`; does not replace Black Arcana `WorldEffectPolicy` |
| optional CC telemetry/control | ComputerCraft peripherals exist for Prism and Scroll Holder behind mod-id gate | `OPTIONAL / CURRENTLY ABSENT`; no current pack authority and no fallback |

## Cross-provider rules

1. Ars Nouveau remains authority for mana, Source primitives, spell resolver/grammar, Warp Scroll/Portal and ritual identity/effects.
2. Ars Controle routing, filtering, delay and relay operations remain inside the original Ars causal action; Black Arcana must not double-charge resources, Mastery, cooldowns, Arcane Danger, Corruption or Strain.
3. Provider `GlobalPos`/UUID/data-component state is configuration state, not a Black Arcana security/claim/target fact.
4. Provider force-loading is not precedent for Black Arcana force-loading.
5. Scryer's Linkage delegates the actual remote capability; the remote mod/system remains owner of the underlying inventory/fluid/energy/etc. transaction.
6. Client payloads/highlights are presentation/control requests, never Black Arcana gameplay authority.
7. Any future adapter requires an exact-version supported seam. Internal public classes, attachments, mixins or item NBT/components are insufficient by themselves.

## Remaining validation

Installed-JAR behavior against Ars Nouveau 5.13.1, effective configs/datapacks, event/mixin ordering with the full Ars addon set, client behavior and full dedicated-server/modpack QA remain separate from this source-catalog delta.
