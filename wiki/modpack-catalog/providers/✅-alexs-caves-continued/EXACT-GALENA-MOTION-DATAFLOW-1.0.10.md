# Galena Gauntlet — definições locais de destino e velocidade (1.0.10)

**DISCOVERY_ONLY / NO_MUTATION.** Publisher 1.0.10, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c32e9f2e95bffae0e7c`, 75.279.314 bytes; NeoForge 21.1.250 na modlist, MC 1.21.1, Java 21.

O [dossiê de movimento](EXACT-GALENA-MOVEMENT-1.0.10.md) selou fórmulas de directMovementTowards e mão do controller, mas deixou aberta a origem dos argumentos de destino e velocidade na chamada @1551 de tick. A nova sonda `docs/qa/alexscaves_1010_galena_motion_dataflow_probe.py` fixa o mesmo classfile, 744 instruções, instruction SHA `3478b6038fe3dad88fd11a2b7aeca49fc85a9ccadc1ad4e9fca089b423b8e9bc`, Code SHA `eaf08e761f108f4e5f15816ca7f72807c068e51376ec9ed27588d65a6385a699` e exige tabela de exceções vazia. Modela arestas normais de CFG e união de definições alcançáveis dos slots 5/6, incluindo sobrescrita por valores de dois slots e exclusão de código não alcançável. Exige que @1547/@1549 sejam os reads esperados e @1551 seja directMovementTowards. Não prova viabilidade semântica de cada condição nem valor efetivo do target. Cinco checks sintéticos e replay determinístico; primeiro resultado reproduzido abaixo.

Sem alteração de runtime, ficha concorrente, certificado, QA ou raiz semântica.

## Resultado reproduzido

[Run 45535078520, job 138939581922](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45535078520/job/138939581922), HEAD `eb66f5946fd358c7914ffde62bc836de51445415`: cinco checks sintéticos, 744 instruções pinadas, 82 sites de branches normais, tabela de exceções vazia. Duas saídas idênticas de **92.039 bytes**, SHA-256 `1a7bcfba2c077eaf9d84fd624a34ef8c5c2f11c60f3ee5d0451a0e01f1b046f1`. O workflow fixa tamanho/digest; replay final obrigatório. Os testes sintéticos não constituem red-green observado nem QA de Minecraft.

| Local lido na chamada final | Todas as escritas observadas | Definições alcançáveis |
|---|---|---|
| 5, aload @1547 | @220 astore, @280 istore, @484 astore null, @713, @826, @926, @1481 astore | @713, @826, @926, @1481 |
| 6, fload @1549 | @298 astore, @535 fstore, @718 fstore | @535, @718 |

A reutilização de slots no ramo Teletor não contamina a chamada de movimento do ramo Player; nenhuma definição não inicializada alcança os dois reads pelo CFG normal. A guarda @1541–1543 testa destino não nulo. A análise é may-reaching (união, não prova viabilidade de todos os caminhos), e o grafo fixado permite reconciliar as atribuições e os ramos abaixo.

| Ramo do Player | Destino q em coordenadas mundiais | Escalar float s |
|---|---|---|
| EntityHitResult e playerUseCooldown==0 | target.position + (0,0.5F×target.getBbHeight(),0) @695–713 | 0.2F @715–718 |
| Rota alternativa à seleção de entidade | player.getEyePosition + player.getViewVector(1F)×(R−20F) @804–826; R=30+5×nível de Field Extension quando o gate da stack passa | 0.1F @533–535 |
| Rota de BlockHitResult alcançada, bloco não air | HitResult.getLocation @923–926; distinta da seleção de BlockPos para mineração, cujo gate usa distância²<2.25D @886–901 | 0.1F; não há nova escrita no slot 6 neste ramo |
| Owner Player não usando a Gauntlet | player.position+(0,1,0) @1472–1481; retorno/solicitação de inventário em distância<1.4D, sujeito aos demais gates @1493–1537 | 0.1F |

O ramo Teletor chama directMovementTowards separadamente em @415 com s=0.1F; não extrapolar ataque ou custo do player ao Teletor. A fórmula anterior de impulso é v+q_normalizado_condicional×s, seguida do movimento e amortecimento; s não é velocidade fixa nem alcance. A seleção de bloco e o destino de movimento são decisões distintas; não confundir distância ao centro do bloco de mineração com raio de dano. Nenhum novo resultado de world-write, hook, certificado ou QA. `NO_MUTATION`.
