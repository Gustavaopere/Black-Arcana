# Hexalia 1.3.6 — Mortar & Pestle Catalog

## Status

`SOURCE-PINNED 1.3.6 / 12/12 REGISTERED RECIPES CATALOGED / EXECUTION LIFECYCLE CONFIRMED / INSTALLED-RUNTIME EQUIVALENCE PENDING`

Canonical source pin:

`AstralyaStudios/Hexalia@4952c65233bf31e9f0d3e55ff76be7fa1007ee3d`

Installed pack identity remains separate: `hexalia-neoforge-1.3.6.jar` reports runtime metadata `1.3.5`, so source-derived behavior is not promoted to exact installed-runtime fact until artifact/runtime QA resolves that mismatch.

## Provider-owned execution contract

Mortar & Pestle is a Hexalia preparation system, not a Black Arcana cast surface.

The 1.3.6 source defines:

- recipe type `hexalia:mortar_and_pestle`;
- shapeless matching;
- exactly 1–3 non-empty ingredient slots per recipe;
- one-item maximum per input slot;
- one output slot;
- `SPIN_TICKS = 20`;
- `REQUIRED_SPINS = 3`;
- output settlement only after the third completed spin;
- input consumption at successful completion;
- shift + empty-hand manual spin interaction;
- redstone-neighbor signal may also start a valid spin automatically;
- pending recipe/progress is persisted by the block entity.

A future Black Arcana integration must therefore not bypass this sequence by directly replacing inputs with outputs unless an explicit provider-supported integration boundary exists.

## 12/12 source-pinned recipes

| Recipe | Inputs | Output | Deduplication significance |
|---|---|---|---|
| `bone_meal_from_mortar` | `minecraft:bone` | `5x minecraft:bone_meal` | mundane utility processing only |
| `sugar_from_mortar` | `minecraft:sugar_cane` | `2x minecraft:sugar` | mundane utility processing only |
| `blaze_powder_from_mortar` | `minecraft:blaze_rod` | `3x minecraft:blaze_powder` | mundane/nether reagent processing; does not create fire-magic authority |
| `salt_from_mortar` | `hexalia:saltsprout` | `hexalia:salt` | feeds Hexalia salting/ritual preparation |
| `mutavis_from_mortar` | `hexalia:tree_resin` + `minecraft:slime_ball` + `#hexalia:crushed_herbs` | `hexalia:mutavis` | creates the provider reagent that drives Hexalia mutation mechanics |
| `siren_paste_from_mortar` | `hexalia:siren_kelp` | `hexalia:siren_paste` | provider reagent used by aquatic/witchcraft preparations |
| `dream_paste_from_mortar` | `hexalia:dreamshroom` | `hexalia:dream_paste` | provider reagent used by brews/rituals/mutations |
| `spirit_powder_from_mortar` | `hexalia:spirit_bloom` | `hexalia:spirit_powder` | provider reagent; must not be conflated with Malum spirit economy or Black Arcana soul state |
| `ghost_powder_from_mortar` | `hexalia:ghost_fern` | `hexalia:ghost_powder` | provider reagent used by stealth/necromantic-adjacent preparations |
| `fragrant_nectar_from_mortar` | `#minecraft:small_flowers` + `minecraft:honeycomb` + `#hexalia:herbs` | `hexalia:fragrant_nectar` | witchcraft/alchemical reagent path |
| `brambleguard_salve_from_mortar` | `minecraft:poppy` + `hexalia:rabbage` + `minecraft:azure_bluet` | `hexalia:brambleguard_salve` | defensive anti-bleeding preparation; see salve behavior audit |
| `menders_salve_from_mortar` | `minecraft:cornflower` + `hexalia:tree_resin` + `minecraft:oxeye_daisy` | `hexalia:menders_salve` | healing/regeneration preparation; see salve behavior audit |

## Salve outputs produced here

Both salves use Hexalia's `SalveItem` execution path:

- 60-tick use time;
- on successful use, the user's canonical `hexalia:bleeding` effect is removed immediately;
- the salve-specific effect is then applied for `20 * 90 = 1800` ticks = 90 seconds;
- the consumed salve does not return a container.

### Brambleguard Salve

`hexalia:brambleguard_salve` applies `hexalia:brambleguard` amplifier 0 for 90 seconds.

The 1.3.6 `BrambleguardEffect` checks active effects every tick and removes any effect whose registry path contains `bleed` or `bleeding`, regardless of namespace. This is broader than merely clearing Hexalia's own Bleeding at application time.

Integration consequence: Black Arcana must not claim Brambleguard as a generic cure for Black Arcana-owned wounds unless that cross-provider interaction is explicitly desired and runtime-tested. The provider implementation is name/path based rather than a Black Arcana status contract.

### Mender's Salve

`hexalia:menders_salve` applies vanilla `minecraft:regeneration` amplifier 0 for 90 seconds after removing canonical `hexalia:bleeding` once at use time.

Unlike Brambleguard, no ongoing generic `bleed`/`bleeding` registry-path purge is supplied by the shared salve wrapper itself.

## Bleeding quantitative note

The source-pinned `hexalia:bleeding` effect applies every tick. At amplifier 0 it deals `HexaliaConfig.bleedingDamage()` generic damage per tick; the 1.3.6 default config value is `0.5`, with `+0.2` damage per amplifier level.

Because the installed JAR reports runtime metadata 1.3.5 while the filename/source release is 1.3.6, this quantitative behavior remains `SOURCE-PINNED / RUNTIME QA PENDING` rather than accepted installed-runtime balance evidence.

## Authority / integration rules

- Hexalia owns recipe matching, Mortar & Pestle progress, output settlement and its reagent graph.
- Do not award Black Arcana casting mastery merely for mortar spins or passive redstone automation.
- If progression credit is ever integrated, it requires a discrete provider completion event with causal player identity; the currently audited block entity does not by itself prove such an event exists.
- Do not duplicate Mutavis, Spirit Powder, Ghost Powder, Siren Paste or Dream Paste as Black Arcana resources.
- Salve effects remain provider-owned and must not be rewritten into Black Arcana hazard/corruption channels.
- Source class visibility is not a supported external API contract.

## Runtime QA blockers

1. resolve the physical `1.3.6` filename vs runtime metadata `1.3.5` discrepancy;
2. verify all 12 recipes in the installed JAR/datapack surface;
3. verify manual and redstone spin behavior in the installed pack;
4. verify Brambleguard's namespace-agnostic bleed-name removal against the actual modpack effect registry;
5. verify Mender's 90-second Regeneration and one-time Hexalia Bleeding clear;
6. do not promote any provider hook for Black Arcana integration until a stable public boundary is identified.
