# Herd Phalanx — `alexscaves:herd_phalanx` (1.0.10)

**Contrato técnico estático:** ✅ `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`. **Hooks mutadores:** `NOT_VERIFIED`. **QA física:** `NOT_TESTED`. **Integração:** `NO_MUTATION`. O certificado cobre este encantamento e a cadeia defensiva Grottoceratops delimitada; não encerra a Extinction Spear inteira, outros espíritos ou o universo do provider.

## 1. Identidade e descrição original

- **Provider / versão:** Alex's Caves Continued / `alexscaves`, Minecraft 1.21.1; `alexscaves-1.0.10-neoforge+1.21.1.jar`, CurseForge projeto `1645389`, arquivo `8856293`, **75.279.314 bytes**.
- **JAR SHA-1:** `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`; **SHA-256:** `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- **Recurso:** `data/alexscaves/enchantment/herd_phalanx.json`; **SHA-256:** `294818f10b6327c0ca06ef4510d599bba0a61a6c47ffc044236268411ccc0616`.
- **Tag de item:** `data/alexscaves/tags/item/enchantable/extinction_spear.json`; SHA-256 `950e56b0643bb55cb9acab23c3eecdfd75f6ee7ae3f1253d9866c3f2f7fdf5e7`.
- **Descrição literal em `en_us.json`:** “Extinction Spear Grottoceratops defense summons more armored heads”. Tradução explicativa: a defesa Grottoceratops da Extinction Spear tenta invocar mais cabeças. Não há descrição Herd Phalanx no `pt_br.json` examinado.
- **Provas:** [manifesto individual](../EXACT-HERD-PHALANX-CONTRACT-1.0.10.json) e [escopo/reprodução](../EXACT-HERD-PHALANX-CONTRACT-1.0.10.md), reaproveitando o [contrato Spirit Dinosaur](../EXACT-SPIRIT-DINOSAUR-CONTRACT-1.0.10.md).

A varredura dos 1.555 class entries por referência ao campo `HERD_PHALANX` encontrou o registro `ACEnchantmentRegistry` e o consumidor `ExtinctionSpearItem`. O levantamento de símbolos não exclui reflexão, mixins ou usos em outros mods. A fonte pública `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` declara **1.1.1** e é corroboração adjacente, sem autoridade sobre os parâmetros 1.0.10 abaixo.

## 2. JSON, níveis, slots e aquisição

| Campo | Valor literal publisher | Limite de interpretação |
|---|---|---|
| `description.translate` | `enchantment.alexscaves.herd_phalanx` | Chave de tradução |
| `supported_items` | `#alexscaves:enchantable/extinction_spear` | Tag empacotada contém somente `alexscaves:extinction_spear` |
| `weight` | `2` | Peso declarado, não chance medida |
| `max_level` | `3` | Limite publicado; leitor Java não o aplica como clamp |
| `min_cost` | `base=1`, `per_level_above_first=13` | I/II/III: 1/14/27 pelo modelo do JSON |
| `max_cost` | `base=41`, `per_level_above_first=10` | I/II/III: 41/51/61 pelo modelo do JSON |
| `anvil_cost` | `4` | Custo de encantamento, não mana por cabeça |
| `slots` | `mainhand` | Slot declarado no recurso |

Não há campos `effects` ou `exclusive_set` nesse JSON. O comportamento é implementado em Java; ausência do campo não certifica compatibilidade universal com outros mods/datapacks. `ACCompat.enchantLevel` percorre os encantamentos da stack e devolve o primeiro inteiro cujo Holder corresponde à chave, ou zero; não limita o valor ao max_level publicado. O produtor lê a stack fornecida ao callback, sem guarda própria adicional de mão; isso não substitui as regras de slots da engine nem QA de offhand.

