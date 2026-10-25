# Ars Nouveau 5.13.1 — quinze Effects de dano, tempo e propagação

Revisão de **25/10/2026**, a partir da `main@094c9dc7ec954e26b5b41f5baef917274dfedbb8` (PR #903). Este lote acrescenta quinze contratos individuais: **35/67 Effects**, **53/85 glyphs**, **53/138 fichas Ars detectadas** e **53/2075 fichas candidatas globais**. Augments permanecem **13/13**, Forms **5/5**, providers integralmente certificados **0/164**. As barras atuais são geradas no [índice global](../INDEX.md), no [índice Ars](INDEX.md) e no [índice de Effects](glyphs/effects/INDEX.md); os denominadores são recortes observados, sem fechamento do universo integrável.

## Proveniência e alcance da certificação

Source oficial imutável `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`, release **5.13.1**. Publisher Modrinth [qEFs5RRw](https://modrinth.com/mod/ars-nouveau/version/qEFs5RRw), `ars_nouveau-1.21.1-5.13.1.jar`, **20107711 bytes**, SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`, SHA-256 `99dff85e8778f7ae21dfd51cdedadf20f555a834fc757c0afe5f03c10eea96f2`. A [auditoria compilada](EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md) comprova **85 glyphs +24 rituais**, seus IDs e classes; não comprova equivalência de todos os métodos do source com o JAR nem execução em jogo. O publisher coincide com o fingerprint histórico físico #047; o perfil original não foi novamente medido.

Cada ficha distingue sete campos: identidade, comportamento, parâmetros, targeting, custos, integração e validação. O [manifesto](../../meta/PERK-READY-CERTIFICATIONS.json) mantém `claim_scope=STATIC_TECHNICAL_CATALOG_ONLY`, `evidence_grade=PINNED_SOURCE_PLUS_SHA_EXACT_BINARY_IDENTITY`, **`mutating_hook=NOT_VERIFIED`** e **`physical_qa=NOT_TESTED`**. Há APIs nativas inspecionadas; o contrato executável seguro de uma perk RPG/Black Arcana continua por comprovar. Fatos, paráfrases e referências foram usados sem incorporar implementação ou assets upstream.

## Contratos individuais

| Effect | Parâmetro e consumidor que uma perk precisa distinguir |
|---|---|
| [Cold Snap](glyphs/effects/cold-snap.md) | Dano condicionado ao estado frio, congelamento e shards têm etapas separadas; cancelamento do dano inicial não veta automaticamente os efeitos secundários. |
| [Flare](glyphs/effects/flare.md) | Dano inicial, geração de Cinders e consumo/detonação de Blast são operações distintas, com caminhos de dano próprios. |
| [Wind Shear](glyphs/effects/wind-shear.md) | A fórmula lê distância por blocos de ar e amplification; uma chave de configuração declarada não implica que a fórmula a consuma. |
| [Wind Burst](glyphs/effects/wind-burst.md) | AOE altera o raio da explosão TRIGGER, amplification altera a força do calculator e Sensitive troca a entidade-fonte; o WindCharge auxiliar não é emitido como projétil. |
| [Fangs](glyphs/effects/fangs.md) | Padrão e número de presas, warmup e dano da entidade invocada são eixos separados; a entidade não usa o helper de dano do glyph. |
| [Firework](glyphs/effects/firework.md) | Rocket existente e fallback sintetizado interpretam augments de formas diferentes; Split multiplica emissões. |
| [Gravity](glyphs/effects/gravity.md) | Presença de Extend Time seleciona status persistente em vez do impulso imediato; o consumidor de queda não é a aplicação do status. |
| [Rune](glyphs/effects/rune.md) | Bloco, tile, trigger e conversão por Runic Chalk definem o lifecycle; a descrição de rune temporária não fecha todos os caminhos de permanência. |
| [Delay](glyphs/effects/delay.md) | Contagens de Extend/Reduce, duração calculada e ordem da EventQueue controlam retomada; não basta alterar durationMultiplier. |
| [Reset](glyphs/effects/reset.md) | Manipula contextos e escopos de composição; a permissão para ultrapassar certos limites consulta um conjunto explícito, não todos os glyphs. |
| [Rewind](glyphs/effects/rewind.md) | Histórico de entidade, callbacks de contexto e tempo solicitado são limites distintos; restauração de saúde por setHealth não é um evento de cura comum. |
| [Linger](glyphs/effects/linger.md) | Volume, frequência, alvos por passagem, lifetime e budget de procs diferem entre o ramo de entidades e Sensitive. |
| [Wall](glyphs/effects/wall.md) | A varredura de entidades e o ramo Sensitive têm cadências diferentes; o histórico de hits e seu vencimento precisam de deduplicação própria. |
| [Burst](glyphs/effects/burst.md) | Propaga a receita restante em posições/alvos discretos; geometria por blocos não é esfera contínua exata nem prova de LOS. |
| [Orbit](glyphs/effects/orbit.md) | Contagem, fase angular, raio, velocidade e receita residual são entradas diferentes; o divisor de velocidade tem um ponto singular sem clamp local. |

As fórmulas literais, unidades, defaults, limites de configuração, receitas, XP e referências de classe/método/linhas estão nas fichas. Um comportamento ausente de um callback pode existir em uma entidade, status, evento ou addon; as ausências são delimitadas ao código efetivamente inspecionado.

## Superfícies públicas e limites de mutação

[`SpellStats.Builder.build`][stats-build] aplica augments e itens, publica `SpellModifierEvent` e devolve os stats do builder original. O [evento público][modifier] permite investigar mutação **in-place** do builder; substituir `event.builder` não troca o objeto retornado. Cada consumidor ainda decide entre número, flag, contagem e receita residual. Escrever amplification, por exemplo, não reescreve automaticamente Pierce, Split, configuração ou uma entidade já criada.

[`EffectResolveEvent.Pre`][effect-event] é cancelável e expõe os objetos da resolução. No [`SpellResolver.resume`][resume], apenas `isCanceled()` é consultado explicitamente depois do evento; reatribuir os campos do payload não substitui os valores locais de stats, effect, alvo ou contexto. Mutações no objeto original compartilhado são outra operação e requerem análise do consumidor. O resolver também calcula `hitPos`/`hitEntity` antes do loop; um adapter que altere seu hit durante o loop precisa considerar as capabilities já selecionadas.

O mesmo fluxo publica `EffectResolveEvent.Post` inclusive quando uma capability retorna `STOP_ALL` ou pula o Effect. **Post não é confirmação de dano, spawn, cura ou mutação de mundo bem-sucedidos.** Cancelar um dano individual também não cancela operações subsequentes que o callback executa sem condicionar ao resultado. Cada ramo documentado precisa de confirmação e deduplicação compatíveis com o que realmente ocorreu.

[`SpellContext.makeChildContext`][children] considera `IContextManipulator`, parent e receita restante. Resolver derivado, emissão de campo, tick, alvo adicional, trigger de rune ou retomada de Delay não são por si mesmos um novo cast pago nem um novo crédito de Mastery. O [`resume`][resume] inspecionado não cobra mana; [admissão e pagamento][costs] têm cálculos/eventos separados (`SpellCostCalcEvent.Pre/Post`) e clamp de custo em zero. Uma perk de custo precisa preservar ambos e a autoridade do caster.

## Autoridade, validade e pendências

Ars Nouveau governa composição, seleção, mana do jogador, Source quando aplicável, aprendizagem, entidades e estados nativos. RPG Skill Tree governa sua progressão/perks/gates por contrato; Black Arcana conserva seu casting, Corruption, Strain, WorldEffectPolicy e causalidade; Enshrouded conserva seus sistemas ambientais. Nenhum desses limites autoriza repetir o efeito de Ars ou recompensar cada tick como cast independente.

Os caps e budgets locais são propriedades do caminho documentado, não garantias globais de segurança. Config implantada, listeners, claims/PvP, casters automatizados, persistência, multiplayer, custos efetivos, correspondência integral de bytecode e QA em cliente/servidor permanecem pendentes. Mudança de JAR, source, configuração ou consumidores exige reauditoria. Este lote não altera runtime, hooks executáveis ou Stage.

[stats-build]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellStats.java#L138-L152
[modifier]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/event/SpellModifierEvent.java#L16-L32
[effect-event]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/event/EffectResolveEvent.java#L11-L50
[resume]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellResolver.java#L203-L270
[children]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellContext.java#L143-L168
[costs]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellResolver.java#L273-L307
