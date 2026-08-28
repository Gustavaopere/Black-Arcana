# Candidate host viability matrix — NeoForge 1.21.1

Status: PREPARATORY. This matrix converts Stage 01 thematic host preferences into explicit engineering confidence levels. It does **not** authorize adapter implementation before Stage 03.

Runtime baseline: see `runtime-host-baseline.md`.

## Confidence levels

- `CORE`: Black Arcana must own the authoritative state/effect/safety contract. Host mods may provide presentation, invocation or resources, but the mechanic cannot depend on undocumented host internals.
- `PUBLIC_API`: the host role needed by Black Arcana is covered by a public/documented extension surface at planning level. Stage 03 still compiles/tests the exact installed version.
- `PROBE`: the host clearly has the desired gameplay concept/resource, but Stage 01 has not proven a stable extension seam for the exact required operation. Stage 03 must inspect supported source/API and prototype before the host becomes a dependency.
- `FALLBACK`: if the preferred optional host cannot support the contract safely, Black Arcana keeps the mechanic in core or chooses another documented host instead of reaching into private internals.

A candidate may combine levels because Black Arcana can own the effect while Iron's owns spell invocation, for example.

## Dominion / wards

| Candidate | Authoritative owner | Host surface | Confidence | Stage 03 requirement / fallback |
| --- | --- | --- | --- | --- |
| Exclusion Ward | Black Arcana ward + permission runtime | Eidolon ritual presentation optional | CORE + PROBE | Probe whether Eidolon can invoke an external prepared ritual cleanly. If not, Black Arcana supplies its own ritual surface. |
| Gravitic Ward | Black Arcana bounded force/eligibility policy | Iron's cast trigger optional | CORE + PUBLIC_API | Register as Iron's spell only if stable API lifecycle is sufficient; otherwise direct Black Arcana cast. |
| Vigil Ward | Black Arcana ward runtime | Eidolon presentation optional | CORE + PROBE | No external host required. Eidolon integration is cosmetic/invocation enhancement only. |
| Malison Constellation | Black Arcana node graph, curse selection and budgets | Eidolon grand-ritual presentation optional | CORE + PROBE | Never implement graph execution inside undocumented Eidolon internals. Fallback is native Black Arcana ritual network. |
| Hexward Aegis | Black Arcana barrier entity/state and damage policy | Iron's active spell | CORE + PUBLIC_API | Iron's owns invocation/mana/cooldown; Black Arcana owns barrier integrity and compatibility logic. |
| Covenant | Black Arcana persistent UUID permission state | Eidolon ceremony optional | CORE + PROBE | Covenant must work without Eidolon. Probe only for ritual UX hooks. |
| Inner Dominion | Black Arcana session journal, participant state, return safety and world policy | Iron's trigger or ritual presentation optional | CORE + PUBLIC_API/PROBE | Invocation may use Iron's public spell API; any ritual host is optional. Domain/session logic never moves into another mod. |

## Liminal

| Candidate | Authoritative owner | Host surface | Confidence | Stage 03 requirement / fallback |
| --- | --- | --- | --- | --- |
| Threshold Gate | Black Arcana endpoint/permission/throughput safety | Ars spatial integration preferred | CORE + PROBE | Determine whether installed Ars 5.13.0 exposes a supported extension route for the desired paired-threshold behavior. If not, keep Black Arcana-owned and avoid cloning generic Warp travel. |
| Veilstep Reflex | Black Arcana reaction gate and safe-position search | Iron's or Ars resource/invocation | CORE + PUBLIC_API/PROBE | Iron's active/passive integration is preferred if expressible publicly. Ars is optional until a supported hook is proven. |
| Anchor Recall | Black Arcana projectile ownership/age/safe-landing state | Iron's or Ars cast surface | CORE + PUBLIC_API/PROBE | Use Iron's public spell registration if suitable; Ars-specific ownership hooks require probe. |
| Reciprocal Transposition | Black Arcana atomic endpoint transaction | Ars presentation/resource preferred | CORE + PROBE | Both endpoints and swap mutation remain Black Arcana-owned. Ars may provide source/visual language only if supported. |
| Vector Reversal | Black Arcana velocity/boss/PvP caps | Iron's active spell | CORE + PUBLIC_API | Straightforward Iron's-hosted spell with Black Arcana effect implementation. |

