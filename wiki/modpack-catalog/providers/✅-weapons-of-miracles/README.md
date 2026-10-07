# Weapons of Miracles — 2.0.178

Status: `✅ CATALOGED / EXACT PHYSICAL=PUBLISHER ARTIFACT / 64-SKILL REGISTRY FULLY DISPOSITIONED / 13 SUPERNATURAL ACTION ROOTS / 12 COUNTED_EXACT + 1 CONDITIONAL / RUNTIME QA SEPARATE`

## Current physical identity

Current sibling authority: `neoforge-rpg-skilltree` current physical dossier for row **#568**.

- JAR: `WeaponsOfMiracles-2.0.178.jar`;
- mod id: `wom`;
- runtime: `2.0.178`;
- Minecraft / loader: 1.21.1 / NeoForge;
- physical SHA-1: `b507eb376778cfd1cbecec2841c38891b26a7349`;
- required combat host in the pack: Epic Fight `21.17.3.1`.

The provider is cross-domain rather than a general spell engine. It owns Epic Fight skills, unique weapon techniques and several explicitly supernatural actions. Only the latter qualify for the semantic-magic ledger.

## Exact publisher-artifact closure

NON-MERGE evidence PR **#499** audits CurseForge project/file `918614 / 8829395` and hard-gates the downloaded artifact against the physical pack fingerprint.

Final semantic evidence checkpoint used by this catalog:

- audit HEAD: `1e63f962843d740beb93e4949f8d7efa19124059`;
- exact-artifact run: `36907520048` — **SUCCESS**;
- evidence artifact: `11186035998`;
- artifact digest: `sha256:425ff719514fa7a1d226c5967b0889712f666fe05cc65b0e2aae8dcde4b29ba8`;
- publisher SHA-1: `b507eb376778cfd1cbecec2841c38891b26a7349`;
- publisher SHA-256: `0c36ba17bc812c65f5e37f9227d8b6a5185aac70b82a88d1bf52ee13103592cc`;
- bytes: `20,941,584`.

The publisher SHA-1 exactly equals the physical sibling SHA-1.

See [`EXACT-2.0.178-ARTIFACT-AUDIT.md`](EXACT-2.0.178-ARTIFACT-AUDIT.md).

## Exact skill registry — 64 IDs

The exact `WOMSkills` registrar closes **64 unique provider-owned skill IDs**:

- 8 dodge skills;
- 6 guard skills;
- 14 passive skills;
- 3 mover skills;
- 8 identity skills;
- 15 weapon-innate skills;
- 10 weapon-passive skills.

The publisher description's historical/public `27 skills` figure is therefore not used as the technical denominator. The exact installed JAR is authoritative.

Every one of the 64 IDs is dispositioned in [`skills/SKILL-DISPOSITION-2.0.178.md`](skills/SKILL-DISPOSITION-2.0.178.md).

## Semantic-magic result — 13 supernatural action roots

Under the canonical semantic-magic rule, WOM contributes **13 discrete supernatural player-action identities**:

### Exact and currently catalog-reachable — 12

1. `wom:ender_step` — Ender Step;
2. `wom:ender_obscuris` — Ender Obscuris;
3. `wom:shadow_step` — Shadow Step;
4. `wom:time_travel` — Time Travel;
5. `wom:voodoo_magic` — Voodoo Magic;
6. `wom:avatar_of_might` — Avatar of Might;
7. `wom:agony_plunge` — Sky Dive;
8. `wom:true_berserk` — True Wrath;
9. `wom:demonic_ascension` — Demonic Ascension;
10. `wom:plunder_perdition` — Ender Ritual;
11. `wom:lunar_eclipse` — Lunar Eclipse;
12. `wom:solar_arcano` — Solar Arcano.

These twelve have exact current identity plus a provider-native acquisition route closed at catalog level: the first six are present in the exact WOM Epic Skills tree; the weapon-bound roots map to exact owners whose current recipe/chest-loot route is proven in the hash-matched artifact.

### Cataloged but reachability-open — 1

13. `wom:flash_mutilation` — Flash Mutilation.

The exact weapon capability maps this root to `wom:nova`. The audited exact recipes and the provider's chest/drop classes do not close a normal acquisition route for Nova, so the identity remains **`CONDITIONAL`** and contributes **+0 strict**.

