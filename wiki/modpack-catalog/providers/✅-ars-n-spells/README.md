# Ars 'n' Spells 3.3.4

Status: `PHASE 2AG — INSTALLED 3.3.4 / COUNTED_RELEASE_BOUNDED 5 RITUALS / EXACT NEOFORGE SOURCE THROUGH 3.3.3 / EXACT 3.3.4 BINARY INTERNALS UNVERIFIED`

## Physical identity

- Mod id: `ars_n_spells`
- Physical JAR: `ars_n_spells-3.3.4.jar`
- Runtime version: `3.3.4`
- SHA-1: `53966330a468e626cd6469259af6778a5a7d9305`
- Minecraft: `1.21.1`
- Loader: NeoForge `21.1.248`
- Physical companion engines relevant to this bridge: Ars Nouveau `5.13.1`, Iron's Spells 'n Spellbooks `1.21.1-3.16.3`, Ars Elemental `0.7.10.1`, Ars Zero `2.0.2`.

## Evidence layers

The installed artifact is **3.3.4**. Current physical authority is the sibling `neoforge-rpg-skilltree@12a99071f241a3d61b4a48f5da15c67fd61c88b0`, whose certified row #46 records `ars_n_spells-3.3.4.jar`, runtime `3.3.4` and SHA-1 `53966330a468e626cd6469259af6778a5a7d9305`.

The strongest public source for the same NeoForge 1.21.1 line reaches exact **3.3.3** at official `otectus/ars-n-spells` commit `41fac17065c381104b17fdaab307d89ba21b49ab`; its `gradle.properties` declares `mod_version=3.3.3`, NeoForge `21.1.248`, Ars Nouveau `5.13.1.1400` and Iron's `1.21.1-3.16.3`. The historical 3.3.0 pin remains `a9930223c96806e5d748ea69d02f9a32cab62de9`.

Therefore this catalog distinguishes:

1. **physical-exact 3.3.4 facts** — installed version and physical hash;
2. **publisher-exact 3.3.4 facts** — CurseForge file `8881108` and its declared lifecycle/config/network/loot delta;
3. **source-exact 3.3.3 facts** — current public NeoForge registrations/topology and implementation surfaces visible at `41fac17065c381104b17fdaab307d89ba21b49ab`;
4. **unverified 3.3.4 binary internals** — exact class/signature/registry parity is not claimed without exact 3.3.4 source or installed-JAR registry evidence.

Two exact source continuity checks are material to semantic counting: `RitualRegistryHandler.java` is Git blob `b25378e8a67ea084c77116bfe936f10512d3f691` at both 3.3.0 and 3.3.3; `ArsCrossProxyRegistry.java` is Git blob `f4e35f708aa41f7c4bf2599f2517429a4871f82b` at both checkpoints, while `CrossModSpellComponents.PROXY_POOL_SIZE` remains `8` in 3.3.3.

The exact 3.3.4 release consolidates native payment/cast lifecycle ownership, debit/refund recovery, config/default alignment, carrier revisions, network protocol 7 and Blank Scroll loot restoration. It does **not** announce a ritual/spell registry identity addition or removal. That supports a **release-bounded continuity** classification; it is not byte-for-byte registry proof.

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

The exact NeoForge 3.3.3 source registers the same five ritual identities as the 3.3.0 baseline under the physical pack condition where Iron's is installed:

1. `ars_n_spells:spell_uninscription` — unconditional cleanup/uninscription ritual;
2. `ars_n_spells:spell_transcription` — transcribes one supported spell source onto one blank carrier target;
3. `ars_n_spells:spellbook_binding` — binds an exported Ars spell carrier into an Iron's spellbook/native wheel flow;
4. `ars_n_spells:mana_infusion` — one-shot mana grant routed through the active provider bridge;
5. `ars_n_spells:mana_well` — continuous area mana regeneration routed through the active provider bridge.

Each primitive is cataloged under [`rituals/`](rituals/).

The first four one-shot rituals use the provider's `AnsRitual` lifecycle at the 3.3.0 NeoForge source pin, whose default duration is 60 server ticks before `onEnd()`. `Mana Well` directly extends Ars's ritual base and has its own continuous tick behavior; it must not be mislabeled as a 60-tick one-shot ritual.

## Internal Iron's proxy registry is not eight new spells

