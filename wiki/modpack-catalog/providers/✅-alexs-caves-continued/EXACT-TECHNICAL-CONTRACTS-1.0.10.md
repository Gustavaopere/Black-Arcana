# Alex's Caves Continued 1.0.10 — contratos técnicos estáticos das oito ações

```text
claim_scope=STATIC_TECHNICAL_CATALOG_ONLY
evidence_grade=SHA_EXACT_BINARY_BEHAVIOR
version=1.0.10
artifact_sha1=6960b299a39a039ac8a5eb9b07be4ad0e3e0a570
artifact_sha256=36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c
artifact_size_bytes=75279314
semantic_magic_roots=8
provider_universe_closed=false
mutating_hook=NOT_VERIFIED
physical_qa=NOT_TESTED
```

## Escopo e autoridades

A revisão fecha os sete campos estáticos das **oito ações sobrenaturais já identificadas**, usando as classes e os dados do JAR **1.0.10**. Não acrescenta raízes semânticas. A [enumeração de identidades anterior](EXACT-1.0.10-ARTIFACT-AUDIT.md) continua válida; o contrato agora inclui os parâmetros e seus consumidores, além dos limites de persistência, autoridade e integração.

Artefato oficial: [CurseForge projeto 1645389, arquivo 8856293](https://www.curseforge.com/minecraft/mc-mods/alexs-caves-continued/files/8856293), [download](https://edge.forgecdn.net/files/8856/293/alexscaves-1.0.10-neoforge%2B1.21.1.jar). Os hashes acima foram recalculados sobre os 75.279.314 bytes. A identidade coincide com o fingerprint físico registrado no catálogo; isso não comprova execução do mod no pack nesta auditoria.

O arquivo contém **8.898 entradas ZIP**, sendo **8.464 arquivos e 434 diretórios**. Há **1.555 classfiles Java 21 (major 65)** e 6.909 arquivos que não são classes. O contador histórico de 7.343 entradas não-class também inclui os diretórios. Há 1.573 caminhos sob `data/alexscaves/`, incluindo diretórios. São medidas de inventário, não quantidades de habilidades.

O [manifesto dos contratos](EXACT-TECHNICAL-CONTRACTS-1.0.10.json) sela as oito fichas, os classfiles e os recursos examinados. Os métodos são identificados pelo owner, nome e descriptor JVM; suas âncoras retêm somente offsets e instruções/referências delimitadas. O manifesto não redistribui JAR, classes, assets ou implementações completas.

## Diferença entre fonte e release

A fonte anteriormente citada, [`523308608422ab8e31974befa7111ecdf495dd37`](https://github.com/Codx-org/AlexsCavesContinued/blob/523308608422ab8e31974befa7111ecdf495dd37/stonecutter.properties.toml#L12-L18), declara **`mod.version = "1.1.1"`**. O commit pai [`233b7a635bf001f94e7e86675ef184421d630dbf`](https://github.com/Codx-org/AlexsCavesContinued/blob/233b7a635bf001f94e7e86675ef184421d630dbf/stonecutter.properties.toml#L12-L18) declara **1.1.0**. A mensagem de commit que menciona várias releases não constitui um pin 1.0.10.

A árvore também usa Stonecutter e ramos condicionais de versão/loader. Portanto, nem a declaração da versão nem um método aparente dessa árvore permitem transferir seus parâmetros para o JAR instalado. Nesta entrega, a fonte 1.1.1 é **corroboração adjacente**; a autoridade dos valores e relações certificados é o bytecode/dado 1.0.10 indicado nas fichas. Não se afirma compilação reproduzível, equivalência integral entre source e binário ou um pin de fonte 1.0.10 que não foi comprovado.

## Sete campos por ação

| Ação | Ficha | Contratos documentados |
|---|---|---|
| Water Bolt | [Sea Staff](actions/sea-staff-water-bolt.md) | Dano, seleção e homing, colisão, cooldown, custo, owner e duração |
| Peppermint Cast | [Sugar Staff](actions/sugar-staff-peppermint-cast.md) | Quantidade, órbita/velocidade, targeting, dano, duração, save/load |
| Hex Cast | [Sugar Staff Hex](actions/sugar-staff-hex-cast.md) | Posição/escala, AABB versus alcance, dano, tempo e restauração de owner |
| Summon Deep Ones | [Magic Conch](actions/magic-conch-summon-deep-ones.md) | Carga, custos, número/tipos de summons, duração, ownership e cleanup |
| Possession | [Totem](actions/totem-possession-remote-control.md) | Binding, geometria de olhar, navegação/velocidade, ataque, desgaste e rede |
| Remote Observation | [Beholder](actions/occult-gem-beholder-observation.md) | Binding, pacote, autorização, distância, tickets de chunks e encerramento |
| Darkness Incarnate | [Cloak](actions/cloak-darkness-incarnate.md) | Charge, tecla, duração, voo, gates de ambiente e remoção do efeito |
| Biome Conversion | [Crucible](actions/conversion-crucible-biome-conversion.md) | Seleção de bioma, ofertas, tempos, geometria quart, blocos, fila e persistência |

Cada ficha fornece identidade, comportamento, parâmetros, targeting, custos, fronteira de integração e validação. Tipos de dano, projétil, área, duração e seleção de alvo são especificados quando aplicáveis; uma ação de observação não recebe dano inventado e biome conversion não recebe alcance de cast de projétil.

## Fronteiras relevantes para perks

Um valor de renderer, tracking ou busca de advancement não é automaticamente uma hitbox ou raio de dano. O Totem tem caminhos diferentes para movimento, ataque e sincronização; `PossessionKeyMessage` não é seu pacote de comando. O Crucible usa largura 10 para a conversão e uma busca de jogadores a ±32 para advancements; essa busca não é seu raio de conversão. As fichas mantêm também as diferenças entre entidades em memória, owner salvo e campos efetivamente restaurados.

As expressões de `Math.min`, limites de `nextInt`, comparações float/double, continuações após `discard` e guardas de pacote são descritas literalmente nos métodos examinados. Consequências dependentes de execução, mixins, claims, dados ou ordem de eventos são hipóteses de QA. Nenhuma ocorrência de falha no modpack ou exploração de rede é declarada demonstrada.

A autoridade continua no provider: cast, custo, cooldown, spawn, controle, dano, tickets, voo e alteração de mundo não devem ser liquidados uma segunda vez pelo RPG Skill Tree/Black Arcana. Um método acessível ou setter não é homologação de hook mutador por jogador. Hooks continuam **NOT_VERIFIED**; QA física continua **NOT_TESTED**.

## Reprodução e alcance dos checks

Com JDK 21, `javap -p -c -s -classpath <jar> <owner>` reproduz os descriptors e offsets citados. O comando automatizado é:

```sh
python3 docs/qa/alexscaves_1010_action_contract_audit.py \
  --jar /caminho/alexscaves-1.0.10-neoforge+1.21.1.jar \
  --manifest 'wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-TECHNICAL-CONTRACTS-1.0.10.json' \
  --provider-root 'wiki/modpack-catalog/providers/✅-alexs-caves-continued' \
  --javap /caminho/jdk-21/bin/javap
```

A CI verifica identidade exata do artefato, hashes das fichas e membros, descriptors e âncoras selecionadas. Rejeita mudança de ficha, offset, opcode, recurso ou escopo sem atualização da evidência. O relatório exporta metadados delimitados. A interpretação causal dos sete campos é revisão técnica das fichas: a existência de uma âncora, isoladamente, não prova todo o comportamento descrito, runtime, paridade de source ou segurança de mutação.

## Catálogo das ações versus provider inteiro

O [índice de ações](actions/INDEX.md) pode exibir **8/8 contratos estáticos documentados**. O [índice do provider](INDEX.md) e a fila alfabética devem manter o universo integral aberto: há [famílias adicionais integráveis](PERK-INTEGRATION-SCOPE-1.0.10.md), como armas, armaduras, enchantments, efeitos e sistemas. O [inventário dessas famílias](INTEGRATION-SCOPE-INVENTORY-1.0.10.json) impede usar a exclusão semântica de uma arma como justificativa para ignorar suas perks.

Nenhum fechamento alfabético integral, Stage ou integração executável resulta desta certificação das oito ações. O trabalho continua em Alex's Caves Continued antes de avançar ao próximo provider.
