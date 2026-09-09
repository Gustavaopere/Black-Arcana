# Monsters & Spellbooks 0.0.16.3

Status: `PHASE 2AH — PARTIAL / EXACT PHYSICAL+RELEASE / CURRENT PUBLIC SOURCE BASELINE WITH STALE BUILD METADATA`

## Physical identity

- Mod id: `monstersspellbooks`
- Physical JAR: `monstersspellbooks-0.0.16.3.jar`
- Runtime version: `0.0.16.3`
- Physical SHA-1: `b3aa89fd081bf4bfaf8d0f4380bcdc393c66ab0e`
- Minecraft: `1.21.1`
- Loader: NeoForge `21.1.248`
- Relevant host: Iron's Spells 'n Spellbooks `1.21.1-3.16.3`

The physical pack and the exact CurseForge release agree on filename/version. CurseForge project `1428928`, File ID `8788560`, is the exact public NeoForge 1.21.1 release uploaded 2026-09-01.

## Evidence boundary

The official public source repository is `RedReaper28/Monsters-Spellbooks-1.21.1`. Its current `main` head inspected for this checkpoint is `1ab9b72af2ea44c3c8b816e665d06531ea44ddc2`, also dated 2026-09-01.

That source head is **not** promoted to exact 0.0.16.3 artifact authority because its `gradle.properties` still declares:

- `mod_version=0.0.14`;
- NeoForge `21.1.216`;
- Iron's `1.21.1-3.15.4`.

The installed pack instead runs NeoForge `21.1.248` and Iron's `1.21.1-3.16.3`. No release tag or commit declaring `0.0.16.3` was found in the official repository. Exact installed-JAR bytes were not available for local inspection.

Therefore this catalog has three explicit layers:

1. **exact physical/release 0.0.16.3** — identity, file/release metadata and exact published 0.0.16.3 changelog;
2. **current public source baseline** — registrations and code structure observed at official source head `1ab9b72...`, but not asserted to equal the installed binary;
3. **exact 0.0.16.3 internals** — registry parity, exact class/signature/API/config/network/save behavior remain `UNVERIFIED / FAIL-CLOSED` unless independently proven by release-exact evidence.

## Provider classification

Primary class: `IRON'S SPELL CONTENT PROVIDER / CUSTOM SCHOOLS / GEAR+MOBS+WORLD CONTENT`.

The publisher describes the current line as adding **90+ spells, 2 new spell schools**, substantial gear and enemies. Public project scope also includes armor, weapons, ores, accessories, mobs and structures. These public scale statements are not substituted for an exact installed registry inventory.

The current public source baseline registers 98 `AbstractSpell` objects grouped across 11 families. That 98 count is recorded as **source-baseline inventory**, not as proof that the installed 0.0.16.3 JAR contains exactly 98 active spells.

See [`SPELL-INVENTORY-SOURCE-BASELINE.md`](SPELL-INVENTORY-SOURCE-BASELINE.md).

## Source-baseline schools

The source head registers provider school ids:

- `monstersspellbooks:necro`;
- `monstersspellbooks:aero`.

Necro is a provider-owned school with its own focus/power/resistance/cast/damage surfaces in the source baseline.

Aero requires special caution. The exact 0.0.16.3 changelog says some remaining Aero content was deleted to avoid tag interference, while the public source head still contains an Aero school registration and the source spell registry contains no Aero spell registrations. Exact installed 0.0.16.3 Aero registration/status is therefore **not proven**.

See [`SCHOOLS-AND-AUTHORITY.md`](SCHOOLS-AND-AUTHORITY.md).

## Exact 0.0.16.3 release delta

Publisher release notes for File ID `8788560` report changes in these areas:

- removal of some remaining Aero content/files to avoid tag interference;
- stronger Fall Curse slowness;
- reduced Wither Bomb nerf;
- further Necro visual changes;
- Necro Rune jewellery insertion fix;
- attribute-operation correction;
- effect-removal correction.

These are exact release-delta facts. They do not prove complete class/registry/config parity with the current public source tree.

## Black Arcana authority and deduplication

Iron's remains authority for its base spell engine, mana and standard cast lifecycle. Monsters & Spellbooks remains authority for its own provider spell/school/content behavior when that behavior is actually present. Black Arcana remains authority for its own canonical cast pipeline, spell domains, hazards, Corruption, Strain, Arcane Danger and world-safety runtime.

Black Arcana must not:

- debit Iron's mana a second time for one provider cast;
- replay provider damage, summons, debuffs, buffs, projectiles or attribute settlement;
- infer an exact provider school/resource/API hook from spell names or source-baseline classes;
- equate provider `Necro` automatically with Black Arcana Souls & Death, Goety Soul Energy, Malum spirits, Corruption, Strain, Arcane Danger or RPG Mastery;
- treat names such as `Lichdom`, `Soul *`, `Gravity *`, `Space *` or `Wither *` as proof of a Black Arcana implementation gap;
- bypass provider targeting/ownership/friendly-fire/world-effect semantics with a second execution path.

Any future adapter that depends on exact 0.0.16.3 registries, classes, events, config keys or signatures remains **fail-closed** until those contracts are proven against the installed release.

## Coverage consequence

Phase 2AH does **not** increment the global catalog numerator. Canonical coverage remains **36/100** because the current-version registry/internals delta is unresolved. This is deliberate application of the catalog rule that a partial provider or unresolved current-version delta contributes zero closed-component points.

Phase 3 remains blocked.

## Provenance

See [`EVIDENCE-AND-PROVENANCE.md`](EVIDENCE-AND-PROVENANCE.md).