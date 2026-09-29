# Gaze 1.1.7.1 — exact-artifact semantic audit

## Scope and authority

This record closes only facts that can be reconstructed from the physically installed Gaze 1.1.7.1 artifact and the current physical provider set. It does not transfer Malum or Iron's runtime authority to Black Arcana and does not treat source defaults as deployed configuration.

Physical anchor:

- JAR: `gaze-1.1.7.1.jar`;
- mod id: `gaze`;
- version: `1.1.7.1`;
- SHA-1: `a8cb3190bde157f78160ce65c202ce2d47fb2041`;
- Minecraft 1.21.1 / NeoForge `21.1.248`;
- physical modlist SHA-1: `7aaece7acbfb07ba4d0c66029042f36c50d046f0`.

Gaze is All Rights Reserved. This is a clean-room compatibility/catalog audit: only artifact identity, registry/member/type relationships, resource identities/paths and targeted control-flow gate facts are retained. No implementation bodies, recipe ingredients, numerical balance values, localization prose, assets, models or sounds are copied.

## Reproducible exact-artifact evidence

Isolated evidence branch/PR:

- branch: `audit/gaze-1.1.7.1-exact-artifact`;
- NON-MERGE draft PR: #201;
- audited HEAD: `2f4ff6536663b1c629a6a5ea92416765bea17b1e`;
- final evidence workflow run: `34676660467` — GREEN;
- evidence artifact: `10292013626`;
- artifact digest: `sha256:fb69f353b672f7c8ec7b470c454d24d1c3110cb996a250076a16d2b053f23f71`.

The workflow materialized Modrinth version `od4ltbRo` and hard-failed unless the downloaded file SHA-1 matched the physical-modlist SHA above. That closes installed-artifact identity for this audit.

## Exact semantic inventory surfaces

### Spirit Rites

The exact artifact exposes `GazeRiteRegistry` as a `DeferredRegister<SpiritRiteType>` with **26 distinct `RiteHolder<SpiritRiteType>` identities**. The exact Gaze progression setup references all 26 holders and uses Malum's Spirit Rite codex page types. This proves that these are intended player-facing rite identities rather than spare registry slots.

The 26 identities are:

- `gaze_lesser_arcane_rite`;
- `gaze_greater_arcane_rite`;
- `gaze_lesser_sacred_rite`;
- `corrupt_gaze_lesser_sacred_rite`;
- `gaze_greater_sacred_rite`;
- `corrupt_gaze_greater_sacred_rite`;
- `gaze_lesser_aerial_rite`;
- `corrupt_gaze_lesser_aerial_rite`;
- `gaze_greater_aerial_rite`;
- `corrupt_gaze_greater_aerial_rite`;
- `gaze_lesser_aqueous_rite`;
- `corrupt_gaze_lesser_aqueous_rite`;
- `gaze_greater_aqueous_rite`;
- `corrupt_gaze_greater_aqueous_rite`;
- `gaze_lesser_earthen_rite`;
- `corrupt_gaze_lesser_earthen_rite`;
- `gaze_greater_earthen_rite`;
- `corrupt_gaze_greater_earthen_rite`;
- `gaze_lesser_infernal_rite`;
- `corrupt_gaze_lesser_infernal_rite`;
- `gaze_greater_infernal_rite`;
- `corrupt_gaze_greater_infernal_rite`;
- `gaze_lesser_wicked_rite`;
- `corrupt_gaze_lesser_wicked_rite`;
- `gaze_greater_wicked_rite`;
- `corrupt_gaze_greater_wicked_rite`.

### Geas effect types

The exact artifact exposes two provider `GeasEffectType` holders:

- `pact_of_encroaching`;
- `domain_of_swords`.

They are visible in the provider progression surface, but the canonical semantic-action metric already excludes base-Malum `GeasEffectType` identities as effects/status-like types rather than discrete spell/rite actions. Gaze follows the same rule, so these two identities add **0** to the semantic-action numerator.

### Rune items

Eight Gaze rune items are progression-visible and have provider resource/acquisition surfaces. They remain item/equipment/passive identities, not standalone spells, glyphs, rites or equivalent action-registry identities under the current metric. They add **0**.

## Rite configuration gate

The exact artifact defines `Config.DISABLE_GAZE_RITES` / `disableGazeRites` as a `COMMON` boolean configuration. Its code default is `false`, but the resolved current-pack value is authoritative, not the source default.

Targeted exact-artifact control-flow evidence shows that when the resolved `disableGazeRites` value is true, Gaze skips registration/initialization of the rite registry/effect-type surfaces. Therefore all 26 rite identities are **configuration-conditional**.

No authoritative deployed Gaze COMMON config containing the effective `disableGazeRites` value is present in the current project attachments or repository evidence. Phase 2BJ therefore does **not** promote those 26 rites. A source default is not substituted for current-pack state.

## Iron's compatibility spell

The exact artifact contains one Gaze-owned Iron's spell registration surface:

- `SOULWARD_SHIELD` — a `Supplier<AbstractSpell>` in Gaze's Iron's `SpellRegistry`.

`IronsCompat.init` checks `ModList.isLoaded("irons_spellbooks")`; when the provider is present, its fallthrough registers Gaze's Iron's spell registry together with the associated compat surfaces. The current physical pack satisfies that provider condition:

- JAR: `irons_spellbooks-1.21.1-3.16.3.jar`;
- mod id: `irons_spellbooks`;
- runtime version: `1.21.1-3.16.3`;
- SHA-1: `017fd8140c477f9ae602cf95594f1c23bef1d6e3`.

Therefore Soulward Shield is a current-pack registered Gaze-owned standalone spell identity. Generic Iron's host runtime/config behavior remains separate QA, consistent with the treatment already used for exact Iron's spell-content addons; no Gaze-specific spell-disable gate was observed for this registration.

## Canonical semantic disposition

Phase 2BJ disposition:

- **+1 `COUNTED_EXACT`** — Soulward Shield;
- **26 `CONDITIONAL`** — Gaze Spirit Rites, blocked only by missing deployed `disableGazeRites` COMMON-config evidence;
- **2 `EXCLUDED`** — Geas effect types, excluded by the existing metric definition;
- **8 `EXCLUDED`** — rune items/passives, excluded by the existing metric definition.

Resulting global values after this narrow promotion:

- strict reconstructible semantic minimum: **1250**;
- provider-component closure: **57/100**, unchanged;
- global semantic denominator: still incomplete;
- no final semantic-magic coverage percentage may be derived.

Gaze is **not** promoted to a closed provider component because the 26 rite identities still depend on an unavailable deployed configuration value.

## Authority and runtime boundary

Malum remains authority for Spirit Rite/Geas runtime semantics and resources. Iron's remains authority for its spell framework and host settlement. Gaze owns the addon identities it registers. Black Arcana does not reproduce Gaze rite execution, Geas processing, Iron's spell settlement, Malum spirit resources or provider configuration.

Runtime mechanics, numerical balance, complete-modpack behavior and any future Black Arcana adapter/API seam remain fail-closed until separately proven.