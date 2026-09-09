# Capability-matrix delta — Monsters & Spellbooks 0.0.16.3

## Provider closure signal

Monsters & Spellbooks contributes a large Iron's-hosted spell surface: **98 registered spell objects** in the current public registry inventory. The inspected source also exposes Necro and Aero SchoolType registrations, but those school observations are not exact 0.0.16.3 binary pins; Aero runtime existence is specifically `NÃO VERIFICADO` because the exact release line removes Aero content.

This delta is for deduplication. It does **not** declare 98 Black Arcana gaps.

## Registration distribution

| Source family | Count | Deduplication handling |
|---|---:|---|
| blood | 5 | compare against existing blood/curse providers and Black Arcana Blood & Curses; no automatic equivalence |
| ender | 12 | compare against displacement/void/gravity/Ender providers; preserve provider casting authority |
| evocation | 3 | compare as Iron's-hosted support/defense identities |
| fire | 10 | compare against fire/black-flame providers; theme alone does not prove Black Flame equivalence |
| holy | 4 | compare against Holy/Paladin/divine providers |
| hydro | 8 | compare against water/hydro providers |
| ice | 8 | compare against existing Ice providers |
| lightning | 14 | compare against lightning/redstone/electric providers |
| nature | 7 | compare against poison/nature/summon providers |
| necro | 25 | compare against souls/death/necro providers; do not map automatically to Black Arcana Corruption/Strain |
| technomancy | 2 | compare against technology/magic and summon/projectile providers |
| **Total** | **98** | **provider identities, not automatic gaps** |

## Strong overlap candidates

The source identities expose obvious candidates for semantic comparison with already cataloged capability families, including:

- teleport/displacement/space/gravity;
- summon/minion/army/patrol/drone;
- forms/aspects/transformative state;
- fields/mines/area denial;
- life drain/soul/fire/wither/necro;
- slash/cleave/projectile/beam/blast/nova;
- buff/protection/undying/intervention;
- frost/terrain/hydro/nature/poison;
- lightning/redstone/electric effects.

These labels only establish **review queues**. Individual equivalence requires behavior-level evidence.

## Authority matrix

| Capability surface | Authority/evidence boundary |
|---|---|
| spell registration/implementation | Monsters & Spellbooks, hosted by Iron's; 98 source identities closed semantically |
| host cast engine | Iron's Spells 'n Spellbooks |
| provider spell mana/cooldown | Iron's/provider contracts |
| source-observed Necro school power/resistance/damage identity | Monsters & Spellbooks source; exact installed parity not asserted |
| source-observed Aero school | stale source-head observation; installed 0.0.16.3 existence `NÃO VERIFICADO` after release-line removal |
| Black Arcana Corruption/Strain/Arcane Danger | Black Arcana only |
| Black Arcana destructive mutations | Black Arcana `WorldEffectPolicy` only |
| RPG Skill Tree Mastery/progression | sibling RPG provider only through real boundary |

## Dedupe consequences

Phase 3 must **not** add a capability merely because Monsters & Spellbooks uses a different spell name. Conversely, the presence of a similarly named spell does not automatically eliminate a Black Arcana concept if authority, invocation, costs, lifecycle or semantic result are materially different.

Specific no-duplication rules:

- do not double-cast an Iron's spell and a mirrored Black Arcana effect;
- do not debit Iron's mana twice;
- do not mirror a provider summon into another authoritative entity lifecycle;
- do not create a second Necro stat ledger;
- do not convert provider Necro effects into Corruption/Strain without a causal adapter;
- do not assume `monstersspellbooks:aero` exists in the installed 0.0.16.3 runtime;
- do not treat Aero's source-head SchoolType observation as an active spell inventory.

## Evidence ceiling

The 98-registration inventory is closed at semantic/source identity level. Exact 0.0.16.3 numerical/API internals and uncertain installed-school surfaces remain fail-closed because the contemporaneous public source tree keeps stale 0.0.14 build metadata and the release line explicitly removes Aero content.

This closure is sufficient to move the provider out of the `inventory unknown` bucket; it is not sufficient to authorize runtime integration against unverified exact binary signatures or school registrations.
