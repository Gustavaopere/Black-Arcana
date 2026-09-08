# Capability Matrix Delta — Leyline Spellbooks 1.0.3

Scope: provider-level semantic deduplication for installed `leylines-1.0.3.jar` while the complete exact registry remains unavailable.

This overlay does not convert the nine public signature names into a complete spell inventory. Unknown 1.0.3 content is treated as **unknown occupied provider space**, not as evidence of a Black Arcana gap.

| Capability / semantic family | Leyline evidence | Provider authority | Black Arcana disposition | Exactness / blocker |
|---|---|---|---|---|
| Short-range blink + haste | Blink Step is publicly described as vanish/reappear with a burst of haste | Leyline spell semantics; Iron's generic cast substrate | `OVERLAP — DO NOT DUPLICATE GENERIC BLINK+HASTE` | distance, collision safety, duration, values and hooks unverified |
| Linked portal pair | Rift Gate publicly places two linked portals | Leyline portal-pair lifecycle | `PROVIDER-OCCUPIED`; any BA spatial spell needs a distinct forbidden-magic contract | IDs, lifetime, cleanup, dimension rules and portal implementation unverified |
| Return anchor | Anchor Recall publicly marks a place and later returns the caster | Leyline anchor state | `PROVIDER-OCCUPIED`; no parallel BA storage for the same provider action | persistence, replacement, safe-position and dimension rules unverified |
| Temporal slow + self acceleration | Chrono Tether publicly slows what is ahead while accelerating caster | Leyline temporal effect semantics | `OVERLAP`; no second tick/effect/attribute pipeline for provider spell | mechanism, values, area and target filters unverified |
| Brief temporal freeze | Temporal Stutter publicly freezes a foe briefly | Leyline temporal-control semantics | `OVERLAP`; generic time-stop/stun clone blocked | implementation, duration, boss/PvP rules unverified |
| Ground rupture + launch | Fissure publicly ruptures earth and launches enemies upward | Leyline spell semantics | `OVERLAP`; no duplicate rupture/knock-up spell without meaningful delta | damage, area, block modification and knock-up values unverified |
| Charge / spend-power loop | Publisher groups Beam, Ley Blast and Eclipse under a general charges/power statement | Leyline provider state if/where implemented | `PROVIDER-OWNED UNKNOWN STATE`; Black Arcana must not create/read/write a guessed Leyline charge ledger | exact charge resource, ownership, persistence and per-spell mapping unverified |
| Beam | Public name confirmed only | Leyline spell identity | `UNKNOWN SEMANTIC SPACE`; do not infer channel/hitscan/piercing | individual behavior and all quantitative fields unverified |
| Ley Blast | Public name confirmed only | Leyline spell identity | `UNKNOWN SEMANTIC SPACE`; do not infer projectile/explosion/AoE | individual behavior and all quantitative fields unverified |
| Eclipse | Public name confirmed only | Leyline spell identity | `UNKNOWN SEMANTIC SPACE`; do not infer darkness/weather/celestial/AoE | individual behavior and all quantitative fields unverified |
| Night pillar / attunement infrastructure | Publisher describes night-time pillars feeding Leyline Rift progression | Leyline world/progression state | `PROVIDER-OCCUPIED`; BA must not create a second pillar-charge progression for this provider | block IDs, charging formula, persistence and API unverified |
| Bounded wave rifts | Publisher describes Leyline Rifts with waves; 1.0.3 fixes death/abandon/leash/persistence behavior | Leyline encounter lifecycle | `PROVIDER-OCCUPIED`; BA domains do not own rift completion/waves | server storage/networking/multiplayer ownership unverified |
| Rift failure on death | 1.0.3: death fails encounter and denies completion reward/crystal | Leyline encounter authority | `DO NOT INTERCEPT/REWARD IN PARALLEL` | implementation hook unknown |
| Rift abandonment | 1.0.3: >60 blocks collapses active encounter | Leyline encounter authority | `DO NOT ADD SECOND ABANDONMENT STATE` | implementation hook unknown |
| Rift mob leash | 1.0.3: >40 blocks returns wave mobs to arena | Leyline encounter authority | `DO NOT ADD SECOND LEASH` | implementation hook unknown |
| Rift reward / Ley Crystal chance | Publisher states thematic loot/XP/chance of Ley Crystal | Leyline reward/progression authority | `DO NOT DUPLICATE REWARD LISTENER` | chances/tables/IDs unverified |

## Black Arcana school consequences

### Space / spatial magic

Rift Gate and Anchor Recall already occupy generic paired-portal and return-anchor semantics. Presentation differences are not enough to justify duplicate Black Arcana spells. A Black Arcana spatial candidate must demonstrate a different forbidden-magic mechanic, causal contract and state ownership.

### Order

Leyline's time/space control does not automatically make it an Order provider. It does, however, consume several obvious control mechanics that an Order spell might otherwise duplicate. Order still needs its law/seal/constraint identity and must compare against these capabilities before approval.

### Chaos

Leyline Rifts may look chaotic, but they are structured provider-owned encounters. Black Arcana Chaos must not clone their wave lifecycle, abandonment, leash or reward state under different VFX.

### Forbidden Domains

Black Arcana remains authority for its own bounded domains and WorldEffectPolicy. Leyline remains authority for Leyline Rift encounter state. Any future interoperability requires a real exact-version boundary; absent one, integration remains fail-closed.

## Unknown-content rule

The publisher explicitly says the nine signature spells are followed by `and more`. Until the exact 1.0.3 registry is inspectable, semantic deduplication must reserve additional unknown Leyline space. Phase 3 cannot treat an unlisted mechanic as a confirmed gap solely because it is absent from these nine public names.