When Iron's is present, the exact NeoForge 3.3.3 source preserves the finite pool of eight real Iron's `AbstractSpell` registry objects from the 3.3.0 baseline:

`ars_n_spells:ars_cross_1` … `ars_n_spells:ars_cross_8`

These are **transport/proxy slots**, not eight distinct player-authored magic capabilities. The real payload is a serialized Ars spell selected for a particular carrier/book entry. The proxy exists so Iron's native spellbook wheel can resolve a legitimate registered spell id and delegate execution to the Ars cross-cast pipeline.

Semantic dedup therefore records:

- registry objects: 8 baseline proxy entries;
- new standalone semantic spells contributed by those proxies: **0**;
- hard native-wheel Ars-entry ceiling at the exact 3.3.3 source: **8 slots per book**.

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

The provider owns the serialization/export/inscription lifecycle that lets Ars spell graphs be carried across the engine boundary. The 3.3.3 source/release line adds the provider Blank Scroll, direct binding through Iron's Inscription Table and a redesigned/hardened Spell Loom while preserving provider ownership of carrier validation and repair. Earlier 3.3.0 source hardening around non-mutating preview, reusable sources and cleanup remains historical implementation evidence where not superseded.

See [`systems/spell-loom-and-carriers.md`](systems/spell-loom-and-carriers.md).

## Black Arcana authority and deduplication

Black Arcana remains authoritative only for its own casting, hazards, Corruption, Strain, Arcane Danger and world-safety runtimes. Ars 'n' Spells remains authority for the Ars↔Iron's bridge behavior it actually owns.

Black Arcana must not:

- create a second Ars↔Iron's combined mana pool or conversion ledger;
- debit both host resources again after Ars 'n' Spells settles a bridged cast;
- treat `ars_cross_*` as ordinary independent offensive spells and process them a second time;
- mirror provider cooldown/progression/school attribution for the same causal cast;
- bypass the provider's carrier validation, proxy allocation or native-wheel routing with a second cross-cast packet path;
- infer exact 3.3.4 internal signatures from 3.3.3 source or publisher notes.

For a provider-routed cast, Black Arcana integration must preserve one causal cast identity. If an integration needs an exact internal hook that is not proven on 3.3.4, it remains **fail-closed**.

## World and hazard boundary

Ars 'n' Spells does not transfer authority over Black Arcana Corruption, Strain, Arcane Danger or `WorldEffectPolicy`. Conversely, Black Arcana does not reinterpret provider mana/progression/casting state as its own hazard channels merely because both systems participate in a cast.

If a Black Arcana effect triggered through an approved adapter performs destructive world mutation, that Black Arcana-owned mutation still requires the canonical `WorldEffectPolicy` path.

## Current 3.3.3 / 3.3.4 delta

Current facts that matter to the catalog:

- 3.3.1 removes the transaction receipt HUD;
- 3.3.2 fixes contextual Iron's mana-bar/XP-bar visibility;
- exact 3.3.3 source adds the provider Blank Scroll, direct Iron's Inscription Table binding and Spell Loom/carrier hardening without adding a sixth ritual registration;
- exact 3.3.4 publisher notes consolidate payment/cast lifecycle ownership, debit/refund recovery and cooldown/scroll settlement;
- carrier revisions cover every native item component and the client/server network protocol advances to **7**;
- fresh-config Curios/affinity/resonance/Source Jar/primary-school values are aligned, while existing saved config choices remain unchanged;
- Blank Scroll drops are restored in Iron's Catacombs armory and Citadel tomes.

These are lifecycle, compatibility, presentation and acquisition changes. They do not grant the client gameplay authority and do not create additional semantic spell identities under the current evidence.

## Semantic consequence

Current disposition:

- ✅ provider cataloged;
- physical line: **3.3.4**;
- **5** semantic ritual identities;
- **8** `ars_cross_*` proxy registry objects contribute **0** additional semantic spells;
- evidence state: `COUNTED_RELEASE_BOUNDED`;
- semantic delta versus the prior 3.3.2 catalog: **+0**;
- global strict reconstructible minimum remains **1382**.

## Evidence/provenance

See [`EVIDENCE-AND-PROVENANCE.md`](EVIDENCE-AND-PROVENANCE.md).

Phase 3 remains blocked. This provider closure is deduplication evidence; it is not permission to add a competing universal mana/spellbook bridge to Black Arcana.