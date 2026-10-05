# Traveloptics 4.4.0.1 — Blackout versioned acquisition boundary

Status: `PUBLISHER ROUTE EXISTS ON FULL PROJECT / 1.20.1 INTRODUCTION CONFIRMED / EXACT 1.21.1 GENERIC RANDOM LOOT ROUTE NEGATIVE / OTHER ACQUISITION + CURRENT-PHYSICAL REACHABILITY STILL UNVERIFIED`

## Purpose

The public T.O Magic n' Extras project page currently describes a concrete acquisition route for **Blackout**:

- `Call Forth The Dead King` summons the Enraged Dead King;
- defeating the Enraged Dead King can yield the exclusive Blackout spell;
- the page describes Blackout as obtainable from that boss.

That route is real publisher documentation for the broader project, but it is **not automatically evidence for the installed deprecated 1.21.1 alpha**.

The current pack uses:

- `traveloptics-4.4.0.1-1.21.1.jar`;
- CurseForge File `6342780`;
- NeoForge 1.21.1;
- publisher status: deprecated alpha / partial port.

## Versioned publisher evidence

Official CurseForge sources:

1. project page:
   `https://www.curseforge.com/minecraft/mc-mods/to-tweaks-irons-spells`

   The current description documents the Dead King → Blackout route for the full project.

2. 1.20.1 File `6010839`:
   `https://www.curseforge.com/minecraft/mc-mods/to-tweaks-irons-spells/files/6010839`

   Its changelog explicitly introduced together:

   - spell `Blackout`;
   - spell `Call Forth The Dead King`;
   - entity `Enraged Dead King`.

   This is strong evidence that the documented boss acquisition loop belongs to the full 1.20.1 feature line.

3. installed-version publisher File `6342780`:
   `https://www.curseforge.com/minecraft/mc-mods/to-tweaks-irons-spells/files/6342780`

   The publisher labels this 1.21.1 build a deprecated alpha and states that only about 20% of the project had been ported. The file note says Cataclysm-based spells and some items are present, while large portions of content/mechanics are missing.

The generic project page therefore cannot be projected onto File `6342780` without artifact/runtime evidence that the relevant boss/acquisition chain exists in this alpha.

## Exact 1.21.1 artifact evidence

The existing exact clean-room audit of File `6342780` already proves:

- `traveloptics:blackout` is one of the **33 exact registered spell identities**;
- `BlackoutSpell` inherits the non-craftable Unique-spell gate;
- no direct structured loot/resource reference to `blackout` was found;
- no provider-owned reference to `TOSpells.BLACKOUT_SPELL` outside the spell registry was found;
- the exact artifact carries **32 residual localization-only spell roots** that are absent from the active registry;
- `call_forth_the_dead_king` is among those residual/unregistered localization roots.

The exact resource audit also enumerated **41 loot/loot-modifier JSON resources** for File `6342780`. They cover the alpha's current Cataclysm/chest surfaces, including entities such as Leviathan, Ignis, Maledictus, Kobolediator, Koboleton, Prowler, Watcher and others. No Enraged Dead King loot/resource identity appears in that exact structured-resource inventory.

### Exact-alpha generic/randomized loot boundary

A focused clean-room follow-up now closes the ordinary Iron's randomized-loot exception space for File `6342780`.

Temporary NON-MERGE audit **#626**, HEAD `5670beca2b61ee5e302bd95db3c6bb595ddeb152`, run `37251558059` SUCCESS, text artifact `11321475072`, digest `sha256:1b3bb4e570afa9dd0a0333dc00b4e36eb7a16baf7b31d690dc41293ff8550b9d`, establishes:

- `BlackoutSpell` inherits provider `AbstractUniqueSpell.allowLooting()`;
- that exact provider override is constant **false**;
- 151 provider JSON files contain 23 `spell_filter` / `randomize_spell` nodes;
- all 23 filters are explicit spell lists;
- structured references to `traveloptics:blackout`: **0**;
- explicit Blackout filters: **0**;
- forced Eldritch school filters: **0**;
- across 250 provider classes, references to host `SpellFilter`: **0** and `RandomizeSpellFunction`: **0**;
- `BLACKOUT_SPELL` is referenced only by `TOSpells`, the registry holder.

Current Iron's 3.16.3 source pin `e4056af90302d37eb1739f5ff05020b020e6e252` defines ordinary random-loot admission through `allowLooting()`, while explicit spell lists or `force=true` school filters can bypass that predicate. The exact Traveloptics artifact contains neither bypass for Blackout.

Therefore **provider-owned generic/randomized loot is a negative result for exact File `6342780` under current Iron's 3.16.3 semantics**. This still does not exclude external datapack/KubeJS/progression grants, another provider-specific acquisition mechanism not captured by the audited loot surface, or changes in current physical SHA-1 `7b74816e...`.

Canonical detail: [`BLACKOUT-GENERIC-LOOT-EXCLUSION-CHECKPOINT.md`](BLACKOUT-GENERIC-LOOT-EXCLUSION-CHECKPOINT.md).

This establishes a version boundary:

- the publisher's broader Dead King → Blackout route is real;
- the exact 1.21.1 alpha does **not** expose the supporting Dead King route in the structured surfaces already audited;
- its provider-owned generic/randomized loot surface also excludes Blackout under the current Iron's 3.16.3 host contract;
- this does **not** prove Blackout is impossible to obtain by every conceivable runtime path;
- it does prove that the generic 1.20.1/full-project route is insufficient evidence for the installed alpha.

## Current Gate 3 acceptance rule

To close `traveloptics:blackout` for the actual 1.21.1 pack, require one of:

1. an authoritative File-6342780-specific/provider source showing a 1.21.1 acquisition mechanism;
2. an actual assembled-pack datapack/script/loot/progression route resolving specifically to `traveloptics:blackout`;
3. deterministic current-pack runtime observation of a survival acquisition path, with the physical Traveloptics hash identified.

Do **not** close the gate using only:

- the current broad project description;
- a 1.20.1 changelog;
- creative/commands;
- the registry identity;
- `.guide`/localization text;
- generic statements that "spells are obtainable in survival".

## Catalog consequence

Traveloptics remains **⚠️ Parcial / condicionado**.

- registered inventory remains 33 exact publisher-release identities;
- strict semantic delta remains `+0` while current-pack reachability/runtime gates remain open;
- Blackout remains an exact registered but reachability-unresolved identity;
- the Dead King route is retained as **versioned historical/publisher context**, not current-alpha acquisition proof.

Black Arcana must not synthesize a Dead King route, inject a Blackout scroll, or repair missing provider progression.
