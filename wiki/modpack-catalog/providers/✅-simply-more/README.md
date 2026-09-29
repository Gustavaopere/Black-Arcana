# Simply More — 1.3.0 Alpha 5 physical line

Status: `✅ CATALOGED / EXACT PHYSICAL-PUBLISHER FILE / COMPLETE 24-ACTION OBJECT CATALOG / EXACT CURRENT ACTION DENOMINATOR 24 / DEPLOYED REACHABILITY OPEN / +0 STRICT`

> Folder-prefix rule (2026-09-29): **✅ means the current semantic/action denominator is fully cataloged and materialized.** Deployed config, reachability or runtime QA may still keep individual identities conditional or outside the strict numerator; those conditions remain documented here and do not make the folder structurally partial.

## Current physical authority

- sibling checkpoint: `neoforge-rpg-skilltree@8aa9b92197c2a6eed5b67b16fa6b6a4adb88fd35`;
- physical row: `#502`;
- JAR: `simplymore-forge-1.3.0_alpha.jar`;
- mod id: `simplymore`;
- runtime: `1.3.0_alpha`;
- physical SHA-1: `51636477cd5c378f42d9700e1fe35cd952c8f4f1`;
- publisher CurseForge File: `8736778`;
- publisher Alpha-5 filename: `simplymore-neoforge-1.3.0_alpha5+1.21.1.jar`;
- required host: Simply Swords `1.70.2-1.21.1`.

The exact publisher artifact downloaded by NON-MERGE audit PR #446 hash-matches the physical pack JAR.

Final exact audit evidence:

- audit HEAD: `53155432f050554cd2dec4e5bd1125c1cffaf72f`;
- run: `36516484341` — GREEN;
- artifact: `11011476182`;
- artifact digest: `sha256:e2d668d43f80663370e6ddcf03feab090e8de432e70ab13a5cfbb329cfeab859`.

See [EXACT-ALPHA5-ARTIFACT-AUDIT.md](EXACT-ALPHA5-ARTIFACT-AUDIT.md).

## Release-correlated source

Official repository:

`jay-jay0101/Simply-More`

Release-correlated Alpha-5 checkpoint:

`55977c5e6a4fdaf4281781d9c4475a52286b3184`

The source declares Minecraft 1.21.1 and `mod_version=1.3.0_alpha`. It is used for semantic classification and provider/host gating, not as a byte-equality substitute for the exact JAR.

Upstream is All Rights Reserved. Black Arcana retains only factual catalog/interoperability evidence.

## Exact current semantic inventory — 24 player actions

The exact artifact plus release-correlated semantic classification close the current-pack action denominator at **24**.

### 10 active-API actions

The exact JAR has 11 concrete `UniqueWeaponActiveAbility` classes, but only 10 declare a provider activation implementation:

1. Black Pearl;
2. Blade of the Grotesque;
3. Grandfrost;
4. Lustrous Moxie;
5. Magmaseep;
6. Moundshifter;
7. Ruyi Jingu Bang;
8. Soulfracture;
9. Stasis;
10. The Blood Harvester.

`IdolItem` / Ruptured Idol is excluded: it implements the interface but declares no provider player-action method, and the exact host interface fallback does not manufacture an activation when the item supplies none.

### 13 legacy direct-use actions

The exact JAR contains 13 registered non-active-interface Unique classes with their own player `use(...)` surface:

1. Boa's Fang;
2. Culterex;
3. Death's Eyrie;
4. Glimmerstep;
5. Great Slither;
6. Matterbane;
7. Myrmedge;
8. Perforiscus;
9. Revvengine;
10. Serpentine Valour;
11. Smouldering Ruin;
12. The Vessel Breach;
13. Tidebreaker.

Bounded exact call-target inspection proves these are functional provider action routes rather than inert `super.use` placeholders.

### 1 shared Mimicry action

The exact artifact contains one abstract `MimicryItem` action implementation and 25 registered concrete forms.

All 25 inherit the same `use` / held-use path and none overrides a separate action method. They therefore contribute **one shared Mimicry transformation root**, not 25.

Semantic total:

`10 + 13 + 1 = 24`.

## Fichas canônicas

