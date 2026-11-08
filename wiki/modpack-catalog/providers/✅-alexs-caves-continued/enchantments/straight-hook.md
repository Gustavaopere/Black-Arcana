# Straight Hook — `alexscaves:straight_hook` (1.0.10)

**Estado:** ✅ contrato técnico estático individual SHA-exato. **Hook mutador:** `NOT_VERIFIED`; **QA física:** `NOT_TESTED`; **runtime:** `NO_MUTATION`. Esta conclusão documenta comportamento compilado, não trajetória testada no cliente.

## 1. Identidade, fonte e descrição

- Provider: **Alex's Caves Continued**, mod ID `alexscaves`, Minecraft 1.21.1 / NeoForge / Java 21.
- JAR físico: `alexscaves-1.0.10-neoforge+1.21.1.jar`, CurseForge arquivo `8856293`, **75.279.314 bytes**, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- Registro de encantamento `alexscaves:straight_hook`; `data/alexscaves/enchantment/straight_hook.json` (**369 bytes**, SHA-256 `75508b5c035e6e240a17ca3e31a4757838cb03e6b7f444e2ece49df284cc3b6f`).
- Tag `#alexscaves:enchantable/candy_cane_hook` contém somente `alexscaves:candy_cane_hook`; SHA-256 `b1d1990dd02fec11c14976f0f0a893e30b6c25e443efc013428cbdd4ef334310`.
- Descrição própria: o encantamento grava no gancho recém-construído um estado sincronizado de resistência à gravidade. Durante voo sem recolhimento, o retorno de gravidade torna-se zero enquanto a velocidade horizontal é superior ao limiar compilado. A descrição oficial em inglês menciona lançamento à frente; não foi constatado um segundo vetor de lançamento específico causado por esse encantamento.

## 2. Ativação, owner e ordem causal

`CandyCaneHookItem.use(Level, Player, InteractionHand)` é o produtor nativo. A chamada de uso constrói `CandyCaneHookEntity(Player,Level,ItemStack,boolean)` com a stack usada sob as condições de lançamento e as guardas de lado servidor descritas nas auditorias anteriores [Sharp Cane](sharp-cane.md) e [Far Flung](far-flung.md). O item pede inserção da entidade e registra UUID/reeling na stack; esses pedidos não provam sucesso físico de spawn ou colisão.

**No construtor exato de 231 instruções**, `@437–440` lê `ACEnchantmentRegistry.STRAIGHT_HOOK` por `ACCompat.enchantLevel(stack, key)`. `ifle 460 @443` deixa o estado padrão para nível `<=0`; nível positivo leva `@446–457` a escrever `Boolean.TRUE` no campo `RESISTS_GRAVITY` de `SynchedEntityData`. O valor é capturado na criação, sem releitura contínua do nível da stack no método de gravidade.

## 3. Parâmetro exato e condição de gravidade

O método `CandyCaneHookEntity.getDefaultGravity()D` tem **20 instruções completas**, SHA-256 de representação JVM parseada `6661bcce0135dbf5e4a239c8277c9ca7ebc4093322584ce7140b8376247e9695`.

| Condição compilada | Retorno `double` |
|---|---:|
| `isReeling()` verdadeiro | `0D` |
| Não recolhendo, `RESISTS_GRAVITY=true` e `getDeltaMovement().horizontalDistance() > 0.05000000074505806D` | `0D` |
| Demais caminhos | `0.07999999821186066D` |

Âncoras: `isReeling@1/ifne40@4`, flag `@11/ifeq44@23`, velocidade horizontal `@27–30`, limiar `@33`, `dcmpl@36/ifle44@37`, retornos `dconst_0@40` e `ldc2_w@44`/`dreturn@47`. O valor é comparado **estritamente maior**, logo igualdade e velocidade abaixo do limiar retornam o valor padrão. Velocidade horizontal é a magnitude da componente horizontal do vetor de deslocamento, não o alcance ou distância ao alvo.

O `defineSynchedData(Builder)V` (47 instruções) inicializa `RESISTS_GRAVITY=false` em `@82–90`. Recolhimento já seleciona retorno `0D` **sem depender de Straight Hook**. Os literais acima são valores JVM alargados de floats; a movimentação observada, o valor de gravidade efetivamente consumido pela engine, interpolações e mundo real continuam sujeitos à QA física.

## 4. Demais parâmetros e custos