O ID consta diretamente nas tags publisher `minecraft:in_enchanting_table`, `minecraft:non_treasure`, `minecraft:on_random_loot` e `minecraft:tradeable`. Essas declarações não garantem tags finais resolvidas, disponibilidade no pack ou aquisição executada. A receita shaped empacotada da lança é ` T ` / `TST` / `ABA`: três tectonic_shard, uma limestone_spear, duas amber_curiosity e um heavy_bone; resultado extinction_spear, com count omitido no JSON.

## 3. Consumidor, quantidade e ingresso

**Produtor:** `com/github/alexmodguy/alexscaves/server/item/ExtinctionSpearItem.class`, método `onUseTick`, ABI `(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/item/ItemStack;I)V`.

**SHA-256 do classfile produtor:** `846709940e9e400c4d6e894ec07887b762598b0d8f116fff951fa5585245bfd8`.

O método só entra quando **`remainingUseTicks == getUseDuration(stack,null)`** (`@0–8`); o base `SpearItem.getUseDuration` retorna **72000 ticks**. É uma igualdade de parâmetros do callback, não um token de cast nem prova de uma única execução sob chamadas arbitrárias. No ramo elegível:

```text
N = 3 + ACCompat.enchantLevel(stack, HERD_PHALANX)
step = 360F / (float)N
para i de 0 até i < N:
    spirit = ACCompat.createEntity(DINOSAUR_SPIRIT, level)
    spirit.copyPosition(user)
    spirit.setDinosaurType(GROTTOCERATOPS)
    spirit.setPlayerUUID(user.UUID)
    spirit.setRotateOffset((float)i * step)
    level.addFreshEntity(spirit)  // booleano descartado
```

| Nível lido | Tentativas nativas N | Espaçamento angular solicitado |
|---|---:|---:|
| 0 — sem encantamento | 3 | 120° |
| I | 4 | 90° |
| II | 5 | 72° |
| III | 6 | 60° |

São **tentativas**, não cabeças garantidas ou bloqueios de dano medidos. `HERD_PHALANX @38` é lido por `enchantLevel @41`; soma inteira em `@44`; divisão em `@47–52`; loop em `@58–62`; inserção em `@122`, resultado descartado em `@125`. `createEntity` delega a `EntityType.create(level)`, sem guard local de null antes de `copyPosition`. Não há guarda própria de servidor, teste de inserção aceita, limite por jogador ou lista de deduplicação nesse produtor.

O nível altera a **quantidade**; não é escrito como enchantmentLevel nas entidades criadas. O produtor não define alvo ofensivo, duração extra, dano, armadura ou pontos de vida por nível. A entidade é `DinosaurSpiritEntity extends Entity`, com tipo GROTTOCERATOPS; outros tipos do mesmo classfile têm funções distintas e não são variações ofensivas de Herd Phalanx.

O base `SpearItem.use` só rejeita iniciar uso quando a stack é damageable e `damageValue >= maxDamage−1`. Caso contrário solicita `startUsingItem(hand)` e resultado consume; não impõe uma transação de mana. O construtor/registro da lança declara durabilidade **1300**. A economia completa do item e seu arremesso pertencem ao [contrato de Spirit Dinosaur](../damage-types/spirit-dinosaur.md).

## 4. Órbita, dimensões e duração

O registro `DINOSAUR_SPIRIT` declara categoria MISC, dimensões **1F×1F**, update interval **1**, receive velocity updates true e fireImmune. Isso não define raio de proteção ou escala visual de uma cabeça. A proteção não depende de colisão física da cabeça com o ataque: ela é consumida pelo handler descrito na seção 5.

`tickGrottoceratops(Player)` calcula:

```text
rot = rotateOffset + (float)(player.tickCount * 5)
offset = Vec3(0, 1, 2).yRot((float)-toRadians(rot))
delta = (player.position + offset - spirit.position) * 0.25D
XRot = 10F
noPhysics = true
```

