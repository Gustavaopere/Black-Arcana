# Extend Time

- Registry ID: `ars_nouveau:glyph_extend_time`
- Source class: `AugmentExtendTime`
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`
- Default tier: **2**
- Default mana: **10**

## Source-pinned behavior

Adds **+1.0** to Ars Nouveau's duration modifier. Compatible effects use that stat for provider-owned duration behavior, including effects, summons and other timed spell results.

## Acquisition / learning

- Provider-generated Glyph recipe: `minecraft:clock` + `#c:storage_blocks/redstone`.
- Source-default recipe XP: **55 XP** (Tier II).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Boundary

Duration scaling is provider-owned. Black Arcana durations/cooldowns remain separate server-owned policy values and cannot be silently multiplied by this Ars stat.

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME+CONFIG QA PENDING`.

## Engenharia para perks — operador e consumidores

- **Classe Java exata:** [`AugmentExtendTime.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/augment/AugmentExtendTime.java), source pin `112920ff774831f204031da75b4c4e73d3765157` (Ars Nouveau 5.13.1).
- **Operador source:** `applyModifiers` chama `builder.addDurationModifier(1.0)`; custo default 10, tier II.
- **Regra de efeitos com `IPotionEffect`:** `ticks=baseSeconds*20+extendSeconds*SpellStats.getDurationInTicks()`, com `getDurationInTicks=(int)(20*durationMultiplier)`. `Harm` usa a presença de Extend Time para **trocar dano direto por Poison**, de modo que não é apenas um bônus de duração.
- **Perks:** não alongar cooldown/ritual/estado de outra autoridade por analogia; verificar a regra específica do receptor.
- **Mutação externa:** o contrato de integração por perk RPG/Black Arcana continua **NOT_VERIFIED**; a revisão abaixo identifica a API pública sem presumir um adapter validado. Config real, Survival e integração permanecem condicionados.

## Revisão técnica para índice de perks — 25/10/2026

`technical_perk_dossier: 1`. **Escopo: contrato técnico estático SOURCE-PINNED 5.13.1; ⛔ contrato mutador RPG/Black Arcana não comprovado; ⚠️ QA físico NOT_TESTED.** A classificação estática exige revisão do manifesto e não concede autoridade para executar uma segunda magia.

