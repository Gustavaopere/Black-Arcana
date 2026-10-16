# Epic Fight — 21.17.3.1

## Perks — parâmetros e causalidade (16/10/2026)

**Duas evidências com denominadores distintos:**

- **Core skill registry exato 21.17.3.1:** ✅ **43/43 identificadas/dispositionadas**; 3 ações sobrenaturais `COUNTED_EXACT` para magia, 40 core skills excluídas apenas da **métrica de magia**. O piso global permanece inalterado.
- **Aprofundamento causal para perks:** 🟡 **13/43 = 30,23%** pesquisadas em **10 dossiês**, com revisão `21.17.3` **source-adjacent**; as 4 passivas novas (`technician`, `berserker`, `stamina_pillager`, `death_harvest`) permanecem nesse estado.
- **Parâmetros binários exatos do JAR 21.17.3.1:** ✅ **9/43 = 20,93%** com os nove JSONs empacotados, hashes publisher/pack, símbolos verificados em **12 classes**, 6/6 testes sintéticos, 0 divergências. [Prova estática Java21](EXACT-BINARY-PERK-PARAMETERS-21.17.3.1.md) / [run #38979022783](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38979022783). **Não valida** execução de perks, hook seguro, mundo, override de datapacks, stamina efetiva ou Mastery.

[Checkpoint de pesquisa e pendências](skills/PERK-TECHNICAL-CHECKPOINT-2026-10-16.md) · [Parrying](skills/technical/PARRYING-21.17.3-SOURCE-ADJACENT.md) · [Impact Guard](skills/technical/IMPACT-GUARD-21.17.3-SOURCE-ADJACENT.md) · [Swordmaster](skills/technical/SWORDMASTER-21.17.3-SOURCE-ADJACENT.md) · [Forbidden Strength](skills/technical/FORBIDDEN-STRENGTH-21.17.3-SOURCE-ADJACENT.md) · [Roll/Step](skills/technical/DODGE-ROLL-STEP-21.17.3-SOURCE-ADJACENT.md) · [Trident Innates](skills/technical/TRIDENT-INNATES-21.17.3-SOURCE-ADJACENT.md) · [Technician](skills/technical/TECHNICIAN-21.17.3-SOURCE-ADJACENT.md) · [Berserker](skills/technical/BERSERKER-21.17.3-SOURCE-ADJACENT.md) · [Stamina Pillager](skills/technical/STAMINA-PILLAGER-21.17.3-SOURCE-ADJACENT.md) · [Death Harvest](skills/technical/DEATH-HARVEST-21.17.3-SOURCE-ADJACENT.md).

Death Harvest gera uma orb de **recuperação de gauge weapon innate** na fonte adjacente, e não um projétil ofensivo independente. Sem objeto mágico novo, perk/adaptor novo, teste de execução real ou avanço de Stage. Epic Fight conserva stamina, state, damage e animações; Black Arcana controla seu runtime mágico.

Status: `✅ CATALOGED / EXACT PHYSICAL=PUBLISHER ARTIFACT / 43-SKILL REGISTRY FULLY DISPOSITIONED / 3 COUNTED_EXACT SUPERNATURAL TRIDENT INNATES / RUNTIME QA SEPARATE`

## Current physical identity

Current sibling physical authority identifies:

- physical row: **#260**;
- JAR: `epic-fight-21.17.3.1-mc1.21.1-neoforge.jar`;
- mod id: `epicfight`;
- runtime: `21.17.3.1`;
- Minecraft / loader: 1.21.1 / NeoForge;
- physical SHA-1: `fb199b7bbea2fc402da28ab586e73f47e32f8fc0`.

Epic Fight is primarily the pack's action-RPG combat framework. It owns battle mode, stamina, stun, weapon capabilities, movesets, skills and special attacks. Only a narrow subset of its exact core skill registry qualifies for the Black Arcana semantic-magic metric.

## Exact publisher-artifact closure

NON-MERGE evidence PR **#562** audits CurseForge project/file `405076 / 8175609` and hard-gates the publisher artifact against the physical pack fingerprint.

Final exact evidence checkpoint:

- audit HEAD: `3b8e5ccd58e72bc99fdeeaac84b10d8f25538ca0`;
- exact-artifact run: `37170317148` — **SUCCESS**;
- evidence artifact: `11291375884`;
- evidence digest: `sha256:88fbb713615e5f996a40c609facb03792df812c4a762e47247bb3e1d6466821b`;
- publisher SHA-1: `fb199b7bbea2fc402da28ab586e73f47e32f8fc0`;
- publisher SHA-256: `8b882554cf10086398340fbdc741819ee72a801a3adce516c7f4768326a39526`;
- bytes: `8,578,288`.

The publisher SHA-1 exactly equals the physical sibling SHA-1.

The exact artifact contains **3,213 archive entries / 1,530 classes / 1,683 non-class resources / 117 skill-like classes / 280 skill-like resources / 174 provider-data paths**.

See [`EXACT-21.17.3.1-ARTIFACT-SKILL-AUDIT.md`](EXACT-21.17.3.1-ARTIFACT-SKILL-AUDIT.md).

## Exact core skill registry — 43 IDs

Direct exact-artifact inspection closes **43 unique Epic Fight core skill IDs**:

- 2 technical/core skill slots;
- 3 dodge/wakeup movement skills;
- 3 guard skills;
- 14 passive skills;
- 2 identity skills;
- 2 mover skills;
- 16 weapon-innate skills;
- 1 weapon-passive skill.

All 43 IDs are dispositioned in [`skills/SKILL-DISPOSITION-21.17.3.1.md`](skills/SKILL-DISPOSITION-21.17.3.1.md).

## Semantic-magic result — 3 exact roots

Epic Fight 21.17.3.1 contributes exactly **3 provider-owned supernatural player-action identities** under the current semantic metric:

1. `epicfight:wrathful_lighting` — **Wrathful Lightning**;
2. `epicfight:tsunami` — **Tsunami**;
3. `epicfight:everlasting_allegiance` — **Everlasting Allegiance**.

All three are weapon-innate actions on the provider's exact trident moveset and are selected by normal vanilla trident enchantments:

- **Riptide** -> `epicfight:tsunami`;
- **Channeling** -> `epicfight:wrathful_lighting`;
- **Loyalty** -> `epicfight:everlasting_allegiance`;
- otherwise -> `epicfight:grasping_spire`.

This exact selector closes current catalog reachability without inventing a separate Epic Fight item-acquisition path: the owner remains `minecraft:trident`, while the vanilla enchantment parameter selects the provider-owned Epic Fight innate.

Object cards:

- aggregate: [`actions/SUPERNATURAL-ACTION-CARDS.md`](actions/SUPERNATURAL-ACTION-CARDS.md);
- [Wrathful Lightning](actions/wrathful-lightning.md);
- [Tsunami](actions/tsunami.md);
- [Everlasting Allegiance](actions/everlasting-allegiance.md).

Individual-card checkpoint: [`INDIVIDUAL-ACTION-CARDS-CHECKPOINT.md`](INDIVIDUAL-ACTION-CARDS-CHECKPOINT.md).

## Why the three count

### Wrathful Lightning

The exact animation/control seam attaches the provider server-side `SUMMON_THUNDER` event to the skill action. The provider therefore owns a discrete player-triggered lightning invocation rather than merely a martial swing animation.

### Tsunami

The exact trident innate selector resolves Tsunami for Riptide. Exact Tsunami resources and control flow provide provider-specific tide/water behavior, strengthened use while the player is in water or rain, Tsunami particles and a dedicated skill settlement. This is a discrete supernatural movement/attack action rather than ordinary trident use.

### Everlasting Allegiance

The exact selector resolves Everlasting Allegiance for Loyalty. The provider tracks the thrown trident and invokes its own `recalledBySkill()` lifecycle, returning the trident through a damaging recall path. That deliberate supernatural recall is a distinct Epic Fight action, not merely vanilla Loyalty's passive return.

## Why the other 40 IDs do not count

The semantic-magic ledger does not count every Epic Fight skill. The remaining 40 exact IDs are excluded because they are technical slots, dodge/wakeup, guard/parry, passive/reactive combat behavior, locomotion, combat identities or conventional weapon techniques.

Important boundary examples:

- `forbidden_strength` remains excluded despite magical wording: exact implementation is a passive stamina/health substitution skill, not an independent cast/action;
- `meteor_slam`, `demolition_leap` and `phantom_ascent` are combat movement/mobility;
- `revelation` is a combat identity/counter-weakpoint mechanic;
- `grasping_spire`, `heartpiercer`, `battojutsu`, `blade_rush`, `eviscerate` and the other ordinary weapon innates remain martial special attacks;
- `battojutsu_passive` is a weapon-passive support skill.

## Skillbook and acquisition boundary

The exact artifact packages Epic Fight's skillbook loot system, but the three counted roots are **weapon innates selected by the trident moveset**, not ordinary skillbook-unlock entries. Their catalog reachability therefore comes from the exact trident + enchantment selector above.

Skillbook loot, stamina, innate gauge/resource state, animation timing, damage and downstream particles/lightning/trident hits remain provider-owned settlement details and do not create extra semantic identities.

## Authority boundary

Epic Fight remains authority for:

- battle mode and player/entity patches;
- stamina, stun and skill state;
- weapon capabilities and movesets;
- trident innate selection;
- skill execution, animation and resource settlement;
- provider damage/hit/event processing.

Black Arcana catalogs the three supernatural identities but must not replay Epic Fight skills, apply a second stamina/cooldown/resource charge, duplicate thunder/trident damage, or treat downstream particles/events as separate spells.

## Runtime QA remains separate

Catalog closure is not an assembled-pack runtime PASS. Battle-mode state, multiplayer settlement, skill-slot conflicts, addon precedence, weapon-capability datapacks, Werewolves compatibility, EFIS/Iron's casting coexistence, controller/input and render compatibility remain runtime QA.

## Result

**✅ Cataloged — exact current 43-ID skill denominator closed and fully dispositioned.**

Current Epic Fight core semantic inventory: **3 exact-current supernatural player actions + 40 excluded non-magic skill identities**.

Strict semantic delta: **+3 `COUNTED_EXACT`**.
