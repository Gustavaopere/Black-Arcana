# Traveloptics 4.4.0.1 — Blackout generic-loot exclusion checkpoint

Status: `EXACT FILE 6342780 / BUILT-IN PROVIDER GENERIC-LOOT ROUTE EXCLUDED / EXTERNAL PACK ROUTES + CURRENT PHYSICAL STILL OPEN`

## Purpose

This checkpoint closes one narrow acquisition question for `traveloptics:blackout`:

> Could the exact publisher alpha File `6342780` still yield Blackout through the provider's built-in generic Iron's random-spell loot surface even though no direct Blackout loot JSON exists?

For the audited exact alpha, the answer is **no**.

This is not a complete survival-reachability closure.

## Exact provider evidence

Temporary NON-MERGE clean-room audit PR **#626**:

- CurseForge project/file: `1046916 / 6342780`;
- exact SHA-1: `3808493ce45cdfeb6408e85578adecf13df698e8`;
- authoritative audit HEAD: `5670beca2b61ee5e302bd95db3c6bb595ddeb152`;
- workflow run: `37251558059` — **SUCCESS**;
- text artifact: `11321475072`;
- artifact digest: `sha256:1b3bb4e570afa9dd0a0333dc00b4e36eb7a16baf7b31d690dc41293ff8550b9d`.

Bounded retained results:

- `BlackoutSpell` itself declares no `allowLooting()`;
- provider ancestor `AbstractUniqueSpell` declares `allowLooting()` as a constant **false**;
- provider JSON files scanned: **151**;
- structured `traveloptics:blackout` references: **0**;
- `spell_filter` nodes: **23**;
- `randomize_spell` nodes: **23**;
- forced Eldritch filters: **0**;
- explicit Blackout filters: **0**;
- all 23 retained filters are explicit spell lists and none contains Blackout;
- provider classes scanned: **250**;
- provider classes referencing host `SpellFilter`: **0**;
- provider classes referencing host `RandomizeSpellFunction`: **0**;
- provider classes referencing `BLACKOUT_SPELL`: **1** — `TOSpells` registry only.

No method bodies, bytecode instruction sequences, reconstructed formulas, assets, localization prose or binary content are retained.

## Current Iron's host contract

Current physical Iron's Spellbooks is `1.21.1-3.16.3`, with source authority pinned at:

`iron431/irons-spells-n-spellbooks@e4056af90302d37eb1739f5ff05020b020e6e252`.

At that pin:

- `SpellFilter.isSpellAllowed(spell)` requires `spell.isEnabled()` and, unless `force=true`, `spell.allowLooting()`;
- school/global filter generation therefore excludes non-lootable spells unless forced;
- explicit spell-list filters retain their listed spell identities and are independently bounded by the exact JSON audit;
- `RandomizeSpellFunction` obtains candidates from its `SpellFilter`.

The exact Traveloptics audit found no forced Eldritch filter and no explicit list containing Blackout.

## Exact-alpha conclusion

For publisher File `6342780`:

- Blackout is registered;
- Blackout is non-craftable through the provider Unique gate;
- Blackout is also non-lootable through that provider Unique ancestry;
- no direct structured Blackout acquisition anchor exists;
- no built-in explicit random-spell filter includes Blackout;
- no school/global forced filter can re-admit it;
- no provider-owned code path references `BLACKOUT_SPELL` outside the registry.

Therefore:

**the exact alpha's provider-owned direct + built-in generic Iron's loot surfaces do not expose a Blackout acquisition route.**

This materially narrows Gate 3, but does not prove that Blackout is impossible to obtain in the assembled modpack.

## Still open

The audit does not exclude:

- external datapacks;
- KubeJS/server scripts;
- progression/reward mods outside the Traveloptics JAR;
- commands/creative access, which do not count as survival reachability;
- a different acquisition path present only in the current physical Traveloptics SHA-1 `7b74816e89cc15dd0b5a31d9ea1e456024e8fae4`;
- runtime injection by another provider.

The current physical Traveloptics artifact remains `OTHER_VERIFIED` relative to File `6342780`; exact-current registry/content equality is not proven.

A separate retained-evidence search found no **literal/object-specific acquisition route** for Blackout after excluding Black Arcana's Traveloptics QA-probe references as read-only observation. No preserved Library KubeJS/datapack source resolving to Blackout was found. Generic external school/global `SpellFilter` / `RandomizeSpellFunction` routes remain unresolved because they may not mention `blackout` or `traveloptics` literally. This is **negative retained-evidence only**, not proof that the assembled current pack has no external route. See [`BLACKOUT-EXTERNAL-ROUTE-RETAINED-EVIDENCE-CHECKPOINT.md`](BLACKOUT-EXTERNAL-ROUTE-RETAINED-EVIDENCE-CHECKPOINT.md).

## Catalog consequence

Blackout remains:

`REGISTERED / UNIQUE / allowCrafting=false / allowLooting=false / EXACT-ALPHA BUILT-IN LOOT EXCLUDED / NO PRESERVED LITERAL ROUTE FOUND / GENERIC EXTERNAL FILTERS UNRESOLVED / CURRENT-PACK SURVIVAL REACHABILITY UNVERIFIED`.

To close current-pack acquisition, require a concrete external/current route resolving specifically to `traveloptics:blackout`, or an exact-current physical/runtime attestation proving such a route.

Black Arcana must not synthesize or repair provider acquisition.