As 24 raízes exatas estão materializadas objeto-a-objeto em [ACTION-CARDS-ALPHA5.md](ACTION-CARDS-ALPHA5.md). As fichas preservam o denominador exato e os gates implantados de reachability; nenhuma promove o strict sem a evidência atual exigida abaixo.

## Explicit exclusions

- **Ruptured Idol** — interface participant without provider action implementation: +0.
- **Ascended Idol / Tarnished Idol / Holylight / Darksent** — old `TO_REMOVE` implementations are not referenced by exact ItemRegistry; current IDs route through `RemovedItem` proxies: +0.
- **Reforming Remnant** — player use opens a selection/reformation workflow and the only exact C2S packet is its transformation packet. Classified as upgrade/item preparation, not a standalone magical action: +0.
- **Tidesinger compatibility** — exact JAR contains a Mythic Metals riptide-use class, but release-correlated source gates its registry behind `Platform.isModLoaded("mythicmetals")`. The current sibling modlist contains no Mythic Metals provider, so this optional action is outside the current assembled denominator.
- **passive/on-hit/aura behavior** — equipment/proc mechanics: +0.
- **four Simply More weapon implicits** — equipment proc identities, not player-selected magical actions: +0.
- **effects, entities/projectiles, HUD state, cooldowns and downstream consequences** — deduplicated under their root action.

The prior [ALPHA5-SEMANTIC-LOWER-BOUND.md](ALPHA5-SEMANTIC-LOWER-BOUND.md) is retained as historical evidence for the earlier 9-action checkpoint and is superseded for denominator purposes by the exact audit.

## Packet/input completeness

The exact artifact has exactly one provider C2S packet class: `C2STransformRemnantPacket`.

That packet belongs to the already excluded Reforming Remnant reformation workflow. No second provider keybind/C2S action family remains outside the 24-root inventory.

## Config / reachability boundary

The **denominator is closed; deployed reachability is not**.

Strict counting remains fail-closed until current assembled-pack evidence establishes which of the 24 roots are normally player-reachable, including:

- Simply Swords Awakening/unlock behavior for the active-API uniques;
- normal acquisition/reformation routes for the surviving action-bearing uniques;
- effective Mimicry form-disable state where it changes usable transformation outcomes;
- any deployed config/datapack/script state that suppresses otherwise present roots.

The read-only deployed-evidence collector now has a bounded Alpha-5 route for the
Mimicry portion of this gate. It hashes `simplymore-forge-1.3.0_alpha.jar`, compares
against physical/publisher SHA-1 `51636477cd5c378f42d9700e1fe35cd952c8f4f1`,
then reads only `config/simplymore/unique_effect.toml` and the exact 25
`mimicry.config.<form>.disabled` booleans. Missing/malformed values remain
fail-closed and no unrelated config body is retained.

That collector evidence does not promote the provider by itself. Awakening/unlock,
acquisition/reformation and other deployed suppression surfaces remain open.

Source or artifact defaults are not substituted for deployed state.

Therefore current disposition remains:

**`EXACT DENOMINATOR 24 / +0 STRICT`**.

## Ownership and deduplication

- Simply Swords owns its base weapon ecosystem, active-ability substrate and reused base implicits.
- Simply More owns the 24 current provider action identities and its provider-native passive/equipment behavior.
- Optional Mythic Metals behavior remains owned by that compatibility surface and is absent from the current pack while Mythic Metals is absent.
- Black Arcana must not duplicate provider activation, cooldown/state lifecycle, projectile/entity settlement, effect application, transformation or upgrade logic.
- RPG Skill Tree remains sibling authority only for progression/attributes/Mastery/perks/gates through verified contracts.

## Runtime QA remains separate

Catalog closure of the 24-root denominator is not an assembled-runtime PASS. Relevant later QA includes:

- client/dedicated-server boot on the exact prerelease stack;
- active and legacy use paths in remote multiplayer;
- held-use cancellation/cleanup;
- once-per-activation/cooldown settlement;
- Awakening/reformation persistence;
- Mimicry transformation and disabled-form behavior;
- no duplicate Simply Swords/Simply More action settlement.

## Result

**✅ Catalog complete — exact current semantic denominator 24; deployed reachability remains conditional.**

Current exact inventory: **24 provider-owned player-invoked supernatural action roots**.

Strict global delta: **+0** until deployed reachability/config evidence is closed.