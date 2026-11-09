# Taxing Bellow — `alexscaves:taxing_bellow` (Alex's Caves Continued 1.0.10)

**Contrato técnico individual:** ✅ **estático, SHA-exato** (`STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`). **Hook mutador:** `NOT_VERIFIED`. **QA física:** `NOT_TESTED`. **Política:** `NO_MUTATION` / fail-closed. A certificação cobre os consumidores delimitados abaixo, não execução de Minecraft nem o universo inteiro do provider.

## 1. Identidade, descrição e fonte física

- **Provider / mod ID:** Alex's Caves Continued / `alexscaves`, Minecraft 1.21.1, NeoForge, Java 21; registro `alexscaves:taxing_bellow`, `ACEnchantmentRegistry.TAXING_BELLOW`.
- **JAR instalado (modlist, linha física #019):** `alexscaves-1.0.10-neoforge+1.21.1.jar`; CurseForge file `8856293`, 75.279.314 bytes. SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`; SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- **Recurso:** `data/alexscaves/enchantment/taxing_bellow.json`, **443 bytes**, SHA-256 `275b7ef42207724ae8ee2048097d3f16dbdfc60796f06a98eb77356ddb744df1`.
- **Equipamento declarado:** `#alexscaves:enchantable/magic_conch` contém `alexscaves:magic_conch`, tag SHA-256 `730151144ab45cb149cf6adfdf5d9cfb69b450238ff126f7f1ac33a0406d2cd8`.
- **Descrição funcional própria:** ao liberar um Magic Conch suficientemente carregado, Taxing Bellow substitui o desgaste normal por uma escrita específica no dano do item. Caso exista um summon não nulo ao final dos laços no servidor, solicita um único débito de reputação dos Deep Ones para o UUID do invocador. Não cria outra magia, outro summon, mana, dano ou entidade.
- O texto localizado em inglês descreve preservação da durabilidade em troca de opinião pior dos Deep Ones. **O bytecode usa `Math.min(0,damage−1)`, que não é simplesmente “preservar dano anterior”.** Efeito final de `ItemStack.setDamageValue` no domínio de inteiros negativos exige validação própria; não substituir o literal por uma interpretação intuitiva.

## 2. Definição JSON, níveis e incompatibilidade

| Campo | Contrato do publisher 1.0.10 |
|---|---|
| `max_level` | **1** (I); `releaseUsing` testa apenas nível `>0`, sem clamp adicional do nível nessa rotina |
| `supported_items` | `#alexscaves:enchantable/magic_conch` |
| `slots` | `[mainhand]` |
| `weight` | `2` — peso de encantamento, não probabilidade de efeito |
| `min_cost` | `base=1`, `per_level_above_first=19`: nível I = 1 |
| `max_cost` | `base=41`, `per_level_above_first=10`: nível I = 41 |
| `anvil_cost` | `4`: dado de aquisição, não custo por conjuração |
| `exclusive_set` | `minecraft:unbreaking`, `minecraft:mending` — incompatibilidades declarativas, não prova de todo ambiente de datapacks/mods |

O encantamento modifica **a ação semântica única** [Magic Conch — Summon Deep Ones](../actions/magic-conch-summon-deep-ones.md). `Charting Call` (quantidade) e `Lasting Morale` (duração/cooldown) são contratos separados; o recurso Taxing Bellow não declara incompatibilidade com eles. A tag, a definição e o limite I não garantem o estado de stacks adulterados, addons ou datapacks.

## 3. Gatilho, execução e ordem dos custos

**Produtor:** `MagicConchItem.releaseUsing(ItemStack,Level,LivingEntity,int)V` tem **211 instruções JVM** e digest `f8a7f97d8a15e513a06cf81e0c4cb2fde5fad9a100b1a3187a9ab4f4f9dd7894`. O `use` do mesmo item inicia o uso segurado e solicita som; `getUseDuration` retorna **1.200 ticks**, máximo da animação de uso e não tempo mínimo.

O release solicita o som de liberação **antes** do teste de carga (`@0–20`). Calcula `charge = getUseDuration(stack,null) − timeLeft` (`@23–32`). Quando `charge <=25` (`if_icmple451 @41`), retorna sem os custos/summons/cooldown posteriores. Para **`charge >25`**:

1. `ACCompat.enchantLevel(stack,TAXING_BELLOW)` (`@44–51`) testa nível **positivo**.
2. Se positivo, solicita `stack.setDamageValue(Math.min(0, stack.getDamageValue()−1))` (`@54–65`), ativa **flag local 6 = true** (`@68–69`) e salta sobre o desgaste normal (`goto80 @71`).
3. Sem o encantamento, solicita `ACCompat.hurtAndBreakUsedHand(stack,1,user)` (`@74–77`). **São ramos alternativos**, não desgaste e reputação em duplicidade.
4. O release calcula `time=1200+400×level(LASTING_MORALE)` (`@86–101`) antes da guarda explícita do servidor `Level.isClientSide @104/ifne418 @107`. Ambos os caminhos de desgaste são alcançados antes dessa guarda; autoridade/física do ItemStack no cliente exigem teste.
5. No ramo servidor, prepara pedidos e tenta invocar Deep One, Knight e Mage conforme os laços nativos; os retornos não nulos substituem o slot local 10 pelo **último summon não nulo**, não uma contagem de entidades realmente aceitas.
6. Terminados os laços, `if (!flag6) goto418` (`@397–399`); se `lastNonNullSummon==null`, também salta (`@402–404`). Caso contrário, chama **uma vez** `lastNonNullSummon.addReputation(user.getUUID(),−2)` (`@407–415`).
7. O bloco de stat/cooldown depois de `@418` exige `user instanceof Player`; usa a variável `time` via `ACCompat.addCooldown(player,stack,time)` em `@448`. O método não condiciona esse bloco à aceitação de summons, e não possui outra guarda explícita de lado nessa região.

**Valor passado ao dano do item:** `d = getDamageValue()` → `Math.min(0,d−1)`. Para `d>0`, o argumento é `0` quando `d>=1`; para `d=0`, o argumento é **−1**. Isso é **argumento ao setter**, não garantia de valor de componente após a engine, de reparo durável ou de efeito legítimo com itens adulterados. `max_level=1` limita aquisição normal, não impede nível positivo externo.

## 4. Reputação: consumidor, clamp e eventos adicionais

A chamada `addReputation(UUID,−2)` é feita **no último `DeepOneBaseEntity` não nulo**, mas a reputação não é guardada apenas na instância: `DeepOneBaseEntity.getReputationOf` (`@14–28`) e `setReputationOf` (`@14–25`) consultam `ACWorldData.get(Level)` no servidor e então `getDeepOneReputation(UUID)` / `setDeepOneReputation(UUID,int)`. Os caminhos de acesso ao lado cliente devolvem zero na leitura ou não escrevem na atribuição; acesso sem world data também não realiza escrita.

**Contrato do armazenamento físico:**

| Consumer | Evidência SHA-exata |
|---|---|
| `DeepOneBaseEntity.addReputation(UUID,int)` | Lê antigo (`@2`); calcula `antigo+delta` (`@6–8`), classifica `DeepOneReaction.fromReputation` (`@9`) e pede `setReputationOf(UUID,novo)` (`@19`) |
| `ACWorldData.getDeepOneReputation(UUID)` | Consulta o mapa `deepOneReputations` com `Map.getOrDefault(UUID,0)` (`@9–28`); valor não encontrado usa zero |
| `ACWorldData.setDeepOneReputation(UUID,int)` | **`Mth.clamp(valor,−100,100)`** (`@6–10`), depois `Map.put(UUID,clamped)` (`@16`) |
| `DeepOneBaseEntity.addReputation`, reação | Compara a categoria de reação antes/depois (`@22–28`); se houve mudança e o Player foi resolvido no nível (`@35–43`), pode solicitar advancements específicos e mensagem client-side (`@46–100`). Não garante visualização efetiva nem um proc por ponto |

Assim, o valor que **o método solicita** alterar é `−2` por release elegível, não `−2 × número de invocados`. O valor de reputação **escrito no mapa é limitado a [−100,+100]**. Ex.: a partir de −99, uma chamada normal tenta −101 e o setter grava −100, desde que os guards e a escrita sejam alcançados. Esta ilustração é consequência algébrica do CFG, **não gameplay medido**.

`setDeepOneReputation` não invoca diretamente `setDirty` nesse corpo de 11 instruções. O status da persistência do `ACWorldData` após salvamento/recarga, dirty tracking externo, dimensionamento da storage e sincronização efetiva **não está certificado** por isso. Não inferir que o valor se perde ou persiste sem o restante do ciclo do mundo e QA.

## 5. Summons, targeting, autoria e possíveis exceções

O Magic Conch cria **uma família semântica de invocação**, com Deep One, Knight e Mage como participantes. Os laços base solicitam até 3/2/1 entidades; os limites dos laços e o RNG especial de `Charting Call` pertencem ao [contrato específico](charting-call.md). `Taxing Bellow` não altera dano, vida, atributos, quantidade, velocidade, tipos de mob, janela de spawn, alcance, AOE, targeting de combate ou duração. Não há `DamageSource` própria nem hitbox/projétil independente do encantamento; nesses eixos, **N/A** como efeito direto.

`MagicConchItem.summonDeepOne` tenta posição X/Z aleatória entre −10 e +9, inicial Y +7, verifica superfície/água, configura `setSummonedBy`, `summonTime` e target via `copyTarget` após `ACCompat.finalizeSpawn`. Ao passar no `checkSpawnObstruction`, chama `Level.addFreshEntity` (`@290`) e **descarta seu retorno booleano** (`@293`), copia target e retorna a entidade não nula; portanto a condição para reputação **não é prova de spawn aceito**.

`setSummonedBy(LivingEntity,int)` define `summonerUUID` e um contador sincronizado. O estado de summon e tempo tem NBT próprio da entidade (`ConchSummoned`, `ConchUUID`, `ConchTime`), auditado na raiz. O débito reputacional usa `user.getUUID()`, não a identidade de um alvo de combate ou a quantidade de mortes/XP. Vítimas e AI pertencem às entidades e à engine.

**Interação crítica:** `Charting Call` pode passar limites zero a `RandomSource.nextInt` no JAR 1.0.10; se a execução terminar excepcionalmente antes do ramo `@397–415`, reputação e cooldown posteriores podem não ser alcançados. Isso é **risco estático**, não crash reproduzido. Não somar “−2 sempre” por tentativa nem afirmar debit/cooldown final em erro, cancelamento ou falha de inserção.

## 6. Grafo técnico, métodos e fingerprints

Censo de **1.555 classfiles**: o token compilado direto `TAXING_BELLOW` está somente no `ACEnchantmentRegistry` e `MagicConchItem`. Reflexão, mixins, addons e transformações são fronteiras externas.

| Classe (prefixo `com/github/alexmodguy/alexscaves/`) | SHA-256 do classfile e papel |
|---|---|
| `server/item/MagicConchItem.class` | `4cfad894baabc9540b09de8df8eaf263952292e9c7cc06f86d288cecfb833ce2` — produtor, ramificação de custo, spawn, flag de reputação e cooldown |
| `server/entity/living/DeepOneBaseEntity.class` | `185df23946292e403300849222018480a3cc1397ee6d6d60e0b28abc40e97470` — reputação, reação, owner, alvo e lifecycle |
| `server/level/storage/ACWorldData.class` | `ddb140795a4a38e077575effb858c2f7664780f11046475335ca132200b031f5` — `getDeepOneReputation` e `setDeepOneReputation` com clamp |
| `server/enchantment/ACEnchantmentRegistry.class` | `60006fab1b3b29f5f93c8365416815a12770cf8877a059298cb4ee82f7a92f32` — registro da chave do encantamento |

**Digests individuais SHA-256 de métodos parseados (`javap -c -p -s`)**: `MagicConchItem.releaseUsing` 211 instruções / `f8a7f97d8a15e513a06cf81e0c4cb2fde5fad9a100b1a3187a9ab4f4f9dd7894`; `summonDeepOne` 134 / `c355ab39634de12bb46dd45a2286aca99dcacd1843c98c80d4fe6723fbdf6d25`; `DeepOneBaseEntity.addReputation` 48 / `e3d32551f26215b7656be6eceefc58def1bbf56e954ef6205165959023079054`; `getReputationOf` 18 / `ea5cf310a6760f138c4faca6f9839426a5b2076ec9d5b1e97c2dd7a2f98efa4a`; `setReputationOf` 15 / `7895787ccf834312f55df189ab36f76e62b9bf6a8966755aae5fb1875ce5a35b`; `ACWorldData.getDeepOneReputation` 13 / `d9f33377e874c412a7e9a751e8c743643800a7fb7d140053649e820b3a23923d`; `setDeepOneReputation` 11 / `17caf9eb177f1a8d53077d6715a562b0e11d125bc0e33e3e30e84520e608e4c0`.

Todos os consumidores selecionados, descritores, contagens, digests e janelas de bytecode estão no [manifesto individual](../EXACT-TAXING-BELLOW-STATIC-1.0.10.json). Não redistribuímos JAR nem classes de terceiros.

## 7. Perks, atributos, Mastery e boundary

Uma perk poderia conceitualmente alterar o custo por uso (desgaste versus reputação), clamp, duração, tipo/quantidade de invocados ou regras de obtenção, **mas não há API mutadora segura verificada** para nenhuma dessas alterações. `Math.min`, `ItemStack.setDamageValue`, o flag local, `ACWorldData.setDeepOneReputation` e o release da Conch são **consumidores provider-native, não hooks públicos aprovados**.

**Riscos:** reparo ou dano fora dos limites, bypass de custo, double debit de reputação se interceptado mais de uma vez, alteração indevida da reputação global do jogador, loops e `nextInt(0)` em Charting Call, summons não aceitos, duplicação de cast/XP/kill, reaplicação após reload e client authority. Toda mutação deve manter caps, proteção PvP/claims, autorização do servidor, atomicidade, deduplicação e ownership. Sem boundary real e QA: **`NO_MUTATION` / fail-closed**.

Black Arcana conserva seu runtime, segurança, rituais, casting e efeitos. RPG Skill Tree é apenas sibling de progressão, atributos, perks e Mastery por contratos reais. **Não** creditar Mastery por três tipos de invocado como se fossem três casts novos, nem atribuir dano de cada participante automaticamente a Taxing Bellow.

## 8. Evidências, validação e pendências

- [Manifesto 1.0.10](../EXACT-TAXING-BELLOW-STATIC-1.0.10.json) · [relatório e reprodução](../EXACT-TAXING-BELLOW-STATIC-1.0.10.md) · [sonda read-only](../../../../../docs/qa/alexscaves_1010_taxing_bellow_static_probe.py) · [testes sintéticos negativos](../../../../../docs/qa/alexscaves_1010_taxing_bellow_static_probe_test.py).
- CI do JAR publisher com fingerprint completo, classe/símbolo/custódia de reputação: [execução de descoberta 42545396083](https://github.com/Gustavaopere/Black-Arcana/actions/runs/42545396083); o selo individual deve ser comparado em CI final.
- **Pendências físicas:** uso em 25/26 ticks, dano do item anterior 0/positivo, valores negativos externos, creative/client/server, caps reputação −100/+100, map storage save/reload e `dirty`, duas mãos/usuários, ausência de summon, `addFreshEntity=false`, falha de RNG sob Charting Call, cooldown/XP e integração de perks. Tudo `NOT_TESTED`.
- **Fronteiras não provadas:** persistência final, efeito aceito de `ItemStack.setDamageValue`, alteração real da reputação e mensagens/advancements, extensões externas e hooks. `NOT_VERIFIED`; o universo completo de Alex's Caves permanece aberto.
