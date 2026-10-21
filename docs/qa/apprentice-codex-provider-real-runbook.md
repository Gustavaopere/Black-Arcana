# Apprentice's Codex 0.9.7.1 — provider-real acceptance runbook (Stage 09)

**Status: ⚠️ PENDING / NOT EXECUTED.** Prepared 2026-10-14 against Black Arcana main `e23dfbd511e1056ae909ef52bf60e53d441a9cb0` and sibling modlist main `93d5f091fd6c52e55b55019ee5aaae80b9148f6e`. These are **preparation references**, not a frozen gameplay candidate. No row below is PASS. Stage 06.05 remains 🟡; Stage 09 owns D035 physical acceptance.

## Sources and strict evidence limits

- Exact installed provider `apprentice_codex-0.9.7.1+mc1.21.1.jar`, mod ID `apprenticecodex`, SHA-1 `b514315add32b93b0049c8673075627d7ef812e0` and SHA-256 `f0dfab67154f344c02c6fbe561f73456fa46ed9d018fae661dcdf4da95c67fe2` (9,945,619 bytes); CurseForge file 8768955.
- Declared upstream source `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`. [Completed opcode checks](apprentice-codex-binary-audit-2026-10-14.md) include Arcane Beam, Unite Luna, Palette Shift and Mana Mending; exact-hash binary postmerge workflow [#38570133913](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38570133913) SUCCESS. These **do not** prove gameplay.
- Recorder: [pending five-case JSON ledger](apprentice-codex-provider-real-evidence.json). Validate formatting with `python3 docs/qa/apprentice_codex_provider_real_evidence.py`. Only the four/five dedicated case checks and direct client/server observations may eventually justify a human-reviewed PASS; the script reports `physical_gameplay_authenticity_verified_by_automation=false` and `stage_promotion_authorized=false` in every case.
- Clean-room: observe and document outputs; do not ship, decompile into Black Arcana, copy provider implementation, modify third-party JAR, forge hook identities or add an RPG Skill Tree adapter.

## Candidate freeze BEFORE physical observation

1. Acquire an **authorized, actual Minecraft 1.21.1 NeoForge instance**, matching the current sibling modlist. Record exact Black Arcana production commit SHA and production JAR SHA-256, sibling modlist commit SHA, instance mods manifest SHA-256, actual NeoForge and Iron's Spellbooks versions, an anonymous operator tag and UTC start time. Do **not** automatically reuse the preparation-reference SHA after main advances.
2. Verify exact provider SHA-1 and SHA-256 above by hashing the **actual installed file**; verify presence of Iron's and other relevant mods at runtime, not merely the modlist Markdown. Freeze a single instance/world/candidate before the first observation. An alternate profile (e.g., Iron's absent or PvP/claims) is a separate campaign, not a silent modification of the frozen one.
3. Use Survival for authoritative mana, damage and durability checks. Creative or command privileges may be used **only to establish a controlled test arena/items**; do not interpret Creative no-cost casting as successful economy QA. Use a staging/copy world with known backup and avoid permanent destructive tests on real saves.
4. Record client footage, server logs and instance digest under immutable, accessible references with SHA-256 per file; avoid publishing player/account/private server information. Correlate client frames to server timestamps. A URL or an unsigned manual assertion is **not** proof that the observation occurred; check original evidence during human review.
5. If no authorized client/server/modpack is available, leave all rows `PENDING`. If an attempted row cannot be exercised with a real, specified blocker, set `BLOCKED` and give the blocker without marking assertions true. Any mismatch is `FAIL` with actual behavior and raw evidence.

## AC-P01 — exact binary and provider runtime bootstrap

**Preparation:** normal modpack launch, fresh and/or safe copy world, multiplayer-capable dedicated server, actual Iron's spell menu. Verify full runtime logs identify both `irons_spellbooks` and `apprenticecodex`. Check that `apprenticecodex:arcane_beam`, `apprenticecodex:unite_luna`, `apprenticecodex:palette_shift` and `apprenticecodex:mana_mending` are discoverable through legitimate gameplay/commands/API surfaces; do not inject registry entries by client-only state.

**Record:** game/server startup identity, hashes for actual loaded candidates, mod IDs and versions, four registry IDs and any startup exceptions. Do not infer that passing Black Arcana's independent CI loaded the provider. `PASS` requires all four AC-P01 assertions witnessed on the real candidate.

## AC-P02 — Arcane Beam cadence, DPS and lifecycle

**Source-derived hypothesis:** `ArcaneBeamEntity.tick` calls `damageHitTarget` for `tickCount % 5 != 0`; the comment says once in five ticks, so the **compiled condition is inconsistent with that comment**. Iron's `ArcaneBeam` is continuous (`castTime=60` ticks), with a 12-second cooldown. The source-level callback creates one beam entity, updates pose/clip per tick and discards the entity on completion/cancellation. Health alone may conceal hit attempts because of immunity frames, absorption and other mods.

