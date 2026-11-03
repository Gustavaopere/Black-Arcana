# Double Stab — multiplicação de dagas do Desolate Dagger (publisher 1.0.10)

**Estado:** ⚠️ ficha individual **parcial/condicionada** para `alexscaves:double_stab`. A identidade do recurso, o registro e o consumidor compilado já foram documentados na auditoria SHA-exata do Desolate Dagger. Esta ficha faz o crosswalk do encantamento para perks sem criar um novo certificado individual, hook ou runtime. **`claim_scope=EXISTING_SHA_EXACT_CONTRACT_REUSE` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED` · `perk_certification=NOT_CERTIFIED` · `NO_MUTATION`.**

**Comportamento delimitado:** Double Stab altera a **quantidade de tentativas de criar entidades Desolate Dagger** depois que o callback de ataque da arma passa no gate nativo. Sem encantamento, o loop tenta uma entidade; com o nível I normal, tenta duas. Cada entidade recebe o **mesmo ID de alvo** e seu próprio contador inicial de órbita. Não há segunda ação/cast, mudança automática no dano individual, nem garantia de dois spawns ou dois hits aceitos.

## 1. Autoridade e provenance

| Superfície | Evidência existente do artefato 1.0.10 |
|---|---|
| Mod / plataforma | Alex's Caves Continued, mod ID `alexscaves`, Minecraft 1.21.1 / NeoForge |
| JAR publisher | `alexscaves-1.0.10-neoforge+1.21.1.jar`, 75.279.314 bytes; CurseForge projeto `1645389`, arquivo `8856293` |
| SHA-1 do JAR | `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570` |
| SHA-256 do JAR | `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c` |
| Encantamento | `data/alexscaves/enchantment/double_stab.json`; SHA-256 `554b3d0fb8e157ef912716cba8180b43cae340f01ee64ca931465b1d2884ff71` |
| Tag de itens | `data/alexscaves/tags/item/enchantable/desolate_dagger.json`; SHA-256 `c350c3e59d1bbff4d9fd24fa54c96e5fa075682f862c9eba0081c4ef2b97b264` |
| Registry compilado | `server/enchantment/ACEnchantmentRegistry.class`; SHA-256 `60006fab1b3b29f5f93c8365416815a12770cf8877a059298cb4ee82f7a92f32` |
| Producer compilado | `server/item/DesolateDaggerItem.class`; SHA-256 `ca020279666b45f5d8ede7082ba20c026a870989a6d90166fd1587af921a95ef` |
| Entidade consumidora | `server/entity/item/DesolateDaggerEntity.class`; SHA-256 `f82a3f5f1cc05bbe52dfb7e3742f33c2289cbc37810b069a53b45002cfeb4351` |

Fontes de autoridade reutilizadas: [manifesto binário exato](../EXACT-DESOLATE-DAGGER-CONTRACTS-1.0.10.json), [memorial e reprodução](../EXACT-DESOLATE-DAGGER-CONTRACTS-1.0.10.md), [equipamento/produtor](../equipment/desolate-dagger.md) e [entidade/dano](../damage-types/desolate-dagger.md). A fonte pública `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` declara **1.1.1**; seus métodos **não** foram equiparados ao JAR 1.0.10. Esta inclusão reutiliza provas seladas e **não afirma ter reaberto ou executado novamente o JAR**.

## 2. Definição do encantamento e disponibilidade

| Campo do JSON publisher | Valor documentado no recorte exato |
|---|---|
| ID de registro | `alexscaves:double_stab`; `ACEnchantmentRegistry.<clinit>()V @374–380` vincula `DOUBLE_STAB` |
| `supported_items` | `#alexscaves:enchantable/desolate_dagger`, incluindo `alexscaves:desolate_dagger` na tag |
| `weight` | **2** — peso de encantamento, não chance de ativação do golpe |
| `max_level` | **1** (I) |
| `min_cost` | `base=1`, `per_level_above_first=12` |
| `max_cost` | `base=41`, `per_level_above_first=10` |
| `anvil_cost` | **4** |
| `slots` | `mainhand` |
| `exclusive_set` no próprio `double_stab.json` | **Não declarado** no recorte documentado; `impending_stab.json` declara `exclusive_set: [alexscaves:double_stab]` |

No nível I, o intervalo declarativo mínimo/máximo de encantamento é **1–41**. Os custos de encantamento/bigorna não são mana, stamina, durabilidade gasta por entidade, nem cooldown de ataque. A **aplicação real** dos itens elegíveis, da exclusão e dos custos depende de dados resolvidos pelo jogo e outros mods; a declaração assimétrica no JSON adjacente não comprova por si só o comportamento final de todas as rotas de enchanting, bigorna ou comandos.

