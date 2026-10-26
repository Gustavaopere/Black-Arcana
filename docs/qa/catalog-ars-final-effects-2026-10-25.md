# Ars Nouveau — dezesseis Effects finais, 25/10/2026

Base reconciliada com o trabalho de outro chat: `Black-Arcana/main@88368f2d37a14de855c54579bc53cd1b173581a1`, PR #914. Merge e três checks pós-merge dessa base conferidos como SUCCESS: `verify`, `stage05_qa_companion_smoke`, `provider_index_consistency`. As fichas já integradas foram preservadas; a branch local anterior de preparação dos32 Effects não tinha alterações pendentes.

## Entrega e recorte

Foram auditadas as16 fichas ainda pendentes de Effects: Access Ender Inventory, Infuse, Interact, Item Pickup, Toss, Name, Wololo, Intangible, Prestidigitation, Animate Block, Bubble, Summon Decoy, Summon Steed, Summon Undead, Summon Vex e Summon Wolves. O [documento comum](../../wiki/modpack-catalog/providers/✅-ars-nouveau/EFFECT-STATIC-REMAINING-SIXTEEN-5.13.1.md) reúne as fronteiras compartilhadas; cada ficha documenta os sete campos e os consumidores próprios.

O manifesto preserva as **93 entradas anteriores** e acrescenta16, mantendo todos os demais campos, rosters e registros de providers. Contadores: **67/67 Effects**, **85/85 glyphs**, **24/24 rituais**, **109/138 fichas Ars detectadas**, **109/2075 fichas candidatas globais** e **0/164 providers integralmente certificados**. Não foram criadas novas identidades ou fichas candidatas. Restam29 fichas Ars observadas: seis familiares, vinte perks e três sistemas; esse recorte não fecha o universo integral do provider.

O gerador dos índices recebeu duas precisões documentais: uma barra global de **fichas estáticas observadas** (109/2075=5,3%), com denominador explicitado separadamente da barra de providers integrais (0/164=0%); e um cabeçalho de subpasta concluída somente quando há fichas e todas estão certificadas. O ramo de certificação integral de provider continua independente. Os85 glyphs são componentes, não85 magias acabadas ou uma enumeração de combinações possíveis.

Todos os novos registros mantêm `claim_scope=STATIC_TECHNICAL_CATALOG_ONLY`, `evidence_grade=PINNED_SOURCE_PLUS_SHA_EXACT_BINARY_IDENTITY`, **`mutating_hook=NOT_VERIFIED`** e **`physical_qa=NOT_TESTED`**. APIs públicas existem; um adapter seguro de perks RPG/Black Arcana, com custos, caps, autoridade e deduplicação, não foi homologado.

## Fonte e identidade binária

Source oficial `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`, release5.13.1. Publisher Modrinth **qEFs5RRw**, arquivo `ars_nouveau-1.21.1-5.13.1.jar`, **20107711 bytes**, SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`, SHA-256 `99dff85e8778f7ae21dfd51cdedadf20f555a834fc757c0afe5f03c10eea96f2`. Fatos, fórmulas, paráfrases e referências foram incorporados sem copiar implementações completas ou assets upstream.

Auditoria existente `docs/qa/ars_5131_exact_ids_binary_audit.py` executada novamente com Java21 e o publisher JAR: **PASS**, `SHA_MATCHED_COMPILED_109_RESOURCELOCATION_CLASS_IDS_NOT_RUNTIME`,85 glyphs+24 rituais e+0 raízes semânticas. Os16 pares de ID/classe deste lote foram cruzados com o resultado. A prova é de identidade; não equipara todos os métodos Java/bytecode nem carrega o registry em jogo. O perfil físico original não foi novamente medido.

## Achados relevantes para perks

- Inventário: preferência de handler não garante busca global com resultado; uma PriorityQueue percorrida por for-each não comprova ordenação estrita de inserção. Restituição não tem idempotência geral demonstrada. Infuse inclui poções comuns pelo provider DEFAULT; consumo, frasco vazio, jar e modo de emissão são caminhos separados. Pickup Post recebe o restante; Toss desconta budget solicitado, não apenas rendimento real.
- Estados: Name pode alterar offhand do caster ao nomear outra entidade; lookup de name tag não é consumo. Wololo tem receptores discretos/contínuos e cache cujo limite não é comprovado pelo nome FixedStack. Intangible e ParticleTile têm contagens por ticks processados e serialização própria; isso não é um rollback universal ou garantia de dirty save a cada tick.
- Entidades: Bubble modifica um evento de dano já existente; os dois campos de pop e a captura automática não fornecem uma deduplicação universal. Animate difere entre bloco e cabeça, com gasto de tempo por ataque e restauração de dados específica. Decoy redireciona alvos inicialmente, sem demonstrar taunt contínuo ou filtro genérico de hostilidade.
- Invocações: Horse/Wolf descartam por contador; Skeleton sofre starve periódico após expirar; Vex separa lifetime vanilla do campo exposto pela interface Ars. `getOwner` e `getOwnerAlt` não são equivalentes para todos os consumidores. Spawn solicitado, SummonEvent, Dispel e callbacks de morte precisam de atribuição e confirmação próprias.
- Integração: builder original mutável e veto de Pre são superfícies reais. Reatribuir payload não substitui automaticamente os locais do resolver. Post, contexto filho, partícula, inserção tentada, captura ou tick não confirmam um cast novo, pago ou merecedor de Mastery adicional.

## Verificação

- Revisão independente dos quatro grupos, consumidores, custos/receitas, documento comum e manifesto: **PASS**. Precisões de geometria/identidade compilada e de Prestidigitation foram corrigidas e reavaliadas.
- Nas16 fichas e no documento comum: **307 referências source pinadas com limites de linhas**, **69 arquivos upstream distintos**, **55 links locais** e **17 tabelas**; revisão, arquivos, limites, labels e colunas válidos. Referências repetidas não são307 hooks diferentes.
- **202 testes existentes PASS**:20 de índices,3 do gerador,36 de contratos de Effects,33 de rituais,12 de registro estático Ars,15 de IDs compilados Ars,52 do catálogo global,5 do ledger físico e26 do tracker de pendências. Não foram criados novos testes que espelhem o texto das fichas.
- Cenários manuais do cabeçalho: grupo certificado, parcial e vazio conferidos; grupo vazio não recebe ✅. Barra observada5,3% e barra de providers0% verificadas de forma independente.
- Auditoria de **509 índices PASS**:164 providers,2075 candidatas,109 certificados,0 providers integrais e0 problemas. Reordenação incidental de três índices Goety causada pelo gerador foi restaurada à base; esse provider não foi modificado.
- `generate_perk_ready_indexes.py --check`: **PASS**,509 índices,2075 candidatas,0 erros. Nos **26 Markdown** alterados: **579 links locais** e **29 tabelas** válidos, sem referências indefinidas, arquivos ausentes ou colunas inconsistentes. `git diff --check`: limpo.

Nenhum Java/runtime, adapter executável, dependência, lockfile, comportamento do provider ou Stage foi alterado. Config instalada, claims/PvP, side effects de addons, cliente/servidor, multiplayer, unload/reload, persistência física e integração de perks continuam pendentes. CI, merge e smoke tests do repositório não equivalem a QA das magias do pack.
