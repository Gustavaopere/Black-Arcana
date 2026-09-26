# Ars 'n' Spells 3.3.4

Status: `✅ CATALOGED / INSTALLED 3.3.4 / RELEASE-BOUNDED 3.3.4 / PUBLIC NEOFORGE SOURCE CURRENT THROUGH 3.3.3 / 5 PROVIDER RITUAL IDENTITIES / +0 VERSION-DELTA TO SEMANTIC COUNT`

## Physical identity

- Mod id: `ars_n_spells`
- Physical JAR: `ars_n_spells-3.3.4.jar`
- Runtime version: `3.3.4`
- SHA-1: `53966330a468e626cd6469259af6778a5a7d9305`
- Minecraft: `1.21.1`
- Loader: NeoForge `21.1.248`
- Physical companion engines relevant to this bridge: Ars Nouveau `5.13.1`, Iron's Spells 'n Spellbooks `1.21.1-3.16.3`, Ars Elemental `0.7.10.1`, Ars Zero `2.0.2`.

## Evidence layers

The installed artifact is **3.3.4**. Physical identity is closed by the current 587-entry modlist.

Official CurseForge file `8881108`, `ars_n_spells-3.3.4.jar`, is a NeoForge 1.21.1 Release dated 2026-09-14. Its published 3.3.4 delta is concentrated on native cast/payment ownership, measured debit/refund recovery, cooldown lifecycle alignment, Curios attribute mirroring defaults, carrier revisions/protocol 7, MixinExtras restoration and blank-scroll loot restoration.

The official NeoForge 1.21.1 source branch is public through the **3.3.3** implementation line (`otectus/ars-n-spells@41fac17065c381104b17fdaab307d89ba21b49ab`; its `gradle.properties` declares `mod_version=3.3.3`). The 3.3.3 source and its architecture inventory explicitly expose **five rituals**: unconditional Spell Uninscription plus Iron's-gated Spell Transcription, Spellbook Binding, Mana Infusion and Mana Well.

Therefore the current evidence stack is deliberately split:

1. **physical/release-exact 3.3.4** — installed version/hash and publisher release delta;
2. **source-pinned 3.3.3** — exact current public ritual registry/bridge architecture before the 3.3.4 payment/cast hardening;
3. **release-bounded semantic closure for 3.3.4** — the 3.3.4 publisher delta does not introduce a new ritual/spell registration surface, while the named five-ritual provider model remains the documented/current bridge surface;
4. **unproven 3.3.4 internals** — exact class byte parity/signatures are not claimed without the physical JAR or a public 3.3.4 source pin.

The result is a current provider count of **5 ritual identities**, with **zero semantic count delta** from the previously counted 3.3.2 line.
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

The provider ritual model remains five identities on the public NeoForge 1.21.1 source line; the detailed implementations below remain pinned to the audited 3.3.0 baseline, while public 3.3.3 still exposes the same named ritual family under the current pack condition:

1. `ars_n_spells:spell_uninscription` — unconditional cleanup/uninscription ritual;
2. `ars_n_spells:spell_transcription` — transcribes one supported spell source onto one blank carrier target;
3. `ars_n_spells:spellbook_binding` — binds an exported Ars spell carrier into an Iron's spellbook/native wheel flow;
4. `ars_n_spells:mana_infusion` — one-shot mana grant routed through the active provider bridge;
5. `ars_n_spells:mana_well` — continuous area mana regeneration routed through the active provider bridge.

Each primitive is cataloged under [`rituals/`](rituals/).

The first four one-shot rituals use the provider's `AnsRitual` lifecycle at the 3.3.0 NeoForge source pin, whose default duration is 60 server ticks before `onEnd()`. `Mana Well` directly extends Ars's ritual base and has its own continuous tick behavior; it must not be mislabeled as a 60-tick one-shot ritual.

## Internal Iron's proxy registry is not eight new spells

When Iron's is present, the audited source line registers a finite pool of eight real Iron's `AbstractSpell` registry objects; public 3.3.3 still exposes `PROXY_POOL_SIZE = 8` / `ars_cross_1..8`:

`ars_n_spells:ars_cross_1` … `ars_n_spells:ars_cross_8`

