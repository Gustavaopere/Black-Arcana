# Ars Nouveau 5.13.1 — contrato estático dos 13 augments

**Revisão de 25/10/2026**, base Black Arcana `43661700cd027bc2cf51eb09e9ed46ea9c551f4e` (#897). A conclusão certificada é a documentação estática de cada componente no [manifesto](../../meta/PERK-READY-CERTIFICATIONS.json). Não certifica integração de perk, configuração implantada, gameplay ou todo o provider. A família tem 13 fichas; o provider tem 138 fichas candidatas detectadas e seu universo integral continua aberto.

## Proveniência e identidade

[Source oficial][version] `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`, versão declarada 5.13.1, Minecraft1.21.1/NeoForge21.1.228; pack registrado NeoForge21.1.250. A [licença do source][license] inclui LGPLv3 e reserva os assets; somente fatos, paráfrases e referências foram incorporados nesta revisão, sem código ou arte upstream.

Publisher Modrinth [qEFs5RRw](https://modrinth.com/mod/ars-nouveau/version/qEFs5RRw), arquivo `ars_nouveau-1.21.1-5.13.1.jar`: medidos **20107711 bytes**, SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`, SHA-256 `99dff85e8778f7ae21dfd51cdedadf20f555a834fc757c0afe5f03c10eea96f2`. O SHA-1 coincide com a modlist física histórica #047 e com a [auditoria compilada de 85 glyphs +24 rituais](EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md). Não é nova medição do perfil original, ausente nesta sessão. Identidade binária não equipara todos os métodos/consumidores ao source nem prova execução em jogo.

## Operadores próprios e interpretação pelo receptor

Todos são **augments composicionais**: não possuem cast autônomo, alvo, hitbox, DamageType, projétil ou duração de entidade próprios. Quando pertinentes, esses eixos pertencem à Form/Effect que consome os stats, a contagem ou a receita. Cada ficha identifica consumidores concretos; o operador abaixo não substitui essa análise.

| Augment / ficha | Operador no source | Mana default / tier |
|---|---|---|
| [Accelerate](glyphs/augments/accelerate.md) | `addAccelerationModifier(+1.0f)` | 10 / II |
| [Amplify](glyphs/augments/amplify.md) | `addAmplification(+1.0)` | 20 / I |
| [AOE](glyphs/augments/aoe.md) | `addAOE(+1.0)` | 35 / II |
| [Dampen](glyphs/augments/dampen.md) | `addAmplification(−1.0)` | 0 / II |
| [Decelerate](glyphs/augments/decelerate.md) | `addAccelerationModifier(−0.5f)` | 5 / II |
| [Extend Time](glyphs/augments/extend-time.md) | `addDurationModifier(+1.0)` | 10 / II |
| [Extract](glyphs/augments/extract.md) | Sem override de applyModifiers; consumidores leem contagem/presença | 30 / II |
| [Fortune / Luck](glyphs/augments/fortune.md) | Sem override; consumidores leem contagem/presença | 80 / II |
| [Pierce](glyphs/augments/pierce.md) | Sem override; consumidores leem contagem/receita | 40 / II |
| [Randomize](glyphs/augments/randomize.md) | Overload contextual chama `builder.randomize()` | 0 / I |
| [Reduce Time](glyphs/augments/reduce-time.md) | `addDurationModifier(−1.0)`, ID `glyph_duration_down` | 15 / II |
| [Sensitive](glyphs/augments/sensitive.md) | `builder.setSensitive()`; contagem é dado distinto | 10 / I herdado |
| [Split](glyphs/augments/split.md) | Sem override; Form consome contagem | 20 / III |

Evidências por classe/método/linha estão nas fichas. Nenhum operador oferece percentual universal de dano, raio, velocidade ou tempo. Extract/Fortune têm incompatibilidade **declarada na descrição**; o veto programático default do par não foi comprovado no recorte auditado, e Break tem consumidores distintos para ambos.

## Construção dos stats e API pública existente

[SpellStats.Builder.build][build] percorre augments, aplica modificadores dos itens e então publica [SpellModifierEvent][modifier-event], antes de devolver os stats. O evento expõe `builder`, caster, part, hit, world e context. Existe, portanto, **superfície pública de escrita** antes do consumidor. O contrato seguro de perk RPG/Black Arcana — inscrição, lado servidor, seleção por glyph, limites, custos, atribuição e deduplicação — continua **NOT_VERIFIED**.

O caminho observado permite investigar mutação **in-place** no builder original. Reatribuir `event.builder` a outro objeto não é consumido pelo retorno de build, que devolve seu próprio `spellStats`. Não confundir acesso público com substituição efetiva do resolver ou garantia de que um consumidor leia o campo alterado.

No [SpellResolver][resolver], stats da Form são construídos no cast; [stats de cada Effect][effect-stats] são construídos de novo no resume. Augments não são executados como Effects independentes. Um evento de modifier pode ocorrer por componente e por contexto derivado; não é confirmação de dano, pagamento ou novo cast/Mastery. Depois do build, [EffectResolveEvent.Pre](VERIFIED-EVENT-SURFACES-5.13.1.md) oferece outra fase, com contrato diferente.

[SpellStats][stats] separa números, flags e lista de augments. Alterar a lista depois do build não recompõe automaticamente amplification/AOE/acceleration/duration. Pierce do projétil pode ler a receita original, enquanto Split lê `getBuffCount` dos stats; uma única mudança no builder não equivale a uma mutação universal dos dois.

## Caps, mana e aprendizagem

[AbstractSpellPart][part-config] configura enabled, mana, starter, limite global por spell e tier. Limites por augment pertencem ao receptor; se a tabela está ausente, getAugmentLimit retorna Integer.MAX_VALUE. O [validador padrão][validator] aplica compatibilidade/caps/combo na montagem da receita; certas validações em cast dependem de flags do servidor. Não apresentar um default local como limite físico universal.

[AbstractAugment#getCostForPart][augment] consulta custo do receptor quando existe tabela de override; os números da tabela são defaults, não preço final da spell. A composição, itens, caster e eventos de custo continuam Ars-owned. Mana do jogador e Source de mundo/crafting são recursos distintos. Modificar apenas um ponto do custo pode separar admissão e débito; ver [superfícies verificadas](VERIFIED-EVENT-SURFACES-5.13.1.md).

[Datagen][recipes] fixa ingredientes por glyph; [XP por tier][recipe-builder] é derivado no builder. Tier I/II/III corresponde a 27/55/160 XP de receita neste source. Config em execução pode alterar custo/tier/starter sem reescrever a receita já gerada. As fichas e [aquisição](ACQUISITION.md) registram os ingredientes; Survival/config real continua pendente.

## Autoridade e validação

Ars controla SpellResolver/SpellContext/SpellStats, mana, Source, aprendizagem, efeitos e mutações de mundo. RPG Skill Tree mantém progressão/perks/gates; Black Arcana mantém seu runtime e WorldEffectPolicy; Enshrouded mantém seus efeitos ambientais. Nenhum desses projetos recebe autorização para repetir efeitos, duplicar loot, criar outro SpellStats ou premiar cada projétil/retomada como novo cast.

**Grau admitido:** `STATIC_SOURCE_PINNED + BINARY_IDENTITY_ONLY`. **Integração mutadora:** `NOT_VERIFIED`; **QA físico:** `NOT_TESTED`. O manifesto não promove Stage ou certifica todo o mod. Mudança de JAR, source, configuração, operadores ou consumidores exige revisão. Os [índices gerados](glyphs/augments/INDEX.md) contabilizam somente certificados individuais com evidências locais; os 164 providers continuam sem fechamento integral certificado.

[version]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/gradle.properties#L9-L18
[license]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/license.txt#L1-L12
[build]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellStats.java#L138-L152
[modifier-event]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/event/SpellModifierEvent.java#L16-L32
[resolver]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellResolver.java#L119-L134
[stats]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellStats.java#L48-L129
[part-config]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L218-L279
[validator]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/validation/StandardSpellValidator.java#L33-L72
[augment]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractAugment.java#L34-L60
[recipes]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/GlyphRecipeProvider.java#L37-L48
[recipe-builder]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/GlyphRecipeProvider.java#L142-L162

[effect-stats]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellResolver.java#L203-L231
