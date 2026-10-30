# Alex's Caves Continued 1.0.10 — escopo de integrações ainda aberto

Os recortes das oito ações mágicas e dos oito efeitos registrados têm contratos estáticos próprios. Eles **não cobrem todo o conteúdo integrável por perks** do mod. A classificação histórica `EXCLUDED` em [42 classes de interação](ITEM-ACTION-DISPOSITION-1.0.10.md) significa exclusão do denominador de magia, não exclusão do trabalho de integração.

Autoridade: JAR 1.0.10, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`, 75.279.314 bytes. O [inventário JSON](INTEGRATION-SCOPE-INVENTORY-1.0.10.json) enumera os nomes exatos abaixo a partir do artefato, sem importar os parâmetros da fonte 1.1.1. [Limites e reprodução](EXACT-TECHNICAL-CONTRACTS-1.0.10.md).

| Família | Universo exato identificado | Trabalho necessário antes de fechar o provider |
|---|---|---|
| Ações sobrenaturais | Oito raízes já contadas | Sete campos estáticos documentados nas oito fichas; hooks e QA física separados |
| Itens / equipamento | 81 classes externas de itens; 42 com assinaturas de interação já classificadas semanticamente | Individualizar os contratos relevantes de armas, movimento, comida, defesa, itens passivos e helpers; separar classes base de registros concretos |
| Enchantments | 51 JSONs em `data/alexscaves/enchantment/` | Ficha por contrato: nível/custo/slots/exclusividade e consumidor real de cada modifier, inclusive tecnologia/armas |
| Damage types | **11/11 JSONs e seis tags, 11 factories e 14 chamadas estáticas diretas em 12 classes; adicionalmente, offsets de escrita dos dois accessors sincronizados da Dark Arrow no Dreadbow** ([fichas](damage-types/INDEX.md), [manifesto de bytecode](damage-types/EXACT-CONSUMERS-1.0.10.json)); 0/11 contratos integrais de consumidores certificados | Factories e cinco métodos helpers selecionados auditados ([manifesto](damage-types/EXACT-DAMAGE-HELPERS-1.0.10.json)); ainda rastrear tags finais, origem dos dados sincronizados, restante do fluxo de dano, efeitos, proteções e settlement. Nenhum hook homologado |
| Mob effects | Oito campos de registro de efeitos | **8/8 contratos estáticos documentados**, incluindo aplicações e consumidores; [fichas](effects/INDEX.md) e [prova exata](EXACT-EFFECT-CONTRACTS-1.0.10.md). Hooks e QA física pendentes |
| Potions | 12 campos de registro de poções | Conteúdo, níveis/tempo e aquisição, sem contar variantes como novas magias |
| Config servidor | 40 campos em `ACServerConfig` | Defaults/bounds, momento de leitura, autoridade global/por jogador e consumidores; não presumir valores em execução |
| Config cliente | 15 campos em `ACClientConfig` | Distinguir HUD, luz, shader, som e câmera de comportamento servidor e atributos |
| Rede | 18 classes externas sob `server/message/`, incluindo transporte/helpers | Direção, registro/protocolo, autenticação, seleção de entidade, limites, autoridade e lifecycle |
| Mobs/montarias e eventos | Classes e interfaces inventariadas, sem denominador final de fichas | Atributos, dano, targeting, domesticação/reputação, medidores e skills de montaria; separar AI de raiz mágica do jogador |
| Mundo, dados e compatibilidade | Registries, block entities, tags, loot, crafting e mixins | Disposição explícita por consumidor ou suporte; aquisição, proteção e persistência não podem ser inferidas de assets |

Essas famílias se sobrepõem. Não somar 81+51+11 etc. como denominador final: um item pode ser owner de uma ação existente, uma classe base pode atender vários registros e um efeito pode ter vários consumidores. Os números descrevem superfícies identificadas, não novas fichas concluídas ou novos spells.

## Contratos não mágicos que não podem ser descartados

Dreadbow, spears, Ortholance, Desolate Dagger e Primitive Club oferecem combate e modifiers. Galena Gauntlet, Raygun, Quarry Smasher e Remote Detonator oferecem controle magnético, energia, mineração e explosivos. Candy Cane Hook, Floater e Submarine oferecem mobilidade. Armor passiva, comida e itens como Sack of Sating, Gazing Pearl e Holocoder também precisam de disposição de integração. Os nomes e assinaturas estão no inventário; ainda não constituem revisão completa de seus corpos.

As interfaces de montaria `FlyingMount`, `KeybindUsingMount` e `RidingMeterMount`, assim como `CommonEvents`, progresso de Cave Book e reputação Deep One, são candidatos a contratos de sistemas. Uma assinatura de API não é, sozinha, um hook seguro. A próxima catalogação deve documentar o consumidor, os parâmetros e os limites de autoridade antes de marcar essas superfícies completas.

## Estado dos índices

As oito ações e os oito efeitos certificados sustentam ✅ nos recortes de `actions/` e `effects/`. O provider inteiro permanece pendente, e o registro alfabético continua em **Alex's Caves Continued**. Um percentual 16/16 de fichas observadas não fecha o universo maior identificado aqui. Nenhuma família acima foi declarada inexistente por ainda não possuir ficha individual. A próxima família permanece dentro deste provider: enchantments e seus consumidores de armas/equipamentos, além dos demais sistemas ainda abertos.

## Dark Arrow — pontos de escrita observados

[Manifesto do estado sincronizado](damage-types/EXACT-DARK-ARROW-STATE-1.0.10.json): o JAR 1.0.10 confirma `SHADOW_ARROW_DAMAGE` e `PERFECT_SHOT` com defaults `0.0f`/`false`, setters em `DarkArrowEntity` e três invocações diretas em `DreadbowItem`. Não confundir essa superfície com API de perks estável; filtro de friendly fire, owner, múltiplos impactos, autoridade servidor/multiplayer e settlement estão pendentes. `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`.
