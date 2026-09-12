# Phase 2BJ Checkpoint — Gaze 1.1.7.1 exact artifact

## Scope

Reconcile Gaze 1.1.7.1 against the exact physically installed artifact and current physical provider set. This phase is catalog/evidence-only; it does not modify Black Arcana runtime authority or advance a runtime Stage.

## Git synchronization

- repository: `Gustavaopere/Black-Arcana`;
- durable branch: `docs/magic-catalog-phase2bj-gaze-exact`;
- fresh base: `main@21d63c58a2ad6cd19f4f68131bb39e4b39bdd1c2`;
- no equivalent open durable Gaze documentation PR existed when this branch was created;
- isolated exact-artifact evidence is preserved separately in NON-MERGE draft PR #201.

## Physical identity

- Gaze JAR: `gaze-1.1.7.1.jar`;
- Gaze mod id/version: `gaze` / `1.1.7.1`;
- Gaze SHA-1: `a8cb3190bde157f78160ce65c202ce2d47fb2041`;
- current Iron's provider: `irons_spellbooks-1.21.1-3.16.3.jar`, mod id `irons_spellbooks`, SHA-1 `017fd8140c477f9ae602cf95594f1c23bef1d6e3`;
- Minecraft 1.21.1 / NeoForge `21.1.248`;
- physical modlist: 595 top-level entries, SHA-1 `7aaece7acbfb07ba4d0c66029042f36c50d046f0`.

## Exact evidence

Audit branch `audit/gaze-1.1.7.1-exact-artifact` materialized Modrinth version `od4ltbRo` and required its SHA-1 to equal the physical-modlist SHA before structural inspection.

Final exact-artifact evidence:

- audit HEAD: `2f4ff6536663b1c629a6a5ea92416765bea17b1e`;
- workflow run: `34676660467` — GREEN;
- evidence artifact: `10292013626`;
- digest: `sha256:fb69f353b672f7c8ec7b470c454d24d1c3110cb996a250076a16d2b053f23f71`.

Gaze is ARR; inspection was clean-room and retained only factual identity/registry/type/resource/gate evidence.

## Semantic result

Exact artifact evidence closes these surfaces:

- 26 distinct Gaze `SpiritRiteType` identities, all referenced by the provider progression setup;
- 2 provider `GeasEffectType` identities;
- 8 progression-visible rune items;
- 1 Gaze-owned Iron's `AbstractSpell` supplier: Soulward Shield.

Disposition under the existing semantic metric:

- Soulward Shield: **+1 `COUNTED_EXACT`**. Its optional-provider gate is satisfied because Iron's 3.16.3 is physically present;
- 26 Spirit Rites: **`CONDITIONAL`**. Exact control flow proves they are suppressed when resolved COMMON config `disableGazeRites=true`; the deployed pack value is unavailable, so source default `false` is not substituted;
- 2 Geas types: **`EXCLUDED`** by the same metric rule that excludes base-Malum Geas effect identities;
- 8 rune items: **`EXCLUDED`** as item/equipment/passive identities.

Canonical candidate resulting from this phase:

- strict reconstructible semantic minimum: **1250**;
- provider-component closure: **57/100**, unchanged;
- Gaze component remains open because its 26 rites still require deployed config evidence;
- global semantic denominator remains incomplete; no final semantic percentage.

## Runtime and authority result

- Malum retains authority over Spirit Rite/Geas runtime and spirit resources;
- Iron's retains authority over its spell framework/settlement;
- Gaze owns its addon identities;
- Black Arcana gains no second rite engine, Geas engine, Iron's casting pipeline or provider resource;
- runtime mechanics, balance and adapter/API seams remain fail-closed.

## Remaining validation before merge

- reconcile current ledger/provider docs without rewriting historical phase values;
- run `git diff --check`/postconditions on the exact durable diff;
- run Black Arcana CI on the exact durable HEAD;
- re-fetch/reconcile `origin/main` immediately before merge;
- rerun validation if synchronization changes HEAD;
- after merge, validate the exact merge SHA and confirm the canonical QA artifact.