# Capability Matrix Delta — Ars Nouveau: Two-Way Portals 2.0.0

Status: `EXACT 2.0.0 RELEASE SURFACE + 1.3.4 PUBLIC SOURCE BASELINE / 2.0.0 BINARY QA PENDING`

| Capability | Current evidence | Black Arcana consequence |
|---|---|---|
| Permanent bidirectional Ars portal pair | exact 2.0.0 publisher page states a Double-Sided Stable Warp Scroll links matching Source Stone frames bidirectionally, including vertical/horizontal and cross-dimension pairs | generic permanent two-way Ars portal creation is occupied; BA spatial magic needs a materially distinct forbidden-magic identity rather than another paired-warp wrapper |
| Regular-portal anti-reentry | exact 2.0.0 publisher page states a three-second re-entry cooldown; public 1.3.4 source baseline implements 60 server ticks for ServerPlayer successful portal teleports | do not create a second cooldown ledger or duplicate teleport suppression around provider portals |
| Pair identity / endpoint lifecycle | 1.3.4 baseline tags Ars PortalTiles with pair id + partner dimension/coordinates and tears down paired endpoints on ordinary frame break | pair ownership remains provider-native; BA must not persist a competing endpoint map for the same portals |
| Nullify one endpoint | exact project description and 1.3.4 baseline expose Portal Nullify Scroll; baseline removes only the contacted regular endpoint | do not reinterpret nullification as a BA global pair delete or replay endpoint destruction |
| Immersive Portals conversion | exact 2.0.0 publisher page advertises optional seamless Immersive mode; 1.3.4 baseline converts an accepted Ars pair to Immersive Portals entities | Immersive Portals owns its portal-engine semantics; BA must not perform a second teleport after the provider/engine settles one |
| Portal rotation / gravity transform | exact publisher page documents Dominion Wand normal/shift rotation modes | generic post-creation orientation control is occupied; gravity behavior must remain provider-engine owned |
| Frame mutation protection | exact 2.0.0 page says 1.21.1 replaces the old Silk Touch replacement flow with Ars Weave blocks, while the same page still carries older Leap/Silk Touch/Break+Extract prose | current frame-mutation details are fail-closed until 2.0.0 binary/source inspection; BA must not bind to the old 1.3.4 mixin implementation |
| Bounded portal geometry | 1.3.4 baseline flood-fills portal blocks with a 1024-block ceiling when inspecting/cleaning connected Ars portals | any BA-owned spatial scan remains independently bounded; provider bounds do not authorize unbounded BA scans |
| Scroll acquisition/reset | 1.3.4 baseline contains two apparatus recipes and one shapeless reset recipe; exact 2.0.0 description confirms crafting a configured double-sided scroll alone clears coordinates | acquisition remains Ars/provider-owned; no duplicate BA unlock/cost ledger |

## Semantic disposition

The installed provider materially occupies **Ars-native permanent paired portals, endpoint nullification, regular-portal anti-loop behavior and optional Immersive Portals conversion**. A darker texture, different particles or a renamed portal spell does not establish a Black Arcana gap.

A Black Arcana spatial mechanic remains valid only if its causal identity is genuinely different — for example a bounded forbidden displacement/domain effect with Black Arcana Corruption/Strain/world-safety semantics — and it must not reuse the provider pair state, cooldown ledger or teleport settlement as if BA owned them.

## Authority / deduplication

- Ars Nouveau owns its portal/warp primitives and Stable Warp Scroll lifecycle.
- Two-Way Portals owns the pair-specific bridge/lifecycle it adds.
- Immersive Portals owns its portal entity/engine semantics when the optional bridge is actually active.
- Black Arcana owns only BA casts/hazards/world effects and must route BA-owned world mutation through `WorldEffectPolicy`.
- One accepted provider teleport settles once. Observers must not issue another teleport for presentation, progression or hazard bookkeeping.
- Client visuals or portal rendering never become teleport authority.
