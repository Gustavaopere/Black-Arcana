# Lasting Morale — `alexscaves:lasting_morale` (1.0.10)

**Contrato técnico estático:** ✅ `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`. **Hooks mutadores:** `NOT_VERIFIED`. **QA física:** `NOT_TESTED`. **Integração:** `NO_MUTATION`. O recorte conclui o encantamento e os consumidores delimitados de tempo/cooldown do Magic Conch; não conclui Charting Call, Taxing Bellow, os ataques dos três mobs ou o universo do provider.

## 1. Identidade e descrição original

- **Provider / versão:** Alex's Caves Continued / `alexscaves`, Minecraft 1.21.1; artefato `alexscaves-1.0.10-neoforge+1.21.1.jar`, CurseForge projeto `1645389`, arquivo `8856293`, **75.279.314 bytes**.
- **JAR SHA-1:** `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`; **SHA-256:** `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- **Recurso:** `data/alexscaves/enchantment/lasting_morale.json`, 365 bytes; SHA-256 `8c662fb7f68987d8e564ec053ebccdd9232593e5961d2213bbbed037b270232f`.
- **Tag de item:** `data/alexscaves/tags/item/enchantable/magic_conch.json`; SHA-256 `730151144ab45cb149cf6adfdf5d9cfb69b450238ff126f7f1ac33a0406d2cd8`.
- **Descrição literal de `en_us.json`:** “Deep Ones summoned by Magic Conch will stay around longer”. Tradução explicativa: os Deep Ones invocados pelo Conch permanecem por mais tempo. Não há entrada própria no `pt_br.json` examinado. A descrição não explicita o cooldown compartilhado identificado abaixo.
- **Produtor:** `server/item/MagicConchItem.class`, SHA-256 `4cfad894baabc9540b09de8df8eaf263952292e9c7cc06f86d288cecfb833ce2`; **consumidor de duração:** `server/entity/living/DeepOneBaseEntity.class`, SHA-256 `185df23946292e403300849222018480a3cc1397ee6d6d60e0b28abc40e97470`. Prefixo de classes: `com/github/alexmodguy/alexscaves/`.
- **Provas:** [manifesto individual](../EXACT-LASTING-MORALE-CONTRACT-1.0.10.json), [reprodução](../EXACT-LASTING-MORALE-CONTRACT-1.0.10.md) e [ação Magic Conch já catalogada](../actions/magic-conch-summon-deep-ones.md).

A varredura das classes do JAR por referência ao campo `LASTING_MORALE` localizou `ACEnchantmentRegistry` e `MagicConchItem`. Esse levantamento não cobre reflexão, transformações ou consumidores externos. A fonte pública `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` declara **1.1.1** e é apenas corroboração adjacente; os parâmetros desta ficha vêm do binário/dados **1.0.10**.

## 2. JSON, níveis e aquisição

| Campo | Valor literal publisher | Significado / limite |
|---|---|---|
| `description.translate` | `enchantment.alexscaves.lasting_morale` | Chave de tradução |
| `supported_items` | `#alexscaves:enchantable/magic_conch` | Tag empacotada contém somente `alexscaves:magic_conch` |
| `weight` | `2` | Peso declarado, não probabilidade medida |
| `max_level` | `3` | Domínio normal publicado I–III |
| `min_cost` | `base=1`, `per_level_above_first=8` | I/II/III: 1/9/17 pelo modelo JSON |
| `max_cost` | `base=41`, `per_level_above_first=10` | I/II/III: 41/51/61 pelo modelo JSON |
| `anvil_cost` | `4` | Custo de encantamento, não débito por cast |
| `slots` | `mainhand` | Slot declarado no recurso |
| `effects` / `exclusive_set` | Ausentes neste JSON | Não certifica ausência de comportamento Java ou compatibilidade global |

O registro liga `LASTING_MORALE` à chave `lasting_morale`; `ACCompat.enchantLevel` percorre os encantamentos da stack, devolve o primeiro nível cujo Holder corresponde à chave, ou zero. Esse leitor e a aritmética do release não revalidam tag/slot nem limitam o valor ao máximo III. Componentes/níveis forçados não são um domínio seguro homologado para perks.

As quatro tags empacotadas `minecraft:in_enchanting_table`, `minecraft:non_treasure`, `minecraft:on_random_loot` e `minecraft:tradeable` contêm o ID. O loot `gameplay/deep_one_knight_barter.json` inclui **o item Magic Conch**, com peso 10 em um pool de um roll, sem garantir obtenção nem o encantamento na instância. Overrides e aquisição real no modpack não foram executados.

## 3. Gatilho, fórmula e vínculo com cooldown

`MagicConchItem.use` inicia uso segurado, emite `INSTRUMENT_PLAY` e retorna consume. `releaseUsing(ItemStack,Level,LivingEntity,int)V` toca o som antes de testar a carga. Calcula `getUseDuration(stack,null) − timeLeft` e só entra no ramo de custo/tempo/invocação/cooldown quando a carga é **estritamente maior que 25 ticks**. `getUseDuration` retorna **1200**, a animação é **BOW**, e `isFoil` retorna true; brilho não comprova presença de Lasting Morale.

