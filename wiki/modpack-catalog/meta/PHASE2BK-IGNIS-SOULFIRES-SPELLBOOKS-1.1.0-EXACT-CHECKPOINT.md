# Phase 2BK — Ignis Soulfires: Spellbooks 1.1.0 exact checkpoint

## Result

`EXACT HASH-MATCHED ARTIFACT / BRIDGE_COMPAT + GEAR_LOOT_SUPPORT / ZERO_BRIDGE_INFRA / +0 SEMANTIC / COMPONENT #58`

Phase 2BK closes the exact installed `ignissoulfires_spellbooks` 1.1.0 artifact without inventing spell content from its magic-adjacent theme.

## Physical and publisher anchor

- Minecraft `1.21.1`
- NeoForge `21.1.248`
- physical modlist SHA-1 `7aaece7acbfb07ba4d0c66029042f36c50d046f0`
- JAR `ignissoulfires_spellbooks-1.1.0.jar`
- mod id `ignissoulfires_spellbooks`
- runtime `1.1.0`
- physical/audit SHA-1 `dcde77db35b6de3562b4e6de0025746eaf68f119`
- CurseForge project/file `1572171 / 8620663`
- artifact metadata license `ARR`

The old PR #172 closed release provenance only and intentionally left semantic state `OPEN`. Phase 2BK supersedes that blocker with exact artifact evidence rather than repeating publisher prose.

## Reproducible evidence

Isolated NON-MERGE PR #203:

- audit branch: `audit/ignis-soulfires-spellbooks-1.1.0-exact-artifact`
- audit HEAD: `ed807b77345cde1803767d804e26ea972c41d964`
- workflow run: `34688273425` — GREEN
- text-only evidence artifact: `10296406134`
- artifact digest: `sha256:5e96a319aea648aadf2c70bdf9b870a26a9503068307befc8a9972bb7b1cd52e`
- exact JAR SHA-256 observed during audit: `27d9270a4b718be50fe30accbd231dff824bb9b2bd14117ce1c081f731c77704`

The ARR JAR was temporary audit input and was not uploaded as evidence.

## Exact semantic closure

The hash-matched artifact contains 11 provider classes total. Its own registry surfaces are one armor-material registry and one item registry with exactly five equipment items. Across every provider class there are zero structural hits for `AbstractSpell`, `registerSpell`, `SpellRegistry`, `Ritual`, `Rite` or `Ability`; packaged provider data contains equipment tags/recipes rather than a spell/ritual/action registry.

Therefore this provider contributes **0 independent semantic magic objects** under the canonical metric. Equipment and its passive/flight/render behavior remain excluded by definition.

Semantic disposition: `ZERO_BRIDGE_INFRA`.

## Component closure

`ignissoulfires_spellbooks` was already one open unit in the reconciled 100-component magic/cross-domain denominator. Exact artifact inspection now closes its real scope and deduplication boundary strongly enough to close that component.

- previous component coverage: `57/100`
- Phase 2BK component delta: `+1`
- resulting component coverage: **`58/100`**

This 58/100 is an internal technical closure metric, not a spell/magic percentage.

## Semantic totals

- Phase 2BK semantic delta: **+0**
- strict reconstructible semantic minimum: **1250**
- global semantic denominator: still incomplete
- final semantic coverage percentage: **not declared**

## Authority boundary

Ignis Soulfires: Spellbooks owns only the compatibility equipment/material surfaces it actually registers. Cataclysm: Ignis Soulfires remains owner of Souled Ignitium base semantics; Cataclysm: Spellbooks/Iron's remain owners of their spell framework and magic registries. Black Arcana receives no new runtime authority or adapter from this catalog closure.

## Clean-room posture

The provider is ARR. Canonical evidence retains only cryptographic identity, metadata/resource paths, class/member/type signatures and narrow registry type/count facts. No implementation bodies, recipe ingredient payloads, localization prose or assets are copied/adapted; no upstream JAR is redistributed.
