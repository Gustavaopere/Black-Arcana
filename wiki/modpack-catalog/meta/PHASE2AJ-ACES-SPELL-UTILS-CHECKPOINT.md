# Phase 2AJ checkpoint — Ace's Spell Utils 1.2.7.2

## State

`CATALOG CLOSURE CANDIDATE / NOT CANONICAL UNTIL LATEST-MAIN RECONCILIATION + EXACT-HEAD CI GREEN + MERGE`

## Base

- initial canonical `main`: `9e2011a46e228fb8e2dd7c9d275c6f43290f6bb8`
- branch: `docs/magic-catalog-phase2aj-aces-spell-utils-1.2.7.2`
- canonical coverage at branch creation: `37/100 = 37%`
- candidate result after merge: `38/100 = 38%`

No equivalent open PR/branch was found immediately before branch creation.

## Physical identity

- artifact: `aces_spell_utils-1.2.7.2-1.21.1.jar`
- mod id: `aces_spell_utils`
- version: `1.2.7.2-1.21.1`
- physical SHA-1: `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca`
- CurseForge project/file: `1299492 / 8789930`
- exact publisher release: `2026-09-02`, Minecraft 1.21.1 NeoForge
- license: MIT

## Exact source pin

Official source revision:

`AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`

Source metadata at that revision declares exactly:

- `mod_version=1.2.7.2-1.21.1`
- Minecraft `1.21.1`
- NeoForge `21.1.230`
- Iron's `1.21.1-3.11.0`

Physical pack currently runs NeoForge `21.1.248` and Iron's `1.21.1-3.16.3`. Exact host-runtime compatibility therefore remains QA/fail-closed; source inventory identity remains exact to the published version line.

## Closure inventory

Standalone provider spells:

- **0** `registerSpell(...)` calls / **0** provider standalone spell registrations.

Exact source registry/runtime surface:

- 3 Iron's SchoolTypes: `ritual`, `hydro`, `technomancy`;
- 19 attributes: 13 general + 6 school power/resistance;
- 3 school damage-type keys;
- 1 copy-on-death Boolean attachment;
- 1 custom trail particle type;
- 14 tag contracts: 9 item + 3 entity + 2 spell;
- 8 NeoForge rarity enum extensions;
- 27 unconditional `example_*` item registrations;
- 8 optional protocol `4.0.0` S2C visual payloads;
- 2 required mixins;
- 5 common config values;
- reusable entity/boss/item/staff/mace/curio/summon/domain/VFX API families;
- provider server-event runtime for 11 attribute/proc families plus magic-gun casting, keep-inventory and VFX maintenance.

## Important normalization decisions

1. `aces_spell_utils:ritual` remains the registry identity even though current publisher display language calls the school Occult. No `aces_spell_utils:occult` school is invented.
2. `aces_spell_utils:hydro` is the real ResourceLocation. The source supplier named `ABYSSAL` and old comment do not create an Abyssal registry.
3. 27 `example_*` item registrations are cataloged as real registry objects but do not count as spells/capabilities by simple cardinality.
4. The custom creative tab is dev-only; example item registration is not.
5. `AbstractDomainEntity` is a third-party helper and never becomes Black Arcana domain/casting authority.
6. Network payloads registered by `PayloadHandler` are all client-bound VFX transport; they are not C2S cast intent.
7. Source-version equality is not promoted to byte-for-byte source/JAR equivalence without independent reproducibility evidence.

## Architecture consequences

- Iron's remains cast/mana/cooldown authority for Iron's spells.
- Ace's owns its shared attributes/proc helpers/mixins/attachments/VFX/API behavior.
- concrete consuming addons retain authority over spells/items/entities they build on this API.
- Black Arcana retains one canonical server-authoritative magic runtime, Corruption, Strain, Arcane Danger and WorldEffectPolicy.
- RPG Skill Tree remains progression/mastery provider only through real contracts.
- no second Mana Steal/Mana Rend/crit/healing/iframe/death-copy pipeline.
- no duplicate cast from magic-gun/passive helper paths.

## Files in Phase 2AJ

Provider tree:

- `wiki/modpack-catalog/providers/aces-spell-utils/README.md`
- `REGISTRIES-AND-ATTRIBUTES.md`
- `API-AND-RUNTIME-SURFACES.md`
- `NETWORK-MIXINS-AND-EXAMPLES.md`
- `EVIDENCE-AND-PROVENANCE.md`

Meta:

- `CAPABILITY-MATRIX-DELTA-ACES-SPELL-UTILS.md`
- this checkpoint
- current provider queue
- current coverage ledger

## Remaining QA after catalog closure

These do not reopen semantic catalog closure but continue fail-closed for runtime integration:

- source↔physical-JAR byte equality;
- exact behavior against pack Iron's 3.16.3 / NeoForge 21.1.248;
- Evasive event+mixin combined runtime;
- event ordering with Apothic Attributes/other proc providers;
- full-modpack client/dedicated-server VFX and passive-item behavior;
- stable API guarantees for any future Black Arcana adapter.

## Merge gate

Component #38 is awarded only after:

1. latest `origin/main` re-fetch;
2. semantic reconciliation if main advanced;
3. diff review;
4. PR review blockers resolved;
5. full Black Arcana CI GREEN on the exact reconciled HEAD;
6. immediate final `main` fetch;
7. merge with expected head SHA;
8. confirmation of final `main` SHA.

Until then canonical coverage remains **37/100**.
