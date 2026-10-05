# Traveloptics 4.4.0.1 — Blackout generic-loot exclusion checkpoint

Status: `EXACT FILE 6342780 + CURRENT IRON'S 3.16.3 HOST / PROVIDER-OWNED GENERIC RANDOM LOOT NEGATIVE / CURRENT-PHYSICAL + EXTERNAL-PACK REACHABILITY STILL OPEN`

## Purpose

This checkpoint narrows only one unresolved part of `traveloptics:blackout` acquisition: whether exact publisher File `6342780` can surface Blackout through its own Iron's-style randomized scroll loot without an explicit Blackout reference.

It does **not** prove that Blackout is impossible to obtain in the assembled current pack.

## Exact provider audit

Temporary NON-MERGE PR **#626** audits exact CurseForge File `1046916 / 6342780` at SHA-1 `3808493ce45cdfeb6408e85578adecf13df698e8`.

Authoritative v2 result:

- audit HEAD: `5670beca2b61ee5e302bd95db3c6bb595ddeb152`;
- workflow run: `37251558059` — **SUCCESS**;
- text artifact: `11321475072`;
- artifact digest: `sha256:1b3bb4e570afa9dd0a0333dc00b4e36eb7a16baf7b31d690dc41293ff8550b9d`.

Retention was limited to class identity, `allowLooting()` outcome classification, structured spell-filter summaries and provider class/reference identities. No method body, bytecode sequence, implementation reconstruction, asset, localization prose or binary redistribution is retained.

## Provider inheritance result

For Blackout:

- `BlackoutSpell` does not declare `allowLooting()`;
- its provider parent is `AbstractUniqueSpell`;
- `AbstractUniqueSpell` declares `allowLooting()`;
- the bounded exact-bytecode outcome is **constant false**.

Therefore exact-alpha Blackout is explicitly excluded from ordinary host random-loot selection paths that honor `allowLooting()`.

## Structured loot-filter result

The audit scanned all **151** provider JSON resources under `data/traveloptics/**/*.json`.

It found:

- **23** `spell_filter` nodes;
- **23** `irons_spellbooks:randomize_spell` nodes;
- **0** structured references to `traveloptics:blackout`;
- **0** explicit spell filters containing Blackout;
- **0** forced Eldritch school filters;
- all 23 retained filters are explicit spell lists.

Those explicit lists account for the already-cataloged structured spell anchors and none contains Blackout.

## Provider code-reference result

Across **250** provider class entries:

- classes referencing host `SpellFilter`: **0**;
- classes referencing host `RandomizeSpellFunction`: **0**;
- classes referencing `BLACKOUT_SPELL`: **1** — `com.gametechbc.traveloptics.init.TOSpells`, the registry holder itself.

This independently preserves the earlier negative result that no provider-owned class outside the registry directly references Blackout.

## Current Iron's 3.16.3 host boundary

Current physical host authority is Iron's Spellbooks `1.21.1-3.16.3`, SHA-1 `017fd8140c477f9ae602cf95594f1c23bef1d6e3`.

Matching public source pin:

`iron431/irons-spells-n-spellbooks@e4056af90302d37eb1739f5ff05020b020e6e252`

At that pin:

- `AbstractSpell.allowLooting()` is the generic random-loot admission predicate;
- `SpellFilter.isSpellAllowed` requires `spell.isEnabled() && (force || spell.allowLooting())`;
- no-filter/default and ordinary school-filter pools therefore exclude a spell whose `allowLooting()` is false;
- explicit spell lists can bypass the allow-looting predicate at the filter-list stage;
- `force=true` school filters can also bypass it.

The exact Traveloptics audit closes both bypass cases negatively for Blackout: no explicit Blackout filter and no forced Eldritch filter are present.

## Catalog conclusion

For **exact publisher File `6342780` running under current Iron's 3.16.3 host semantics**:

**provider-owned generic/randomized loot does not provide an evidenced Blackout route.**

This is stronger than the previous statement “no direct loot anchor found,” but it is deliberately narrower than “Blackout cannot be obtained.”

Still open:

- assembled-pack datapack/KubeJS/progression grants external to the provider artifact;
- any current-physical route introduced by SHA-1 `7b74816e89cc15dd0b5a31d9ea1e456024e8fae4`;
- a deterministic survival runtime observation tied to the current physical artifact;
- authoritative File-6342780-specific source/documentation for another acquisition mechanism.

The broad 1.20.1 Dead King → Blackout route remains versioned publisher context and is not projected into the deprecated 1.21.1 alpha.

## Disposition

- exact-alpha Blackout registry identity: **PROVEN**;
- exact-alpha craftability: **false**;
- exact-alpha generic/randomized provider loot route under current host: **NEGATIVE / CLOSED**;
- exact-alpha other acquisition route: **UNVERIFIED**;
- current physical `7b74816e...` acquisition route: **UNVERIFIED**;
- actual current-pack survival reachability: **UNVERIFIED / FAIL-CLOSED**.

Traveloptics therefore remains **⚠️ partial/conditioned** and contributes **+0 strict** for the current physical artifact.
