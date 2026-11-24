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

Os métodos de barter encontrados por nome são candidatos de descoberta; corpos maiores que 180 instruções ficam com janelas de sites e hash, sem inferência de fluxo integral. O relatório não comprova dispatch efetivo, handlers externos, referências dinâmicas ou interpretação de loot pela engine. CI exige replay idêntico e publica o relatório. Primeiro resultado e selo ainda pendentes.

**Estado:** `static_contract=NOT_CERTIFIED; mutating_hook=NOT_VERIFIED; physical_qa=NOT_TESTED; NO_MUTATION`. Não promover Glow Ink Bomb por equivalência da classe. Nenhum delta de raízes.
