# Not Enough Glyphs

Status: `PHASE 2AF — SOURCE-PINNED 4.6.1 / CURRENT-PACK REGISTRATION MATRIX COMPLETE / 40 REGISTERED PRIMITIVES, 39 SOURCE-ENABLED / SPELL BINDER + PERKS + RUNTIME BOUNDARIES AUDITED / FULL-MODPACK QA PENDING`

## Runtime identity

- Mod id: `not_enough_glyphs`
- Physical JAR: `not_enough_glyphs-1.21.1-4.6.1.jar`
- Runtime version: `4.6.1`
- Physical SHA-1: `e5fd04b7c40d6d5a9aea5d6356f3eb628941fca4`
- Embedded Sauce: `0.0.42.89`
- Loader/game: NeoForge 1.21.1
- Phase 2 class: `ARS GLYPH / FALLBACK-COMPAT / CAST-DEVICE / PERK PROVIDER`
- Exact source-semver pin: `Alexthw46/NotEnoughGlyphs@2f0c7b9fcf802c7e85b4ed4d7ed94123bcee398b`

The source commit declares `mod_version=4.6.1`. This is a source-semver pin, not a claim that the public source tree was independently reproduced byte-for-byte into the physical installed JAR.

## Current-pack registration result

Registration is conditional on loaded providers. In the physical 2026-09-08 pack:

- `ars_elemental` **is installed** → NEG does not register its local Arc/Homing fallbacks; it only references the four real Ars Elemental primitives in its internal `registeredSpells` list and enables four Elemental Binder focus perks.
- `ars_controle` **is installed** → NEG does not register its local `ars_controle:filter_random` fallback.
- `toomanyglyphs` **is absent** → NEG registers 14 Too Many Glyphs fallback primitives under the historical `toomanyglyphs` namespace.
- `arsomega` **is absent** → NEG registers 8 Ars Omega fallback primitives under `arsomega`.
- `ars_trinkets` **is absent** → NEG registers 2 Ars Trinkets fallback filters under `ars_trinkets`.
- `ars_scalaes` is absent, but Resize is registered unconditionally under `ars_scalaes` by current NEG source.

Result for this pack: **40 calls to `APIRegistry.registerSpell` by NEG**. `not_enough_glyphs:momentum` is still registered but explicitly returns `isEnabled() = false`, so **39 are source-enabled before user/provider config**.

The internal documentation list additionally contains four real Ars Elemental primitives. They are **not** counted as NEG registrations.

See [`REGISTRATION-MATRIX.md`](REGISTRATION-MATRIX.md) and [`glyphs/`](glyphs/).

## Spell Binder correction

The old catalog sentence “stores up to 25 spells” was too coarse. Exact 4.6.1 source exposes two distinct surfaces:

- item capability/container: **25 storage slots**;
- Ars caster data: `BinderCasterData(10)` = **10 caster/radial spell slots**;
- `SpellBinder.getBinderCaster` synchronizes the **first 10** inventory slots into the caster.

The container visibly exposes slots 0–24. `Events.attachCaps` also reacts to changes across the 25-slot item handler and calls `setSpell(..., slot)`. How slots 10–24 interact with the 10-slot caster is therefore a **runtime QA item**, not something to infer from storage capacity.

See [`SPELL-BINDER-AND-PERKS.md`](SPELL-BINDER-AND-PERKS.md).

## Provider-owned systems

NEG 4.6.1 additionally registers:

- one Spell Binder item;
- one `spell_holder` menu;
- one network-synchronized Binder caster data component;
- two custom projectile entities: `trail` and `missile`;
- three NEG MobEffects: `grow`, `shrink`, `stuffed`;
- two C2S custom payloads for opening the Binder and selecting a caster slot;
- 13 Binder perks/threads in this pack: nine base + four Ars Elemental focus threads;
- particle/timeline integrations and turret behavior for Trail, Missile and Ray;
- two mixins extending Ars Scribe's Table / Summoning Focus behavior.

## High-impact coverage

Current NEG coverage materially overlaps generic design space for:

- contingency/event-triggered Ars casting;
- ray, missile, trail and propagated-projectile delivery;
- chained resolution;
- planar/circular/hollow geometry;
- target-filter predicates;
- block tilling/flattening;
- entity mounting;
- feeding/Stuffed/crush interaction;
- resize/grow/shrink;
- multi-spell storage/casting device;
- Binder focus, crit, damage, knockback, mana-discount and random spell-stat modifiers.

These overlaps are not automatically Black Arcana gaps.

## Authority / fail-closed

- Ars Nouveau/NEG/Sauce remain authority for their glyph execution, contingency storage/triggers, caster state and mana settlement.
- Historical namespaces on fallback primitives are deliberately preserved; NEG implementing a fallback does not make Black Arcana the owner of that capability.
- Black Arcana must not replay a provider cast, duplicate a contingency trigger, double-debit Ars mana, mirror Binder state, or spawn a second provider projectile merely to observe the action.
- `Plow` contains an explicit provider claim-respect check. `Flatten` does not expose the same explicit check in its audited class; effective protection is therefore a QA question, not a declared bypass or declared safety guarantee.
- Client packets are requests. Server handlers re-resolve the Binder from the declared hand before mutating/opening provider state.
- Exact behavior inherited only from Sauce/Ars base classes remains attributed to those bases unless directly observed in NEG source.

## Validation boundary

This phase closes the source-level current-pack inventory and provider contract. It does **not** claim:

- byte-for-byte source/JAR reproducibility;
- real-client/full-modpack interop PASS;
- that Binder storage slots 10–24 are castable;
- that every downstream world mutation has been tested against the user's protection/claim stack;
- that a Phase 3 Black Arcana feature is now approved.

Phase 3 remains blocked by the canonical deduplication rule.

## Files

- [`REGISTRATION-MATRIX.md`](REGISTRATION-MATRIX.md)
- [`SPELL-BINDER-AND-PERKS.md`](SPELL-BINDER-AND-PERKS.md)
- [`RUNTIME-BOUNDARIES.md`](RUNTIME-BOUNDARIES.md)
- [`DELEGATION-AND-DISABLED.md`](DELEGATION-AND-DISABLED.md)
- [`EVIDENCE-AND-PROVENANCE.md`](EVIDENCE-AND-PROVENANCE.md)
- [`glyphs/`](glyphs/)

## Phase 2BI — exact config authority (semantic delta +0)

The remaining 39-glyph semantic blocker is now narrowed to the deployed Ars/NeoForge server-config values rather than an unknown Not Enough Glyphs-specific switch. Exact Ars Nouveau 5.13.1 source at `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` shows that `GlyphRegistry.registerSpell(...)` builds each `AbstractSpellPart` config and registers it as `ModConfig.Type.SERVER` using `<namespace>/<path>.toml`. For NEG-owned IDs the concrete filename family is therefore `not_enough_glyphs/<glyph>.toml`.

`AbstractSpellPart.buildConfig(...)` defines `[general].enabled` with source default `true`, and `isEnabled()` reads that config value. `momentum` remains a separate provider override that returns disabled in NEG source. NeoForge 1.21.1 SERVER configs are server-authoritative/synchronized and may be overridden per world under `world/serverconfig`; consequently the source default is not accepted as the deployed pack state.

No authoritative deployed NEG glyph-config TOMLs are present in the current project attachments/repository evidence. Phase 2BI therefore changes **neither** metric: strict semantic minimum remains **1249**, and provider-component closure remains **57/100**. A future promotion may count only those of the 39 candidates whose effective deployed `[general].enabled` state is proven true. Runtime/balance/protection QA remains separate.