`player.tickCount*5` é uma multiplicação int antes da conversão. O deslocamento `(0,1,2)` e a posição do usuário definem o destino da órbita; não constituem range de dano ou garantia de que a entidade já esteja naquela posição. No tick comum, o espírito **move com o delta anterior**, aplica damping `0.8999999761581421D` e só depois calcula o novo delta do subtipo. Interpolação e partículas cliente têm guards próprios.

O teste próprio de parada do Grotto ocorre no servidor: se o item atualmente em uso pelo Player **não é do tipo `EXTINCTION_SPEAR`**, marca fading. A comparação é de tipo de item, sem token da stack original/cast. Não há contador próprio de duração fixa no corpo Grotto. O loop de órbita e o dispatch não ficam globalmente sob essa guarda de servidor.

No ciclo comum, ausência de Player solicita fading; `!fading && fade<10F` aumenta fade em 1, fading com fade positivo o reduz em 1. Quando fading e fade<=0, solicita `discard`, **sem return** antes do restante do movimento/dispatch daquele tick. Fading já exclui a cabeça da seleção defensiva, mesmo enquanto a entidade visual ainda está sendo processada. Não converter fade em dez bloqueios ou dez ticks garantidos de proteção.

## 5. Consumo defensivo, targeting e ordem de eventos

**Seleção:** `ExtinctionSpearItem.killGrottoGhostsFor(Player,boolean)`, ABI `(Lnet/minecraft/world/entity/player/Player;Z)Z`.

Consulta `DinosaurSpiritEntity` na **AABB corporal do Player expandida em `(30D,30D,30D)`** (`@9–24`), não esfera de raio 30 nem o raio visual da órbita. Para cada instância, compara UUID com o Player, exige tipo GROTTOCERATOPS e `!isFading`. UUID.equals é executado **antes** do filtro de tipo, sem null-check próprio nesse ponto; estado não vinculado é um risco estático de entrada, sem falha física reproduzida.

Com `justTheClosest=false`, marca todos os elegíveis como fading e retorna true mesmo quando nenhum foi encontrado. Com true, escolhe no máximo uma instância e só retorna true se encontrou e marcou uma. O comparador compilado é **`closest.distanceTo(player) > candidate.distanceTo(closest)`** (`@104–116`), não `candidate.distanceTo(player)`. Não prometer seleção geométrica da cabeça mais próxima do usuário.

**Consumidor indireto:** `CommonEvents.acCancelDamage` verifica vítima Player e item em uso igual a Extinction Spear, então chama `killGrottoGhostsFor(player,true)` (`@91–143`). Não consulta o nível Herd nesse ramo: a defesa base de nível zero também é alcançável. Se o helper retorna true, marca um booleano e solicita SHIELD_BLOCK. Outras condições anteriores/posteriores do mesmo handler podem marcar o booleano independentemente; uma condição anterior verdadeira não impede necessariamente o consumo Grotto.

O adapter instalado **NeoForge `CommonEvents.livingHurt(LivingDamageEvent.Pre)`** chama esse helper e, se true, solicita **`event.setNewDamage(0F)`**. Isso não equivale a `setCanceled(true)`, não comprova retorno false do `Entity.hurt` original e não garante cancelamento de todos os efeitos secundários. Registro/entrega do evento, ordem de listeners e resultado final pertencem à engine/modpack e continuam sem QA física.

Nesse ramo Grotto não há filtro próprio por atacante, DamageType, LOS, cone frontal, aliado ou tamanho do dano. Não inventar política PvP/claims nem imunidade universal a partir dessa ausência. Repetição de callbacks/eventos não é deduplicada por token de cast; cada invocação usa as instâncias elegíveis naquele momento. Não conceder XP/Mastery por uma simples tentativa de spawn, som ou booleano de handler.

## 6. Custos, cleanup e persistência

