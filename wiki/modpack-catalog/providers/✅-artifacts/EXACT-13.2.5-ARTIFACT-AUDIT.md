# Artifacts 13.2.5 — exact artifact audit

Status: `EXACT PHYSICAL=PUBLISHER / CURRENT 13.2.5 / 49 ITEM FIELDS / ITEM-ABILITY COMPONENT INFRA / ZERO INDEPENDENT SEMANTIC ACTION REGISTRY`

## Evidence packet

- temporary NON-MERGE PR: **#493**;
- audit HEAD: `a744600829646f2cd49aec541f690eff0dd392d8`;
- exact-artifact workflow: `audit-artifacts-13.2.5`;
- run: `36834282003` — SUCCESS;
- artifact: `11148453543`;
- artifact digest: `sha256:207eabe4db1c82141868e88eb5d1fe2d736d819ac928b13db45d1d2fc856a245`.

| Field | Value |
|---|---|
| physical SHA-1 | `fb6cd3be2d034dde369ffd7558c95c6daa44189e` |
| publisher File | CurseForge `312353 / 8791899` |
| publisher SHA-1 | `fb6cd3be2d034dde369ffd7558c95c6daa44189e` |
| publisher SHA-256 | `e36a929420a0a616abdb28f5bbbdb866a426aa3bb78d1b39bc1183927c101ce6` |
| bytes | `1,086,922` |
| equality | **EXACT** |

Official source-version checkpoint: `ochotonida/artifacts@7cf7dc42e322e13f096eea16cee17a4b400b75f7` (`Update 13.2.5`).

Physical↔publisher exactness is established independently of source reproducibility.

## Exact archive inventory

Bounded audit of the exact installed artifact:

- archive entries: **1,058**;
- class files: **334**;
- non-class resources: **724**;
- class files under the ability-component surface: **37**;
- `ModItems` top-level `Holder<Item>` fields: **49**.

The 37 ability-related class files include nested/support classes and are **not** treated as 37 semantic magic identities. Class count is structural evidence only.

## Exact item registry cardinality

`artifacts.registry.ModItems` exposes exactly these 49 top-level item fields:

`MIMIC_SPAWN_EGG`, `UMBRELLA`, `EVERLASTING_BEEF`, `ETERNAL_STEAK`,
`PLASTIC_DRINKING_HAT`, `NOVELTY_DRINKING_HAT`, `SNORKEL`, `NIGHT_VISION_GOGGLES`,
`VILLAGER_HAT`, `SUPERSTITIOUS_HAT`, `COWBOY_HAT`, `ANGLERS_HAT`,
`LUCKY_SCARF`, `SCARF_OF_INVISIBILITY`, `CROSS_NECKLACE`, `PANIC_NECKLACE`,
`SHOCK_PENDANT`, `FLAME_PENDANT`, `THORN_PENDANT`, `CHARM_OF_SINKING`,
`CHARM_OF_SHRINKING`, `CLOUD_IN_A_BOTTLE`, `OBSIDIAN_SKULL`, `ANTIDOTE_VESSEL`,
`UNIVERSAL_ATTRACTOR`, `CRYSTAL_HEART`, `HELIUM_FLAMINGO`, `CHORUS_TOTEM`,
`WARP_DRIVE`, `DIGGING_CLAWS`, `FERAL_CLAWS`, `POWER_GLOVE`, `FIRE_GAUNTLET`,
`POCKET_PISTON`, `VAMPIRIC_GLOVE`, `GOLDEN_HOOK`, `ONION_RING`, `PICKAXE_HEATER`,
`WITHERED_BRACELET`, `AQUA_DASHERS`, `BUNNY_HOPPERS`, `KITTY_SLIPPERS`,
`RUNNING_SHOES`, `SNOWSHOES`, `STEADFAST_SPIKES`, `FLIPPERS`, `ROOTED_BOOTS`,
`STRIDER_SHOES`, `WHOOPEE_CUSHION`.

This independently corroborates the sibling's **45 wearables + 4 utility/non-wearable = 49** inventory.

## Formal ability-component surface

The exact artifact exposes provider data-component types and implementation classes for behavior including:

- double jump;
- swim/flight-like movement in air;
- death-protection teleport;
- Ender Pearl hunger cost / damage immunity;
- post-damage effects and cooldowns;
- retaliation effects;
- damage absorption / immunity;
- cure effects;
- attack effects;
- fluid collision;
- hunger replenishment / post-eating plant behavior;
- equipment mob effects;
- tool-tier upgrade;
- attribute/enchantment modifiers;
- toggle/presentation/state helpers.

Exact `ModItems` bytecode binds these components to concrete item owners, for example:

- `cloud_in_a_bottle` → `DOUBLE_JUMP`;
- `helium_flamingo` → `SWIM_IN_AIR`;
- `chorus_totem` → `DEATH_PROTECTION_TELEPORT`;
- `warp_drive` → Ender Pearl cost/immunity components;
- `vampiric_glove` → `DAMAGE_ABSORPTION`;
- `withered_bracelet` → `ATTACK_EFFECTS`;
- `aqua_dashers` / `strider_shoes` → `FLUID_COLLISION`;
- `shock_pendant`, `flame_pendant`, `thorn_pendant` → `RETALIATION_EFFECTS`.

This proves concrete item behavior. It does **not** create a standalone action-ID namespace.

## Current-stack deduplication

The physical pack also contains Reliquified Artifacts 1.0.8. Its existing canonical Black Arcana catalog closes:

- **48 `artifacts:<id>` semantic owners redirected/extended**;
- **52 owner-scoped named Relics ability roots**;
- strict semantic state: `COUNTED_SOURCE_PINNED +52`.

The base Artifacts provider does not expose another named `AbilityTemplate`/spell/focus/action identity roster. Its item/data-component behavior remains base item machinery under the same owner surface.

Under the canonical semantic metric:

- the 49 items themselves are excluded;
- data-component implementation classes are excluded as implementation types;
- attributes/statuses/procs/toggles are excluded unless they establish an independent provider-owned action identity;
- Reliquified Artifacts' 52 named roots remain counted once;
- base Artifacts contributes **+0 additional identities**.

## Source-version correlation

The sibling pins exact source commit `7cf7dc42e322e13f096eea16cee17a4b400b75f7`. Official source comparison from 13.2.3 to 13.2.5 leaves `ModItems.java` unchanged; the current 49-item denominator is therefore source-version consistent with the exact physical artifact evidence.

Source-version correlation is used only for factual naming/structure. The physical/publisher byte-equality claim comes from the exact artifact audit.

## Clean-room boundary

The durable repository stores only factual identifiers, counts, ownership/deduplication conclusions and bounded structural observations. It does not redistribute the third-party JAR, class bodies, textures, models or localization prose.

## Result

- current provider item denominator: **49/49 closed**;
- independent semantic spell/glyph/ritual/action identities: **0**;
- strict semantic delta: **+0**;
- provider catalog state: **✅ complete**;
- runtime/integration QA: separate and fail-closed.