**Steps:** while in Survival and with effective config recorded, place a stationary valid target with known health/armor/effects in a fixed unobstructed corridor; establish baseline without casting. Invoke one complete beam channel with uninterrupted aim. Record tick-aligned **server-side damage attempts, accepted damage events, and actual health delta separately**, plus source/owner/cast identity where observable. Repeat with deliberate cancellation and occlusion. If the installed pack has no legitimate instrumentation that can distinguish attempted vs accepted hits, record `BLOCKED` for the tick-cadence subcase rather than equating animation/health ticks with internal invocations.

**Review:** expected source-derived attempt gate is nonzero remainder (nominally four of five ticks after active start), not a guaranteed four accepted damage events per five ticks. Confirm cleanup after cancel without assuming an exact accepted-DPS. Do not add Black Arcana a second damage/cast settlement.

## AC-P03 — Unite Luna Counterspell amplification and world safety

**Source-derived hypothesis:** `UniteLunaMoonEntity.onAntiMagic` triggers `explodeByAntiMagic` when the moon is active, with constant `COUNTERSPELL_DAMAGE_MULTIPLIER=3.0f`. The normal impact uses 1.0f. Antimagic is therefore **not necessarily a harmless dispel** for this provider.

**Steps:** in a protected staging arena with tagged owner, neutral and allowed hostile targets, record a controlled normal moon impact and then a separate cast whose moon receives a legitimate compatible Counterspell/antimagic interaction **before the burst phase**. Log the phase, target, raw/accepted damage values where available, entity owner/source, impact/expiry, allied damage, wall/claim policy. Do not use Black Arcana `WorldEffectPolicy` as if it automatically governed this external entity. If installed Counterspell cannot hit this projectile, record a concrete `BLOCKED` rather than substituting manual `onAntiMagic` invocation.

**Review:** compare **provider raw damage paths** for 1.0 vs 3.0 only when the measurement surface supports it; armor/invulnerability may affect health deltas. Report any PvP/claim or friendly-fire regression as `FAIL` with reproduction. A classfile literal alone is not a gameplay observation.

## AC-P04 — Palette Shift affinity and cancelled next cast

**Source-derived hypothesis:** `PaletteShift.checkPreCastConditions` requires a Pastel Staff; `onCast` applies `PALETTE_RECEPTION` for 600 ticks. `PaletteShiftReceptionEvent.onSpellPreCast` intercepts a **subsequent different spell** at HIGHEST priority; if at least one held Pastel Staff has its affinity/color changed, the effect is removed and `event.setCanceled(true)` is called.

**Steps:** record the starting staff affinity/color, both hands, active effects, Iron's mana and cooldowns. Cast Palette Shift with a legitimate staff in hand. Initiate a different identifiable spell while effect is active, record authoritative pre-cast cancellation, absence/presence of that spell's actual effect, updated staff state and mana/cooldown settlement. Repeat with hands changed before the second spell; separately record the case where no eligible Pastel Staff is held. Do **not** assume cancelled pre-cast necessarily refunds/takes mana unless the real Iron's pipeline is observed.

**Review:** no second Black Arcana root cast, no double resource charge and no fake successful-spell mastery credit. `PASS` needs evidence of affinity transfer, cancellation and resource bookkeeping as **observed**, not inferred from particle count.

## AC-P05 — Mana Mending ItemStack identity and save/restart

**Source-derived hypothesis:** `ManaMendingCastData.matchesTarget` compares `targetStack == stack`, not semantic item equality. Lock data contains hand, fractional `pendingRepairAmount` and progress but the Java `ItemStack` field is transient, so the NBT payload does not persist the object reference. Repair is processed each ten elapsed cast ticks and may combine fractional amounts. Complete repair cancels the cast.

**Steps:** prepare two distinguishable damaged but repair-eligible items with recorded NBT/durability; choose offhand-first resolution and record authoritative mana. Run a normal sustained repair; log durability before/after each 10-tick interval where feasible, fractional progression and host mana. During a separate cast replace/swap held stack (including same-looking but different instance) and observe fail/cancel handling. Repeat a carefully documented logout/relogin/restart of the *same saved world* during the repair, checking resumption/relock behavior, duplicate repairs, item loss and resource settlement. Restore the backup only *after* preserving observations.

**Review:** treating an identical-looking replacement as the original locked object would contradict the source-level intent unless the restart/relock path legitimately creates a new lock. Do not assume the transient reference should survive save/load. `PASS` requires evidence for item identity swap, actual durability deltas, restart and no duplicate resource/repair outcome; otherwise `BLOCKED` or `FAIL` as appropriate.

## Ledger states, evidence, review and release gate

Every row begins `PENDING`. `PASS` and `FAIL` require a frozen exact candidate, timestamped observation, at least two immutable evidence references with SHA-256, and explicit assertion outcomes. `FAIL` must identify at least one false assertion. `BLOCKED` must state a concrete, at-least-20-character blocker, and must not certify unobserved assertions. The validator checks **structure and declared completeness only**; it cannot authenticate the original recording or prove live gameplay.

A physical `FAIL` reopens the originating behavior/integration for minimal authority-preserving correction and deterministic regression testing. Physical `PASS` needs independent human review of media/logs and canonical Stage 09 decision; **never** mark Stage 06.05 ✅ or Stage 09 release-ready just because a JSON validator exits zero. Under D035, unresolved physical rows remain release-blocking. RPG Skill Tree Mastery/perks integration remains ⛔ until real contracts are audited.