O produtor de cabeças não debita diretamente mana, stamina, Soul Energy, stack ou durabilidade, nem registra `addCooldown`; isso não significa custo global zero para uma integração. Custos de encantamento no JSON, elegibilidade de uso, reparo e arremesso são mecanismos diferentes. Liberação por qualquer Player chama `killGrottoGhostsFor(player,false)` **fora do ramo de arremesso bem carregado**; até uma liberação com carga insuficiente tenta limpar os Grotto elegíveis. Essa limpeza não prova descarte imediato ou sucesso de inserções anteriores.

`getUsingPlayer` usa UUID: no cliente consulta a Level local; no servidor resolve na **PlayerList global de jogadores online**, sem teste próprio de mesma dimensão, vida ou spectator. UUID de um usuário LivingEntity não Player pode ser gravado pelo produtor, mas não se transforma automaticamente em Player resolvido. A consulta defensiva continua na Level atual do Player.

O NBT próprio do espírito grava/lê somente `UsingPlayerUUID` e `DinosaurType`; não grava explicitamente rotateOffset, delay, nível, fading, usingAbility, duration, abilityProgress ou dealtDamage. Camadas genéricas de Entity são externas; não se afirma ausência de todo NBT. Recriação não restaura automaticamente o estado transitório nem o token de uso, que não existe nesse recorte.

O enum tem ordinais 0/1/2; `getDinosaurType` usa `values()[clamp(raw,0,values().length)]`, cujo limite superior é **3**. Entrada raw>=3 chega estaticamente a índice inválido. O produtor auditado usa enum GROTTOCERATOPS/ordinal1, mas isso não torna NBT arbitrário ou setters uma API segura para perks. Não há crash reproduzido ou correção nativa nesta ficha.

## 7. Integração, validação e conclusão

| Alteração pretendida | Contrato necessário | Estado |
|---|---|---|
| Mais cabeças / nível | Soma inteira3+L, valores JSON, igualdade do callback e inserções recusadas | Hook `NOT_VERIFIED`; não duplicar a criação ou presumir idempotência |
| Mais proteção / duração | Consumo por entidade não fading, item atual em uso e pedido de dano zero no Pre | Não equiparar N cabeças a N bloqueios físicos garantidos |
| Range ou targeting | AABB30 por eixo, UUID/Level e comparador assimétrico | Órbita visual e seleção defensiva são parâmetros distintos |
| Tamanho / velocidade | Dimensões1×1, destino orbital, delta0.25 e movimento anterior | Nenhum redimensionamento ou collider de escudo homologado |
| Recursos / Mastery | Ausência de custo próprio do summon versus custos nativos do item; eventos sem token | Black Arcana/RPG Skill Tree preservam settlement; sem proc duplicado |
| Enshrouded / mundo | Defesa nativa por evento; sem mutação própria de blocos ou novo DamageType | Sem adapter executável, escola nova, Stage ou proteção física promovidos |

O [selo individual](../EXACT-HERD-PHALANX-CONTRACT-1.0.10.json) reúne a cadeia Herd/Grotto e o suporte reaproveitado do manifesto Spirit Dinosaur, sem alterar esse manifesto histórico. Métodos de contexto da lança/registro não certificam os outros espíritos, o dano Spirit Dinosaur ou o equipamento inteiro. [Testes semânticos](../../../../../docs/qa/alexscaves_1010_herd_phalanx_cards_test.py) verificam produtor, cadência de ingresso, seleção, evento Pre, lifecycle e contagens separadas.

**Contabilidade:** uma ficha individual de encantamento; **+0 raízes mágicas novas**. `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`; `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`. Os vinte dossiers parciais anteriores permanecem parciais; o provider integral continua aberto.

QA física pendente: callback inicial não entregue/repetido, spawn recusado/null, offhand e níveis não nativos, múltiplos usuários, Player ausente/outra dimensão, entidades sem UUID, consumo de cabeça e listeners concorrentes, dano final/efeitos secundários, cancelamento/reinício de uso, save/reload e composição com perks. Próxima identidade sem ficha na fila: `alexscaves:humungous_hex`.
