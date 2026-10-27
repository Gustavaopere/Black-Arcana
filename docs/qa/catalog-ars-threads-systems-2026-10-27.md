# Ars Nouveau — 16 Threads e três sistemas, 27/10/2026

Base reconciliada: `Black-Arcana/main@abdaeb62c713257196392fda25158d0bb8ac24ef` (PR #917). Os commits do Goety até a PR #924 foram preservados. As PRs anteriores do Ars foram integradas em ordem: #915 (16 Effects), #916 (seis familiares) e #917 (quatro Threads), com revisão e checks dos HEADs atualizados. Este lote acrescenta contratos para as19 fichas restantes do recorte observado.

## Entrega e contadores

Threads: Amethyst Golem, Blank Thread, Chilling, Depths, Drygmy, Feather, Heights, High Step, Immolation, Kindling, Magic Capacity, Spell Power, Starbuncle, Warding, Whirlisprig e Wixie. Sistemas: Perk Slot Providers, Player Mana e Spellbooks/Glyph Learning. O [contrato comum](../../wiki/modpack-catalog/providers/✅-ars-nouveau/PERK-SYSTEM-STATIC-REMAINING-5.13.1.md) distingue operações por instância, maior slot, atributos, callbacks, persistência e recursos.

O manifesto preserva as **119 entradas anteriores**, os rosters e todos os demais campos, acrescentando19 certificados source-only. Contadores: **20/20 Threads**, **3/3 sistemas candidatos**, **138/138 fichas Ars detectadas** e **138/2075 fichas globais observadas (6,7%)**. Permanecem **85/85 glyphs**, **24/24 rituais**, **6/6 familiares** e **0/164 providers integralmente certificados**. Não foram criadas novas identidades ou fichas candidatas.

O denominador138 é um recorte da heurística atual de arquivos. `source-resource.md` e o apoio de composição continuam fora desse denominador; outros objetos integráveis também podem existir. O resultado138/138 não fecha o universo do Ars Nouveau. As barras continuam separando fichas estáticas observadas de providers com escopo integral certificado.

## Evidência e limites

Source oficial imutável `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`, versão declarada **5.13.1**. Publisher `ars_nouveau-1.21.1-5.13.1.jar`: **20107711 bytes**, SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`, SHA-256 `99dff85e8778f7ae21dfd51cdedadf20f555a834fc757c0afe5f03c10eea96f2`. Hash e tamanho foram conferidos independentemente durante a revisão. O perfil instalado original não foi novamente medido.

Grau dos19 novos certificados: **`PINNED_SOURCE_WITH_RELEASE_SHA_ONLY`**. O fingerprint é proveniência do release, não prova de classfile, registry carregado ou equivalência de método. A auditoria compilada dos109 pares de ID/classe cobre apenas85 glyphs e24 rituais; não comprova Threads, familiares ou sistemas. Mantidos `claim_scope=STATIC_TECHNICAL_CATALOG_ONLY`, `mutating_hook=NOT_VERIFIED` e `physical_qa=NOT_TESTED`, com sete evidências locais por ficha.

Não foram copiados implementações completas ou assets upstream: foram incorporados fatos, fórmulas, paráfrases e referências. Nenhum Java/runtime, adapter executável, dependência ou Stage foi alterado.

## Precisões de código

- `countForPerk` calcula o maior slot; callbacks de eventos e aplicação de atributos podem percorrer cada instância. IDs fixos de modifiers não comprovam soma linear entre peças. Tier da armadura, valor de slot e progressão RPG são dimensões distintas.
- Depths/Heights consomem o maior slot em caminhos específicos; Feather tem atributo limitado e ordem própria de dano. High Step/Starbuncle usam ResourceLocation no caminho ativo, distinguindo constantes UUID antigas não consumidas ali.
- Chilling e Kindling despacham por instância; Kindling substitui fire ticks e pode reduzir um estado maior. Immolation combina condições independentes e consumidor de dano de fogo; isso não prova extensão universal de duração.
- Magic Capacity, Spell Power, Warding e Amethyst Golem têm operações/atributos/consumidores próprios. Mana cache, dano pelo helper e mitigação ordenada não são o mesmo ponto de mutação.
- Drygmy usa dois mixins de loot; Whirlisprig altera a saturação acumulada; Wixie distingue beneficiário/aplicador e o receptor de sync. O pacote não transporta todos os flags/amplifier. Blank herda o retorno default sem alteração, não cria modifiers novos por si só.
- Slots são ordenados antes de associar perks; a alteração da armadura pode substituir tags sem copiar todo estado anterior. `IPerk.applyAttributeModifiers` é chamado por `instance.getPerk()`, não por um método homônimo de PerkInstance.
- Mana tem reserva, cache, regen e recálculo em fases diferentes. A chamada literal `Mth.clamp(0,newReserve,1)` não comprova o clamp pretendido; a ordem de branches também impede afirmar saldo sempre não negativo sob máximo negativo. Admissão e débito de cast são calculados separadamente.
- Conhecimento persistido, starters, glyphBonus, book tier, GUI, receita e XP são estados/gates diferentes. Não transferir validação de interface para uma garantia universal do servidor, nem confundir aprendizagem de Ars com Mastery RPG.

## Reconciliação do trabalho paralelo

As três fichas de sistemas também haviam recebido auditorias na `main`. Foram preservados seus fatos, tabelas e testes, combinados com os novos contratos de sete campos. Status antigos de certificação pendente foram datados como checkpoint de26/10/2026. O dossiê histórico aponta para o contrato atual. A qualificação de `setMana` sob máximo negativo foi reconciliada para evitar duas afirmações incompatíveis.

O módulo existente dos quatro Threads avançados mantém os mesmos quatro CASES e demais verificações; somente o contador atual de Threads passou de4 para20. Os testes de source dos três sistemas foram preservados sem alteração. Não foram acrescentados testes que apenas espelhem as novas fichas.

## Verificação

- Revisões independentes dos quatro grupos de Threads, três sistemas, comum, manifesto e reconciliação: **PASS**, após correções de nomenclatura/API, retorno default, sync e qualificação de mana.
- Nas19 fichas e no comum: **378 referências source pinadas**, sendo **354 com linhas** e24 de arquivo completo, **105 arquivos upstream distintos**; caminhos, versão e limites conferidos. Referências repetidas não equivalem a378 hooks diferentes.
- **222 testes existentes PASS**:22 de índices,3 do gerador,36 de Effects,33 de rituais,7 de familiares,6 de Threads avançados,5 de sistemas,12 de registro estático Ars,15 de IDs compilados Ars,52 do catálogo global,5 do ledger físico e26 de pendências.
- **509 índices PASS**:164 providers,2075 candidatas,138 certificados,0 providers integrais e0 problemas. Gerador `--check`: PASS.
- Nos **27 Markdown** alterados: **398 links locais** e **35 tabelas** válidos, sem referências indefinidas, arquivos ausentes ou colunas inconsistentes. `git diff --check`: limpo. O diff contra a base não altera arquivos do Goety.

CI e smoke tests do repositório não substituem QA de modpack. Continuam pendentes configuração instalada, client/server, multiplayer, save/reload, ordem com addons, permissões, safe bridge de perks e deduplicação causal. Black Arcana, RPG Skill Tree e Enshrouded conservam suas autoridades; nenhuma escrita externa em Ars foi homologada por esta documentação.