Object-level cards:

- aggregate: [`actions/SUPERNATURAL-ACTION-CARDS.md`](actions/SUPERNATURAL-ACTION-CARDS.md);
- [Ender Step](actions/ender-step.md);
- [Ender Obscuris](actions/ender-obscuris.md);
- [Shadow Step](actions/shadow-step.md);
- [Time Travel](actions/time-travel.md);
- [Voodoo Magic](actions/voodoo-magic.md);
- [Avatar of Might](actions/avatar-of-might.md);
- [Sky Dive](actions/sky-dive.md);
- [True Wrath](actions/true-wrath.md);
- [Demonic Ascension](actions/demonic-ascension.md);
- [Ender Ritual](actions/ender-ritual.md);
- [Lunar Eclipse](actions/lunar-eclipse.md);
- [Solar Arcano](actions/solar-arcano.md);
- [Flash Mutilation](actions/flash-mutilation.md).

Individual-card checkpoint: [`INDIVIDUAL-ACTION-CARDS-CHECKPOINT.md`](INDIVIDUAL-ACTION-CARDS-CHECKPOINT.md).

## Why the other 51 skill IDs do not count

The semantic-magic ledger counts an equivalent discrete **supernatural player action**, not every Epic Fight skill.

The remaining 51 exact skill IDs are explicitly excluded because they are one or more of:

- ordinary or enhanced dodge/roll/charge/kick/guard/parry/combo techniques;
- passive/reactive stat, damage, stamina or trigger behavior;
- locomotion helpers such as wall running, swimming or sprinting;
- automatic identity/combat triggers rather than a supernatural causal action;
- weapon-passive support;
- ordinary reload/resource management;
- explicitly technological weapon actions (`ender_blast`, `ender_fusion`, `orbital_beam`);
- active weapon-combat states whose exact evidence does not establish a supernatural/arcane action (`regierung`, `sakura_state`, `unbreakable`, `charybdis`).

`soul_protection` and `shulker_cloak` are not promoted merely because their names are magical-looking: exact bytecode ties them to reactive `TAKE_DAMAGE_PRE` guard behavior with charge/state, not to an independent player cast.

`meditation` is explicitly a provider `PassiveSkill`, and `voodoo_magic` is deliberately treated differently: its exact identity path uses player input/state to cause a health↔stamina conversion, so it is a distinct supernatural player action rather than a passive proc.

## Acquisition and ownership boundary

Exact current evidence closes:

- WOM Epic Skills tree acquisition for all six counted non-weapon roots;
- `wom:agony` via provider chest-loot injection -> `agony_plunge`;
- `wom:tormented_mind` via provider chest-loot injection -> `true_berserk`;
- `wom:antitheus` exact smithing recipe -> `demonic_ascension`;
- `wom:ruine` via provider chest-loot injection -> `plunder_perdition`;
- `wom:moonless` via provider chest-loot injection -> `lunar_eclipse`;
- `wom:solar` exact crafting recipe -> `solar_arcano`.

`wom:nova` is present and maps to `flash_mutilation`, but normal current acquisition remains unresolved in the bounded exact audit.

Epic Fight remains authority for its combat/skill runtime. WOM remains authority for these skill identities, owner bindings, resource/cooldown state, animations, effects and settlement. Black Arcana must not replay WOM actions, charge a second cost, or treat individual downstream teleports/effects/projectiles as new identities.

## Strict semantic disposition

- exact WOM skill registry: **64**;
- supernatural semantic roots: **13**;
- `COUNTED_EXACT`: **12**;
- `CONDITIONAL`: **1** (`flash_mutilation`);
- `EXCLUDED`: **51**;
- strict semantic delta: **+12**.

## Runtime QA remains separate

Catalog closure is not an assembled-pack runtime PASS. Later QA still includes Epic Fight input/animation compatibility, multiplayer causal settlement, owner persistence, skill-tree progression, loot/recipe overrides, optional gamerules and coexistence with other Epic Fight addons.

## Result

**✅ Cataloged — exact current skill denominator closed and fully dispositioned.**

Current WOM semantic inventory: **13 supernatural action roots = 12 strict + 1 reachability-conditional**.
