# Ars 'n' Spells 3.3.2

Status: `PHASE 2AG — INSTALLED 3.3.2 / EXACT RELEASE DELTA / NEOFORGE 1.21.1 SOURCE BASELINE 3.3.0`

## Physical identity

- Mod id: `ars_n_spells`
- Physical JAR: `ars_n_spells-3.3.2.jar`
- Runtime version: `3.3.2`
- SHA-1: `2d2274ff786c42ea46c53fec866116f83d98fe5a`
- Minecraft: `1.21.1`
- Loader: NeoForge `21.1.248`
- Physical companion engines relevant to this bridge: Ars Nouveau `5.13.1`, Iron's Spells 'n Spellbooks `1.21.1-3.16.3`, Ars Elemental `0.7.10.1`, Ars Zero `2.0.2`.

## Evidence layers

The installed artifact is **3.3.2**. The strongest public source available for the same loader/game line is the official `otectus/ars-n-spells` branch `port/neoforge-1.21.1` at commit `a9930223c96806e5d748ea69d02f9a32cab62de9`, whose `gradle.properties` declares `mod_version=3.3.0`, Minecraft `1.21.1`, NeoForge `21.1.248`, Ars Nouveau `5.13.1.1400` and Iron's `1.21.1-3.16.3`.

Therefore this catalog deliberately distinguishes:

1. **physical/release-exact 3.3.2 facts** — presence, version, hash and published 3.3.1/3.3.2 release deltas;
2. **source-pinned 3.3.0 NeoForge facts** — registrations, registry paths, proxy pool, mana modes and implementation boundaries visible at the official 1.21.1 source pin;
3. **unverified 3.3.2 binary internals** — exact class/signature/registry parity after 3.3.0 is not claimed without exact JAR extraction.

The exact 3.3.1 release removes the transaction receipt HUD. The exact 3.3.2 release fixes contextual Iron's mana-bar visibility and states that there are **no config, network-protocol or save-format changes from 3.3.1**. Those deltas do not publicly announce gameplay registrations being added or removed, but absence from release notes is not promoted to byte-for-byte registry proof.

## Provider classification

Primary class: `BRIDGE / COMPAT / PROGRESSION`, with a real ritual/workstation surface.

Ars 'n' Spells is not treated as a new independent spell engine. Its high-value capabilities are cross-engine routing and lifecycle:

- configurable Ars Nouveau ↔ Iron's mana/resource routing;
- cross-engine casting and carrier-aware settlement;
- shared school/progression/equipment behavior;
- storing serialized Ars spells on supported carrier items;
- exposing bound Ars spells through Iron's native spell wheel;
- Spell Loom inscription/export workflows;
- provider-owned ritual workflows.

No Ars Nouveau glyph registrations owned by Ars 'n' Spells were proven in this pass.

## Current semantic ritual surface

The exact 3.3.0 NeoForge source baseline registers five ritual identities under the physical pack condition where Iron's is installed:

1. `ars_n_spells:spell_uninscription` — unconditional cleanup/uninscription ritual;
2. `ars_n_spells:spell_transcription` — transcribes one supported spell source onto one blank carrier target;
3. `ars_n_spells:spellbook_binding` — binds an exported Ars spell carrier into an Iron's spellbook/native wheel flow;
4. `ars_n_spells:mana_infusion` — one-shot mana grant routed through the active provider bridge;
5. `ars_n_spells:mana_well` — continuous area mana regeneration routed through the active provider bridge.

Each primitive is cataloged under [`rituals/`](rituals/).

The first four one-shot rituals use the provider's `AnsRitual` lifecycle at the 3.3.0 NeoForge source pin, whose default duration is 60 server ticks before `onEnd()`. `Mana Well` directly extends Ars's ritual base and has its own continuous tick behavior; it must not be mislabeled as a 60-tick one-shot ritual.

## Internal Iron's proxy registry is not eight new spells

When Iron's is present, the 3.3.0 NeoForge source registers a finite pool of eight real Iron's `AbstractSpell` registry objects:

`ars_n_spells:ars_cross_1` … `ars_n_spells:ars_cross_8`

These are **transport/proxy slots**, not eight distinct player-authored magic capabilities. The real payload is a serialized Ars spell selected for a particular carrier/book entry. The proxy exists so Iron's native spellbook wheel can resolve a legitimate registered spell id and delegate execution to the Ars cross-cast pipeline.

Semantic dedup therefore records:

- registry objects: 8 baseline proxy entries;
- new standalone semantic spells contributed by those proxies: **0**;
- hard native-wheel Ars-entry ceiling at the source baseline: **8 slots per book**.

See [`systems/cross-casting-and-proxy-pool.md`](systems/cross-casting-and-proxy-pool.md).

## Mana unification modes

The 3.3.0 NeoForge source baseline exposes five modes:

- `ISS_PRIMARY` / `iss_primary`;
- `ARS_PRIMARY` / `ars_primary`;
- `HYBRID` / `hybrid`;
- `SEPARATE` / `separate`;
- `DISABLED` / `disabled`.

`ISS_PRIMARY`, `ARS_PRIMARY` and `HYBRID` are provider-defined shared-pool modes; `SEPARATE` is the provider's dual-cost mode; `DISABLED` leaves the systems independent. Black Arcana does not reproduce these algorithms or invent a second unified mana ledger.

See [`systems/mana-unification.md`](systems/mana-unification.md).

## Spell Loom / carriers

The provider owns the serialization/export/inscription lifecycle that lets Ars spell graphs be carried across the engine boundary. The 3.3.0 NeoForge source/release baseline includes correctness hardening so preview is non-mutating, reusable books/foci are not consumed as disposable sources, inscription handles stack counts deliberately, and cleanup removes ANS-owned cross-cast state without treating ordinary native spells as its own authority.

See [`systems/spell-loom-and-carriers.md`](systems/spell-loom-and-carriers.md).

## Black Arcana authority and deduplication

Black Arcana remains authoritative only for its own casting, hazards, Corruption, Strain, Arcane Danger and world-safety runtimes. Ars 'n' Spells remains authority for the Ars↔Iron's bridge behavior it actually owns.

Black Arcana must not:

- create a second Ars↔Iron's combined mana pool or conversion ledger;
- debit both host resources again after Ars 'n' Spells settles a bridged cast;
- treat `ars_cross_*` as ordinary independent offensive spells and process them a second time;
- mirror provider cooldown/progression/school attribution for the same causal cast;
- bypass the provider's carrier validation, proxy allocation or native-wheel routing with a second cross-cast packet path;
- infer exact 3.3.2 internal signatures from the 3.3.0 source baseline.

For a provider-routed cast, Black Arcana integration must preserve one causal cast identity. If an integration needs an exact internal hook that is not proven on 3.3.2, it remains **fail-closed**.

## World and hazard boundary

Ars 'n' Spells does not transfer authority over Black Arcana Corruption, Strain, Arcane Danger or `WorldEffectPolicy`. Conversely, Black Arcana does not reinterpret provider mana/progression/casting state as its own hazard channels merely because both systems participate in a cast.

If a Black Arcana effect triggered through an approved adapter performs destructive world mutation, that Black Arcana-owned mutation still requires the canonical `WorldEffectPolicy` path.

## Current 3.3.2 HUD delta

Current UI facts that matter to the catalog:

- the transaction receipt HUD is **not current content**; it was removed in 3.3.1;
- 3.3.2 fixes the contextual Iron's mana bar so full displayed mana hides correctly with fractional maximums and the XP bar can return at the XP anchor;
- 3.3.2 states no config, network-protocol or save-format change from 3.3.1.

These presentation changes do not grant the client any new gameplay authority.

## Evidence/provenance

See [`EVIDENCE-AND-PROVENANCE.md`](EVIDENCE-AND-PROVENANCE.md).

Phase 3 remains blocked. This provider closure is deduplication evidence; it is not permission to add a competing universal mana/spellbook bridge to Black Arcana.