# RadioactiveBlockItem, RadioactiveItem e RadioactiveOnDestroyedBlockItem — descoberta 1.0.10

**DISCOVERY_ONLY / NO_MUTATION / NOT_CERTIFIED / NOT_TESTED.** Base `9eeb5db432e5c9c552e8866214d34ec9fd20da73`, modlist sibling #19, publisher `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`, 75.279.314 bytes. Coleta binária comprovada abaixo; sem novo dump físico. 59/81 classes com disposição registrada na main; as três novas ainda não alteram contadores.

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

[Auditor](../../../../docs/qa/alexscaves_1010_radioactive_items_probe.py) fixa hash/tamanho/roster do publisher e quatro factories já seladas; projeta todos os métodos próprios das três classes, candidatos por referências tipadas e janelas de construção de entidade/item, bootstrap handles que apontam para produtores encontrados no mesmo owner, recursos JSON filtrados por filename. Os candidatos e janelas são **pistas**, não prova completa do fluxo de ID no registry; conferir helpers indiretos, parâmetros de construtor e consumers antes de qualquer ficha certificada. Verificar comportamento por item, stack/custo, probabilidades, radiação, lifecycle de item destruído, nuvem, owner, proteção, persistência, gates server-side, loot/receitas, integração e testes. [Workflow](../../../../.github/workflows/alexscaves-1010-radioactive-items.yml) exige dois replays idênticos. Quatro fichas parciais nesta proposta, sem novo certificado. Próximo: reconciliar RainbounceBootsItem, RaygunItem, RemoteDetonatorItem e ResistorShieldItem sem duplicação antes de SackOfSatingItem.

NO_MUTATION / FAIL_CLOSED / PHYSICAL_QA_NOT_TESTED. Sem Stage promotion.

## Resultado observado

[Run 45750603107/job 139677193397](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45750603107/job/139677193397), HEAD `afb4f82f63f94391648bf53803b1a297e6540dcb`: 42/42 workflows; oito checks da sonda, 10 declarações (6 próprias + 4 factories), 5 owners tipados, 6 construtores candidatos, 2 métodos com bootstrap windows (6 sites), 88 JSONs. Dois relatórios byte-idênticos 232.851 bytes SHA-256 `b8fd8880d0f888ee137a436ec0aa81ea7916c6e6883acc0237d2915525499c97`, selados na nova HEAD. RadioactiveItem class SHA `6a46aa885ce5e5728c22691033b0a0f892d69f6c6fa7dd86a96c8f33c81d9436`; RadioactiveBlockItem `1c769a4b64f0e4b3b9a2f5589bfc44ce3e27ec46c616b447d4e1359ffb21bd4b`; RadioactiveOnDestroyedBlockItem `853e1f6318cfaa2c97ab27955e6b068e4e5f34ab94f4354092233e69bc502f24`. Os dois acInventoryTick compartilham Code SHA `a98c07b15db89b72116500877e23e3f95db45ec8223dfeaa00fb76980bacc47d`. Construtor armazena rate; addEffect retorno ignorado e mensagem visual posterior; boolean de seleção não lido.

- [Charred Remnant](items/charred-remnant.md)
- [Fissile Core](items/fissile-core.md)
- [Uranium](items/uranium.md)
- [Uranium Shard](items/uranium-shard.md)

## Itens de bloco: limite da identidade

