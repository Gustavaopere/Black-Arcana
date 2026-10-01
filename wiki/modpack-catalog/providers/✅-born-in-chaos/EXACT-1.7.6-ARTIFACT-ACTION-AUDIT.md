# Born in Chaos 1.7.6 — exact artifact player-magic audit

Status: `EXACT PHYSICAL=PUBLISHER / PLAYER-ACTION SURFACE BOUNDED / 17 COUNTED_EXACT`

## Artifact identity

- physical row: **#84**;
- physical JAR: `born_in_chaos_[Neoforge]_1.21.1_1.7.6.jar`;
- mod id: `born_in_chaos_v1`;
- runtime: `1.7.6`;
- physical SHA-1: `73704f38ac368c03716f9cc8f537470d3b352fa2`;
- CurseForge project/file: `686437 / 8268280`.

NON-MERGE PR #501 final evidence:

- HEAD `7e0fb1d74e543661926fe053f7085f2136aa8205`;
- exact-artifact run `36919074090` — SUCCESS;
- Black Arcana CI #4041 — SUCCESS;
- artifact `11190708455`;
- artifact digest `sha256:37e2646bec350a0dce723445b5a58b86e9e45c2532b3f8a8c256675c6b47c8d0`;
- publisher SHA-1 `73704f38ac368c03716f9cc8f537470d3b352fa2`;
- publisher SHA-256 `a0271a24db8622434d9573c5e789d451a05c9211173885049284e1911e2499c7`;
- bytes `11,842,184`.

Physical and publisher SHA-1 are identical.

## Bounded archive inventory

The exact JAR contains:

- archive entries: **4,364**;
- classes: **1,550**;
- resources: **2,814**;
- item classes: **212**;
- procedure classes: **514**;
- registry-like classes audited: **4**;
- provider data paths: **618**;
- provider asset paths: **2,051**.

Because this MCreator-era provider has a large generated procedure surface, class totals are not used as the semantic denominator.

## Player-action narrowing

The audit performs four bounded passes:

1. enumerate item classes and detect player-action-shaped methods (`use`, `useOn`, `releaseUsing`, `finishUsingItem`, interaction/hit/tick seams);
2. resolve exact procedure classes directly called by those item methods;
3. scan all provider procedures transiently but retain only compact item/event/effect/entity seams when an item or player-interaction event is involved;
4. parse provider recipes, loot tables and item tags into a normalized acquisition index.

The global bounded item-procedure index contains **74 procedure rows**. It proves, among other things:

- `DarkRitualDaggerPProcedure` is a player `EntityInteract` path using `DARK_RITUAL_DAGGER`, applying provider `SACRIFICE`, durability/cooldown and player interaction settlement;
- `TransmutingElixirclicProcedure` is a player `EntityInteract` path using `TRANSMUTING_ELIXIR`, consuming the item while replacing supported entities;
- `FrostbittenBladePriShchielchkiePKMProcedure` is shared by Frostbitten Blade and Icy Sweetness;
- Fel Lamp and Lord Pumpkinhead's Lamp resolve distinct provider mount entity types;
- Bone Heart, five Charms, Dark Atrium, Bonescaller Staff and Stormcaller's Horn have explicit active procedures rather than passive item metadata.

## Acquisition index

The normalized exact provider index closes:

- item IDs with provider recipe/loot/tag evidence: **202**;
- normalized acquisition rows: **455**.

Counted roots have a direct current route:

| Owner/action surface | Exact current provider evidence |
|---|---|
| `bone_heart` | `recipe/bone_heart_k.json` |
| five `charmof_*` owners | `loot_table/entities/missioner.json` + `missionary_raider.json`; rare-loot tags |
| `dark_atrium` | `recipe/dark_atrium_craft.json` |
| `dark_ritual_dagger` | `recipe/dark_ritual_dagger_k.json` |
| `ethereal_spirit` | multiple exact spirit-entity loot tables |
| `bonescaller_staff` | `recipe/staffofthe_summoner_k.json` |
| `fel_lamp` | recipe + `pumpkinhead` loot |
| `lord_pumpkinheads_lamp` | recipe + `lord_pumpkinhead_head` loot |
| `frostbitten_blade` | `recipe/frostbitten_blade_craft.json` |
| `icy_sweetness` | `recipe/icy_sweetness_craft.json` |
| `pumpkinstaffa` | `pumpkinhead` loot |
| `staff_of_magic_arrows` | Bonescaller/Supreme Bonescaller loot + provider recipe |
| `stormcallers_horn` | `recipe/stormcallers_horn_craft.json` |
| `transmuting_elixir` | `recipe/transmuting_elixirkraft.json` |

`staffof_blindness` has no recipe, loot-table item entry or provider item-tag membership in the exact acquisition index.

## Semantic classification

### Counted

The exact player-facing magical set contains **17** causal roots:

- 7 direct ward/charm/dark-ritual activations (Bone Heart + five Charms + Dark Atrium);
- Dark Ritual Dagger Sacrifice;
- Ethereal Spirit pumpkin animation;
- Bonescaller Staff summoning;
- Fel Lamp summoning;
- Lord Pumpkinhead's Lamp summoning;
- one shared Frostbitten Blade/Icy Sweetness Icy Splash;
- Pumpkin Staff magical staff action;
- Staff of Magic Arrows action;
- Stormcaller's Horn Snow Storm;
- Transmuting Elixir transmutation.

### Deduplicated / excluded

Semantic classification deliberately does not map one-to-one to item classes.

- Frostbitten Blade + Icy Sweetness share one active procedure -> **1 root**.
- Transmuting Elixir block/entity target branches -> **1 root**.
- Pumpkin Staff projectile/explosion/block-hit summon consequences -> **1 root**.
- Felsteed spirit capture/refill is setup for lamp state -> **+0**.
- Staff of Blindness and Dark Charge share the same blindness-projectile family; Dark Charge is a normal primary projectile item and Staff of Blindness lacks normal provider acquisition -> **+0** independent semantic roots.
- Pumpkin Pistol and bombs/Easter Eggs are primary projectile/throwing modes -> **+0**.
- drink/food status delivery -> **+0**.
- reactive armor/totem/hat behavior and weapon on-hit procs -> **+0**.
- mob-native abilities -> **+0 player-owned roots**.

## Result

**17 `COUNTED_EXACT` provider-owned supernatural player-action identities.**

The provider semantic denominator is closed for the exact current artifact. Runtime/config/assembled-pack QA remains a separate concern.

## Clean-room boundary

The durable catalog retains only factual hashes, IDs, counts, registry/method/event relationships, compact call-target facts, provider data paths and behavior-level semantic classification. The third-party JAR, protected assets and full implementation bodies are not committed.
