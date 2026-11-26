# Alex's Caves Continued — radioactive block suppliers and exact resource attribution

**Escopo parcial, NO_MUTATION / NOT_CERTIFIED / NOT_TESTED.** Base main cef700523ac1e81476851d62966146fa22ec0c24, modlist sibling 18144e8318978b8904b584b80b4ddd630f22f8f0, #019 Alex's Caves Continued 1.0.10 e #001 NeoForge 21.1.250. Publisher SHA-256 36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c32e9f2e95bffae0e7c, 75.279.314 bytes; sem novo dump físico instalado.

## Evidência já aproveitada nas quatro fichas

- [Block Of Uranium](items/block-of-uranium.md): compressão e descompressão 9:1, loot, tags distintas.
- [Radrock Uranium Ore](items/radrock-uranium-ore.md): Silk Touch, Fortune, smelting/blasting, worldgen declarativo.
- [Unrefined Waste](items/unrefined-waste.md): receitas de transformação e custo distinto de exposição.
- [Waste Drum](items/waste-drum.md): fronteira oficial de destruição, nuvem e persistência; modelo float32 reproduzido localmente com struct.pack/unpack (2F e -2F/12000; 9001 reduções até <0.5F). Não implica execução no jogo.

Evidência: [replay suplementar](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45793839880/job/139819307102) e [prova nativa](EXACT-RADIOACTIVE-ITEMS-1.0.10.md), [engine](EXACT-DESTROYED-ITEM-ENGINE-REFERENCE-21.1.250.json), [nuvem](EXACT-FOUR-ITEMS-DOWNSTREAM-21.1.250.md), [geometria](EXACT-INK-BOMB-IMPACT-21.1.250.md). Não transportar as propriedades do bloco colocado por analogia.

## Gate adicional

[Sonda](../../../../docs/qa/alexscaves_1010_block_resource_attribution_probe.py) valida o classfile do registry e os cinco offsets por identidade já comprovados. Resolve os handles dos quatro suppliers reais (não adivinha classes pelo ID), projeta propriedades de item, factory e owners nativos alcançados, classifica declarações sem Code e corpos deferred, e percorre o roster para localizar referências aos quatro campos de bloco. A seguir, atribui caminhos de JSON por ID completo dos quatro blocos e seis itens de alimento/essência; distingue IDs literais (contexto de registry obrigatório) de referências potenciais a tags de item ou bloco, inclusive ciclos e entradas opcionais. Não confundir nome igual em item/block/worldgen. Não afirmar completude de consumidores dinâmicos, reflexão, scripts, datapacks externos ou execução transformada.

[Workflow](../../../../.github/workflows/alexscaves-1010-block-resource-attribution.yml) compila, roda seis checks sintéticos, verifica SHA-exato e exige dois relatórios idênticos. Primeira execução e interpretação pendentes; sem promover ledger. Próxima decisão por identidade depende do resultado, não do sucesso do parser isolado. Não são novos casts, hooks ou QA física.

## RED e correção

Run [45896635692](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45896635692), job 140172036133: compilação e checks iniciais passaram, mas a extração real falhou com KeyError new_sites. A função projection usa type_operands com opcode new e owner resolvido, não new_sites. Corrigido o consumidor desse schema e acrescentada regressão sintética que distingue new de checkcast. O segundo workflow falhou independentemente com HTTP 429 na resolução de Gson 2.10.1 pelo Maven (job 140173897484); não alterar dependências ou gates. A nova CI deve provar GREEN. Base reconciliada 9e206b0c00e7da34642f90db1cb37f1a8f8792dd. Nenhuma promoção de contrato.