ACBlockRegistry.lambda$getBlockSupplier$440(Supplier)BlockItemWithSupplier (Code SHA `97cdb48022a1d0e97196956a30d852cc346aad92de1c88cc8f6590109bfd71f3`) cria RadioactiveBlockItem com rate 0.001F; bootstrap @81. $441, Code SHA `6659fa766f94d238df90308e900913b9bb93b1edc19ea32f34b4f3a90b6e425f`, cria RadioactiveOnDestroyedBlockItem com rate 0.01F; bootstrap @88. Ainda não há vínculo causal com IDs de bloco específicos. Recursos JSON com uranium/nuclear não bastam. A classe destruída herda RadioactiveBlockItem, onDestroyed Code SHA `34f73b931946ae63544f4cbe9e35d1bd10fcab90f25b000bbdc54b98bc8b8881` (82 instruções). Super @3; retorna se dano de jogador criativo ou ItemEntity já removida (@10/@17); discard @21; cria AreaEffectCloud na posição do item, sem owner setado no corpo, GAMMAROACH, cor 7853582, IRRADIATED 9600 ticks amp1, raio2F, duration12000, waitTime0, radiusPerTick=−radius/duration float; addFreshEntity @135 retorno ignorado, depois pedido de explosão BLOCK @165 (sem guard explícito de lado, claims, owner ou aceite de spawn). Parâmetros da explosão e downstream serão detalhados na ficha por identidade; não interpretar raio da nuvem como raio de destruição. Nenhum hook mutador nem QA.

[Coleta suplementar](../../../../docs/qa/alexscaves_1010_radioactive_block_bindings_probe.py) projeta seletor, braços de switch, helpers e janelas de candidatos de binding. Replays separados; resultado ainda pendente. 60/81 classes com disposição mapeada ou anteriormente documentada, mais duas classes de bloco analisadas sem vínculo de ID. 137/164 fichas estáticas propostas, 27 parciais. Não fechar universo.

## RED e correção da sonda suplementar

Run 45793236357/job 139817275195: os dois replays originais reproduziram SHA b8fd8880... e 232851 bytes; a sonda suplementar compilou, mas falhou com `AuditError: selector heading`. Causa: escapes duplicados nas regex Python raw. Corrigidos escapes do cabeçalho, braços de switch e referências de método; quatro checks sintéticos de regressão, exigência de braços do switch e janelas do inicializador ampliadas para até 600 candidatos (não dispensam vínculo causal). A nova CI deve confirmar o GREEN. Download direto no ambiente local indisponível por DNS; validação binária depende do workflow publisher. Sem mudança de contrato ou contagem.

## GREEN e quatro bindings de bloco comprovados

[Run 45793839880/job 139819307102](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45793839880/job/139819307102), HEAD `e992226c0d80b5d6393e0a99de49d185c406a807`: quatro regressões passaram e dois replays de bindings byte-idênticos, 1.106.955 bytes SHA-256 `52f90cc908f4e775a29711454c2a58a411dc491116020680d77eaf553a299709`. 249 janelas. ACBlockRegistry class SHA `b4de04f32f6e1d92eeda55480b8480f7ed69f3813164f330f49d0eced202e54c`, getBlockSupplier Code SHA `0491a61abf0d322efcd2b927a9d55591d5f25a2f094e9d386121b5ad3ed45b68`, helper registerBlockAndItem Code SHA `d1a0bd80dc6b33272d28f317f10161bc4fbacda2d8b41529fe2a53d82141f32c`. Switch 4->80->indy81->$440 e 5->87->indy88->$441. Helper registra bloco @5 e item com mesmo nome @18. Quatro literal-ID callsites do inicializador: radrock_uranium_ore selector 4 @2068; waste_drum selector 5 @2201; block_of_uranium selector 4 @2301; unrefined_waste selector 4 @2330. Nova HEAD sela tamanho/digest e adiciona assertions de roster de bindings sem modificar o relatório. Os parâmetros de bloco no mundo e engine permanecem fora do contrato parcial.

- [Radrock Uranium Ore](items/radrock-uranium-ore.md)
- [Waste Drum](items/waste-drum.md)
- [Block Of Uranium](items/block-of-uranium.md)
- [Unrefined Waste](items/unrefined-waste.md)

Estado candidato: oito fichas radioativas parciais, 137/168 observadas, 62/81 classes com disposição. Oito classes existentes adicionais e onze owners finais serão reconciliados na #1234; nenhum novo certificado. NO_MUTATION.
