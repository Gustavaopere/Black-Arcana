# Candidate mechanic specifications

Status: PREPARATORY. These specs are implementation-facing clean-room contracts derived from Black Arcana design decisions and public behavior descriptions. Exact numeric balance remains Stage 08 work. A mechanic marked `DEFER` in the classification matrix is not authorized by this file.

Each candidate defines minimum behavior, cost class, progression class, safety rule, host intent and acceptance-test obligations.

## Dominion / wards

### Exclusion Ward
- Behavior: create a bounded temporary ward that rejects non-permitted living entities crossing its perimeter while allowing owner/covenant members.
- Cost: ritual materials plus bounded duration/upkeep; no free permanent field.
- Progression: T2 Dominion.
- Safety: no block movement; no permanent collision geometry; player blocking obeys PvP/server policy; max radius and active wards per owner.
- Host: Eidolon presentation if supported; Black Arcana owns permissions/world safety.
- Tests: owner passes; stranger rejected; covenant passes; boss/player policy respected; cleanup after expiry/restart.

### Gravitic Ward
- Behavior: apply bounded downward force/movement penalty inside an owned ward, excluding permitted entities if configured.
- Cost: mana/upkeep.
- Progression: T2 Dominion.
- Safety: clamp velocity; protected/boss multipliers; no permanent gravity attribute mutation.
- Host: Iron's or core effect inside Dominion ward runtime.
- Tests: force cap, exit cleanup, immunity tags, PvP reduction.

### Vigil Ward
- Behavior: optional module records/alerts owner when eligible entity crosses a ward perimeter.
- Cost: trivial ritual component or shared ward upkeep.
- Progression: T1.
- Safety: event-driven/spatially indexed; no per-tick world scan; rate-limit notifications.
- Host: core ward framework, optionally surfaced through Eidolon ritual.
- Tests: one crossing -> one bounded notification; spam throttle; owner/covenant filters.

### Malison Constellation
- Behavior: grand ritual forms a validated polygon from bounded ritual nodes; internal pattern parameters select a Black Arcana-defined curse package applied at activation to eligible entities inside.
- Cost: node materials plus activation sacrifice/resource.
- Progression: T4 Dominion.
- Safety: node/edge/area/entity budgets; no arbitrary command execution; players off by default; graph recompute only when dirty/activated.
- Host: Eidolon visual/ritual surface if supported, Black Arcana graph/policy core.
- Tests: valid/invalid polygon, max node budget, effect encoding, PvP exclusion, complexity budget.

### Hexward Aegis
- Behavior: manifest a frontal/area barrier with finite integrity that absorbs approved projectile/spell damage and repels ordinary entities modestly.
- Cost: Iron's mana/channel; integrity cannot exceed balance cap.
- Progression: T2 Dominion.
- Safety: finite lifetime/integrity, knockback cap, boss/projectile tags.
- Host: Iron's active spell.
- Tests: integrity depletion, projectile behavior, expiration, no permanent collision.

### Covenant
- Behavior: explicit consent-based relationship granting permissions used by wards, scrying, domains and other Black Arcana constructs.
- Cost: ritual material/setup, not ongoing mana by default.
- Progression: T1/T2 framework unlock.
- Safety: UUID-based persistent state, revocation path, no implicit nearby-player opt-in, server admin inspection/removal.
- Host: Black Arcana core; Eidolon may provide ritual UX.
- Tests: create/accept/revoke, persistence, owner removal, permissions after logout/name change.

### Inner Dominion
- Behavior: open a temporary caster-owned rulespace/session for bounded participants, then return every participant to a validated origin/fallback when session ends.
- Cost: composite high-tier resource + long cooldown + duration cap.
- Progression: T4 forbidden.
- Safety: session recovery journal, no nested domains initially, no persistent loot duplication, guaranteed return paths.
- Host: Black Arcana core; active trigger may be Iron's spell/ritual unlock.
- Tests: normal exit, target/caster death, logout, restart recovery, invalid origin fallback, nested denial.

## Liminal

### Threshold Gate
- Behavior: paired points move eligible entities across a short/bounded threshold; no block or block-entity movement.
- Cost: source/mana/upkeep depending host.
- Progression: T2.
- Safety: loaded destinations only, collision validation, throughput cap, ownership/PvP policy.
- Host: Ars integration where practical.
- Tests: entity transfer, blocked destination, unloaded endpoint failure, player permission.

### Veilstep Reflex
- Behavior: when an eligible incoming threat would hit, consume one bounded charge/resource to blink the caster to a safe nearby position.
- Cost: mana + charge/internal cooldown.
- Progression: T2.
- Safety: no repeated trigger loop; safe-position search bounded; cannot evade protected/unavoidable damage tags.
- Host: Iron's/Ars adapter.
- Tests: charge consumption, cooldown, failed safe search, protected damage.

