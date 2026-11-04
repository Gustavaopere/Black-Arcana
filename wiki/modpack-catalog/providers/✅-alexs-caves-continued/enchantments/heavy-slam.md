# Heavy Slam — `alexscaves:heavy_slam` (1.0.10)

**Contrato técnico estático:** ✅ `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`. **Hooks mutadores:** `NOT_VERIFIED`. **QA física:** `NOT_TESTED`. **Integração:** `NO_MUTATION`. O certificado cobre o encantamento e o consumidor delimitado do Resistor Shield; não certifica o escudo inteiro, os demais encantamentos ou o universo do provider.

## 1. Identidade e descrição do provider

- **Provider / versão:** Alex's Caves Continued / `alexscaves`, Minecraft 1.21.1, JAR `alexscaves-1.0.10-neoforge+1.21.1.jar`; CurseForge projeto `1645389`, arquivo `8856293`, **75.279.314 bytes**.
- **SHA-1 do JAR:** `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`; **SHA-256:** `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- **Recurso:** `data/alexscaves/enchantment/heavy_slam.json`; SHA-256 `927532341a9a53ac73c081f99d7f9b4703f9fa3245c1fdafb609dfdba7733c8a`; hashes de tag, classes e ficha no [manifesto consolidado](../EXACT-HEAVY-SLAM-CONTRACT-1.0.10.json). [Escopo e reprodução](../EXACT-HEAVY-SLAM-CONTRACT-1.0.10.md).
- **Descrição literal empacotada em `en_us.json`:** “Resistor Shield first slam attack deals additional damage”. Tradução explicativa: o primeiro golpe do Resistor Shield solicita dano adicional. O arquivo `pt_br.json` examinado não contém uma descrição própria de Heavy Slam.
- **Consumidor:** `com/github/alexmodguy/alexscaves/server/item/ResistorShieldItem.class`, SHA-256 `ffd3fddd74f8d44049886e9013de2e3d67cbd2a721015369175e8442c5044741`; método `onUseTick`, ABI `(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/item/ItemStack;I)V`.

A varredura dos 1.555 class entries por referências ao campo `HEAVY_SLAM` encontrou o registro `ACEnchantmentRegistry` e o consumidor `ResistorShieldItem`. Isso delimita referências diretas compiladas; não exclui reflexão, mixins e consumidores de outros mods. A fonte pública `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` declara **1.1.1** e é apenas corroboração adjacente, sem autoridade sobre estes parâmetros 1.0.10.

## 2. JSON, níveis e aquisição

| Campo | Valor literal do publisher | Significado delimitado |
|---|---|---|
| `description.translate` | `enchantment.alexscaves.heavy_slam` | Chave de tradução |
| `supported_items` | `#alexscaves:enchantable/resistor_shield` | Tag empacotada contém somente `alexscaves:resistor_shield` |
| `weight` | `10` | Peso publicado, não probabilidade medida |
| `max_level` | `3` | Limite declarado, sem clamp correspondente no leitor Java |
| `min_cost` | `base=1`, `per_level_above_first=6` | I/II/III: 1/7/13 pelo modelo publicado |
| `max_cost` | `base=41`, `per_level_above_first=10` | I/II/III: 41/51/61 pelo modelo publicado |
| `anvil_cost` | `1` | Custo de encantamento, não mana por pulso |
| `slots` | `mainhand`, `offhand` | Slots declarados do encantamento |

O JSON não declara `effects` nem `exclusive_set`; o comportamento de dano é implementado pelo consumidor Java. Ausência desses campos não prova compatibilidade universal com datapacks ou outros mods. O registro cria a ResourceKey `alexscaves:heavy_slam`; não se inventa uma escola ou DamageType Heavy Slam.

O ID consta diretamente nas tags publisher `minecraft:in_enchanting_table`, `minecraft:non_treasure`, `minecraft:on_random_loot` e `minecraft:tradeable`. São declarações de aquisição, sem prova de resolução final de tags, geração de loot, negócio ou obtenção em Survival. A receita shaped do escudo é `SSS` / ` H ` / `AAA`: três scarlet_neodymium_ingot, um heart_of_iron e três azure_neodymium_ingot; resultado resistor_shield com count omitido no JSON. Valores de aquisição não são despesas de uso da habilidade.

## 3. Ingresso, temporização e fórmula de dano

`ResistorShieldItem.use` obtém a stack na mão, solicita `startUsingItem(hand)`, inverte a polaridade quando Player está agachado, solicita som e retorna `ACCompat.useConsume`. Esse helper retorna `InteractionResultHolder.consume`, **sem shrink da stack**. Não há guarda própria de lado lógico nesse corpo; autoridade e chamada do callback são da engine.