## 3. Producer, ordem de execução e fórmula de quantidade

**Entrada de combate:** `DesolateDaggerItem.hurtEnemy(ItemStack,LivingEntity,LivingEntity)Z`, descritor JVM `(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/entity/LivingEntity;)Z`. A ordem é **stack, vítima, atacante**. Em `@0–4`, chama `SwordItem.hurtEnemy`. Em `@7–14`, chama `acSpawnDaggers` **somente se o retorno do método-base for verdadeiro**. Isso não homologa um hit primário aceito em todas as condições de combate, nem a execução em servidor sob qualquer mod de animação.

**Consumidor específico:** `DesolateDaggerItem.acSpawnDaggers(ItemStack,LivingEntity,LivingEntity)V`, mesmo trio de argumentos, com descritor `(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/entity/LivingEntity;)V`.

1. `@0–7`: lê **uma vez** o nível de `IMPENDING_STAB`; não é o valor que controla quantas entidades serão tentadas.
2. `@9–23`: inicia `i=0` e, **em cada teste do loop**, lê `DOUBLE_STAB` por `ACCompat.enchantLevel(stack,DOUBLE_STAB)` (`@16–19`). O limite é **`i < 1 + L`**, com `L` igual ao nível então retornado pelo helper.
3. `@26–47`: solicita `ACEntityRegistry.DESOLATE_DAGGER` via `ACCompat.createEntity(type,attacker.level())`; esse wrapper delega à factory de entidades.
4. `@49–67`: grava o ID inteiro da **vítima** por `setTargetId(victim.getId())`, copia a posição do **atacante** por `copyPosition(attacker)` e passa o stack para `setItemStack(stack)`. O produtor não chama `setPlayerId` nem faz `ItemStack.copy()` nesses caminhos.
5. `@70–96`: cada entidade recebe `orbitFor=(Impending>0 ? 40 : 20)+attacker.getRandom().nextInt(10)`, isto é, **40–49** ou **20–29 ticks** de contador inicial. O sorteio é por iteração, sem prova de independência estatística efetiva em jogo.
6. `@99–108`: solicita `attacker.level().addFreshEntity(dagger)` e descarta o booleano de retorno. Depois incrementa `i` e reavalia o nível para a próxima iteração (`@109–115`).

**Quantidade normal de tentativas**, se `L` for estável e não negativo:

| Estado | Nível | Tentativas no loop | Spawns / impactos garantidos |
|---|---:|---:|---|
| Sem Double Stab | 0 | 1 | **Não** |
| Double Stab I (máximo JSON) | 1 | 2 | **Não** |
| Nível não convencional | `L > 1` | `1+L`, se estável | **Não**; sem clamp próprio nesse método |

A consulta do nível **não é congelada** antes do loop: mutação do stack durante `addFreshEntity`, níveis anômalos e outros hooks podem alterar quantas vezes o limite é avaliado. O método não apresenta guarda própria de factory nula antes de usar a referência. Não reinterpretar `1+L` como quantidade garantida de entidades, golpes, triggers de dano ou XP.

## 4. Targeting, geometria, dano e ciclo de vida downstream

O Double Stab não cria um seletor AoE: cada entidade fica vinculada pelo **mesmo ID inteiro de vítima**, sem checagem adicional de distância, LOS, classe de alvo, autorização PvP ou claim no produtor. É a [entidade nativa](../damage-types/desolate-dagger.md) que resolve `level().getEntity(targetId)`; IDs ausentes/mortos, mudança de dimensão e colisões de IDs são dependências separadas.

A `DesolateDaggerEntity` tem dimensões de registro **0,6 × 0,6**, categoria `MISC` e velocidade/atualização próprias. Durante o tick, orbita com offset baseado na posição/largura/altura da vítima e, no servidor, decrementa `orbitFor` enquanto o alvo está vivo. Caso contrário, ou após a contagem, incrementa `STAB` até 1 com **`min(STAB+0.2F,1F)`**; só então solicita o ataque. Dimensão de entidade, raio de seleção, comprimento de lâmina e alcance de cast são conceitos distintos: **nenhum raio ou alcance de Double Stab foi identificado no loop produtor**.

No stab, **cada entidade** consulta o nível de `IMPENDING_STAB` no stack associado e pede `2F+2F*level(IMPENDING_STAB)` ao dano `alexscaves:desolate_dagger` via `ACCompat.hurt`. Sem Impending, o pedido base é **2F por entidade**. O pedido **não equivale a dano líquido** após armadura, invulnerabilidade, eventos, i-frames e regras do servidor. Duas tentativas de spawn, portanto, não provam duas chamadas de dano, dois acertos ou dano dobrado na vítima.

