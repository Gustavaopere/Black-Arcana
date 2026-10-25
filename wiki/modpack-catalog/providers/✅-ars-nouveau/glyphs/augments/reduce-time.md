# Reduce Time

- Registry ID: `ars_nouveau:glyph_duration_down`
- Source class: `AugmentDurationDown`
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`
- Default tier: **2**
- Default mana: **15**

## Source-pinned behavior

Adds **-1.0** to Ars Nouveau's duration modifier. Compatible timed glyphs interpret that reduced duration.

The 1.21.1/5.13.1 source deliberately retains the registry path `glyph_duration_down`; an upstream comment only proposes a key rename for 1.22. This catalog therefore preserves the installed-line ID rather than normalizing it to the display name.

## Acquisition / learning

- Provider-generated Glyph recipe: `minecraft:clock` + `minecraft:glowstone_dust`.
- Source-default recipe XP: **55 XP** (Tier II).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Boundary

Ars duration semantics remain provider-owned. Black Arcana must not alter its own cooldown or hazard durations through this glyph unless a future explicit integration contract says so.

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME+CONFIG QA PENDING`.

## Engenharia para perks — operador e consumidores

- **Classe Java exata:** [`AugmentDurationDown.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/augment/AugmentDurationDown.java), source pin `112920ff774831f204031da75b4c4e73d3765157` (Ars Nouveau 5.13.1).
- **Identidade exata:** registry `ars_nouveau:glyph_duration_down` (não `glyph_reduce_time`); class `AugmentDurationDown` e `applyModifiers=builder.addDurationModifier(-1.0d)`; default mana 15, tier II.
- **Ramo condicional:** em `EffectHarm`, a **presença** de Duration Down também troca dano instantâneo por Poison. Em `IPotionEffect`, duração após a alteração depende do produto `extendSeconds * getDurationInTicks()` e do cast context; não interpretar como desconto fixo em ticks universal.
- **Perks:** respeitar recipe/limites/config do receptor e impedir duração negativa ou bypass quando uma magia Black Arcana criar seu próprio contrato.
- **Mutação externa:** o contrato de integração por perk RPG/Black Arcana continua **NOT_VERIFIED**; a revisão abaixo identifica a API pública sem presumir um adapter validado. Config real, Survival e integração permanecem condicionados.

## Revisão técnica para índice de perks — 25/10/2026

`technical_perk_dossier: 1`. **Escopo: contrato técnico estático SOURCE-PINNED 5.13.1; ⛔ contrato mutador RPG/Black Arcana não comprovado; ⚠️ QA físico NOT_TESTED.** A classificação estática exige revisão do manifesto e não concede autoridade para executar uma segunda magia.

| Eixo exigido | Contrato auditado | Evidência e limite |
|---|---|---|
| Identidade | `ars_nouveau:glyph_duration_down`, classe `com.hollingsworth.arsnouveau.common.spell.augment.AugmentDurationDown`, augment tier-padrão II. | [Classe][ta-class] no commit 112920ff774831f204031da75b4c4e73d3765157; [identidade compilada SHA-exata](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md), JAR 5.13.1 SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`. |
| Comportamento e recebedor | `addDurationModifier(−1.0d)` sobre `D=modificador de duração acumulado`. applyModifiers altera D no builder. IPotionEffect consome o modificador; EffectDelay usa a contagem; Harm escolhe Poison pela presença do glifo, mesmo se Extend Time cancelar numericamente D. Mantém-se o ID glyph_duration_down; o comentário de futura renomeação não altera5.13.1. | [Operador][ta-class], [AbstractAugment][ta-base], [build e ordem][ta-build]. O builder executa cada augment aceito antes dos modificadores de item e do evento final. |
| Parâmetros, escala e caps | Cada aplicação aceita soma **−1,0** a D. `getDurationInTicks=(int)(20D)` é uma contribuição assinada; IPotionEffect soma-a à duração base com o coeficiente do efeito. Esse helper não aplica piso positivo local. EffectDelay lê a **contagem** de Duration Down e subtrai DURATION_DOWN_TIME ticks por ocorrência, valor default 10 nesse receptor; não é redução universal de 20 ticks. Compatibilidade, caps e base/coeficientes são do receptor/config; getAugmentLimit e per_spell_limit são controles distintos. [Builder][ta-stats], [conversão][ta-duration], [potion][ta-potion], [Delay][ta-delay], [limites][ta-limits], [mapa][ta-cap-map]. | Valores de config implantada, combinação aceita e efeitos de terceiros não foram observados. Não inferir dose, alvo ou budget universal. |
| Targeting, área, projétil, dano e duração | **N/A como parâmetros próprios:** seleção de alvo, área, tipo de dano, entidade de projétil/hitbox/velocidade. O stat temporal não cria duração ou cooldown autônomos: Form/Effect receptor interpreta-o. Exemplo IPotionEffect altera duração de status; Delay lê contagens; Harm troca o ramo de efeito. [Base][ta-base], [potion][ta-potion], [Harm][ta-harm], [Delay][ta-delay]. | O alvo é da composição; N/A não apaga os efeitos downstream que leem o stat ou a contagem. |
| Custos, cast, cooldown e aprendizado | Mana-padrão **15**; tier II, recipe glyph-padrão**55 XP**, starter default **não**. Receita e ingredientes acima. Sem cast ou cooldown próprios; Ars controla mana da composição e aprendizagem. | [Default][ta-class], [recipe gerada][ta-recipe], [custo após config][ta-cost], [custo por receptor][ta-base], [config][ta-limits], [starter][ta-starter], [aquisição](../../ACQUISITION.md). Overrides do receptor e config podem alterar o custo; Source de mundo/crafting não é player mana. |
| Integração, autoridade e mutabilidade | Há superfície pública source-localizada: `SpellStats.Builder.build` publica `SpellModifierEvent` após augments/itens e antes de retornar stats; o evento expõe builder mutável. Isso não valida um adapter de perk com custo, compatibilidade, caps, origem e dedup. **⛔ SEM_HOOK_SEGURO para integração RPG/Black Arcana neste catálogo; mutating_hook=NOT_VERIFIED.** | [Build][ta-build], [evento][ta-event], [matriz de engenharia](../../PERK-ENGINEERING-MATRIX-5.13.1.md). Não negar a API pública nem tratá-la como bridge implementada; preservar Ars como dono de SpellStats/resolver/settlement. |
| Validação | **STATIC_SOURCE_PINNED + BINARY_IDENTITY_ONLY.** Revisão de operadores e consumidores nas referências fixas, sem comparação integral dos métodos/classfiles ou execução de efeito. | Fonte 112920ff774831f204031da75b4c4e73d3765157 e [IDs JAR SHA-exatos](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md). Config implantada, Survival/cliente/multiplayer, pacote de mods, adapter e QA físico **NOT_TESTED**. Nenhum Stage promovido. |

Exemplos delimitados: com as configs iniciais de Harm em base 5s/extensão 5s, um Extend Time solicita Poison 200 ticks; um Reduce Time solicita 0 ticks; os dois juntos deixam D=0, mas a presença temporal ainda seleciona Poison 100 ticks. São resultados aritméticos desse caminho/config, sem comprovar aplicação efetiva do status ou dano final. Os getters de Harm têm fallbacks 30/8 quando os fields de config são null, distintos dos defaults 5/5. Para Delay com defaults, a fórmula antes de Randomize é `20+20×count(ExtendTime)−10×count(DurationDown)` ticks; não há clamp local de duração no trecho consultado. [Harm][ta-harm], [fallbacks][ta-harm-values], [Delay][ta-delay], [defaults][ta-delay-config].

**Invalidação:** alteração do source/JAR/config, operador, compatibilidade/caps do receptor, recipe/tier ou novo contrato mutador exige revisão por campo. Este dossiê classifica o componente estático, não certifica todas as combinações Ars ou todo o provider.

[ta-class]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/augment/AugmentDurationDown.java#L9-L36
[ta-base]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractAugment.java#L15-L60
[ta-build]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellStats.java#L131-L152
[ta-stats]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellStats.java#L224-L243
[ta-cost]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L125-L145
[ta-limits]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L226-L268
[ta-event]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/event/SpellModifierEvent.java#L13-L32
[ta-recipe]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/generated/resources/data/ars_nouveau/recipe/glyph_duration_down.json#L1-L16
[ta-cap-map]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/util/SpellPartConfigUtil.java#L34-L64
[ta-duration]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellStats.java#L24-L57
[ta-potion]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/IPotionEffect.java#L10-L28
[ta-harm]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectHarm.java#L32-L49
[ta-harm-values]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectHarm.java#L96-L104
[ta-delay]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectDelay.java#L33-L49
[ta-delay-config]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectDelay.java#L63-L80

[ta-starter]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L307-L310
