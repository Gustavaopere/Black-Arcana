# Ozymandias Sundries — physical 0.0.5 / embedded metadata 0.0.1

Status: `✅ CATALOGED / EXACT PHYSICAL=PUBLISHER ARTIFACT / 2 REGISTERED IRON'S SPELLS / COUNTED_EXACT / +2 STRICT / RUNTIME QA SEPARATE`

## Current physical authority

- pack JAR: `ozymandias_sundries-0.0.5.jar`;
- mod id: `ozymandias_sundries`;
- distribution/runtime line: `0.0.5`;
- embedded `neoforge.mods.toml` version: `0.0.1`;
- Minecraft / loader: 1.21.1 / NeoForge;
- physical SHA-1: `b973622ed90f47108aba481fec3beb19b432d853`;
- CurseForge project/file: `1209674 / 6978561`.

The embedded `0.0.1` value is preserved as an exact artifact fact. It does not replace the physical/distribution identity `0.0.5`.

Exact NON-MERGE audit branch `audit/ozymandias-sundries-0.0.5-exact-artifact-2026-09-26` materialized File `6978561` and hard-verified the same SHA-1. Physical↔publisher artifact identity is therefore **closed**.

## Provider role

Ozymandias Sundries is an Iron's Spells 'n Spellbooks addon with equipment/spellbook content plus two provider-owned spell registrations. Iron's remains authority for casting, mana, cooldown infrastructure, schools and generic spell configuration. Black Arcana must not duplicate that runtime.

## Fichas por spell

As **2 identidades registradas exatas** deste provider estão materializadas em [`ACTION-CARDS-0.0.5.md`](ACTION-CARDS-0.0.5.md) e nas fichas individuais de `levitate` e `lightning_warp`. Esta camada editorial preserva `COUNTED_EXACT / +2 strict` e não promove classes/localization residuais.

## Exact semantic inventory

The hash-matched current artifact contains one `SpellRegistries` registrar whose static initializer has:

- **2** final `Supplier<AbstractSpell>` fields;
- **2** `registerSpell(...)` calls;
- **0** conditional branches in the static initializer;
- exactly two instantiated registered spell classes.

Current registered identities:

1. `ozymandias_sundries:levitate` — Ender-school `LevitateSpell`;
2. `ozymandias_sundries:lightning_warp` — Lightning-school `LightningWarpSpell`.

See:

- [`EXACT-0.0.5-ARTIFACT-AUDIT.md`](EXACT-0.0.5-ARTIFACT-AUDIT.md);
- [`SPELL-INVENTORY-EXACT.md`](SPELL-INVENTORY-EXACT.md).

## Exclusions and ownership

The exact JAR carries eight provider spell-named classes and three root spell localization IDs, but registry authority wins over class/localization residue.

Therefore:

- `solar_ray` is excluded because it has a localization root/class but no current registry field/call;
- `PerfectWarriorSpell`, `DeathWard`, `SolarRay`, `SunBurstSpell`, `SparkSpell` and `WolfPackSpell` are excluded because they are not instantiated by the exact registrar;
- equipment/spellbooks that embed or reference Iron's-owned spells do not mint new Ozymandias spell identities.

## Host eligibility boundary

The exact artifact packages **0** paths under `irons_spellbooks_spell_config`. Neither registered spell declares provider overrides of:

- `allowCrafting`;
- `allowLooting`;
- `isEnabled`;
- `canBeCraftedBy`.

Both use ordinary Iron's host schools and expose their own `DefaultConfig` / `getSpellResource`. This is sufficient for exact semantic inventory closure under the same rule used for other unconditional Iron's-addon registries. Effective generic Iron's deployed config remains runtime QA and is not silently substituted from defaults.

## Semantic disposition

**+2 `COUNTED_EXACT` semantic magic objects.**

Current strict contribution is exactly the two provider-owned registered spell identities above.

## Runtime QA remains separate

Still fail-closed:

- effective deployed Iron's spell config/datapack overrides;
- live scroll/acquisition distribution in the assembled pack;
- representative casts, recasts and teleport/levitation settlement;
- multiplayer/network behavior;
- balance and interaction with other Iron's addons;
- equipment/spellbook behavior outside the two semantic identities.

## Result

**✅ Cataloged — `COUNTED_EXACT`.**

Current strict semantic contribution: **2 Ozymandias-owned spells**.