| Campo | Valor / distinção |
|---|---|
| `max_level` | 1 (nível I) |
| `slots` | `mainhand` (declarativo; não prova rechecagem a cada tick) |
| `weight` | 2 (peso de dados, não probabilidade de acerto) |
| `min_cost` | base 1, incremento por nível adicional 12; nível I = 1 |
| `max_cost` | base 41, incremento por nível adicional 10; nível I = 41 |
| `anvil_cost` | 4 (custo de aquisição, não de cada lançamento) |
| Velocidade inicial / alcance | Sem multiplicador próprio de lançamento demonstrado no ramo Straight Hook. `Far Flung` modifica outro parâmetro, `0.5F+0.2F×L`; alcance final não calculado |
| Targeting / AOE / hitbox | Não introduz área, outro alvo, hitbox ou segundo projétil; colisão e busca de alvo são do gancho nativo |
| Dano / tipo / status / cura | `N/A` como efeitos diretos: este ramo só configura gravidade. `Sharp Cane` controla outro parâmetro de dano |
| Duração / cooldown / recursos | Não tem timer, mana, stamina ou cooldown adicionais próprios observados; launcher, recolhimento e desgaste permanecem provider-native |

`exclusive_set` e `effects` não constam no JSON individual; a ausência não certifica compatibilidade global com outros encantamentos ou condições de datapack. Não usar os custos de encantamento para cobrar mana/XP da perk nem conceder XP/Mastery por flag, pedido de spawn ou UUID gravado.

## 5. Grafo técnico, classes e consumidores

- `ACEnchantmentRegistry.class` SHA-256 `60006fab1b3b29f5f93c8365416815a12770cf8877a059298cb4ee82f7a92f32` — registry.
- `CandyCaneHookEntity.class` SHA-256 `e590bb67ea2b594861a30b05a5099fbd5eafe2920ff867883aaa6fd7cec478f8`; construtor com stack (231 instruções), `defineSynchedData` (47) e `getDefaultGravity` (20) são consumidores diretos; `tick` (546), `fling` (73) e callbacks de hit conservam o ciclo do gancho.
- `CandyCaneHookItem.class` SHA-256 `d999251e494c45420e58881181e9d67757247b6865dc4a547bf0da8a46cf8e44`; `use`, `canLaunchHook` e estado de reeling permanecem sob autoridade do item.
- Scan de **1.555 classfiles**: token `STRAIGHT_HOOK` só em registry e gancho; `RESISTS_GRAVITY` só na classe do gancho. Não exclui reflexão, transformação de bytecode, consumers externos ou a física herdada da engine.

## 6. Persistência e integração segura

`RESISTS_GRAVITY` é sincronizado com default `false`. Os overrides próprios `readAdditionalSaveData`/`addAdditionalSaveData` do gancho (23/22 instruções, evidenciados em Sharp Cane) não serializam explicitamente esse flag; persistência herdada, reload, cliente, dimensão e reconstrução física são `NOT_VERIFIED/NOT_TESTED`. Não presumir conservação ou perda após reload sem QA.

Possíveis perks de gravidade, velocidade, duração do voo, targeting ou recolhimento são ideias de design. **Nenhum mutating hook seguro foi verificado.** O Black Arcana controla seu runtime mágico; o RPG Skill Tree só fornece progressão/atributos/Mastery/gates por boundary comprovado. Não alterar sincronização nativa, simular hits, reemitir casts ou multiplicar custos/XP sem prova de causalidade e proteção server-authoritative. Política atual: `NO_MUTATION`, fail-closed.

## 7. Validação e pendências

- [Manifesto SHA-exato](../EXACT-STRAIGHT-HOOK-STATIC-1.0.10.json) · [prova JVM e reprodução](../EXACT-STRAIGHT-HOOK-STATIC-1.0.10.md) · [sonda read-only](../../../../../docs/qa/alexscaves_1010_straight_hook_static_probe.py).
- A sonda confere JAR SHA-1/SHA-256/tamanho, classfiles, recursos, JSON/tag e CFG completo de gravidade, além de digests e janelas JVM dos consumidores. Testes sintéticos verificam rejeição de alterações de ramo. Manifestos SHA-exatos anteriores dos mesmos classfiles fornecem os limites de owner, tick, item e NBT.
- **Ainda pendente:** QA de física/alcance, colocação real de projétil, persistência, multiplayer, compatibilidade de encantamentos, world safety, PvP, datapacks, hook mutador e adapter executável. Nenhuma Stage foi promovida. A certificação estática não fecha o universo dos 51 encantamentos ou o provider.