`onUseTick` primeiro chama o método herdado de ShieldItem e calcula:

```text
t = getUseDuration(stack, null) - remainingUseTicks
slam = (10 <= t && t <= 12)
L = ACCompat.enchantLevel(stack, HEAVY_SLAM)
processar alvos somente se t >= 10 && t % 5 == 0
D = slam ? (float)(6 + 3 * L) : 2F
```

O consumidor herda a duração de uso; não a sobrescreve nem a transforma em lifetime de projétil. A progressão relevante é o valor `t` calculado pelo callback, **não** `UseTime` de animação. Os pulsos elegíveis são `10,15,20,…` enquanto o callback continuar. A janela `10..12` só intersecta essa cadência em **t=10**: não são três pulsos amplificados.

| Nível lido | Dano solicitado em t=10 | Pulsos posteriores elegíveis |
|---|---:|---:|
| 0 — sem Heavy Slam | 6 | 2 |
| I | 9 | 2 |
| II | 12 | 2 |
| III | 15 | 2 |

As operações `6+3×L` são inteiras antes da conversão para float (`@480–487`), sem clamp local. `ACCompat.enchantLevel` retorna o primeiro valor armazenado cujo Holder corresponde à chave, ou zero; não limita esse valor ao `max_level=3` do JSON. Dados não nativos podem sair da tabela acima. Heavy Slam não amplia por si só range, quantidade de pulsos, força de movimento, duração, hitbox ou tipo de dano.

## 4. Targeting, área, dano e movimento

A cada pulso elegível, consulta `LivingEntity` na **AABB do usuário expandida em `(5D,1D,5D)`** (`@379–405`). Depois exige:

1. `!usuário.isAlliedTo(candidato)` (`@435–441`);
2. `!candidato.equals(usuário)` (`@444–450`);
3. `candidato.distanceTo(usuário) <= 5F` (`@453–462`).

É a interseção de uma consulta por caixa e desse limite de distância, não uma esfera irrestrita, hitbox nova ou alcance frontal. Não há filtro próprio adicional de LOS, cone de visão, creative/spectator, vida ou aliança inversa nesse laço. Regras herdadas, imunidades e proteção PvP/claims não são automaticamente homologadas.

A fonte solicitada é **`usuário.damageSources().mobAttack(usuário)`** (`@468–472`), inclusive quando o usuário é Player. Não é um tipo de dano mágico, explosivo ou elétrico criado pelo encantamento. `LivingEntity.hurt(source,D) @492` devolve um booleano **descartado em `@495`**: o valor da tabela é dano solicitado antes de mitigação/recusa. A contagem de tentativas não é contagem de hits aceitos, kills ou procs de Mastery.

O processamento de movimento vem depois desse resultado descartado e conserva parâmetros próprios:

| Polaridade lida | Força passada a `ACCompat.knockback` | Dois componentes direcionais passados |
|---|---|---|
| Scarlet / true | `0.5D` no slam; `0.2D` nos demais pulsos | `targetX−userX`, `targetZ−userZ` (`@517–537`) |
| Azure / false | `0.5D` no slam; `0.2D` nos demais pulsos | **`userX−userX`**, `userZ−targetZ` (`@559–578`) |

O ramo Azure lê X do **usuário nas duas parcelas** (`@560` e `@564`), produzindo componente X zero. Não substituir editorialmente por `userX−targetX` nem prometer atração radial ideal. É uma observação estática, sem defeito físico reproduzido. O helper delega os argumentos diretamente a `LivingEntity.knockback`; normalização, resistência, eventos e deslocamento efetivo são da engine. O pedido de movimento **não depende de hurt retornar true**, mas sua aceitação final não é garantida.

Não há criação de projétil ou redimensionamento de entidade nesse caminho. As partículas de relâmpago são feedback cliente: não comprovam dano elétrico nem tamanho da área de ataque. O ramo visual atualiza UseTime, solicita som em t=10 e emite 5..9 tentativas de partículas nos pulsos; os códigos de som/polaridade são 9/10 e partículas Scarlet/Azure invertem seus endpoints. Esses valores não são número de alvos ou hits.

## 5. Custos, lado lógico e persistência

O construtor do escudo declara stack máxima 1, **durabilidade 1000** e raridade UNCOMMON. Somente **`t==10 && !level.isClientSide()`** solicita `ACCompat.hurtAndBreakUsedHand(stack,1,usuário)` (`@584–601`), mesmo sem candidato elegível. O helper resolve `getUsedItemHand→slotOf` e encaminha a `ItemStack.hurtAndBreak`. Criativo, Unbreaking, eventos e quebra efetiva são externos. Não existe débito próprio de mana, stamina, Soul Energy ou `addCooldown` neste consumidor, nem custo proporcional ao nível L ou a cada pulso posterior.

