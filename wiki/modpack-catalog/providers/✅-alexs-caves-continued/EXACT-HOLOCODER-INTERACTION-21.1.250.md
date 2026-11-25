# Holocoder — ingresso de interação, blocos e liquidação de inventário (21.1.250)

**DISCOVERY_ONLY / NO_MUTATION.** Publisher Alex's Caves 1.0.10, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c32e9f2e95bffae0e7c`, 75.279.314 bytes; NeoForge 21.1.250, Minecraft 1.21.1, Java 21. Modlist #001/#019. Sem runtime transformado.

Reusa [ingresso publisher](EXACT-HOLOCODER-INGRESS-1.0.10.md), [representação recursiva](EXACT-HOLOCODER-ENTITY-LOAD-21.1.250.md) e [downstream](EXACT-FOUR-ITEMS-DOWNSTREAM-21.1.250.md). Captura chama addItem/drop após shrink, sem guarda explícita local de lado; ramo de consumo do projetor tem outra fronteira. O listener publisher e as classes de representação não comprovam o caminho de packet ou a liquidação do inventário.

A sonda `docs/qa/alexscaves_1010_holocoder_interaction_250_probe.py` fixa quatro classes e três Code hashes prévios, pins de distribuição, seleção delimitada do ingresso server de entidade/bloco, dispatch e eventos, Player/Inventory/ItemStack/ItemEntity e callbacks publisher. Nomes candidatos são filtros a confirmar no JAR, não APIs presumidas. Nested classes de packets e listener são descobertas da distribuição, com seleção de métodos por declarações. Duas saídas idênticas obrigatórias. Primeiro resultado pendente. Não afirma autorização efetiva de player, conservação da stack, proteção dos dados ou aceitação física.

Ficha Holocoder permanece parcial; nenhum novo certificado, hook ou raiz.
