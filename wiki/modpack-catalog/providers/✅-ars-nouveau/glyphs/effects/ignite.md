# Ignite

- Registry ID: `ars_nouveau:glyph_ignite`
- Source class: `EffectIgnite`
- School: Elemental Fire
- Default tier: **1**
- Default mana: **15**
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Source-pinned behavior

Ignite sets entities on fire for a configurable duration and can light/create fire around block targets using provider AOE/depth calculations and claim checks. Sensitive changes the block path to Ars Nouveau's short-lived magic fire, which the provider describes as non-spreading/non-destructive. It can also light compatible candles/campfires.

Compatible augments: Extend Time, AOE, Pierce, Reduce Time, Sensitive. Sensitive is limited to 1 by default.

## Acquisition / learning

- Provider-generated Glyph recipe: `minecraft:flint_and_steel` + `#minecraft:coals` ×3.
- Source-default recipe XP: **27 XP** (Tier I).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Boundary

Normal or magic fire created by Ars remains provider-owned. Black Arcana fire/world mutations must still route through `WorldEffectPolicy`; Sensitive's provider behavior is not a universal proof of world-safety for other spells.

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME+CONFIG QA PENDING`.

## Localizadores e parâmetros para Codex — fonte exata

- **Java:** [`EffectIgnite.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectIgnite.java) no commit `112920ff774831f204031da75b4c4e73d3765157` correspondente ao catálogo Ars 5.13.1.
- **Entidade:** `onResolveEntity` chama `setRemainingFireTicks(duration * 20)`; `duration = (int)(POTION_TIME.get() + EXTEND_TIME.get()*spellStats.getDurationMultiplier())`. Valores de config base no `buildConfig`: potion 3 e extend time 2 (unidade de duração conforme provider).
- **Bloco com Sensitive:** `onResolveBlock` pode colocar `BlockRegistry.MAGIC_FIRE` no bloco adjacente substituível; é branch diferente do fogo normal.
- **Bloco sem Sensitive:** candles/campfires são acesos, ou fogo real é tentado em posições calculadas por `SpellUtil.calcAOEBlocks`, com `BlockUtil.destroyRespectsClaim` no caminho de fogo normal.
- **Augments:** Extend Time, AOE, Pierce, Reduce Time, Sensitive; limite default de Sensitive 1.
- **Risco:** fire ticks, área por bloco, e variantes de fogo são categorias separadas de perk; uma perk de "duração" não equivale à de "área" nem autoriza ignorar claims. Mutação de mundo do Ars permanece autoridade Ars.

**Estado:** prova estática de parâmetros por leitura de código; habilidade de mutação por hook externo não verificada. Ars controla composição, execução, mana/Source e configurações; RPG Skill Tree controla perks/Mastery/gates; Black Arcana é autoridade somente de seu runtime próprio. [Padrão universal](../../../meta/PERK-READY-TECHNICAL-STANDARD.md).
