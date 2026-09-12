# Leyline Spellbooks 1.0.3

Status: `EXACT HASH-MATCHED 1.0.3 ARTIFACT / 14 CURRENT REGISTERED SPELL IDENTITIES / NO PROVIDER-SPECIFIC SPELL LOCK OBSERVED / HOST RUNTIME/API QA FAIL-CLOSED`

## Installed authority

- Current JAR: `leylines-1.0.3.jar`
- Mod id: `leylines`
- Runtime version: `1.0.3`
- Minecraft / loader: `1.21.1` / NeoForge
- CurseForge project: `1636676`
- CurseForge file: `8565076`
- Release date: `2026-08-02`
- License: `All Rights Reserved`
- Physical modlist hash: `dfa6908731f432905caaaa1e53b4aedeaa26ed59`
- Provider class: `SPELL PROVIDER / CONTENT + WORLD SYSTEM ADDON`
- Required casting provider: Iron's Spells 'n Spellbooks

The physical modlist is authoritative for the installed JAR/runtime/hash. The current physical snapshot and an independent public manifest for CurseForge File ID `8565076` agree on SHA-1 `dfa6908731f432905caaaa1e53b4aedeaa26ed59`. A previous catalog revision incorrectly assigned SHA-1 `5307a4edc885ab949eed4438d9d7f9cb6176421d` to Leylines; independent manifests associate that hash with `letsdo-wildernature-neoforge-1.1.5.jar` / CurseForge File ID `8543233`. That stale value is rejected for Leylines and must not be reintroduced.

## Official provider identity

The publisher describes Leyline Spellbooks as an Iron's addon with a dedicated **Leyline** school built around underground arcane currents, spatial/temporal manipulation and a world loop of night-time pillars and wave-based Leyline Rifts.

The provider therefore owns more than discrete casts. Its semantic surface includes:

- Leyline school identity;
- underground ley-current/world infrastructure;
- night-time pillar discovery/charging;
- Leyline Rift encounter lifecycle;
- theme loot, XP and Ley Crystal reward chance;
- Leyline Codex and Ley Staff attunement/progression surfaces;
- spell behavior exposed through Iron's casting substrate.

## Public signature-spell lower bound

The official project page names **nine** signature spells. It explicitly ends with `and more`, so nine is a public lower bound, **not** a complete registry count.

1. [Blink Step](spells/blink-step.md) — vanish/reappear with a burst of haste.
2. [Rift Gate](spells/rift-gate.md) — place two linked portals.
3. [Chrono Tether](spells/chrono-tether.md) — slow what is ahead while accelerating the caster.
4. [Temporal Stutter](spells/temporal-stutter.md) — briefly freeze a foe in its timeline.
5. [Fissure](spells/fissure.md) — rupture the ground and launch enemies upward.
6. [Anchor Recall](spells/anchor-recall.md) — mark a position and later return to it.
7. [Beam](spells/beam.md) — name confirmed; individual mechanics not published.
8. [Ley Blast](spells/ley-blast.md) — name confirmed; individual mechanics not published.
9. [Eclipse](spells/eclipse.md) — name confirmed; individual mechanics not published.

The public page groups Beam, Ley Blast and Eclipse under a general sentence about building charges, spending power and reshaping combat. No individual charge contract is assigned without exact-artifact evidence.

## World / progression evidence

See:

- [RIFT-ENCOUNTERS.md](RIFT-ENCOUNTERS.md) — publisher-confirmed encounter behavior, including 1.0.3 reliability/arena rules;
- [PROGRESSION.md](PROGRESSION.md) — publisher-confirmed pillar/rift/reward/attunement surface;
- [TECHNICAL-AUDIT.md](TECHNICAL-AUDIT.md) — artifact/provenance/evidence ceiling.

The 1.0.3 changelog confirms, at provider-semantic level:

- death during an active rift fails the encounter and prevents completion loot/crystal;
- boss-bar cleanup on death, respawn, logout and dimension change;
- abandonment beyond 60 blocks collapses the active rift;
- wave mobs beyond 40 blocks are pulled back to the arena;
- encounter mobs persist across brief player death rather than causing false clear;
- `/leylines spawnpillar` is permission-level-2 admin/debug tooling, not survival progression.

