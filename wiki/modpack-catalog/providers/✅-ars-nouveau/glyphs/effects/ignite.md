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

**Estado:** prova estática de parâmetros por leitura de código; habilidade de mutação por hook externo não verificada. Ars controla composição, execução, mana/Source e configurações; RPG Skill Tree controla perks/Mastery/gates; Black Arcana é autoridade somente de seu runtime próprio. [Padrão universal](../../../../meta/PERK-READY-TECHNICAL-STANDARD.md).

## Certificação estática por pipeline e consumidores — 25/10/2026

**✅ COMPLETE_PERK_READY apenas no escopo `STATIC_TECHNICAL_CATALOG_ONLY` — NÃO é certificação de perk jogável. ⛔ `mutating_hook=NOT_VERIFIED`; ⚠️ `physical_qa=NOT_TESTED`.** O ID e a classe no JAR publisher foram auditados separadamente da semântica lida no commit de source.

| Campo exigido | Contrato source-pinned, limites e classificação para perks |
|---|---|
| Identidade/versionamento | Ars Nouveau `5.13.1`; `ars_nouveau:glyph_ignite`; classe `EffectIgnite`; escola Elemental Fire, tier I. [Source imutável](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectIgnite.java) e [registry do publisher SHA-exato](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md). |
| Comportamento, causalidade e settlement | `onResolveEntity` chama `setRemainingFireTicks(duration*20)` diretamente no hit de Entity. `onResolveBlock` com Sensitive testa o bloco adjacente substituível e tenta colocar `MAGIC_FIRE`, depois retorna. Sem Sensitive, primeiro acende Candle/Campfire elegível; caso contrário verifica bloco acima e percorre `SpellUtil.calcAOEBlocks`, solicita `BaseFireBlock.canBePlacedAt`, `BlockUtil.destroyRespectsClaim` e somente então coloca fogo vanilla com atualização de vizinhos. |
| Parâmetros, escalas e caps | `duration=(int)(POTION_TIME+EXTEND_TIME×durationMultiplier)` e depois ticks=`duration×20`. Defaults configurados `POTION_TIME=3`, `EXTEND_TIME=2` (segundos conforme fonte), mas config implantada não lida. Duração de entidade não usa `IPotionEffect` neste glyph. Sensitive limit default **1**. Número de posições depende de AOE/Pierce e validação de mundo, não de uma grandeza fixa da ficha. |
| Targeting, geometria, projétil, tipo e duração | Entidade (não necessariamente LivingEntity) atingida recebe timer de fogo; alvo de bloco ativa caminho MAGIC_FIRE versus candle/campfire ou fogo normal AOE. Face do hit orienta bloco adjacente, *não* target radius autônomo do glyph. Não há `DamageTypes` explícito/valor de dano nesta classe; dano posterior dos ticks de fogo pertence ao Minecraft. |
| Custos, aprendizagem e limites da receita | Mana default **15**; tier I; XP receita default 27; starter default não; recipe `minecraft:flint_and_steel` + `#minecraft:coals` ×3. [Acquisition 85/85](../../ACQUISITION.md). Cast/cooldown e mana efetiva da composição são autoridade/config Ars Nouveau. Augments: Extend Time, AOE, Pierce, Reduce Time, Sensitive. Sensitive muda **ramo de criação de bloco**, não só duração; o próprio source não chama `destroyRespectsClaim` nessa branch, mas isso não prova ausência de proteções antes da resolução. |
| Integração e segurança | **⛔** Não atribuir proteção universal a MAGIC_FIRE pela descrição de item, nem duplicar fire ticks, entidades, incêndio ou gasto Ars. Exigir testes físicos com claims, mobs PvP, fogo vanilla, mudança de dimensão e rollback de Black Arcana (independente). Contrato de perks RPG Skill Tree e hook mutador para este caminho não verificados. Não trocar target, type, raio, mana nem recipients com API presumida. Black Arcana conserva seu runtime, hazards e `WorldEffectPolicy` para efeitos próprios. |
| Grau de evidência/testes | Source `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`; JAR publisher `ars_nouveau-1.21.1-5.13.1.jar`, SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd` prova **ID/classe registrada**, não todos os métodos do classfile ou gameplay atual. Config final, order de eventos, integrações de outros mods, PvP/claims, servidor e cliente: **NOT_TESTED**. |

**Regra de reauditoria:** alterações de JAR/source, config, modificadores, geometria/ordem de eventos ou consumidor downstream exigem nova verificação técnica antes de liberar qualquer hook. Efeitos/raios/VFX não são eventos novos de cast/Mastery.
