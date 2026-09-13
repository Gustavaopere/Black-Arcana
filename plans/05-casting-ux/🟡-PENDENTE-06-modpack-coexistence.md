# 05.06 — Modpack Casting-Surface Coexistence — Runtime Contract

## State

`IMPLEMENTED / PHYSICAL PROVIDER COEXISTENCE VALIDATION PENDING / VISUAL COEXISTENCE MOVED`

Concrete HUD overlap, readability, keybinding discoverability and combat-animation/client-presentation work is specified in:

`plans/visual-production/05-casting-ux/06-modpack-coexistence-presentation.md`

This numbered plan retains only the authority and integration invariants that can affect gameplay correctness.

## Physical provider context

The planning baseline recorded these relevant surfaces in the assembled modpack: Iron's Spells 'n Spellbooks `1.21.1-3.16.3`, Spell Actionbar `1.1.4`, Epic Fight `21.17.3.1`, EFIS Compat `3.1.0` and Controlling `19.0.5`. Presence/version does not prove a supported Java integration API. Re-read the physical modlist before implementing a new bridge.

## Authority boundary

Black Arcana remains authority for Black Arcana-owned:

- canonical cast transaction and root `ArcanaCastId`;
- loadout identity;
- targeting admission;
- Black Arcana cooldown/charge/session state;
- Arcane Danger, Corruption and Strain;
- world-effect safety;
- synchronized Black Arcana presentation data.

External providers retain authority for their own spells, resources, cooldowns, combat state, animations, keybindings and UI state. Hosting a Black Arcana spell does not transfer Black Arcana gameplay authority to the host.

## Existing Iron's-hosted Black Arcana path

The supported Iron's-hosted probe uses the following boundary:

- `IronsSpellRegistryBridge` registers `black_arcana:irons_integration_probe` through the supported Iron's spell registry;
- `IronsArcanaProbeSpell.onCast` dispatches the host invocation into the Black Arcana hosted-cast dispatcher;
- Iron's owns the supported presentation/invocation host surface;
- Black Arcana owns validation, canonical transactional cost settlement and Black Arcana cooldown;
- `IronsArcanaProbeSpell.getManaCost` returns zero so Iron's pre-cast mana admission cannot become a second resource authority;
- `IronsArcanaProbeSpell.getSpellCooldown` returns zero so Iron's post-cast cooldown cannot become a second cooldown authority;
- `IronsHostedSpellEvents` still neutralizes Iron's native mana deduction at highest and lowest event priority as defense in depth for Black Arcana-hosted spell IDs;
- the real probe cost remains `IronsIntegrationIds.PROBE_MANA_COST` and is settled through the Black Arcana `IronsManaCostProvider` transaction;
- the real probe cooldown remains the Black Arcana `IronsSyntheticContent.COOLDOWN_TICKS` policy.

The invariant is one physical/provider invocation -> one Black Arcana root cast -> one canonical Black Arcana cost/cooldown settlement. A compatibility change that reintroduces provider-native settlement in parallel is invalid.

For Iron's-owned spells, Iron's remains authoritative for its native resource/cooldown semantics unless a separately verified adapter says otherwise.

## Deterministic coexistence coverage

`IronsHostedSpellAuthorityContractTest` locks the non-subjective integration boundary by checking that:

- the hosted probe exposes zero provider-native mana and cooldown settlement;
- one probe invocation contains exactly one hosted dispatcher call;
- the hosted dispatcher contains exactly one authoritative `ArcanaServerRuntimeManager.handleCastIntent` convergence point and one generated root `ArcanaCastId`;
- the high/low `SpellOnCastEvent` mana neutralizers remain installed as defense in depth;
- the Black Arcana cooldown policy remains explicit for the hosted probe;
- the common optional-mod entrypoint references Iron's adapters by class name rather than hard-importing provider adapter classes.

These checks protect the deterministic authority contract. They do not replace physical validation with the assembled client/modpack.

## Canonical implementation evidence

The hosted-authority hardening is canonical through PR #237, `fix: harden Iron's hosted casting authority`:

- final PR head: `4f33d8f87506e9fda63349591cd7a90dc4b0b125`;
- exact-head PR workflow `34788175905`: unit tests, diff sanity, NeoForge build, built-JAR verification, Foundation GameTests and dedicated-server smoke all GREEN;
- squash merge: `main@7c6d1e420a098e0163ccd27688a5558f9e699b29`;
- exact post-merge workflow `34788362522`: full pipeline GREEN, including QA artifact publication;
- canonical QA artifact: `black-arcana-7c6d1e420a098e0163ccd27688a5558f9e699b29`, artifact ID `10326459668`, SHA-256 `e9a2300a91a9aa7b19372901c59f24e19928d1ef7526ccaf414c880189c48081`.

This evidence closes the deterministic implementation tranche only. It does not convert any physical client/provider coexistence row into PASS.

## External invocation surfaces

Any new external item/action/UI invocation surface must prove an exact-version supported boundary before code is added. The integration must:

1. identify whether the operation is provider-owned or Black Arcana-owned;
2. convert one provider action into at most one bounded Black Arcana intent when Black Arcana owns the operation;
3. preserve one root cast identity and server targeting;
4. reserve/commit cost exactly once under the operation's canonical authority;
5. apply cooldown exactly once;
6. prevent provider-native + Black Arcana double execution/settlement;
7. define replay/recursion protection and optional-provider failure;
8. remain dedicated-server classloading safe.

Thematic similarity or visible UI presence is not an integration contract.

## Input and optional-provider boundary

Black Arcana continues to register ordinary Minecraft key mappings and suppresses direct cast input while another normal `Screen` owns focus. Controlling may improve discovery but is not a dependency. No controller framework is currently proven by the planning baseline; do not invent controller APIs.

Epic Fight/EFIS presence does not authorize Black Arcana to derive cast legality from client combat/animation state. If a direct integration becomes necessary, audit the exact installed API first. A cosmetic animation mismatch is not grounds to weaken server authority.

Spell Actionbar may display provider-owned state, but Black Arcana must not mirror or mutate unrelated provider state merely because both surfaces are visible. Any deeper direct bridge requires exact-version evidence and must preserve the one-root/one-settlement rule.

## Runtime acceptance

Engineering acceptance for this plan is limited to invariants that can be proven without subjective presentation judgment:

- one host action cannot create duplicate Black Arcana root casts;
- a Black Arcana-hosted Iron's action cannot double-debit provider/native + Black Arcana cost;
- Black Arcana cooldown settles exactly once;
- optional provider absence/incompatibility fails only the dependent feature;
- GUI focus cannot become a hidden direct-cast bypass;
- no unverified Epic Fight, Spell Actionbar, Controlling or controller API becomes a hard dependency;
- dedicated-server classloading remains safe.

The deterministic hosted-Iron's authority path is implemented and regression-covered. The plan remains pending until the required provider/input coexistence rows are observed in the assembled runtime.

HUD overlap, readability, battle-mode presentation, animation compatibility, key conflict ergonomics and recommended client layout belong to the linked visual-production plan.
