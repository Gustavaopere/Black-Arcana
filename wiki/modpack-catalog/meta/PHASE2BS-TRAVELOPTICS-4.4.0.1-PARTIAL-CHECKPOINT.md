# Phase 2BS — T.O Magic n' Extras / Traveloptics 4.4.0.1-1.21.1 partial checkpoint

## Result

Phase 2BS closes the exact publisher-release **registry inventory** for the physically present T.O Magic n' Extras version line, but intentionally does **not** promote it into the strict semantic numerator or technical component count.

Disposition:

- provider status: **⚠️ partial/conditioned**;
- exact registered spell identities: **33**;
- residual root localization spell IDs absent from registry: **32 excluded**;
- strict semantic delta: **+0**;
- technical component delta: **+0**;
- global strict semantic minimum remains **1344**;
- technical component closure remains **66/100**;
- runtime/full-pack state: **FAIL-CLOSED**.

No semantic coverage percentage is declared. `66/100` is a technical component metric only.

## Installed/release authority

Physical pack evidence establishes:

- JAR/version line: `traveloptics-4.4.0.1-1.21.1.jar`;
- mod id: `traveloptics`.

Exact publisher release used for bounded clean-room inspection:

- CurseForge project `1046916`;
- file `6342780`;
- SHA-1 `3808493ce45cdfeb6408e85578adecf13df698e8`;
- SHA-256 `0372b4b8593288726fb0d6e8cdb86202a87677d0c2dafeb96cab50bf057ec298`;
- license `All Rights Reserved`.

An independent physical local-JAR hash is not preserved in the current repository evidence. Phase 2BS therefore does not claim byte identity with the installed JAR and does not use `COUNTED_EXACT`.

## Registry closure

Exact `TOSpells` reconciliation proves:

- 33 unique spell Supplier fields;
- 33 `registerSpell(...)` calls;
- zero static registry branches;
- 33 unique concrete classes;
- 33 exact unique field -> class -> `traveloptics:<id>` mappings;
- 65 root localization spell IDs total;
- 32 localization roots absent from the exact registry, excluded from semantic counting.

The publisher's broader/historical text and the stale translation surface are not treated as current registrations. This is especially important because file `6342780` is explicitly published as a deprecated partial 1.21.1 alpha.

## Reachability blocker

Provider-owned gate reconciliation proves:

- `AbstractUniqueSpell.allowCrafting() = false`;
- `AbstractWeaponSpell.allowCrafting() = true`.

Ten exact registrations are Unique spells. Nine have direct structured loot references in exact file `6342780`. `traveloptics:blackout` is the exception:

- non-craftable by provider base gate;
- no direct structured-data reference found;
- no provider-owned reference to `TOSpells.BLACKOUT_SPELL` outside the registry class found by focused class/method audit.

The publisher release page states generically that ported spells are obtainable in survival, but that statement does not provide object-level evidence for Blackout. Complete 33/33 survival reachability is therefore not closed.

## Runtime blocker

Exact `TOLootModifiers` structural reconciliation proves:

- registry name `key_loot` present;
- registry name `universal_loot` present;
- `KeyLootModifier.CODEC` referenced twice;
- `UniversalLootModifier.CODEC` referenced zero times.

A later third-party patch describes this same wiring as a registry-startup defect and changes the universal entry. Phase 2BS does not elevate that third-party runtime diagnosis into upstream authority and does not claim a reproduced crash.

However, the exact original JAR's structural wiring plus its publisher `DEPRECATED DONT USE` alpha status is sufficient to prevent runtime/component promotion until authoritative pack evidence shows either:

1. a verified physical patch/replacement is deployed; or
2. the unpatched exact physical artifact initializes successfully in the assembled pack despite the structural risk.

No such evidence is currently stored.

## Audit evidence

Clean-room NON-MERGE audit branch: `audit/traveloptics-4.4.0.1-exact-artifact`.

- exact artifact audit: run `34740821956`, artifact `10312358984`, digest `sha256:2a38dcb75bbdb844ce3371a0b9afcf556c0f99b8ce5793442bf34ad8b5bc28b0`;
- registry reconciliation: run `34740904391`, artifact `10312645516`, digest `sha256:e6d7e908acfb96328285b4f8ca7504d13ca43f02cc07703d0e04c203fcbbfa11`;
- 33/33 semantic reconciliation: run `34741045570`, artifact `10311499946`, digest `sha256:acbcc86f961d603608794f922a26106ab85f1a7479636596ba75dff3fefe8b00`;
- corrected runtime-risk reconciliation: audit HEAD `3dbe6d1f0dc25104a86283ae04e0cfd3365b4998`, run `34741368134`, artifact `10312730434`, digest `sha256:55c933137fabb4f32b90ca7fae08f89c799392b72e63f7de1682edac58cd15da`.

The earlier runtime-risk run intentionally failed because its test assumed `AbstractWeaponSpell.allowCrafting=false`; exact evidence disproved the assumption (`true`), the harness was corrected, and only the corrected GREEN run is authoritative for the final gate fact.

## Canonical accounting rule

Phase 2BS is a **catalog partial**, not component #67.

Do not update:

- strict total `1344`;
- technical closure `66/100`;
- Iron's ecosystem semantic subtotal;
- any global semantic denominator.

A future promotion must satisfy both object-level reachability and authoritative runtime viability. If those gates later close, count only identities proven active/reachable under that evidence; do not assume all 33 retroactively.

## Cross-provider coexistence

Somake Spells already records that both Somake Aqua and the deprecated T.O 1.21.1 alpha are physically present and that the historical migration statement does not prove authority migration to this alpha.

Phase 2BS does not resolve that coexistence question. No new Aqua authority, school pipeline or duplicated spell set is created by Black Arcana.

## Clean-room boundary

The ARR artifact was inspected only for factual interoperability/catalog evidence: hashes, metadata, type/member/registry identities, aggregate control-flow facts, constant gate results and structured identifiers/paths.

No implementation bodies, source reconstruction, upstream prose, assets, models, sounds, recipe/loot payloads or binary redistribution are retained or adapted.