Depois do custo, o release lê Lasting Morale **uma vez**, em `@86–101`, e guarda o inteiro no slot local 8:

```text
time = 1200 + 400 * enchantLevel(stack, LASTING_MORALE)
summonDeepOne(type, summoner, time)  // os três loops usam o mesmo local
ACCompat.addCooldown(player, stack, time)
```

| Nível lido no release | Tempo passado aos summons | Valor passado ao cooldown do Player |
|---|---:|---:|
| 0 — sem encantamento | 1200 ticks | 1200 ticks |
| I | 1600 ticks | 1600 ticks |
| II | 2000 ticks | 2000 ticks |
| III | 2400 ticks | 2400 ticks |

**A duração e o cooldown compartilham a mesma variável.** Não há segunda fórmula ou releitura do nível ao expirar cada entidade. Uma perk que altere esse valor no produtor atingiria ambos os consumidores; esta evidência não identifica um hook suportado para separar seus efeitos. O helper de cooldown usa `stack.getItem()` em `ItemCooldowns.addCooldown(Item,int)`: a chave é o Item, não uma stack única nem o UUID de um summon.

Os três callers de `summonDeepOne` usam o local 8 em `@265/320/375`, antes das chamadas `@267/322/377`. O bloco final `@418–448` exige que o usuário seja Player, mas não consulta quantos summons foram aceitos e não tem outra guarda própria de lado lógico. A emissão servidor de summons tem uma guarda separada `isClientSide` em `@103–107`. Não inferir execução única em rede ou reembolso por falha de spawn somente a partir desse método.

## 4. Invocação, targeting e dano

Sem Charting Call, os limites solicitados são **3 Deep Ones, 2 Knights e 1 Mage**; cada família permite até **99 tentativas**. Os contadores aumentam quando `summonDeepOne` devolve uma entidade não nula. Lasting Morale altera o argumento de tempo, não a quantidade, o tipo de participante, a geometria de colocação ou os filtros de alvo.

Placement começa na posição de bloco do usuário, com offsets inteiros X/Z **−10 a 9** e Y **+7**; procura o piso descendo por água/ar acima da altura mínima. Exige água ou suporte apropriado, posiciona no centro com Y adicional 0,5, define owner/tempo, finaliza como `TRIGGERED`, testa obstrução e solicita inserção. `addFreshEntity @290` tem seu booleano descartado em `@293`; a rotina ainda chama `copyTarget @297` e pode retornar não nulo. **Contagem de retornos não nulos não certifica inserções aceitas.**

`copyTarget` conserva um alvo atual vivo. Caso contrário, prefere `summoner.getLastHurtMob`; só usa `getLastHurtByMob` se o primeiro for null. O candidato deve estar vivo, ser diferente do usuário, não ser Deep One, e passar `candidate.isAlliedTo(summoner)==false` e `candidate.isAlliedTo(this)==false`. Os testes de aliança partem do candidato, sem pressupor simetria. Uma primeira opção não nula mas inelegível não implica uma segunda tentativa com a opção alternativa. Não há seleção pelo cursor, projétil mágico, tamanho de hitbox, raio de ataque ou dano-base definido por Lasting Morale nesse fluxo.

**Dano por hit / DamageType / AoE: N/A como modificadores próprios deste encantamento.** Os ataques permanecem nos sistemas nativos das três entidades; mais tempo de existência pode permitir outras ações, mas não prova número de ataques, DPS ou bônus de dano por impacto. Escala, velocidade, alcance de combate e conversão target→área não são parâmetros do leitor de Lasting Morale.

## 5. Ciclo de vida, proprietário e persistência

`DeepOneBaseEntity` inicia com `summonerUUID=null`, progresso de invocação zero e dados sincronizados `SUMMONED=false`, `SUMMON_TIME=0`. `setSummonedBy` marca summoned, grava o UUID do LivingEntity e passa `time` ao setter sincronizado; esses setters não oferecem clamp próprio de nível, tempo, proprietário ou autorização para uma perk.

No tick de uma entidade summoned, o progresso cresce em direção a **20** enquanto o tempo é positivo e diminui após a expiração. O contador positivo é decrementado **no servidor**, por tick processado da entidade. No ramo de tempo não positivo, o servidor só solicita `remove(RemovalReason.DISCARDED)` quando o progresso chegou a zero. `isEffectiveAi` exige a condição herdada e, para summoned, progresso **>=20**. Portanto a tabela registra o **contador inicial**, não duração física exata, tempo de IA ativa ou prazo garantido de desaparecimento; o fade e outros eventos de remoção são caminhos distintos.

Um Player com UUID igual ao summoner de uma entidade summoned recebe reação `HELPFUL`; os Deep Ones também têm regras nativas de aliança entre si. Esse vínculo não comprova comandos exclusivos, atribuição de kills/Mastery, remoção por logout ou necessidade de manter o proprietário online. Nenhum decremento por relógio externo/offline foi identificado nesse consumidor.

