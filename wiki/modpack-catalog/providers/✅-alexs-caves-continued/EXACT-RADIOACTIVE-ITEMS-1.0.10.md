# RadioactiveBlockItem, RadioactiveItem e RadioactiveOnDestroyedBlockItem — descoberta 1.0.10

**DISCOVERY_ONLY / NO_MUTATION / NOT_CERTIFIED / NOT_TESTED.** Base `9eeb5db432e5c9c552e8866214d34ec9fd20da73`, modlist sibling #19, publisher `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`, 75.279.314 bytes. Coleta nova pendente; sem novo dump físico. 59/81 classes com disposição registrada na main; as três novas ainda não alteram contadores.

## Identidades diretas já comprovadas pelo registro

| ID | Factory | Code SHA-256 |
|---|---|---|
| `alexscaves:charred_remnant` | `ACItemRegistry.lambda$static$74` | `a8f68e374288c6495c5ab854c9c17cd777cc30b4be5e4e71a31e41531873d736` |
| `alexscaves:fissile_core` | `ACItemRegistry.lambda$static$73` | `97c2de487a982e04941e1183de8616b31f8ca5d1b29a6fd9a009ac03cbe85d20` |
| `alexscaves:uranium` | `ACItemRegistry.lambda$static$58` | `1e1c9e0dfea75205c2e2c0d0be0a2bf12982fc02d8ad825bb6b1dfd62e883a0f` |
| `alexscaves:uranium_shard` | `ACItemRegistry.lambda$static$59` | `1e1c9e0dfea75205c2e2c0d0be0a2bf12982fc02d8ad825bb6b1dfd62e883a0f` |

[Registro de itens](systems/item-registry.md). Todos instanciam RadioactiveItem. Uranium e Uranium Shard possuem Code SHA igual; isso não prova equivalência de identidades ou todos os dados downstream. RadioactiveBlockItem e RadioactiveOnDestroyedBlockItem requerem levantamento de registros de blocos e seus suppliers; não inferir IDs a partir do nome da classe nem tomar as quatro factories acima como universo completo.

## Reuso de evidência estática, sem novos certificados

[Irradiated](effects/irradiated.md), [dano Radiation](damage-types/radiation.md) e [manifesto de efeitos](EXACT-EFFECT-CONTRACTS-1.0.10.md) documentam: acInventoryTick de RadioactiveItem / RadioactiveBlockItem, sem lado cliente, portador vivo, jogador não criativo e sem status; probabilidade por chamada nominal count×randomChanceOfRadiation×(1−hazmat/4F), aplicação 1800 ticks amp0. Isso não determina constantes por factory, frequência efetiva de dispatch, clipping de probabilidade, resistência ou sucesso da aplicação. Em RadioactiveOnDestroyedBlockItem.onDestroyed, evidência anterior de instância 9600 ticks amp1, raio 2F e duração de nuvem 12000 ticks; ainda falta fechar gates, comportamento da nuvem, atribuição e alteração de mundo individual. Não confundir amp0 com tick de dano periódico: o efeito próprio shouldTick retorna false para amp<=0, mas presença continua afetando consumidores de cura. Sem novo cast, nenhum aumento artificial de dano ou remoção de proteção Hazmat.

## Nova investigação

[Auditor](../../../../docs/qa/alexscaves_1010_radioactive_items_probe.py) fixa hash/tamanho/roster do publisher e quatro factories já seladas; projeta todos os métodos próprios das três classes, candidatos por referências tipadas e janelas de construção de entidade/item, bootstrap handles que apontam para produtores encontrados no mesmo owner, recursos JSON filtrados por filename. Os candidatos e janelas são **pistas**, não prova completa do fluxo de ID no registry; conferir helpers indiretos, parâmetros de construtor e consumers antes de qualquer ficha certificada. Verificar comportamento por item, stack/custo, probabilidades, radiação, lifecycle de item destruído, nuvem, owner, proteção, persistência, gates server-side, loot/receitas, integração e testes. [Workflow](../../../../.github/workflows/alexscaves-1010-radioactive-items.yml) exige dois replays idênticos. Nenhuma nova ficha ou certificado nesta proposta. Próximo: reconciliar RainbounceBootsItem, RaygunItem, RemoteDetonatorItem e ResistorShieldItem sem duplicação antes de SackOfSatingItem.

NO_MUTATION / FAIL_CLOSED / PHYSICAL_QA_NOT_TESTED. Sem Stage promotion.