Em caso de dano aceito, `SATED_BLADE` pode solicitar ganho de saturação **somente** se a autoria resolvida for `Player` e a saturação for inferior a 5F. Como `PLAYER_ID` nasce em `-1` e não é preenchido pelo produtor observado, a posse da arma **não comprova** essa condição. O descarte da entidade após a tentativa de dano ocorre também quando o pedido é recusado. Double Stab não possui duração de aura, buff, cooldown ou projétil próprio além dessas entidades nativas; há contadores e recursos do equipamento e da entidade que permanecem sob seus respectivos owners.

## 5. Parâmetros de perks e limites de integração

| Eixo de perk | Contrato observado | Limite de interoperabilidade |
|---|---|---|
| **Quantidade / multishot** | `1+L` tentativas sob `acSpawnDaggers` | ⛔ Sem hook mutador certificado; não chamar novamente o callback ou adicionar entidades paralelas |
| **Damage / damage type** | `2+2*ImpendingLevel` solicitado **por entidade** em `DesolateDaggerEntity.tick`; `desolate_dagger` como DamageType | ⛔ Double Stab não altera a fórmula individual; observar dano aceito sem settlement duplicado |
| **Target / área / range** | ID da mesma vítima, sem seleção em área no produtor | ⛔ Não converter em AoE ou novos alvos a partir de setters sem autorização e regras de proteção |
| **Tempo / frequência** | Timer por entidade `20–29` ou `40–49`; progressão de `STAB` em cinco incrementos normais | ⛔ Não inferir dois impactos simultâneos, cooldown próprio ou sincronismo entre entidades |
| **Projétil / tamanho / velocidade** | Entidade `MISC` 0,6 × 0,6; movimento resolvido no tick nativo | ⛔ Não assumir API de alteração de hitbox, trajetória, velocidade ou alcance |
| **Custo / recursos** | `SwordItem.hurtEnemy` chamado uma vez antes do spawn; nenhuma cobrança adicional por dagger nos métodos próprios observados | ⛔ Não duplicar durabilidade/mana, não converter custo de encantamento em custo de cast |
| **Autoria / Mastery / XP** | `TARGET_ID` é definido; `PLAYER_ID` não é preenchido nesse produtor | ⛔ Não atribuir procs por mera tentativa de spawn; deduplicação e autoria precisam de contrato do combate real |
| **Exclusividade / níveis externos** | Máximo normal I; Impending declara exclusão de Double Stab; sem clamp no loop | ⛔ Validar dados ativos, enchanting e entradas anômalas antes de alterar `L` |

**Boundary:** Alex's Caves é dono de ataque, criação, temporizadores, dano, desgaste e efeitos. Black Arcana não deve assumir esse runtime; RPG Skill Tree é provider de progressão/atributos/Mastery/perks/gates apenas por boundary real; Enshrouded não ganha automaticamente controle do consumidor. Sem hook seguro, **fail-closed** para mutações. Observar uma saída confirmada, caso futuramente exista evento estável e teste de autoria, é diferente de reproduzir o hit ou reexecutar spawn.

## 6. Verificação restante e contabilização

**Evidência já selada:** JSON com seus hashes e metadados, tag, registro da chave, `acSpawnDaggers @0–115`, `hurtEnemy @0–20`, helper `ACCompat.enchantLevel`, entidade e dano downstream. Não há nova inspeção física do JAR nesta ficha; o documento consolida **provas previamente existentes**, não certifica bytecode de classes fora do manifesto.

**QA física ainda `NOT_TESTED`:** enchanting/bigorna e exclusividade real; ataque vanilla vs Epic Fight/Better Combat; servidor dedicado e cliente; nível alterado no loop; spawn recusado ou factory nula; alvo morto/descarregado/trocado; divergência de dimensão; stack atualizado durante a órbita; i-frames e dano recusado; eventos/procs de duas entidades; custo efetivo, PvP/claims, save/reload e lag em multiplayer. Verificar proteção e deduplicação no sistema que efetivamente possui autoridade antes de habilitar qualquer perk.

**Contabilidade:** +1 ficha individual **parcial** de encantamento; +0 contratos estáticos individuais certificados; +0 raízes mágicas; +0 providers encerrados; +0 hooks validados; +0 testes físicos realizados. Próximo encantamento alfabético: `alexscaves:energy_efficiency`.