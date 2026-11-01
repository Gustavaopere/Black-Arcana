# Spirit Dinosaur — tipo de dano `alexscaves:spirit_dinosaur` (1.0.10)

**Estado de catalogação:** ⚠️ `RESOURCE_JSON_VERIFIED + SHA_EXACT_SELECTED_BYTECODE_OBSERVED` (escopo parcial). **Contrato técnico estático para perks:** ⚠️ `NOT_CERTIFIED`. **Hooks mutadores:** `NOT_VERIFIED`. **QA física:** `NOT_TESTED`.

## Proveniência e identidade

- **Provider / mod ID:** `Alex's Caves Continued` / `alexscaves`.
- **Versão do artefato:** `alexscaves-1.0.10-neoforge+1.21.1.jar` (Minecraft 1.21.1).
- **JAR SHA-1:** `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`.
- **JAR SHA-256:** `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- **Resource ID exato:** `alexscaves:spirit_dinosaur`.
- **Caminho ZIP:** `data/alexscaves/damage_type/spirit_dinosaur.json`.
- **SHA-256 do JSON:** `82db1eedb1377b9cf24f35db29f646df542da43c7d2c96896ae0bace36014eb4`.
- **Manifesto verificável:** [snapshot dos recursos](EXACT-RESOURCE-MANIFEST-1.0.10.json) e [auditoria da CI](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40985275338).

## Campos JSON confirmados no artefato

| Campo | Valor literal do recurso | Limite de interpretação |
|---|---|---|
| `message_id` | `spirit_dinosaur` | Chave de mensagem; não é sinônimo do registro nem classe de implementação |
| `scaling` | `never` | Campo `scaling` do tipo de dano; não fixa dano causado nem curva de perks |
| `exhaustion` | `0.3` | Valor do campo `exhaustion`; **não** é mana, stamina, custo do feitiço ou dano |

## Tags de tipo de dano declaradas diretamente

- `minecraft:bypasses_cooldown`
- `minecraft:is_fire`

Essas são **entradas textuais diretas** dos seis arquivos `data/*/tags/damage_type/*.json` encontrados no JAR. Elas não comprovam as tags finais resolvidas depois de datapacks, outras dependências ou overrides. Uma referência a tag não prova que o ataque usado no jogo produza este `DamageSource`.
O tag `minecraft:bypasses_cooldown` corresponde à classificação de tipo de dano do Minecraft, **não** demonstra redução/bypass do cooldown de lançamento de magias.


## Superfícies necessárias para perks — ainda não auditadas

| Capacidade pretendida | Situação |
|---|---|
| Factory de `DamageSource` / chamadas JVM | ✅ localizadas estaticamente; comportamento e caminhos efetivos `NÃO VERIFICADO` |
| Origem, atacante, owner, attribution e condições de PvP | ⚠️ caster Player e fallback da lança observados; atribuição final/PvP pendentes |
| Fórmula de dano, mitigação, críticos e resistências | ⚠️ `3+2×enchantment` apenas no Tremorsaurus; impacto da lança e mitigação ainda abertos |
| Alvos elegíveis, tipo target/área, alcance, raio e filtros | ⚠️ lookup por entity ID e colisão da lança observados; alcance/volume e filtros completos pendentes |
| Entidades/projéteis, tamanho, velocidade, colisão e homing | ⚠️ chamada de criação do espírito e retorno da lança observados; spawn real e geometria pendentes |
| Duração, intervalo de hits, custo de ação e cooldown de casting | ⚠️ `dealtDamage` em ordem causal distinta; cooldown/lifetime e hits aceitos pendentes |
| Persistência, ordenação de eventos, server authority e deduplicação | ⚠️ tags `UsingPlayerUUID`/`DinosaurType` observadas; reload e Mastery/deduplicação pendentes |
| Hook de mutação seguro na versão instalada | `NOT_VERIFIED` |
| QA real em modpack/multiplayer | `NOT_TESTED` |

## Boundary / decisão provisória

O *provider* mantém autoridade sobre a criação, classificação e aplicação de dano. Black Arcana não altera `DamageSource`, escola, dano, tags ou projéteis sem evidência dos consumidores Java e hooks seguros. O RPG Skill Tree fornece perks/atributos somente através de boundary verificada, sem double-processing. **Fail-closed:** `NO_MUTATION` até a auditoria dos consumidores e a validação específica.

**Contabilidade:** 1/11 recursos de tipo de dano documentados; **+0 raízes mágicas novas**. Este objeto não recebe status `COMPLETE_PERK_READY` apenas por existir como JSON.

## Evidência compilada 1.0.10 — factory e consumidores diretos

**Escopo:** `SHA_EXACT_STATIC_FACTORY_AND_DIRECT_CALLSITE_ONLY`. [Manifesto dos consumidores](EXACT-CONSUMERS-1.0.10.json) · [CI da auditoria](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40993193816).

- **Classe de fábrica:** `com/github/alexmodguy/alexscaves/server/misc/ACDamageTypes.class`, SHA-256 `389fb88f8d6e1515e3dfe7f401a728bb33629666bd2319ae7e25668f710e4ef6`.
- **Método:** `ACDamageTypes.causeSpiritDinosaurDamage`.
- **Descritor JVM:** `(Lnet/minecraft/core/RegistryAccess;Lnet/minecraft/world/entity/Entity;)Lnet/minecraft/world/damagesource/DamageSource;`.
- **Campo de DamageType lido:** `SPIRIT_DINOSAUR` (offset `19`).
- **Construtor de DamageSource referenciado:** `Method com/github/alexmodguy/alexscaves/server/misc/ACDamageTypes$DamageSourceRandomMessages."<init>":(Lnet/minecraft/core/Holder$Reference;Lnet/minecraft/world/entity/Entity;I)V`.
- **Parâmetros da factory:** `RegistryAccess` e `Entity` — não comprova autoria final.
- **Referências `invokestatic` encontradas:** 2 em 2 classes. Isso não representa quantidade de hits por ataque.

| Classe chamadora | Método chamador | Descritor JVM | Offset | Opcode |
|---|---|---|---:|---|
| `com/github/alexmodguy/alexscaves/server/entity/item/DinosaurSpiritEntity.class` | `private void tickTremorsaurus(net.minecraft.world.entity.player.Player)` | `(Lnet/minecraft/world/entity/player/Player;)V` | 131 | `invokestatic` |
| `com/github/alexmodguy/alexscaves/server/entity/item/ExtinctionSpearEntity.class` | `protected void onHitEntity(net.minecraft.world.phys.EntityHitResult)` | `(Lnet/minecraft/world/phys/EntityHitResult;)V` | 58 | `invokestatic` |

**Limites:** as invocações são referências estáticas no bytecode exato; não demonstram execução, alcance, área, cooldown, fórmula de dano, filtros de alvo, persistência, autoridade/attribution, proteção PvP nem segurança de intercepção. Chamadas indiretas, mixins, reflexão, datapacks e comportamento do modpack não estão comprovados. **`mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NOT_CERTIFIED`**. Black Arcana e RPG Skill Tree devem preservar o settlement nativo, evitando processamento duplicado e aplicando `NO_MUTATION` sem contrato seguro.

## Auditoria do binário 1.0.10 — espírito e lança separados

**Escopo:** `SHA_EXACT_1010_SPIRIT_DINOSAUR_TWO_DAMAGE_CALLERS_SELECTED_METHODS_ONLY`. O [manifesto selado](../EXACT-SPIRIT-DINOSAUR-1.0.10.json) identifica dois arquivos de classe pelo SHA-256, 12 hashes de métodos e 25 offsets críticos. O [probe/testes da PR #988](https://github.com/Gustavaopere/Black-Arcana/pull/988) reexamina o publisher JAR SHA-exato, com janelas curtas de bytecode. Trata-se de observação estática, não de QA executada no modpack.

### Caminho A — `DinosaurSpiritEntity.tickTremorsaurus(Player)`

- A entidade separa `getUsingPlayer()` (associação por UUID), `getAttackingEntity()` (resolução de ID via `Level.getEntity`) e a fonte do dano. Esses papéis não devem ser confundidos em Mastery, crédito de kill ou hooks de PvP.
- O método lê `dealtDamage @116` e, se a flag não bloqueia o caminho, chama `ACDamageTypes.causeSpiritDinosaurDamage(registryAccess, player) @131`.
- O valor **solicitado** a `ACCompat.hurt @143` é **`3 + 2 × getEnchantmentLevel()`**, como demonstram `iconst_3 @134`, `iconst_2 @135`, `getEnchantmentLevel @137`, multiplicação e adição.
- **A flag `dealtDamage` só é marcada em `@151` após o retorno verdadeiro do helper** (`ifeq @146` salta o setter). Retorno falso significa ausência desse update naquele caminho, não autorização para repetir hits pelo Black Arcana.
- `tick()` diferencia `tickSubterranodon`, `tickGrottoceratops` e `tickTremorsaurus`, com condições próprias de movimento, estado, duração e lado lógico. A fórmula acima **não é universal** para todos os tipos de espírito.

### Caminho B — `ExtinctionSpearEntity.onHitEntity(EntityHitResult)`

- A factory de dano `@58` usa `getOwner()` e **faz fallback para a própria entidade da lança quando o owner é nulo** (`ifnonnull @49`, `goto @53`). Uma fonte nula não deve receber atribuição fictícia de Player.
- Diferentemente do espírito, a lança **marca `dealtDamage = true` em `@63–65` antes de `ACCompat.hurt @92`**. Seu `findHitEntity()` lê essa flag para condicionar colisões posteriores. Portanto, a flag da lança não é evidência de que o dano foi aceito.
- O impacto consulta `ACCompat.damageBonus`, solicita `igniteForSeconds @85`, chama `ACCompat.hurt @92` e usa `ifeq @95` para decidir se segue o caminho posterior. A fórmula integral da lança, mitigação e proteções ainda exigem auditoria de CFG.
- O caminho posterior contém `ACCompat.postAttackEffects @139`, `ACEntityRegistry.DINOSAUR_SPIRIT`, `ACCompat.createEntity @168`, `setDinosaurType(SUBTERRANODON) @204`, `setPlayerUUID @214`, `setAttackingEntityId @223`, `PLUMMETING_FLIGHT` via `ACCompat.enchantLevel @248`, e `Level.addFreshEntity @277`. **Referências no bytecode não provam spawn aceito, quantidade de novos espíritos nem procs concedidos.**
- O `tick()` da lança controla retorno ao owner, pickup, velocidade e guardas cliente/servidor; não fixa cooldown de casting ou raio do espírito. A fórmula `3 + 2×enchantment` pertence somente ao `tickTremorsaurus`.

### Persistência, targeting e fronteiras de integração

| Superfície | Evidência observada | Limite |
|---|---|---|
| `UsingPlayerUUID` | `readAdditionalSaveData` e `addAdditionalSaveData` do espírito | UUID persistido não prova que todo ataque futuro credita kills ou Mastery ao jogador |
| `DinosaurType` | Tag NBT e dispatch em `tick` | Cada tipo tem comportamento próprio; não universalizar condições de um tipo |
| `attackingEntityId` | Setter de ID na lança e `Level.getEntity(int)` no espírito | ID volátil não substitui referência persistente/segura de alvo após reload |
| `dealtDamage` | Atualização depois de `hurt` aceito no espírito, antes de `hurt` na lança | Não serve como deduplicador global de dano ou garantia de acerto |
| Encantamentos | `getEnchantmentLevel` e `PLUMMETING_FLIGHT` em pontos diferentes | Não cruzar fórmula de dano do espírito com a da arma nem aplicar custo duplicado |
| Tag do DamageType | `minecraft:bypasses_cooldown` e `minecraft:is_fire` no recurso | Não implica bypass de cooldown mágico, ignição garantida ou proteção PvP homologada |

**Pendências obrigatórias:** guardas completos de criação/atribuição do espírito, fórmula total de dano do impacto, lifetime, alcance, critérios de alvo e WorldEffectPolicy; hooks mutadores; testes físicos com JAR exato em cliente+servidor dedicado, aliados, PvP, efeitos recusados, save/reload e desconexão.

**Decisão:** a ficha permanece ⚠️ `NOT_CERTIFIED`, com `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED` e `NO_MUTATION`. Os dois produtores não criam duas raízes mágicas nem aumentam a contagem global. Black Arcana preserva o settlement nativo; RPG Skill Tree mantém somente progressão, perks e Mastery via contratos verificados.
