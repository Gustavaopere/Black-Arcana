# RadioactiveItem — censo causal de consumidores por identidade 1.0.10

**Estado: CANDIDATE / STATIC_CONSUMER_CENSUS_ONLY / NOT_CERTIFIED / NO_MUTATION / NOT_TESTED.** Base Black Arcana main `8341321f98beafbc0b00e3f17bc16e0e6208f18e`; modlist sibling [#019](https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/18144e8318978b8904b584b80b4ddd630f22f8f0/PROJECT-INSTRUCTIONS/modlist/modlist.md), publisher 1.0.10 `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`, 75.279.314 bytes. Nenhuma nova leitura da instalação física.

## Escopo e razão

O [dossiê anterior](EXACT-RADIOACTIVE-ITEMS-1.0.10.md) projeta owners e recursos filtrados por nome de arquivo. O novo censo busca consumidores das quatro identidades específicas, inclusive recursos com nomes não relacionados e referências JVM aos campos do registry. Não confundir o mesmo classfile, ou até o mesmo Code SHA de duas factories, com identidade de item compartilhada.

| Item | Fieldref | Factory |
|---|---|---|
| [Charred Remnant](items/charred-remnant.md) | CHARRED_REMNANT | lambda$static$74 |
| [Fissile Core](items/fissile-core.md) | FISSILE_CORE | lambda$static$73 |
| [Uranium](items/uranium.md) | URANIUM | lambda$static$58 |
| [Uranium Shard](items/uranium-shard.md) | URANIUM_SHARD | lambda$static$59 |

Os nomes e factories são comprovados no [registro certificado](systems/item-registry.md). A exposição por chamada, guardas, Hazmat e efeito Irradiated já foram documentados individualmente; não repetir certificação do dispatcher, status ou dano. A lacuna é a ligação causal de usos distintos de cada identidade (incluindo receitas, loot, tags e código).

## Método reprodutível

[Auditor](../../../../docs/qa/alexscaves_1010_radioactive_consumer_census.py) usa o leitor de classfiles e o disassembler existentes. Verifica o JAR SHA-exato, 1.555 classfiles, hash do roster, identidade de cada classe, quatro factories e dois classfiles previamente selados; busca Fieldrefs exatos por owner/nome, localiza instruções e registra offset, descriptor, Code SHA e janelas delimitadas. Exige os quatro writes do inicializador. A leitura de todos os JSONs de data/ coleta caminhos de chave/valor de IDs completos. Tags de item são tratadas por fecho transitivo, inclusive ciclos e entradas opcionais; referências a tags são potenciais, não provas de seleção efetiva. Tags de bloco não são promovidas a tags de item. Recursos sem menção literal ou relação de tag conhecida, lookup dinâmico, datapacks externos, scripts, dependências e registries transformados não estão fechados pelo censo.

[Workflow](../../../../.github/workflows/alexscaves-1010-radioactive-consumer-census.yml): compilação, seis checks sintéticos de identidade e travessia, download publisher, duas execuções, comparação byte a byte, SHA-256 e relatório. Resultado ainda NÃO OBSERVADO; não há selo novo até releitura dos logs e reconciliação individual. O censo não é prova da aceitação do efeito, custo, física, comportamento dos consumidores transitivos, compatibilidade ou hook mutador.

## Próximo gate

Classificar os callsites e JSONs por identidade após a CI; fechar consumidores pertinentes e limites de engine/settlement, vincular resultados às quatro fichas e só então avaliar promoção individual com manifesto. Não alterar índices, contagem, Stage ou raízes nesta fase de coleta. Sem novo cast, sem Mastery por tentativa de radiação. `NO_MUTATION / fail-closed`.
