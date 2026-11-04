# Flinging — impulso e alcance do salto da Ortholance (1.0.10)

**Estado:** ⚠️ ficha individual **parcial/condicionada**. Identidade JSON, tag de item e janelas selecionadas do **JAR publisher SHA-exato 1.0.10** foram auditadas em modo read-only. **Não** há hook mutador aprovado, CFG completo, certificação individual para perks, QA física ou prova de alcance final em blocos. Contratos: `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `perk_certification=NOT_CERTIFIED`, `mutation=NO_MUTATION`.

**Definição:** `alexscaves:flinging` modifica a **impulsão de quem usa a Ortholance** no callback nativo `OrtholanceItem.releaseUsing`; não é uma magia lançada pelo Black Arcana. Outros efeitos da arma (ondas, ataque e dano em área) pertencem ao provider e são condicionais, não novos casts nem custos/procs próprios do encantamento.

## 1. Identidade e proveniência

| Objeto | Evidência exata |
|---|---|
| Mod / versão instalada | Alex's Caves Continued, mod ID `alexscaves`; `alexscaves-1.0.10-neoforge+1.21.1.jar`, [modlist sibling](https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/main/PROJECT-INSTRUCTIONS/modlist/modlist.md), item 019 |
| Plataforma | Minecraft 1.21.1 / NeoForge / Java 21 |
| JAR publisher | 75.279.314 bytes, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`; SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c` |
| ResourceKey | `alexscaves:flinging`; símbolo `ACEnchantmentRegistry.FLINGING` observado em classfile |
| Recurso publisher | `data/alexscaves/enchantment/flinging.json`; **359 bytes**, SHA-256 `0680721d1687f85991e11ee33908b67aa8b720339e7b09eeaaaf92cf604356f2` |
| Tag publisher | `data/alexscaves/tags/item/enchantable/ortholance.json`, SHA-256 `1c96a26e08800182b9c4b3b2f5ba4043389fe1bec0dcd5b12f1e5392cc28a5ac`; inclui `alexscaves:ortholance` |
| Produtor de impulso | `com/github/alexmodguy/alexscaves/server/item/OrtholanceItem.class`; SHA-256 `996b208a60f2c26c275e60e5d0e3a2fd0090cfb0ba1687907cac242de9a17d09` |
| Entidade secundária | `com/github/alexmodguy/alexscaves/server/entity/item/WaveEntity.class`; SHA-256 `93fdaee0239cc4985b351a6c2ac1edd23a51cf0088cb1172f983d0f869d9e42e` |
| Registry compilado | `ACEnchantmentRegistry.class`; SHA-256 `60006fab1b3b29f5f93c8365416815a12770cf8877a059298cb4ee82f7a92f32` |

**Evidência:** [EXACT-FLINGING-1.0.10.json](../EXACT-FLINGING-1.0.10.json) contém o recurso JSON exato, tag do JAR, três hashes de classes, descritores e digests dos métodos, com janelas de instruções limitadas. Gerado pela [sonda](https://github.com/Gustavaopere/Black-Arcana/blob/main/docs/qa/alexscaves_1010_flinging_probe.py), [testes fail-closed](https://github.com/Gustavaopere/Black-Arcana/blob/main/docs/qa/alexscaves_1010_flinging_probe_test.py) e [workflow](https://github.com/Gustavaopere/Black-Arcana/blob/main/.github/workflows/alexscaves-1010-flinging.yml). A CI utiliza `--seal` para comparar a extração inteira com o manifesto versionado, após verificar SHA-1/SHA-256/tamanho do artefato. São evidências para **interoperabilidade**, não transferência ou cópia do runtime.

A fonte pública `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` declara **versão 1.1.1**. Sua leitura serviu apenas para localizar candidatos de pesquisa: **não** se presume equivalência de classfiles, métodos ou constantes com a 1.0.10.

## 2. JSON — limites de encantamento

| Campo | Valor publisher 1.0.10 |
|---|---|
| `description.translate` | `enchantment.alexscaves.flinging` |
| `supported_items` | `#alexscaves:enchantable/ortholance` |
| `weight` | **10** — peso da seleção do encantamento; não chance de lançamento ou acerto |
| `max_level` | **3** |
| `min_cost` | `base=1`, `per_level_above_first=8` |
| `max_cost` | `base=41`, `per_level_above_first=10` |
| `anvil_cost` | **1** |
| `slots` | `["mainhand"]` |
| `exclusive_set` | **Não declarado** nesse JSON; outras regras/datapacks não verificados |