## Authority and deduplication

Iron's owns the generic addon-facing spellcasting substrate and mana/cast lifecycle where Leyline delegates to it. Leyline Spellbooks owns its school/content semantics, provider progression and rift encounter state.

Black Arcana must not create parallel authority for:

- Rift Gate portal-pair state;
- Anchor Recall anchor persistence;
- Leyline charge/accounting;
- pillar charging;
- rift waves, completion, abandonment or rewards;
- provider spell cooldown/cost/targeting;
- unknown Leyline registry content.

### Space / portals

Rift Gate and Anchor Recall make generic paired-portal and return-anchor concepts provider-occupied. Black Arcana spatial content needs a mechanically distinct forbidden-magic contract and must not write provider portal/anchor state.

### Time / control

Chrono Tether and Temporal Stutter occupy temporal acceleration/slow and brief temporal freeze semantics. Do not implement a second effect/tick-rate pipeline merely to recreate these outcomes.

### World rupture / control

Fissure already occupies ground-rupture + vertical displacement at semantic level. Whether it changes blocks is unknown and must not be inferred.

### Chaos / domains / rifts

Leyline Rifts are provider-owned bounded wave encounters. Black Arcana domains and Chaos effects remain separate authorities and must not claim Leyline completion, rewards or lifecycle.

### Order

Time, portals and spatial control are not sufficient evidence that Leyline is an Order provider. Order candidates still require their own law/seal/constraint identity and semantic deduplication.

## Phase 2BG exact-artifact closure

The previous nine-name publisher list is now historical lower-bound evidence, not the current inventory ceiling. Isolated non-merge PR #194 materialized CurseForge File ID `8565076`, required SHA-1 equality with the physical pack, and closed the installed registry at **14 unconditional provider spell identities**.

Exact IDs and registry fields/classes are recorded in [EXACT-1.0.3-SPELL-INVENTORY.md](EXACT-1.0.3-SPELL-INVENTORY.md); audit methodology and clean-room boundaries are recorded in [EXACT-1.0.3-ARTIFACT-AUDIT.md](EXACT-1.0.3-ARTIFACT-AUDIT.md).

The exact provider artifact exposes no Leylines-specific spell lock or conditional registration gate. Exact Iron's 3.16.3 source corroborates ordinary host eligibility: the Ley school uses the seven-argument `SchoolType` contract (`requiresLearning=false`, `allowLooting=true`), the 14 spell classes do not override `allowLooting()`/`isEnabled()`, and the generic scroll path can select enabled loot-eligible addon spells without a school filter. Leylines additionally injects a dedicated `charge_leyline` scroll. Deployed generic Iron's per-spell config and full-pack runtime behavior remain separate QA rather than being inferred here.

The Phase 2BG semantic delta is canonically **+14**. Durable PR #195 HEAD `a9d7b55044230bbb011f7233ffd75d9a8321489b` passed CI #2503; squash merge `88f042f68429ff920314a7ec3a6923369edc93fd` passed exact-SHA post-merge CI #2504. Canonical totals are **888 semantic objects / 56 of 100 components**.

## Current exactness ceiling

Verified from the exact installed artifact:

- exact JAR/mod id/runtime/hash and CurseForge project/file;
- one `DeferredRegister<AbstractSpell>` with 14 unconditional spell registrations;
- exact 14 spell IDs/classes and `leylines:ley` school identity;
- exact provider progression resource IDs for Ley Crystal, Leyline Codex and Ley Staff;
- codex/staff recipes and advancement chain identities;
- exact dedicated `charge_leyline` scroll injection;
- exact Ley-school/default facts plus Iron's 3.16.3 generic scroll-selection contract, with deployed generic host config still a separate runtime-QA boundary.

Still fail-closed / separate from this catalog closure:

- assembled-pack final numerical config values and balance QA;
- exact final loot probabilities after all modifiers/datapacks;
- pillar/rift persistence structures, networking schema and multiplayer ownership internals;
- a stable supported Black Arcana adapter/API seam;
- full-modpack runtime acceptance.

Leyline remains authority for its school, spells, progression, portal/anchor state and pillar/rift lifecycle. Black Arcana must not duplicate those systems.
