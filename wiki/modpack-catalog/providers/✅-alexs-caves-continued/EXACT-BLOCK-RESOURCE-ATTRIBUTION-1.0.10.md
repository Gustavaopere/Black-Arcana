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

## GREEN, atribuição por identidade e decisão individual

Run [45903382213](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45903382213), job 140194260474: sete checks, dois relatórios byte-idênticos (227057 bytes, SHA-256 `9708b284726f23dded9e4ad5268296f5ae437bd7aa115ea1bf62e7bc0abdd7a2`), seis owners nativos, 31 métodos projetados, nenhum deferred, 23 sites de referência de campo, 1563 JSONs examinados, 50 arquivos de recursos com 65 ocorrências atribuídas. O [selo por identidade](EXACT-BLOCK-RESOURCE-ATTRIBUTION-SEAL-1.0.10.json) registra as dez fichas sem confundir registries. Referências alimentares vêm do relatório nativo SHA-256 `6c8e0c98af51b60fe40d3bd0b326fb909525f1780b2086740748e158b6bd20ea` (765144 bytes; [run 45796533259](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45796533259), job 139828495853), com replay final obrigatório. A fronteira vanilla de saúde é [job 139828496659](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45796533259/job/139828496659); pipeline distribuído de alimentação: [job 138746986320](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45793839880/job/138746986320) (SHA-256 `ac206f62678acd71876df7df3321eb16ee51832a15325515bf23db71bc566464`).

**Candidatos a certificado individual (sete eixos):** Green Soylent e Slam. Classe RadiationRemovingFoodItem, seis métodos, `finishUsingItem` SHA-256 `550d0a5d6b4b79d401fbde187bc6e83f1467035d88784d44135bce79f6d9ec50`. Cura condicional do consumidor irradiado: `min(maxHealth, health + ceil(1.5F * nutrition + 1))`; Green Soylent +6 HP (nutrição 3), Slam +7 HP (nutrição 4). Slam também declara Strength 400 ticks, amp 0, probabilidade 1. Não remove Irradiated. Native override usa setHealth antes do finish herdado, sem guarda explícita de lado. A autorização do evento Finish não deve ser presumida antes da chamada; não duplicar cura, consumo, custo ou Mastery. Não certifica aceitação física, hook mutador ou dano vanilla de Strength. Custos herdados do pipeline de alimentação, não há débito independente de mana/durabilidade/cooldown.

**Oito fichas continuam parciais:** os quatro blocos (consumidores e fronteiras de colocação/queda/destruição), Spelunkie, Jelly Bean e as duas essências (consumidores específicos e proveniência). Unrefined Waste em contato com LivingEntity fora da tag de resistência reduz vx/vz por fator 0.9, preserva vy e solicita Irradiated 4000 ticks amp 0; não transportar para o item carregado. Radrock tem XP condicionado ao Silk Touch e nenhuma aura de contato no owner projetado; Waste Drum diferencia bloco colocado de destruição de item. Zero ocorrências literais de Licowitch Radiant Essence no recorte JSON não significa ausência de uso ritual. Provider OPEN. NO_MUTATION. QA física NOT_TESTED.

O ledger candidato avança de 142 a 144 contratos em 184 fichas observadas (40 restantes), sem declarar universo integral. Validação final deve reproduzir ambos os relatórios e o selo de recursos/consumidores.
