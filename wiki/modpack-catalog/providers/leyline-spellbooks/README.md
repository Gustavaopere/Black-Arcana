# Leyline Spellbooks 1.0.3

Status: `EXACT INSTALLED ARTIFACT IDENTITY / 9 PUBLIC SIGNATURE NAMES / COMPLETE REGISTRY UNKNOWN / FAIL-CLOSED`

## Installed authority

- Current JAR: `leylines-1.0.3.jar`
- Mod id: `leylines`
- Runtime version: `1.0.3`
- Minecraft / loader: `1.21.1` / NeoForge
- CurseForge project: `1636676`
- CurseForge file: `8565076`
- Release date: `2026-08-02`
- License: `All Rights Reserved`
- Physical modlist hash: `5307a4edc885ab949eed4438d9d7f9cb6176421d`
- Provider class: `SPELL PROVIDER / CONTENT + WORLD SYSTEM ADDON`
- Required casting provider: Iron's Spells 'n Spellbooks

The physical modlist is authoritative for the installed JAR/runtime/hash. An older catalog note associated SHA-1 `dfa6908731f432905caaaa1e53b4aedeaa26ed59` with this CurseForge file through an external index. That value does **not** match the current physical modlist and is no longer accepted as the installed-artifact hash.

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

## Current exactness ceiling

Verified:

- exact installed JAR name/mod id/runtime;
- physical modlist hash;
- exact CurseForge project/file/release identity;
- ARR license;
- provider school/world-loop description;
- nine public signature names and six individually described semantics;
- public 1.0.3 rift rules.

Not verified:

- total spell count;
- spell registry IDs/classes;
- levels/rarities/mana/cooldowns/cast times/ranges/damage formulas;
- exact charge implementation;
- item/block/entity/effect/attribute registry inventories;
- recipes/loot probabilities;
- persistence/network/API hooks;
- multiplayer ownership semantics;
- exact supported integration seam beyond normal Iron's addon dependency.

No public source repository for the exact 1.0.3 build was located. The official CurseForge download flow was reached, but the permitted browser/runtime did not expose inspectable JAR bytes. No Java bytecode was decompiled.

**PENDÊNCIA — REQUER ARTEFATO EXATO INSPECIONÁVEL / NAVEGAÇÃO EXTERNA CAPAZ DE ENTREGAR O BINÁRIO**

Until that gate is resolved, this provider remains `FAIL-CLOSED` for internal/API claims and must not be marked `9/9 COMPLETE` or registry-complete.