`weight`, `min_cost`, `max_cost` e `anvil_cost` são parâmetros de encantamento: não representam cooldown, durabilidade, mana, magnitude da impulsão nem quantidade de ondas. O nível máximo III é **declarativo**; modificadores externos podem produzir níveis anômalos que exigiriam clamp em uma integração futura.

## 3. Contrato nativo: `OrtholanceItem.releaseUsing`

**Descritor JVM exato:** `(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;I)V`, **435 instruções**, digest do método `00705e7177cb6fe2914531158bd978b64d497ca4c8262f8e7634c1b4ec9ef7ae`.

### 3.1. Carga e cálculo do impulso

- `@0–15`: solicita `getUseDuration(stack,null)`, subtrai `useTime`, limita o valor a **0–60** usando `Mth.clamp`, guarda como **C**. O parâmetro `useTime` é o tempo **restante**, não duração adicional gerada por Flinging.
- `@18–24`: consulta `ACCompat.enchantLevel(stack,FLINGING)` e guarda o nível como **F**.
- `@27–41`: `TSUNAMI` é consultado separadamente, convertido a booleano. Flinging **não** altera por si só esse gate.
- `@43–61`: somente se `C>0`, calcula um escalar `f` por dois produtos com **0.1F**, um com C e outro com F, seguidos de soma.
- `@63–93`: soma à velocidade já existente do usuário `LivingEntity.getDeltaMovement()` o **vetor de visão normalizado** multiplicado por `(f, f×0.15F, f)`. `Vec3.multiply(D,D,D) @87` e `Vec3.add @90` são callsites nativos, não callbacks Black Arcana.
- `@836–866`: o mesmo vetor ganha um acréscimo vertical condicionado a `onGround` (**0.2F se em solo**, caso contrário 0) mais `F×0.1F`; então solicita `LivingEntity.setDeltaMovement(Vec3) @866`. Isto modifica **a velocidade solicitada**, não a distância final percorrida.

O trecho compilado determina:

`C = clamp(getUseDuration(stack,null) − useTime, 0, 60)`

`f = 0.1F × C + 0.1F × F`, com efeito somente para `C>0`.

| Nível F | Bônus direto a `f` | Acréscimo vertical próprio |
|---:|---:|---:|
| 0 | 0 | 0 |
| I | +0,1 | +0,1 |
| II | +0,2 | +0,2 |
| III | +0,3 | +0,3 |

**Limite:** não confundir `f` com **blocos de alcance**, velocidade total do usuário, duração de voo, raio do ataque ou bônus de dano. A velocidade prévia do jogador, seu vetor de visão, colisões, gravidade, arrasto e efeitos de outros mods afetam o deslocamento real. A mesma constante F intervém na parcela horizontal e vertical de forma distinta: uma perk que multiplicasse `f` sem levar em conta o bônus vertical poderia alterar o balanceamento e a causalidade.

### 3.2. Custo, ondas e ramo de servidor

A liberação **com C positivo** calcula impulso, mas as rotinas de ondas/dano/disgaste relevantes no método são limitadas por outro gate:

- `@95–106`: **`C>=10`** e **lado servidor** (`!Level.isClientSide`) para entrar na emissão de ondas e resolução do dano correlato.
- `@132–135`: `ACCompat.hurtAndBreakUsedHand(stack,1,livingEntity)` solicita **um ponto de desgaste** no caminho de servidor elegível. Não é um custo adicional de Flinging e pode ser afetado por estado ou modificadores.
- `@138–142`: o número-base de ciclos de ondas é derivado por divisão inteira **`C/5`**. No ramo `TSUNAMI` (`@144–152`), o contador usado no método passa a **5** e há construção de uma `WaveEntity` com `setLifespan(20) @197`, `setWaveScale(5.0F) @204` e `setWaitingTicks(2) @210`.
- No ramo normal, o código registra laços de criação de ondas com `setLifespan`, `setPos`, orientação por `atan2` e várias tentativas de `Level.addFreshEntity` (p.ex. `@371/@449`); a flag `SECOND_WAVE` é consultada **depois** em `@460–466`, e seu ramo usa esperas **8 ticks** em `setWaitingTicks @604` (entre outros callsites). A quantidade de entidades inseridas no mundo **não** é automaticamente igual ao número de invocações, pois `addFreshEntity` retorna um booleano descartado.
- **Flinging não é o seletor de `TSUNAMI` nem de `SECOND_WAVE`.** Ele altera o vetor de impulso, que é utilizado para localização de ondas e para a construção da região de possíveis hits; pode, portanto, ter efeitos indiretos em geometria. Não tratar isso como raio de AoE independente garantido.

**`WaveEntity` downstream:** a sonda inspecionou métodos `setLifespan`, `setWaitingTicks`, `setWaveScale` e `tick`. No `tick` exato, a espera positiva é decrementada **no servidor** (`@13–44`), tornando a onda invisível e retornando antes da progressão normal; `activeWaveTicks`, `getLifespan @575` e `setSlamming @606` controlam a sequência posterior. A entidade é removida em condição observada com `discard @102`, e física/colisões podem alterar trajetória. São entidades autônomas do provider; ondas secundárias não autorizam novo cast, outro débito, novos procs ou novos roots no Black Arcana.

### 3.3. Dano da liberação e targeting

O método nativo consulta entidades dentro de uma `AABB`, mas **as janelas selecionadas não fecham sua geometria exata nem o cálculo completo de seus limites**; a área é uma caixa, não uma esfera nem um raio escalar certificado. O manifesto selecionado prova `Level.getEntitiesOfClass(LivingEntity.class,AABB) @758` e os guards:

- `isAlliedTo @793`: filtra aliados.
- `equals @802`: exclui o próprio usuário.
- `hasLineOfSight @811`: requer visibilidade nativa.
- `LivingEntity.hurt @824` recebe `mobAttack(livingEntity)` e `(float) ACCompat.attackDamageBonus(stack)`; o retorno booleano é **descartado**. `stopRiding @830` ocorre em sequência no ramo elegível, sem guardar a condição de retorno de `hurt`.

**Não atribuir a Flinging um bônus numérico de dano-base.** O valor vem de `ACCompat.attackDamageBonus`, não de `F`, nas janelas auditadas. Flinging pode alterar indiretamente o espaço percorrido/consultado; isso não prova acertos adicionais, dano confirmado, dano em área sem LOS, autoridade para atingir alvos protegidos ou Mastery/XP legítimo. O box do ataque do item, as ondas em servidor e o impulso do usuário são três superfícies causais diferentes que não devem ser registradas como três casts.

## 4. Outros métodos, cooldowns e estados

| Componente | Evidência SHA-exata | Limite |
|---|---|---|
| `OrtholanceItem.use(Level,Player,InteractionHand)` | **20 instruções**; verifica `getDamageValue @9`, `getMaxDamage @14` e chama `startUsingItem @30` quando aceita | Estado do stack quebrado pode impedir uso; não inferir sucesso ou cooldown universal |
| `OrtholanceItem.mineBlock` | **15 instruções**, referência a `ACCompat.hurtAndBreak @20` | O custo de mineração pertence ao item; não reinterpretá-lo como custo do encantamento |
| `OrtholanceItem.getUseDuration(ItemStack,LivingEntity)` | Método próprio observado, **2 instruções**; duração máxima exata da sessão não foi usada como novo contrato de Flinging | O valor C já é limitado a 60 no `releaseUsing` |
| `WaveEntity.tick` | **318 instruções**, controles de espera/lifespan, movimento e descarte; `isClientSide @23`, `getWaitingTicks @13/@31` | Não prometer dano, knockback, persistência, posição exata ou sucesso de spawn por evento de onda |
| Dados de owner e rede | `WaveEntity(Level,LivingEntity)` é construtor chamado nas janelas exatas do item | Não inferir ownership final de procs, replays ou persistência em outras dimensões |
| `SECOND_WAVE` e `TSUNAMI` | Encantamentos distintos, acionados por `ACCompat.enchantLevel` | Coexistência real, `exclusive_set` e datapacks condicionam combinações |