### Anchor Recall
- Behavior: teleport caster to the last valid owned projectile explicitly marked by this spell.
- Cost: mana + cooldown.
- Progression: T2.
- Safety: same permitted dimension by default, projectile ownership, max age/range, safe landing.
- Host: Ars or Iron's.
- Tests: own projectile succeeds; foreign/expired/unloaded projectile denied; collision fallback.

### Reciprocal Transposition
- Behavior: paired sigils atomically exchange two eligible entities/items standing at endpoints.
- Cost: pair charge + host resource.
- Progression: T3.
- Safety: no blocks/block entities, loaded endpoints only, PvP consent, transaction revalidation immediately before swap.
- Host: Ars + Black Arcana transaction core.
- Tests: atomic success, endpoint invalidation, player policy, throughput limit.

### Vector Reversal
- Behavior: impart configured directional impulse to one target or bounded area targets.
- Cost: mana + cooldown.
- Progression: T2.
- Safety: velocity/fall-distance policy, entity-count cap, boss/player multipliers.
- Host: Iron's.
- Tests: clamped velocity, area cap, protected targets.

## Noetic

### Astral Severance
- Behavior: project a controllable non-combat viewpoint/avatar while physical body remains server-side and vulnerable; return on range/timeout/interruption.
- Cost: channel/resource drain.
- Progression: T3.
- Safety: hard radius, no interaction through projection unless explicitly allowed, logout/death restoration.
- Host: Black Arcana core with Eidolon flavor/integration possible.
- Tests: range return, body damage interruption, logout, dimension change denial.

### Namescry
- Behavior: channel limited remote perception of an explicitly resolved loaded target under server policy.
- Cost: focus item + mana/channel.
- Progression: T3.
- Safety: never force-load; same-dimension default; players require server policy/covenant/consent; limited world/entity data.
- Host: Eidolon ritual or Black Arcana core.
- Tests: unloaded/cross-dimension denial, privacy policy, interruption, range/data restrictions.

### Gaze of Stillness
- Behavior: while reciprocal facing/LOS is maintained, impose bounded movement suppression.
- Cost: mana per tick + post-channel cooldown.
- Progression: T2.
- Safety: CC diminishing returns, boss/player duration multipliers, escape by breaking facing/LOS.
- Host: Iron's active spell + Black Arcana CC policy.
- Tests: LOS/facing, escape, reapplication immunity, PvP/boss multiplier.

### Nullifying Gaze
- Behavior: remove or suppress only effects/mechanics explicitly tagged/adapted as nullifiable.
- Cost: mana/channel + cooldown.
- Progression: T3.
- Safety: protected-effect tags; no reflection/private-state mutation; boss resistance.
- Host: Iron's + adapters.
- Tests: approved effect removed, protected/unknown effect untouched, boss policy.

### Occult Appraisal
- Behavior: reveal approved target metadata such as status effects and held item; container inventories only when server permission allows.
- Cost: small channel/mana.
- Progression: T2.
- Safety: privacy policy, distance/LOS, no arbitrary capability dump.
- Host: core/Iron's presentation.
- Tests: metadata whitelist, player/container restrictions, no hidden NBT leak.

### Borrowed Sight
- Behavior: channel the viewpoint of an owned familiar or explicitly consenting bonded target.
- Cost: mana/channel + range.
- Progression: T2.
- Safety: arbitrary hostile player targeting disabled; return on interruption/unload.
- Host: Ars familiar adapter + core camera/session logic.
- Tests: owned familiar success, foreign target denied, unload/logout return.

### Pact Sanctuary
- Behavior: familiar-centered bounded aura temporarily suppresses hostility from eligible ordinary mobs toward covenant members.
- Cost: upkeep + radius budget.
- Progression: T3.
- Safety: no permanent faction mutation, boss/event exclusions, throttled spatial updates.
- Host: Ars familiar adapter + Black Arcana aura runtime.
- Tests: eligible mob suppression, boss unaffected, familiar unload cleanup, tick-budget instrumentation.

## Eidetic Arsenal

### Ephemeral Tempering
- Behavior: temporarily grant a held eligible item a bounded Black Arcana modifier profile (durability protection/mining or melee enhancement only where explicitly configured).
- Cost: mana/spirit + cooldown.
- Progression: T2.
- Safety: no permanent NBT/stat mutation, no unsupported mining-tier escalation, no stacking beyond cap.
- Host: Iron's/Malum adapter.
- Tests: temporary modifier, expiry/restoration, cap/stacking, unsupported item.

### Echo Armament
- Behavior: remember a sanitized eligible weapon profile and manifest an ephemeral echo with bounded durability/lifetime/use permissions.
- Cost: mana + one memory slot/cap.
- Progression: T2.
- Safety: never clone arbitrary NBT/data components; echo cannot persist or enter storage.
- Host: Iron's/core.
- Tests: profile sanitation, container rejection, logout cleanup, unsupported data ignored.

### Rift Blades
- Behavior: conjure spectral melee/projectile blades; successful marked strike may perform a bounded safe gap-close.
- Cost: Iron's mana + cooldown.
- Progression: T2.
- Safety: teleport range/collision validation and projectile cap.
- Host: Iron's spell.
- Tests: damage scaling, gap-close cap, blocked destination, projectile cleanup.

