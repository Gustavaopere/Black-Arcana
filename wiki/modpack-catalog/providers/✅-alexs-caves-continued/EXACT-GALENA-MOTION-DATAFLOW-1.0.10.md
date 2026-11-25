# Galena Gauntlet — definições locais de destino e velocidade (1.0.10)

**DISCOVERY_ONLY / NO_MUTATION.** Publisher 1.0.10, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c32e9f2e95bffae0e7c`, 75.279.314 bytes; NeoForge 21.1.250 na modlist, MC 1.21.1, Java 21.

O [dossiê de movimento](EXACT-GALENA-MOVEMENT-1.0.10.md) selou fórmulas de directMovementTowards e mão do controller, mas deixou aberta a origem dos argumentos de destino e velocidade na chamada @1551 de tick. A nova sonda `docs/qa/alexscaves_1010_galena_motion_dataflow_probe.py` fixa o mesmo classfile, 744 instruções, instruction SHA `3478b6038fe3dad88fd11a2b7aeca49fc85a9ccadc1ad4e9fca089b423b8e9bc`, Code SHA `eaf08e761f108f4e5f15816ca7f72807c068e51376ec9ed27588d65a6385a699` e exige tabela de exceções vazia. Modela arestas normais de CFG e união de definições alcançáveis dos slots 5/6, incluindo sobrescrita por valores de dois slots e exclusão de código não alcançável. Exige que @1547/@1549 sejam os reads esperados e @1551 seja directMovementTowards. Não prova viabilidade semântica de cada condição nem valor efetivo do target. Cinco checks sintéticos e replay determinístico; primeiro resultado pendente.

Sem alteração de runtime, ficha concorrente, certificado, QA ou raiz semântica.