O callback `releaseUsing` pertence ao ciclo de uso do próprio item, não ao protocolo de casting do Black Arcana. Janelas de `getUseDuration`, dano da onda, semântica completa de colisão e filtros de mundo exigem inspeção/QA adicional antes de mutar propriedades.

## 5. Matriz de possíveis perks e condições de homologação

| Intenção | Contrato de partida | Estado e risco |
|---|---|---|
| **Impulso/alcance de deslocamento** | `releaseUsing @43–93`, `setDeltaMovement @866` | Escalar localizado ✅ no sentido de **evidência estática**; mutação de movimento segura ⚠️ não homologada; medir vetor e colisão |
| Altura / bônus vertical | `f×0.15F`, `onGround ? 0.2F : 0`, `F×0.1F` | ⚠️ componente separado; cap e ordem de aplicações sem contrato executável |
| Ondas e quantidade | `C>=10`, `C/5`, `TSUNAMI`, `SECOND_WAVE`, `WaveEntity` | ⚠️ contadores nativos e spawns condicionais; não ampliar procs por onda/tick |
| Targeting/área | AABB nativa com `getEntitiesOfClass`, filtros de aliado/owner e LOS | ⚠️ ampliar o vetor **não** autoriza atravessar claims, atingir aliados, ignorar LOS ou duplicar dano |
| Dano e knockback | `mobAttack`, `attackDamageBonus`, `hurt`, `stopRiding`, `WaveEntity` downstream | ⚠️ Flinging não declara tipo novo de dano; retorno de hurt descartado e settlement condicionado |
| Custo e cooldown | Um desgaste de 1 solicitado no ramo `C>=10` em servidor; outros métodos de item independentes | ⚠️ não adicionar segunda mana, debitar por onda ou inferir cooldown não observado |
| Persistência/rede | Velocity no `LivingEntity`, ondas em `Level.addFreshEntity`, callbacks de item | ⚠️ carregamento de chunks, restart, troca de mão, ordem de packets e anti-replay ainda pendentes |
| Black Arcana / RPG Skill Tree / Enshrouded | Item e ondas são authority do provider; Black Arcana só governa seu runtime e world safety; RPG Skill Tree fornece progressão via contratos reais | ⛔ não criar adapter/hook ou transferir autoridade sem boundary comprovada |

**QA pendente:** testar modpack físico 1.0.10 com níveis 0/I/II/III e carga 1, 9, 10 e 60; solo/água/ar, mudanças de velocidade prévia, colisões, chunk boundaries, queda, Creative, durabilidade, PvP, claims, LOS, aliados, entidades montadas, uso cancelado, mão secundária, ondas com/sem Tsunami e Second Wave, troca de slot, save/reload, owner órfão, latência e FPS/TPS baixos. Instrumentar número de `addFreshEntity` **aceitos** e de hits **efetivos**, não apenas chamadas.

**Conclusão delimitada:** `SHA_EXACT_RESOURCE_AND_SELECTED_JVM_ORTHOLANCE_LAUNCH` + `PARTIAL_ENCHANTMENT_DOSSIER` / ⚠️. **+1 ficha individual parcial**, **+1 referência literal de ID nos manifestos**, **+0 contratos estáticos certificados**, **+0 hooks mutadores**, **+0 raízes mágicas**, **+0 promoção de Stage**. Próxima identidade alfabética: `alexscaves:gamma_ray`.