### Spectral Arsenal
- Behavior: manifest a bounded volley from sanitized profiles of eligible registered weapons without consuming/copying live items.
- Cost: mana per volley/projectile + active-echo cap.
- Progression: T3.
- Safety: profile damage ceiling, no container/ender-chest direct cloning, active entity budget.
- Host: Iron's + Black Arcana projected-profile registry.
- Tests: profile whitelist, damage cap, projectile cap, no persistent item creation.

### Oathforged Ascension
- Behavior: grand ritual consumes eligible weapon/material/spirit sacrifices to assign finite enhancement points to one bounded Black Arcana augmentation track.
- Cost: consumed items + spirit/material budget.
- Progression: T4.
- Safety: hard cap, diminishing returns, recursive input gives no net-positive loop, atomic transaction.
- Host: Eidolon/Malum ritual surface + core ledger.
- Tests: cap, diminishing curve, recursion exploit, rollback on invalid input.

## Sanguine / Sepulchral / Cinder

### Sanguine Harvest
- Behavior: a bounded ward drains eligible nearby life into one configured benefit budget; default design prioritizes caster healing or ritual charge, not simultaneous health/fullness/mana generation.
- Cost: ritual setup + activation/upkeep.
- Progression: T3.
- Safety: target/yield cap, anti-farm weighting, PvP/entity eligibility.
- Host: Eidolon/Malum composite.
- Tests: yield cap, farm repetition, player policy, empty area cost behavior.

### Sympathetic Wound
- Behavior: link caster and target so a capped fraction of qualifying direct damage to caster is echoed to target during a short link.
- Cost: health/spirit + link cooldown.
- Progression: T3.
- Safety: recursion marker, per-event/lifetime cap, boss/PvP multiplier, no arbitrary potion copy.
- Host: Malum/Eidolon + core damage policy.
- Tests: recursion, cap, target death, boss/player policy, link break.

### Blood Price
- Behavior: optional cost provider lets a cast pay a configured bounded fraction of resource cost with real health at an inefficient exchange rate.
- Cost: health itself.
- Progression: T2 perk/knowledge gate.
- Safety: minimum-health floor by default; no absorption/temp-health arbitrage; no passive gain.
- Host: Black Arcana core cost provider.
- Tests: fraction cap, floor, insufficient health, no resource generation.

### Law of Recurrence
- Behavior: timed defensive bargain gives increasing resistance to the last recognized damage family while increasing vulnerability when the family changes.
- Cost: mana/health + cooldown.
- Progression: T3.
- Safety: resistance never reaches ordinary total immunity, stack/duration caps, stable damage-family classifier.
- Host: Iron's/core.
- Tests: repeated/switch families, cap/floor, unknown damage family.

### Equilibrium Rite
- Behavior: exchange a bounded amount of eligible current health between caster and target based on an explicit transfer budget rather than unrestricted raw percentages.
- Cost: high resource + health/material + long cooldown.
- Progression: T4.
- Safety: bosses/PvP default restricted, max transfer, no over-heal/resurrection.
- Host: Iron's/Eidolon/core.
- Tests: transfer cap, low/high health, boss/player denial, no health creation.

### Mortal Ledger / Soul Anchor
- Behavior: eligible observed/credited deaths fill a bounded soul ledger; sufficient valid spirit value can form a small number of Soul Anchors, each consumed atomically to prevent one otherwise-valid death.
- Cost: Malum spirit value or Black Arcana fallback only if Malum absent by configuration.
- Progression: T4 Sepulchral.
- Safety: hard anchor cap, anti-farm eligibility, recovery lockout, no recursive same-event prevention.
- Host: Malum + core death-prevention state.
- Tests: eligible/ineligible deaths, fractional aggregation, cap, atomic consume, post-revival lockout, persistence.

### Spirit Sight
- Behavior: reveal supported spirit/occult entities and Black Arcana ward/domain traces; leverage host visuals where possible.
- Cost: low/toggle.
- Progression: T1.
- Safety: no arbitrary hidden-player/entity reveal; host-owned visibility rules respected.
- Host: Malum/Eidolon adapters.
- Tests: supported spirit visible, normal hidden data not exposed, absent-host fallback.

### Black Pyre
- Behavior: launch/place forbidden soul-fire that damages entities and creates a bounded network of temporary visual/fire cells under `WorldEffectPolicy`.
- Cost: mana plus optional spirit amplification; cooldown.
- Progression: T3 Cinder.
- Safety: temporary default, radius/cell/spread-per-tick/lifetime caps, no chunk loading, protected blocks honored. Entity damage remains functional when terrain effects are disabled.
- Host: Iron's active cast + Malum spirit flavor/cost + Black Arcana world safety.
- Tests: spread budget, expiry/rollback, chunk edge, protected block, safe-mode entity damage, server restart cleanup.
