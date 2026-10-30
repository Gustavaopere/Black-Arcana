# Desolate Dagger — tipo de dano `alexscaves:desolate_dagger` (1.0.10)

**Estado de catalogação:** ⚠️ `RESOURCE_JSON_VERIFIED` (recurso SHA-exato). **Contrato técnico estático para perks:** ⚠️ `NOT_CERTIFIED`. **Hooks mutadores:** `NOT_VERIFIED`. **QA física:** `NOT_TESTED`.

## Proveniência e identidade

- **Provider / mod ID:** `Alex's Caves Continued` / `alexscaves`.
- **Versão do artefato:** `alexscaves-1.0.10-neoforge+1.21.1.jar` (Minecraft 1.21.1).
- **JAR SHA-1:** `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`.
- **JAR SHA-256:** `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- **Resource ID exato:** `alexscaves:desolate_dagger`.
- **Caminho ZIP:** `data/alexscaves/damage_type/desolate_dagger.json`.
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

Essas são **entradas textuais diretas** dos seis arquivos `data/*/tags/damage_type/*.json` encontrados no JAR. Elas não comprovam as tags finais resolvidas depois de datapacks, outras dependências ou overrides. Uma referência a tag não prova que o ataque usado no jogo produza este `DamageSource`.
O tag `minecraft:bypasses_cooldown` corresponde à classificação de tipo de dano do Minecraft, **não** demonstra redução/bypass do cooldown de lançamento de magias.


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
- **Método:** `ACDamageTypes.causeDesolateDaggerDamage`.
- **Descritor JVM:** `(Lnet/minecraft/core/RegistryAccess;Lnet/minecraft/world/entity/Entity;)Lnet/minecraft/world/damagesource/DamageSource;`.
- **Campo de DamageType lido:** `DESOLATE_DAGGER` (offset `19`).
- **Construtor de DamageSource referenciado:** `Method com/github/alexmodguy/alexscaves/server/misc/ACDamageTypes$DamageSourceRandomMessages."<init>":(Lnet/minecraft/core/Holder$Reference;Lnet/minecraft/world/entity/Entity;I)V`.
- **Parâmetros da factory:** `RegistryAccess` e `Entity` — não comprova autoria final.
- **Referências `invokestatic` encontradas:** 1 em 1 classes. Isso não representa quantidade de hits por ataque.

| Classe chamadora | Método chamador | Descritor JVM | Offset | Opcode |
|---|---|---|---:|---|
| `com/github/alexmodguy/alexscaves/server/entity/item/DesolateDaggerEntity.class` | `public void tick()` | `()V` | 339 | `invokestatic` |

**Limites:** as invocações são referências estáticas no bytecode exato; não demonstram execução, alcance, área, cooldown, fórmula de dano, filtros de alvo, persistência, autoridade/attribution, proteção PvP nem segurança de intercepção. Chamadas indiretas, mixins, reflexão, datapacks e comportamento do modpack não estão comprovados. **`mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NOT_CERTIFIED`**. Black Arcana e RPG Skill Tree devem preservar o settlement nativo, evitando processamento duplicado e aplicando `NO_MUTATION` sem contrato seguro.

## Aprofundamento de fluxo — 1.0.10 (instruções compiladas)

**Evidência estática delimitada:** [manifesto de janelas e branch opcodes](EXACT-DAMAGE-PATH-ANCHORS-1.0.10.json), auditado no JAR SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. Classe `com/github/alexmodguy/alexscaves/server/entity/item/DesolateDaggerEntity.class` (SHA-256 `f82a3f5f1cc05bbe52dfb7e3742f33c2289cbc37810b069a53b45002cfeb4351`). Método `public void tick()`, descritor JVM `()V`; 361 instruções extraídas e 20 anchors de branch registrados. Resumo de chamadas diretas: `causeDesolateDaggerDamage` @ `339`.

- Em `tick()`, o método referencia `ACEnchantmentRegistry.IMPENDING_STAB` no offset `317` e `ACCompat.enchantLevel()` no `320`; a factory de tipo de dano é chamada em `339`.
- O offset `344` referencia `ACCompat.hurt()`, seguido pelo desvio `ifeq` em `347`; também existem referências ao descarte da entidade, mas os motivos e o número efetivo de impactos não foram comprovados.
- São pontos relevantes para perks de encantamentos e targeting, sem autorização de mutação ou garantia de proc único.

**Limite metodológico:** offsets, referências de método, testes e desvios são provas do *bytecode*; a análise não reconstruiu exceções, switch dispatch, todos os caminhos de CFG ou condições de runtime. `NOT_CERTIFIED` para comportamento integral; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`. Black Arcana não deve substituir settlement, autorizações de servidor, segurança do mundo ou rotinas próprias do provider.

## Helpers de dano e encantamentos no JAR 1.0.10

**Grau da prova:** `SHA_EXACT_HELPER_ABI_AND_BYTECODE`. [Manifesto fixado](EXACT-DAMAGE-HELPERS-1.0.10.json) e [CI da auditoria](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40997154302). A classe `com/github/alexmodguy/alexscaves/server/misc/ACCompat.class` possui SHA-256 `333738f324e6e9d77a488e14b7e81b169c2b2d4f6db5171206a016ad0271f57b`.

- `public static int enchantLevel(net.minecraft.world.item.ItemStack, net.minecraft.resources.ResourceKey<net.minecraft.world.item.enchantment.Enchantment>)`, descritor `(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/resources/ResourceKey;)I`, método SHA-256 `775387837bd0e7dbbd2fd04cd5de0375a6ccd2813de5db375fd152f8b63ad8dc`: consulta `ItemStack.getEnchantments()`, itera `ItemEnchantments.entrySet()`, compara a chave com `Holder.is(ResourceKey)`, retorna `Entry.getIntValue()` quando coincide ou zero (`iconst_0`) ao final.
- Essa consulta é o helper lido por `DesolateDaggerEntity.tick()` junto à chave `IMPENDING_STAB` identificada no lote #959. **A leitura da chave não comprova** o efeito desse encantamento na magnitude do dano sem auditoria do caller completo.
- `public static boolean hurt(net.minecraft.world.entity.Entity, net.minecraft.world.damagesource.DamageSource, float)`, descritor `(Lnet/minecraft/world/entity/Entity;Lnet/minecraft/world/damagesource/DamageSource;F)Z`, método SHA-256 `77997f2089224cd768dc079fb789bc5ffa96c8647bf5c0cabe932b8c3a3702b5`: o wrapper passa os três argumentos a `Entity.hurt(DamageSource,float)` e retorna diretamente o booleano; não altera dano nem aplica pós-processamento nele mesmo.

**Para perks:** nível de encantamento, owner, procura de alvo, frequência de impacto, condições de cooldown e semântica do método chamado `Entity.hurt` devem ser respeitados. A extensão segura ainda não foi comprovada. `NOT_CERTIFIED` / `NOT_VERIFIED` / `NOT_TESTED` / `NO_MUTATION`.
