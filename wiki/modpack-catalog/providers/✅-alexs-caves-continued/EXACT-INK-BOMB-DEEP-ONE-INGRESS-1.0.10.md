# Ink Bomb — produtores Deep One e ingresso de troca (1.0.10)

**DISCOVERY_ONLY / NO_MUTATION.** Publisher 1.0.10, 75.279.314 bytes, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. Complementa a auditoria de uso manual, dispenser e recursos de barter. Nenhuma promoção de ficha.

## Evidência já observada

[Run 45464509190 / job 138695690486](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45464509190/job/138695690486), relatório 645.624 bytes, SHA-256 `0ab600a51b26fd3da5e7360ad461deabf629f053817f1e210fe1e4a280821dac`. Logs SEMANTIC reexaminados nesta rodada. Os três produtores usam a assinatura `startDisappearBehavior(Player)Z`.

| Owner | Code SHA-256 | Comportamento observado |
|---|---|---|
| DeepOneBaseEntity | `b585ad2aa8be0ddfc83b205c8faed995ea2c61b4d17dbf3b0f0a050694beb232` | Cria InkBombEntity(Level, this) @9; usa posição/movimento do Player e posição/altura ocular do produtor; sqrt @83; shoot @109, argumento speed 0,5F + 0,2F × float do local 10, inaccuracy 12F. Som WITCH_THROW; addFreshEntity @164; addReputation(UUID,-1) @174; retorna true. Nenhuma guarda de resultado de spawn observada nesse corpo. |
| DeepOneEntity | `180097bf11ee7809d47d474a18706932e4f3f82d63ae91f1aaa2b9ff0557ebc7` | Se mão principal vazia, cria stack Ink Bomb @61; inicia ANIMATION_THROW se sem animação; quando THROW e tick >10, limpa mão se stack é Ink Bomb @134 e delega ao ancestral @139. |
| DeepOneKnightEntity | `1ab97b7f5a3bd3f84e3f0f4e0470d55af4c35cf4a4d76e94065478fab9bbd174` | Se mão principal não vazia, solicita swapItemsForAnimation @58. Na animação THROW com tick >10, se mão contém Ink Bomb, solicita restoreSwappedItem @125; delega ao ancestral @130. |

O efeito de reputação, as stacks criadas para animação e o spawn pertencem à AI nativa. Nenhuma dessas rotas chama diretamente o uso manual InkBombItem.use no corpo observado. Não deduzir custo para Player, consumo de item real, restituição transacional, autoria por Player ou Mastery por simples chamada. O target passado ao método não é necessariamente o atingido pela trajetória.

## Nova sonda

O probe `docs/qa/alexscaves_1010_ink_bomb_deep_one_ingress_probe.py` exige a identidade completa do JAR, 1.555 classfiles, hashes das três classes e dos três corpos conhecidos. Constrói a família de herança pelo próprio classfile e pesquisa Methodref/InterfaceMethodref de quatro assinaturas exatas (startDisappearBehavior, swapItemsForAnimation, restoreSwappedItem, addReputation), mais constantes String exatas de recursos de barter. Registra callsites por operandos CP, não por substring ou simples presença de nome.

Os métodos de barter encontrados por nome são candidatos de descoberta; corpos maiores que 180 instruções ficam com janelas de sites e hash, sem inferência de fluxo integral. O relatório não comprova dispatch efetivo, handlers externos, referências dinâmicas ou interpretação de loot pela engine. CI exige replay idêntico e publica o relatório. Primeira execução e replay confirmados: [run 45514153339 / job 138869143379](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45514153339/job/138869143379). 137.731 bytes, SHA-256 `5e6f799b338bea093af675e9d8a4864fb959baea9e977b9b4c2012f5a3cae854`, sete owners, 19 métodos distintos; três checks de escopo passaram. O workflow fixa tamanho e digest; CI deste novo head pendente.

**Estado:** `static_contract=NOT_CERTIFIED; mutating_hook=NOT_VERIFIED; physical_qa=NOT_TESTED; NO_MUTATION`. Não promover Glow Ink Bomb por equivalência da classe. Nenhum delta de raízes.

## Resultados do censo tipado

| Método | Evidência observada |
|---|---|
| DeepOneDisappearGoal.tick | Code SHA-256 `6ff8845ac0047b81a67bec6a50971b297957794dd08eeb31a551c469b62d0c66`; invokevirtual startDisappearBehavior @113, ifeq @116. |
| DeepOneBaseEntity.swapItemsForAnimation | `7314614ddfcf6668c993d823c5ade506ab9e000820d823edd7f9fd0de509285e`; copia mão não vazia para swappedItem @24 e escreve mão @32. |
| DeepOneBaseEntity.restoreSwappedItem | `f84d84dbe569f78607118ea97b17fa5364524fe1a5fad33fa014269e7a93ea58`; lê swappedItem @5 e escreve mão @8; sem liquidação de inventário de jogador. |
| DeepOneMageEntity.startDisappearBehavior | `bf6aabce697c6fd37ab27bb119238dd09da912b9bab985c880e6460defb3406c`; para navegação @31, usa ANIMATION_DISAPPEAR; tick >50, evento 67 e remove DISCARDED; rota alternativa evento 66 e false. Sem chamada de InkBombEntity nesse corpo. |
| DeepOneBaseEntity.generateBarterLoot | `d3df12394c1f7c4a7f78109c323ba56c1616f02aa2f329dbcb33deb941b09022`; resolve lootTable @11, THIS_ENTITY @30, PIGLIN_BARTER @37 e getRandomItems @43. |
| DeepOneBaseEntity.addReputation | `bfbeb912b8e779e957549f01b5cc2e0eeec04a182ce445f5137ab2b0a1b3fc1f`; compara reação antes/depois, setReputationOf @19, triggers NEUTRAL/HELPFUL e mensagem ao jogador resolvido; não é XP ou Mastery. |

Os inicializadores de DeepOneEntity, Knight e Mage têm literais exatos gameplay/deep_one_barter, gameplay/deep_one_knight_barter e gameplay/deep_one_mage_barter @48, respectivamente; getters retornam BARTER_LOOT. Censo adicional: AbyssalAltarBlockEntity.tick @318 swapItemsForAnimation e @368 addReputation; DeepOneBaseEntity.tick @713 restoreSwappedItem; hurt @75 addReputation; MagicConchItem.releaseUsing @415 addReputation. Essas janelas não provam as condições integrais dos chamadores. Não transferir comportamento de barter para lançamento, nem atribuir ao Mage a rota da bomba. Nenhum certificado, hook mutador ou QA física novo.