| Eixo exigido | Contrato auditado | Evidência e limite |
|---|---|---|
| Identidade | `ars_nouveau:glyph_extend_time`, classe `com.hollingsworth.arsnouveau.common.spell.augment.AugmentExtendTime`, augment tier-padrão II. | [Classe][ta-class] no commit 112920ff774831f204031da75b4c4e73d3765157; [identidade compilada SHA-exata](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md), JAR 5.13.1 SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`. |
| Comportamento e recebedor | `addDurationModifier(+1.0)` sobre `D=modificador de duração acumulado`. applyModifiers altera D no builder. Consumidores escolhem como aplicar: IPotionEffect converte D em ticks; EffectDelay lê a contagem do glifo; Harm muda do ramo de dano direto para Poison ao detectar a presença de um augment temporal, mesmo quando a soma D=0. | [Operador][ta-class], [AbstractAugment][ta-base], [build e ordem][ta-build]. O builder executa cada augment aceito antes dos modificadores de item e do evento final. |
| Parâmetros, escala e caps | Cada aplicação aceita soma **+1,0** a D, que começa0. SpellStats converte `getDurationInTicks=(int)(20D)`, com truncamento final. Em IPotionEffect, `ticks=20×baseSeconds+durationBuffSeconds×(int)(20D)`; não é multiplicador universal nem duração final própria. EffectDelay usa a **contagem** de Extend Time para somar `20×EXTEND_TIME` ticks por ocorrência. Compatibilidade, caps e base/coeficientes são do receptor/config; getAugmentLimit e per_spell_limit são controles distintos. [Builder][ta-stats], [conversão][ta-duration], [potion][ta-potion], [Delay][ta-delay], [limites][ta-limits], [mapa][ta-cap-map]. | Valores de config implantada, combinação aceita e efeitos de terceiros não foram observados. Não inferir dose, alvo ou budget universal. |
| Targeting, área, projétil, dano e duração | **N/A como parâmetros próprios:** seleção de alvo, área, tipo de dano, entidade de projétil/hitbox/velocidade. O stat temporal não cria duração ou cooldown autônomos: Form/Effect receptor interpreta-o. Exemplo IPotionEffect altera duração de status; Delay lê contagens; Harm troca o ramo de efeito. [Base][ta-base], [potion][ta-potion], [Harm][ta-harm], [Delay][ta-delay]. | O alvo é da composição; N/A não apaga os efeitos downstream que leem o stat ou a contagem. |
| Custos, cast, cooldown e aprendizado | Mana-padrão **10**; tier II, recipe glyph-padrão**55 XP**, starter default **não**. Receita e ingredientes acima. Sem cast ou cooldown próprios; Ars controla mana da composição e aprendizagem. | [Default][ta-class], [recipe gerada][ta-recipe], [custo após config][ta-cost], [custo por receptor][ta-base], [config][ta-limits], [starter][ta-starter], [aquisição](../../ACQUISITION.md). Overrides do receptor e config podem alterar o custo; Source de mundo/crafting não é player mana. |
| Integração, autoridade e mutabilidade | Há superfície pública source-localizada: `SpellStats.Builder.build` publica `SpellModifierEvent` após augments/itens e antes de retornar stats; o evento expõe builder mutável. Isso não valida um adapter de perk com custo, compatibilidade, caps, origem e dedup. **⛔ SEM_HOOK_SEGURO para integração RPG/Black Arcana neste catálogo; mutating_hook=NOT_VERIFIED.** | [Build][ta-build], [evento][ta-event], [matriz de engenharia](../../PERK-ENGINEERING-MATRIX-5.13.1.md). Não negar a API pública nem tratá-la como bridge implementada; preservar Ars como dono de SpellStats/resolver/settlement. |
| Validação | **STATIC_SOURCE_PINNED + BINARY_IDENTITY_ONLY.** Revisão de operadores e consumidores nas referências fixas, sem comparação integral dos métodos/classfiles ou execução de efeito. | Fonte 112920ff774831f204031da75b4c4e73d3765157 e [IDs JAR SHA-exatos](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md). Config implantada, Survival/cliente/multiplayer, pacote de mods, adapter e QA físico **NOT_TESTED**. Nenhum Stage promovido. |

Exemplos delimitados: com as configs iniciais de Harm em base 5s/extensão 5s, um Extend Time solicita Poison 200 ticks; um Reduce Time solicita 0 ticks; os dois juntos deixam D=0, mas a presença temporal ainda seleciona Poison 100 ticks. São resultados aritméticos desse caminho/config, sem comprovar aplicação efetiva do status ou dano final. Os getters de Harm têm fallbacks 30/8 quando os fields de config são null, distintos dos defaults 5/5. Para Delay com defaults, a fórmula antes de Randomize é `20+20×count(ExtendTime)−10×count(DurationDown)` ticks; não há clamp local de duração no trecho consultado. [Harm][ta-harm], [fallbacks][ta-harm-values], [Delay][ta-delay], [defaults][ta-delay-config].

**Invalidação:** alteração do source/JAR/config, operador, compatibilidade/caps do receptor, recipe/tier ou novo contrato mutador exige revisão por campo. Este dossiê classifica o componente estático, não certifica todas as combinações Ars ou todo o provider.

[ta-class]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/augment/AugmentExtendTime.java#L9-L36
[ta-base]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractAugment.java#L15-L60
[ta-build]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellStats.java#L131-L152
[ta-stats]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellStats.java#L224-L243
[ta-cost]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L125-L145
[ta-limits]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L226-L268
[ta-event]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/event/SpellModifierEvent.java#L13-L32
[ta-recipe]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/generated/resources/data/ars_nouveau/recipe/glyph_extend_time.json#L1-L16
[ta-cap-map]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/util/SpellPartConfigUtil.java#L34-L64
[ta-duration]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellStats.java#L24-L57
[ta-potion]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/IPotionEffect.java#L10-L28
[ta-harm]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectHarm.java#L32-L49
[ta-harm-values]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectHarm.java#L96-L104
[ta-delay]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectDelay.java#L33-L49
[ta-delay-config]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectDelay.java#L63-L80

[ta-starter]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L307-L310
