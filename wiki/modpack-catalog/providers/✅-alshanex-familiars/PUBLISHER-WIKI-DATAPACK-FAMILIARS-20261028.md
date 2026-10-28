# Alshanex — superfícies públicas de datapack, combate e familiares (wiki, 2026-10-28)

> Escopo: documento de **interoperabilidade e catalogação clean-room**, sem código/asset do fornecedor, sem novo spell/ritual contabilizado e sem certificação `COMPLETE_PERK_READY`. Consulta à wiki pública em 2026-10-28; a página não fornece aqui um pin verificável para a release 4.0.3. Este documento não substitui a autoridade do JAR instalado nem prova comportamento no modpack.

## Configuração publicada de rituais (contrato documental, não bytecode 4.0.3)

A [documentação do fornecedor](https://wiki.pixeldreamstudios.net/mods/alshanex-familiars) descreve um tipo de receita `alshanex_familiars:ritual_recipe` sob `data/alshanex_familiars/recipe/ritual_recipes/`. Campos descritos: `central_item` (ingrediente central obrigatório), `inputs` (quatro entradas de pedestal com `ingredient`, `count` opcional default 1 e `consume` opcional default true), `result` (item, `count` e componentes opcionais), `particle_type` opcional. Pedestais aceitam um item, de modo que `count>1` deve ser tratado como risco/unsupported sem confirmação. `consume=false` significa insumo retido segundo a wiki, **não** um contrato transacional comprovado em 4.0.3.

A página descreve Ritual Core + quatro estátuas cardinalmente dispostas a dois blocos e uma progressão aproximada de cinco segundos; retirada prematura de ingrediente cancela/reinicia esse progresso. Não presumir compatibilidade com o `RitualEngine` do Black Arcana ou com `WorldEffectPolicy` a partir dessas semelhanças. A cadeia de autoridade do provider inclui montagem, consumo, recipes, output, ownership e automação.

O `Ritual Automator` é descrito como consumidor de receitas, com entidade familiar alocada, contêiner e seleção de receita. A wiki especifica alcance de até dez blocos em torno do core (cinco verticalmente), e coordenação entre múltiplos automators. Esses limites são **documentais**, sujeitos a validação do JAR 4.0.3; não criar segundo executor para o mesmo ritual.

## Rosters de feitiços de familiares

A wiki informa que a seleção de spells de ataque/defesa/movimento/suporte pode ser influenciada por *spell tags* de datapack. Superfície documental: `data/alshanex_familiars/tags/irons_spellbooks/spells/<familiar>/<categoria>.json` com categorias `attack`, `defense`, `movement`, `support` e, para Cleric, `buffing` e `healing`. A semântica básica de `replace:false` para adicionar e `replace:true` para sobrescrever é descrita pelo fornecedor. A wiki ressalva que certos spells de assinatura são adicionados separadamente das tags, logo **editar tags não prova controle total sobre todo cast de familiar**.

| Familiar segundo a wiki | Subpasta documental de tags |
|---|---|
| Archmage | `archmage/` |
| Lightning Mage | `mage/` |
| Summoner | `summoner/` |
| Necromancer | `necromancer/` |
| Hunter | `hunter/` |
| Druid | `druid/` |
| Illusionist | `illusionist/` |
| Plague Doctor | `plague/` |
| Scorcher | `scorcher/` |
| Cleric | `cleric/` |
| Bard (condicionado a Tunes) | `bard/` |
| Frostling | `frostling/` |
| Dragoon | `dragon_warrior/` |

Essas **13 pastas documentais não são 13 novos spells** e não constituem inventário físico auditado das tags em 4.0.3. Listas de spells pertencem ao Iron's e ao provider. O Black Arcana não deve relançar spells observados na IA dos familiares nem atribuir `Mastery` por ticks/efeitos auxiliares sem evento causal seguro e regra de deduplicação.

## Scroll Reroll Station — filtros e riscos de integração

Segundo a wiki, uma estação administrada por Archmage examina contêineres próximos em três blocos e aplica filtros de entrada/saída com interseção entre cinco categorias: escola, raridade, faixa de nível, IDs de spells e tags de spells. O reroll editorial ocorre a cada aproximadamente dois segundos, mantendo raridade normalmente e com chance divulgada de **5%** para subir uma raridade; o resultado só retorna ao contêiner ao satisfazer filtro de saída. A wiki declara que `alshanex_familiars:archmage_cannot_reroll`, `archmage_cannot_create` e `station_only_roll` interferem no pool de seleção.

**Não considerar 5%, 2 segundos ou alcance de 3 blocos parâmetros confirmados no JAR 4.0.3.** Nenhuma operação de reroll deve ser duplicada por perks, nem o pool de saída pode ser inferido sem configuração efetiva e filtros. Não tomar cache de UI ou indicação de recipe como sucesso do servidor.

## Tags de suporte que alteram efeitos

A wiki documenta os seguintes nomes de tags, úteis como potenciais pontos de auditoria e não como APIs mutadoras validadas:

- `alshanex_familiars:necromancer_ability_blacklist` — entidade excluída de um comportamento de necromancer;
- `alshanex_familiars:druid_growables`, `druid_cannot_breed` — seleção de blocos e entidades que o druid afeta;
- `alshanex_familiars:freezeable_entities`, `block_freeze_blacklist`, `freeze_destroyable`, `freeze_ignore` — seleção de alvo/bloco em efeitos congelantes;
- `alshanex_familiars:unlocks_revival` — entidade ligada à progressão de revival.

Esses caminhos são **documentação do fornecedor**; existência/identidade exata e processamento no pack exigem inspeção dos recursos do JAR 4.0.3, de tags sobrepostas por datapacks e de eventos reais. Tags de block-world mutation não são autorização de contornar protections do servidor ou de Black Arcana.

## Gates e evidência

| Questão de perk/integrador | Evidência disponível | Estado |
|---|---|---|
| Identidades de 7 spells + 11 rituais | Auditoria do JAR 4.0.3, já contabilizada | `COUNTED_EXACT` identidade |
| Identidade das 13 pastas de tags no JAR | Wiki pública, sem listagem do ZIP exato neste documento | `NOT_VERIFIED` |
| Hook seguro para mudar targeting/range/cooldown/efeito de familiar | Nenhuma assinatura auditada | `NOT_VERIFIED` |
| Tempo, ganho de raridade, transações do Scroll Reroll em 4.0.3 | Wiki pública contemporânea, sem prova binária | `NOT_VERIFIED` |
| Receitas e resultados `*_shard.json` frente à Wiki sobre ovos | Evidências contraditórias entre documento atual e relato do ZIP | `CONFLICT` até prova por versão |
| Teste modpack + Iron's 3.16.3 + FamiliarsLib + Tunes | Não executado nesta contribuição | `NOT_TESTED` |

**Semântica:** nenhuma nova magia, ritual, atributo ou perk é adicionada ao contador. Este dossiê apenas preserva contratos documentais e divergências para a futura catalogação técnica, respeitando arquitetura clean-room e fail-closed.

Fontes: [Wiki oficial de Alshanex's Familiars](https://wiki.pixeldreamstudios.net/mods/alshanex-familiars) — seções *Datapacks*, *Ritual Recipes*, *Familiar Spell Rosters*, *Scroll rerolls*, *Ability tags*; [README da versão instalada](README.md); [auditoria exata](EXACT-4.0.3-ARTIFACT-AUDIT.md).
