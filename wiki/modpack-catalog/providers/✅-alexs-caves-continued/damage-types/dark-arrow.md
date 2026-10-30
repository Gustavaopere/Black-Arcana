# Dark Arrow — tipo de dano `alexscaves:dark_arrow` (1.0.10)

**Estado de catalogação:** ⚠️ `RESOURCE_JSON_VERIFIED` (recurso SHA-exato). **Contrato técnico estático para perks:** ⚠️ `NOT_CERTIFIED`. **Hooks mutadores:** `NOT_VERIFIED`. **QA física:** `NOT_TESTED`.

## Proveniência e identidade

- **Provider / mod ID:** `Alex's Caves Continued` / `alexscaves`.
- **Versão do artefato:** `alexscaves-1.0.10-neoforge+1.21.1.jar` (Minecraft 1.21.1).
- **JAR SHA-1:** `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`.
- **JAR SHA-256:** `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- **Resource ID exato:** `alexscaves:dark_arrow`.
- **Caminho ZIP:** `data/alexscaves/damage_type/dark_arrow.json`.
- **SHA-256 do JSON:** `a8c5a9d4d72a4c064c1b0fca923d2059eb6b718e9866fb8d19dc539bb0ffec93`.
- **Manifesto verificável:** [snapshot dos recursos](EXACT-RESOURCE-MANIFEST-1.0.10.json) e [auditoria da CI](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40985275338).

## Campos JSON confirmados no artefato

| Campo | Valor literal do recurso | Limite de interpretação |
|---|---|---|
| `message_id` | `desolate_dagger` | Chave de mensagem; não é sinônimo do registro nem classe de implementação |
| `scaling` | `never` | Campo `scaling` do tipo de dano; não fixa dano causado nem curva de perks |
| `exhaustion` | `0.3` | Valor do campo `exhaustion`; **não** é mana, stamina, custo do feitiço ou dano |

## Tags de tipo de dano declaradas diretamente

- `minecraft:bypasses_cooldown`
- `minecraft:is_projectile`
- `minecraft:no_impact`

Essas são **entradas textuais diretas** dos seis arquivos `data/*/tags/damage_type/*.json` encontrados no JAR. Elas não comprovam as tags finais resolvidas depois de datapacks, outras dependências ou overrides. Uma referência a tag não prova que o ataque usado no jogo produza este `DamageSource`.
O tag `minecraft:bypasses_cooldown` corresponde à classificação de tipo de dano do Minecraft, **não** demonstra redução/bypass do cooldown de lançamento de magias.


**Ponto de atenção — divergência de nomenclatura:** o arquivo `dark_arrow.json` define `message_id: "desolate_dagger"`, exatamente como `desolate_dagger.json`, e ambos têm o mesmo SHA-256 de conteúdo. São **dois resource IDs diferentes**; não corrigir o JSON nem mesclar os IDs. Isto não prova que dois ataques compartilhem fórmula, alvo ou lógica Java.

## Superfícies necessárias para perks — ainda não auditadas

| Capacidade pretendida | Situação |
|---|---|
| Factory de `DamageSource` / chamadas JVM | ✅ localizadas estaticamente; comportamento e caminhos efetivos `NÃO VERIFICADO` |
| Origem, atacante, owner, attribution e condições de PvP | `NÃO VERIFICADO` |
| Fórmula de dano, mitigação, críticos e resistências | `NÃO VERIFICADO` |
| Alvos elegíveis, tipo target/área, alcance, raio e filtros | `NÃO VERIFICADO` |
| Entidades/projéteis, tamanho, velocidade, colisão e homing | `NÃO VERIFICADO` |
| Duração, intervalo de hits, custo de ação e cooldown de casting | `NÃO VERIFICADO` |
| Persistência, ordenação de eventos, server authority e deduplicação | `NÃO VERIFICADO` |
| Hook de mutação seguro na versão instalada | `NOT_VERIFIED` |
| QA real em modpack/multiplayer | `NOT_TESTED` |

## Boundary / decisão provisória

O *provider* mantém autoridade sobre a criação, classificação e aplicação de dano. Black Arcana não altera `DamageSource`, escola, dano, tags ou projéteis sem evidência dos consumidores Java e hooks seguros. O RPG Skill Tree fornece perks/atributos somente através de boundary verificada, sem double-processing. **Fail-closed:** `NO_MUTATION` até a auditoria dos consumidores e a validação específica.

**Contabilidade:** 1/11 recursos de tipo de dano documentados; **+0 raízes mágicas novas**. Este objeto não recebe status `COMPLETE_PERK_READY` apenas por existir como JSON.

## Evidência compilada 1.0.10 — factory e consumidores diretos

**Escopo:** `SHA_EXACT_STATIC_FACTORY_AND_DIRECT_CALLSITE_ONLY`. [Manifesto dos consumidores](EXACT-CONSUMERS-1.0.10.json) · [CI da auditoria](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40993193816).

- **Classe de fábrica:** `com/github/alexmodguy/alexscaves/server/misc/ACDamageTypes.class`, SHA-256 `389fb88f8d6e1515e3dfe7f401a728bb33629666bd2319ae7e25668f710e4ef6`.
- **Método:** `ACDamageTypes.causeDarkArrowDamage`.
- **Descritor JVM:** `(Lnet/minecraft/core/RegistryAccess;Lnet/minecraft/world/entity/Entity;)Lnet/minecraft/world/damagesource/DamageSource;`.
- **Campo de DamageType lido:** `DARK_ARROW` (offset `19`).
- **Construtor de DamageSource referenciado:** `Method com/github/alexmodguy/alexscaves/server/misc/ACDamageTypes$DamageSourceRandomMessages."<init>":(Lnet/minecraft/core/Holder$Reference;Lnet/minecraft/world/entity/Entity;I)V`.
- **Parâmetros da factory:** `RegistryAccess` e `Entity` — não comprova autoria final.
- **Referências `invokestatic` encontradas:** 1 em 1 classes. Isso não representa quantidade de hits por ataque.

| Classe chamadora | Método chamador | Descritor JVM | Offset | Opcode |
|---|---|---|---:|---|
| `com/github/alexmodguy/alexscaves/server/entity/item/DarkArrowEntity.class` | `protected void onHitEntity(net.minecraft.world.phys.EntityHitResult)` | `(Lnet/minecraft/world/phys/EntityHitResult;)V` | 37 | `invokestatic` |

**Limites:** as invocações são referências estáticas no bytecode exato; não demonstram execução, alcance, área, cooldown, fórmula de dano, filtros de alvo, persistência, autoridade/attribution, proteção PvP nem segurança de intercepção. Chamadas indiretas, mixins, reflexão, datapacks e comportamento do modpack não estão comprovados. **`mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NOT_CERTIFIED`**. Black Arcana e RPG Skill Tree devem preservar o settlement nativo, evitando processamento duplicado e aplicando `NO_MUTATION` sem contrato seguro.

## Aprofundamento de fluxo — 1.0.10 (instruções compiladas)

**Evidência estática delimitada:** [manifesto de janelas e branch opcodes](EXACT-DAMAGE-PATH-ANCHORS-1.0.10.json), auditado no JAR SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. Classe `com/github/alexmodguy/alexscaves/server/entity/item/DarkArrowEntity.class` (SHA-256 `089f0a65444078ca42fc1da2d5023384314ef5f5283ddf3fe8484bf31d4136ad`). Método `protected void onHitEntity(net.minecraft.world.phys.EntityHitResult)`, descritor JVM `(Lnet/minecraft/world/phys/EntityHitResult;)V`; 48 instruções extraídas e 7 anchors de branch registrados. Resumo de chamadas diretas: `causeDarkArrowDamage` @ `37`.

- Em `onHitEntity(EntityHitResult)`, o método referencia `getShadowArrowDamage()` em `11`, `isPerfectShot()` em `17` e a factory em `37`.
- O mesmo método possui referências a `Entity.isAlliedTo()` nos offsets `56` e `64` e a `ACCompat.hurt()` em `82`, registradas como invocações simbólicas do método; as janelas de invocação não constituem prova de reachability.
- Não é seguro promover a possibilidade de friendly-fire, valor de dano ou aumento de precisão sem seguir os saltos, o destino dos operandos e o corpo de `ACCompat.hurt()`.

**Limite metodológico:** offsets, referências de método, testes e desvios são provas do *bytecode*; a análise não reconstruiu exceções, switch dispatch, todos os caminhos de CFG ou condições de runtime. `NOT_CERTIFIED` para comportamento integral; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`. Black Arcana não deve substituir settlement, autorizações de servidor, segurança do mundo ou rotinas próprias do provider.

## Helpers de dano e tiro perfeito no JAR 1.0.10

**Grau da prova:** `SHA_EXACT_HELPER_ABI_AND_BYTECODE`. [Manifesto fixado](EXACT-DAMAGE-HELPERS-1.0.10.json) e [CI da auditoria](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40997154302).

- `public float getShadowArrowDamage()` — `()F`, SHA-256 do método `afe89892cb041a585baf6a4c38a5877942193db84612d830d0f2babdc7c080cf`: lê `SynchedEntityData.get` pelo accessor `SHADOW_ARROW_DAMAGE`, converte `Float.floatValue()` e retorna. **Não** calcula a fórmula de dano nem mostra quando o accessor foi definido.
- `public boolean isPerfectShot()` — `()Z`, SHA-256 do método `c91a50e4a585ac94cd3a7680b8b7faaebe31351cc261c057ae469909551a99cd`: lê `SynchedEntityData.get` pelo accessor `PERFECT_SHOT`, converte `Boolean.booleanValue()` e retorna. **Não** indica por si só chance de tiro perfeito, atribuição ou definição do flag.
- Ambos pertencem a `com/github/alexmodguy/alexscaves/server/entity/item/DarkArrowEntity.class` (SHA-256 `089f0a65444078ca42fc1da2d5023384314ef5f5283ddf3fe8484bf31d4136ad`).
- `public static boolean hurt(net.minecraft.world.entity.Entity, net.minecraft.world.damagesource.DamageSource, float)` — `(Lnet/minecraft/world/entity/Entity;Lnet/minecraft/world/damagesource/DamageSource;F)Z` na classe `com/github/alexmodguy/alexscaves/server/misc/ACCompat.class` (SHA-256 `333738f324e6e9d77a488e14b7e81b169c2b2d4f6db5171206a016ad0271f57b`). Seu bytecode possui cinco instruções e encaminha `Entity, DamageSource, float` para `Entity.hurt(DamageSource,float)`, retornando diretamente o booleano; não há branch próprio nesse wrapper.

**Para perks:** a origem do valor armazenado, os pontos de escrita, o cálculo de `PERFECT_SHOT`, a validação de aliança e os efeitos de `Entity.hurt` ainda exigem evidência específica. `NOT_CERTIFIED` / `NOT_VERIFIED` / `NOT_TESTED` / `NO_MUTATION`. Não duplicar settlement nem substituir o targeting do projectile.

## Escrita e inicialização do estado sincronizado — auditoria JVM 1.0.10

**Autoridade desta seção:** [manifesto SHA-exato das referências](EXACT-DARK-ARROW-STATE-1.0.10.json) e [auditoria CI](https://github.com/Gustavaopere/Black-Arcana/actions/runs/41001621930); JAR publisher 1.0.10, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. A análise não usa a fonte pública 1.1.1 para atribuir comportamento à build instalada.

### Entidade — `DarkArrowEntity`

Classe `com/github/alexmodguy/alexscaves/server/entity/item/DarkArrowEntity.class` (SHA-256 `089f0a65444078ca42fc1da2d5023384314ef5f5283ddf3fe8484bf31d4136ad`).

| Método compilado | Descritor JVM | Referências exatas | Limite |
|---|---|---|---|
| `defineSynchedData` | `(Lnet/minecraft/network/syncher/SynchedEntityData$Builder;)V` | `SHADOW_ARROW_DAMAGE` no offset `6` e `Builder.define` no `13` com `fconst_0` no `9`; `PERFECT_SHOT` no `18` e `Builder.define` no `25` com `iconst_0` no `21` | Defaults compilados `0.0f` e `false`, não valores finais de todos os projéteis |
| `setShadowArrowDamage` | `(F)V` | `SHADOW_ARROW_DAMAGE` no offset `4`; `SynchedEntityData.set` no `11` | Armazena o parâmetro float, não certifica caller autorizado |
| `setPerfectShot` | `(Z)V` | `PERFECT_SHOT` no offset `4`; `SynchedEntityData.set` no `11` | Armazena booleano, não comprova origem ou chance de proc |
| `getShadowArrowDamage` | `()F` | `SynchedEntityData.get` no offset `7` | Leitura do accessor; não substitui fórmula de dano |
| `isPerfectShot` | `()Z` | `SynchedEntityData.get` no offset `7` | Leitura do flag; não certifica targeting |

### Equipamento consumidor — `DreadbowItem`

Classe `com/github/alexmodguy/alexscaves/server/item/DreadbowItem.class` (SHA-256 `b9cd6e843f923877775e38b89214e8649c10d4d5be704ed9dd377900439d44ae`).

| Método/rota | Descriptor JVM | Ponto de escrita observado | Natureza da evidência |
|---|---|---|---|
| `releaseUsing` | `(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;I)V` | `setShadowArrowDamage(float)` no offset `402`, após seleção local `fconst_2` (395) / `ldc_w float 3.0f` (399) e desvio `goto 402` (396) | Argumento bruto `2.0f` ou `3.0f`, condicionado pelo controle anterior (`iload 8`/ `ifeq` em 392); não se infere a origem do flag |
| `releaseUsing` | `(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;I)V` | `setPerfectShot(boolean)` no offset `409` após `iload 10` no `407` | Repassa booleano local; a condição que o construiu ainda carece de auditoria dedicada |
| `onUseTick` | `(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/item/ItemStack;I)V` | `setShadowArrowDamage(float)` no offset `196`, após `fconst_2` em `195` | Argumento bruto compilado `2.0f`; não comprova um disparo efetivo ou target |

Os três pontos acima foram encontrados por referências diretas do bytecode de `DreadbowItem`; o manifesto inclui também referências de rendering no cliente, que **não** constituem escrita de dano no servidor. Este inventário de cinco classes candidatas e quatro classes selecionadas não cobre reflexão, herança, mixins, datapacks nem consumidores externos.

### Restrições para Black Arcana / perks

Os accessors sincronizados pertencem ao provider. **Não** assumir que `setShadowArrowDamage` ou `setPerfectShot` é um hook público estável para manipulação de perks, nem que esses argumentos equivalem ao dano recebido no settlement de `Entity.hurt`. Faltam os cálculos completos do `DreadbowItem`, a origem dos flags, autoridade de servidor, colisões, filtros de aliados, cooldown e multiplayer. `NOT_CERTIFIED` / `mutating_hook=NOT_VERIFIED` / `physical_qa=NOT_TESTED` / `NO_MUTATION`.