**A guarda cliente em `@60–64` cobre somente a região visual anterior a `@365`.** O laço de busca/dano/movimento em `@365–581` fica fora dela. Só a solicitação de durabilidade possui a guarda de servidor acima. Não inferir aplicação duplicada no modpack ou autorizar outro adapter a chamar o pipeline nos dois lados; isso requer QA físico e um contrato de autoridade próprio.

`Polarity` é armazenado na CUSTOM_DATA da stack: ausência de tag retorna false/Azure. `setUseTime` grava o valor anterior em `PrevUseTime` e o novo em `UseTime`; `SwitchTime`/`PrevSwitchTime` são tratados de modo semelhante. Getters interpolados usam `prev + partial×(atual−prev)`, sem clamp próprio. `acInventoryTick` zera os tempos de uso quando um LivingEntity não está usando aquela stack; no cliente aproxima SwitchTime de 5/0 conforme a polaridade. Esses campos de apresentação não alteram `t` nem concedem um cooldown persistente por jogador.

`ACCompat.getTag/getOrCreateTag` trabalham com cópia de CUSTOM_DATA e `setTag` confirma a escrita ou remove o componente quando apropriado. Não se certificam aqui o codec de rede, a identidade pós-reload, transporte de NBT ou stack de mods concorrentes. `releaseUsing` delega à superclasse e solicita limpeza do cache de som; não grava token de cast nem settlement de Mastery.

Reparo adicional aceita scarlet_neodymium_ingot e azure_neodymium_ingot, ou validação herdada. `getEnchantmentValue=1` e `isEnchantable` exige stack count 1. Esses dados não encerram a economia completa do equipamento.

## 6. Contratos de integração

| Perk / sistema pretendido | Fronteira nativa a preservar | Estado |
|---|---|---|
| Dano inicial / nível | Valor L da stack, fórmula inteira e única interseção t=10 | Hook `NOT_VERIFIED`; não somar bônus em todos os pulsos |
| Área, range ou target | AABB `(5,1,5)`, distância `<=5`, filtro unilateral de aliado | Sem autorização para ampliar dano por meio de partícula ou tag |
| Movimento / polaridade | Argumentos distintos Scarlet/Azure, X zero no ramo Azure, knockback nativo após hurt | Não transformar o pedido em deslocamento garantido nem corrigir o provider por perk |
| Tempo, custo ou cooldown | Tempo do callback, pulso a cada cinco ticks e durabilidade só no t=10 servidor | Não usar UseTime interpolado ou anvil_cost como recurso de cast |
| Autoria / XP / Mastery | Fonte mobAttack(user), retorno de hurt descartado, ausência de deduplicador de cast | Black Arcana/RPG Skill Tree não devem duplicar hurt, custo ou proc |
| Mundo / Enshrouded | Nenhuma mutação própria de blocos neste laço; proteção/autoridade são gates externos | Sem adapter executável, nova escola, Stage ou hook mutador homologado |

O Black Arcana preserva o settlement do provider; RPG Skill Tree fornece progressão/perks/Mastery por boundary verificada. Descritor JVM, setter de tag ou assinatura de callback não constituem uma API segura de mutação. `NO_MUTATION` permanece aplicável.

## 7. Validação e conclusão delimitada

O [manifesto](../EXACT-HEAVY-SLAM-CONTRACT-1.0.10.json) sela esta ficha, todos os 20 membros próprios do item, helpers e recursos nomeados. `onUseTick` tem 276 instruções; o selo seleciona a lógica de combate, guards e checkpoints visuais dentro do budget existente, sem afirmar exportação de cada instrução cosmética. As demais fronteiras herdadas continuam explícitas. Os hashes do publisher, de cada recurso/classfile e da ficha são reexaminados por CI; [testes semânticos](../../../../../docs/qa/alexscaves_1010_heavy_slam_cards_test.py) protegem fórmula, cadência, descarte do resultado, lado lógico e os operandos Azure.

**Contabilidade:** uma ficha individual de encantamento, **+0 raízes mágicas novas**. A conclusão é apenas `STATIC_TECHNICAL_CATALOG_ONLY`; os outros vinte dossiers existentes continuam parciais. Não se promove o Resistor Shield inteiro nem o provider. `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, universo integral aberto.

QA física pendente: pulsos aceitos/recusados, níveis nativos e não nativos, aliados/PvP/claims, componente X Azure, resistência e cancelamento de knockback, cancelamento/reinício de uso, mãos/slots, durabilidade/criativo, dois lados lógicos, multiplayer, save/reload e datapacks. Próxima identidade ainda sem ficha na fila: `alexscaves:herd_phalanx`.