## Noetic

| Candidate | Authoritative owner | Host surface | Confidence | Stage 03 requirement / fallback |
| --- | --- | --- | --- | --- |
| Astral Severance | Black Arcana projection session/body vulnerability/return logic | Eidolon flavor optional | CORE + PROBE | Must function without Eidolon. No camera/session state may depend on undocumented host behavior. |
| Namescry | Black Arcana privacy policy, target resolution and perception payload | Eidolon ritual presentation optional | CORE + PROBE | Probe ritual invocation only. Remote perception remains server-owned and never force-loads. |
| Gaze of Stillness | Black Arcana LOS/facing/CC diminishing-return policy | Iron's channeled spell | CORE + PUBLIC_API | Iron's provides cast lifecycle; Black Arcana owns control semantics. |
| Nullifying Gaze | Black Arcana nullifiable/protected tags and adapters | Iron's channeled spell | CORE + PUBLIC_API | No reflection/private host mutation. Each affected mod mechanic requires explicit adapter/tag support. |
| Occult Appraisal | Black Arcana metadata whitelist/privacy | Iron's presentation optional | CORE + PUBLIC_API | Can be direct Black Arcana interaction; Iron's spell shell is optional. |
| Borrowed Sight | Black Arcana camera/session recovery | Ars familiar ownership/target resolution | CORE + PROBE | Confirm supported access to owned familiar identity/state in installed Ars. If unavailable, omit Ars-target mode rather than access internals. |
| Pact Sanctuary | Black Arcana aura scheduling and hostility policy | Ars familiar center/ownership | CORE + PROBE | Confirm supported familiar lifecycle/ownership hooks. Without them, candidate remains unavailable or uses a Black Arcana-owned bonded entity later; do not duplicate Ars familiars. |

## Eidetic Arsenal

| Candidate | Authoritative owner | Host surface | Confidence | Stage 03 requirement / fallback |
| --- | --- | --- | --- | --- |
| Ephemeral Tempering | Black Arcana temporary modifier profile and restoration | Iron's invocation; Malum spirit cost optional | CORE + PUBLIC_API/PROBE | Iron's spell shell is supported at planning level. Malum resource extraction/payment requires probe. |
| Echo Armament | Black Arcana `ProjectedWeaponProfile`, ephemeral item/entity rules | Iron's cast surface | CORE + PUBLIC_API | No arbitrary live ItemStack/NBT copy. Iron's only hosts invocation/scaling where useful. |
| Rift Blades | Black Arcana spectral projectile/gap-close safety | Iron's spell | CORE + PUBLIC_API | Preferred first integration proof because host responsibility is narrow and public spell registration is documented. |
| Spectral Arsenal | Black Arcana sanitized profile registry, projectile budget and damage caps | Iron's spell/channel | CORE + PUBLIC_API | Good Stage 03/07 integration candidate once profile system exists. |
| Oathforged Ascension | Black Arcana sacrifice transaction, enhancement ledger and caps | Eidolon ritual UX + Malum spirit contribution optional | CORE + PROBE | Both hosts must be probed independently. Native Black Arcana grand ritual is fallback; enhancement accounting always remains core. |

## Sanguine / Sepulchral / Cinder