These are **transport/proxy slots**, not eight distinct player-authored magic capabilities. The real payload is a serialized Ars spell selected for a particular carrier/book entry. The proxy exists so Iron's native spellbook wheel can resolve a legitimate registered spell id and delegate execution to the Ars cross-cast pipeline.

Semantic dedup therefore records:

- registry objects: 8 baseline proxy entries;
- new standalone semantic spells contributed by those proxies: **0**;
- hard native-wheel Ars-entry ceiling at the source baseline: **8 slots per book**.

See [`systems/cross-casting-and-proxy-pool.md`](systems/cross-casting-and-proxy-pool.md).

## Mana unification modes

The audited NeoForge source line exposes five mana-unification modes; detailed semantics remain pinned to the 3.3.0 baseline:

- `ISS_PRIMARY` / `iss_primary`;
- `ARS_PRIMARY` / `ars_primary`;
- `HYBRID` / `hybrid`;
- `SEPARATE` / `separate`;
- `DISABLED` / `disabled`.

`ISS_PRIMARY`, `ARS_PRIMARY` and `HYBRID` are provider-defined shared-pool modes; `SEPARATE` is the provider's dual-cost mode; `DISABLED` leaves the systems independent. Black Arcana does not reproduce these algorithms or invent a second unified mana ledger.

See [`systems/mana-unification.md`](systems/mana-unification.md).

## Spell Loom / carriers

The provider owns the serialization/export/inscription lifecycle that lets Ars spell graphs be carried across the engine boundary. The audited 3.3.0 baseline established the original correctness rules; public 3.3.3 materially revises Spell Loom/carrier workflows, and the exact 3.3.4 release further revises carrier payment/revision ownership. Black Arcana treats the provider as sole authority for this lifecycle and does not project unverified 3.3.4 internal signatures.

See [`systems/spell-loom-and-carriers.md`](systems/spell-loom-and-carriers.md).

## Black Arcana authority and deduplication

Black Arcana remains authoritative only for its own casting, hazards, Corruption, Strain, Arcane Danger and world-safety runtimes. Ars 'n' Spells remains authority for the Ars↔Iron's bridge behavior it actually owns.

Black Arcana must not:

- create a second Ars↔Iron's combined mana pool or conversion ledger;
- debit both host resources again after Ars 'n' Spells settles a bridged cast;
- treat `ars_cross_*` as ordinary independent offensive spells and process them a second time;
- mirror provider cooldown/progression/school attribution for the same causal cast;
- bypass the provider's carrier validation, proxy allocation or native-wheel routing with a second cross-cast packet path;
- infer exact 3.3.4 internal signatures from the 3.3.3 public source baseline.

For a provider-routed cast, Black Arcana integration must preserve one causal cast identity. If an integration needs an exact internal hook that is not proven on 3.3.4, it remains **fail-closed**.

## World and hazard boundary

Ars 'n' Spells does not transfer authority over Black Arcana Corruption, Strain, Arcane Danger or `WorldEffectPolicy`. Conversely, Black Arcana does not reinterpret provider mana/progression/casting state as its own hazard channels merely because both systems participate in a cast.

If a Black Arcana effect triggered through an approved adapter performs destructive world mutation, that Black Arcana-owned mutation still requires the canonical `WorldEffectPolicy` path.

## Current 3.3.4 release delta

Current release facts relevant to the catalog:

- transaction receipt HUD remains removed since 3.3.1;
- the 3.3.2 contextual mana-bar fix remains part of the current line;
- 3.3.3 adds Blank Scroll, native Iron's Inscription Table binding and Spell Loom/carrier revisions while retaining the existing five-ritual model;
- 3.3.4 moves payment ownership to the final native cast lifecycle, hardens debit/refund recovery and validation, advances carrier/network revision handling, and restores selected blank-scroll loot;
- none of those published 3.3.4 changes establish a sixth provider ritual identity.

These bridge/payment/presentation changes do not transfer gameplay authority to the client or create extra semantic spells.

## Evidence/provenance

See [`EVIDENCE-AND-PROVENANCE.md`](EVIDENCE-AND-PROVENANCE.md).

Phase 3 remains blocked. This provider closure is deduplication evidence; it is not permission to add a competing universal mana/spellbook bridge to Black Arcana.