**NBT próprio:** `addAdditionalSaveData` sempre grava `ConchSummoned`, mas grava `ConchUUID` e `ConchTime` **somente se `summonerUUID != null`**. `readAdditionalSaveData` aplica o booleano e só carrega UUID/tempo quando `ConchUUID` existe. O progresso de invocação não é salvo por esses corpos. Não generalizar a preservação do tempo a qualquer entidade sem UUID, nem garantir continuidade idêntica de animação/IA após unload, restart ou reload.

## 6. Custos e ordem dos efeitos

O Magic Conch declara durabilidade **5**, raridade **UNCOMMON**, enchantability **1** e só retorna `isEnchantable=true` para stack de contagem 1. Após a carga elegível, sem Taxing Bellow solicita `hurtAndBreakUsedHand(stack,1,user)`; isso precede a leitura do tempo e a guarda servidor de spawn. O helper delega à mão usada. O callback não condiciona esse pedido de desgaste a uma inserção bem-sucedida e não contém reembolso por falha de placement.

Com Taxing Bellow positivo, substitui esse ramo por `setDamageValue(Math.min(0, damage−1))` e marca débito de reputação; ao fim dos loops, pede `addReputation(userUUID,−2)` **apenas se houver último summon não nulo**. `Math.min` não foi reinterpretado como clamp válido a zero; tratamento efetivo do argumento de dano e reputação pertence ao provider/engine. Lasting Morale não multiplica esses custos.

Charting Call atua depois da leitura de tempo e dentro do bloco servidor. Seus bounds compilados para nível positivo são `max(L−1,2)`, `max(L−2,0)` e `max(L−3,0)` em `nextInt`, antes do placement. Os caminhos de bound zero e possíveis efeitos sobre a conclusão do release já estão [documentados na ação original](../actions/magic-conch-summon-deep-ones.md); não são uma falha física reproduzida nem são corrigidos por esta ficha. Ordem de custo, falha intermediária e cooldown precisam ser preservados ao avaliar qualquer mutação futura.

Não há débito próprio de mana, stamina, fome ou itens consumíveis no release auditado. `anvil_cost=4`, custo de encantamento, desgaste da ferramenta, reputação e cooldown são mecanismos distintos; o contador das entidades não os debita novamente a cada tick.

## 7. Integração e evidência

| Perk / sistema pretendido | Contrato a preservar | Estado |
|---|---|---|
| Duração de summon | Leitura única `1200+400L`, contador servidor e fade de progresso | Hook `NOT_VERIFIED`; não prometer desaparecimento exato no tick do cooldown |
| Cooldown independente | Mesmo local alimenta summons e cooldown por Item | Separação de consumidores não homologada |
| Custo / quantidade | Custo antes da guarda de spawn, RNG de Charting e retornos não nulos | Não repetir release, desgaste, reputação ou loops de invocação |
| Targeting / dano / área | Owner UUID e filtros `copyTarget`, ataques sob autoridade dos mobs | Não criar um segundo pipeline de alvo/dano a partir do tempo |
| Autoria / Mastery | Owner inicial e resultado nativo de cada ataque são fatos diferentes | Não atribuir procs/XP por tentativa, retorno não nulo ou duração |
| Persistência | UUID/tempo condicionais e progresso não salvo | Reload e níveis/componentes forçados precisam de QA próprio |
| Black Arcana / Enshrouded / RPG Skill Tree | Provider conserva cast, custo, AI, tempo, cooldown e remoção | `NO_MUTATION`; nenhum adapter executável ou Stage promovido |

O [manifesto individual](../EXACT-LASTING-MORALE-CONTRACT-1.0.10.json) sela identidade, recursos e consumidores relevantes, reaproveitando os [contratos da ação](../EXACT-TECHNICAL-CONTRACTS-1.0.10.json) sem modificar a prova ou ficha anteriores. Métodos extensos têm checkpoints causais delimitados; o selo de classe não é uma reconstrução integral de toda a IA. Os [testes semânticos](../../../../../docs/qa/alexscaves_1010_lasting_morale_cards_test.py) protegem o tempo/cooldown compartilhado, gates, aceitação de spawn, lifecycle e persistência.

**Contabilidade:** uma ficha individual de encantamento; **+0 raízes mágicas novas**. `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`; `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, provider integral aberto. As vinte fichas parciais anteriores permanecem parciais.

QA física pendente: carga 25/26 ticks, níveis 0/I/II/III e componentes forçados, os dois lados lógicos/mãos, combinações Charting/Taxing, spawn recusado/obstruído, cooldown por Item em múltiplas stacks, counter/fade/AI, owner/logout/dimensão, alvo/alianças, autoria de ataques, unload/restart e multiplayer. Próxima identidade sem ficha individual na fila: `alexscaves:multiple_mint`.