| Candidate | Authoritative owner | Host surface | Confidence | Stage 03 requirement / fallback |
| --- | --- | --- | --- | --- |
| Sanguine Harvest | Black Arcana target/yield/anti-farm accounting | Eidolon ritual UX + Malum spirit semantics optional | CORE + PROBE | Probe both; do not require either to preserve candidate behavior. |
| Sympathetic Wound | Black Arcana damage-link recursion marker/caps | Malum/Eidolon resource or ritual flavor optional | CORE + PROBE | Core damage event contract first; optional hosts only provide costs/presentation after supported seams are proven. |
| Blood Price | Black Arcana transactional `CostProvider` | none required | CORE | Directly supported by Foundation reservation/commit/refund seam. External host resources may compose with it in Stage 02/03. |
| Law of Recurrence | Black Arcana damage-family classifier and bounded state | Iron's cast/status presentation optional | CORE + PUBLIC_API | Iron's invocation is safe planning assumption; resistance/vulnerability logic remains Black Arcana-owned. |
| Equilibrium Rite | Black Arcana health-transfer transaction and boss/PvP policy | Iron's cast or Eidolon ritual presentation | CORE + PUBLIC_API/PROBE | Active spell shell can use Iron's; Eidolon ritual route requires probe. Health transaction never delegated. |
| Mortal Ledger / Soul Anchor | Black Arcana death-prevention state, anchor cap and atomic consume | Malum spirits strongly preferred | CORE + PROBE | Stage 03 must prove a supported way to observe/use Malum spirit value without depending on private implementation. If impossible, either use a clearly separate Black Arcana fallback resource by config or gate the Malum-enhanced mode. |
| Spirit Sight | Black Arcana visibility policy for its own traces | Malum/Eidolon spirit visibility integration | CORE + PROBE | Add host-specific visibility only through supported identifiers/events/data. Unknown hidden entities are never exposed generically. |
| Black Pyre | Black Arcana spread graph, temporary cells, cleanup and `WorldEffectPolicy` | Iron's active spell + Malum spirit amplification optional | CORE + PUBLIC_API/PROBE | Iron's is suitable for invocation. Malum amplification is optional until resource adapter is proven. |

## Stage 03 probe queue

The following probes are required before any `PROBE` route becomes canonical:

### Iron's `3.16.3`
1. Compile using the documented API artifact only.
2. Register one inert Black Arcana test spell through the public registry path.
3. Verify mana/cooldown/spell-power access required by a host adapter without importing non-API packages.
4. Verify dedicated-server startup with Iron's present and Black Arcana present.
5. Verify Black Arcana still starts when Iron's is absent if dependency remains optional.

### Ars Nouveau `5.13.0`
1. Identify supported addon/API entry points in the exact installed release.
2. Probe custom spell/glyph or event hooks only if they add unique Black Arcana behavior; do not rebuild Blink/Warp.
3. Determine whether owned familiar identity/lifecycle can be accessed through supported public types/events for Borrowed Sight/Pact Sanctuary.
4. Determine whether source/resource payment can be adapted atomically to `CostReservation`.
5. Repeat against `5.13.1` only if a compatible range is desired.

### Eidolon: Repraised `0.5.0.2`
1. Identify whether external mods can register/invoke ritual or chant behavior through supported registries/events.
2. Probe ritual completion/caster/ingredient context needed to dispatch a Black Arcana-owned ritual effect.
3. If no stable seam exists, classify Eidolon as thematic interoperability only and use Black Arcana ritual runtime.
4. Never patch private ritual state reflectively.

### Malum `1.8.2`
1. Inspect the current 1.8.x public/registry model rather than historical Ritual Plinth code.
2. Identify supported Spirit Type/Rite registration or observation surfaces relevant to adapters.
3. Prove read/reserve/commit/refund semantics for any spirit payment used as a `CostProvider`.
4. Prove supported spirit visibility/harvest hooks before Mortal Ledger, Spirit Sight or Black Pyre amplification depend on them.
5. If transactional reservation cannot be expressed safely, Malum resources may be consumed only through a Black Arcana-owned compensating transaction with explicit failure tests, or the integration is rejected.

### RPG Skill Tree
1. Pin the actual repository/runtime contract when Stage 03 starts.
2. Expose only Black Arcana-owned queries: mastery, attribute value, perk presence and mastery-use recording.
3. Verify missing/disabled RPG integration produces deterministic fallback policy rather than classloading failure.

## Promotion rule

`PROBE` means exactly that: thematic fit is not sufficient evidence. A Stage 03 adapter may be promoted only after compile proof against the installed version, runtime smoke with the host present, absent-host startup where optional, and contract tests for the Black Arcana seam it implements.

No candidate is allowed to bypass this rule by importing private host classes merely because doing so is easier.