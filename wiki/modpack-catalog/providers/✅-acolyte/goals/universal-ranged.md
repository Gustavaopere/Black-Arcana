# UniversalRangedGoal — Acolyte 1.0.3

**Estado:** `EXACT_PUBLISHER_BINARY_STATIC_CONTRACT` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED` · **certificações de perk: 0**.

## Identidade e evidência

Goal de IA `net.raptorzizi.acolyte.entity.goals.UniversalRangedGoal<T extends PathfinderMob & RangedAttackMob>`, superclass Minecraft `Goal`. Sem registry ID ou magia própria; agenda o ataque à distância do mob. Eventuais magias do perfil/ataque continuam sob Iron's, **+0 magias Acolyte**.

Fonte: somente publisher `acolyte-1.0.3.jar`, CurseForge `1534642/8098233`, 621837 bytes; SHA-1 `ad0abc821f3f8a6573ac19a50970fc1bc46b4275`; SHA-256 `73fe745bbb0016fbc00af9ba14c0ecfe0a1d8a7d72a7892557739182b3486256`. Hash do instalado não comprovado. [Contratos binários](../BINARY-CONTRACTS-1.0.3.md) e [manifesto](../ARTIFACT-CATALOG-MANIFEST-1.0.3.json). Evidências R1–R7 referem-se à classe acima, método/descriptor e PC no `javap -p -c -s -constants`; são resumos factuais, sem transcrição de implementação.

| Evidência | Método / descriptor | PC e fato observado |
|---|---|---|
| R1 | `<init>(Lnet/minecraft/world/entity/PathfinderMob;DIF)V` | 4–11 cooldown −1/seeTime 0; 14–33 recebe mob, speed, intervalo, raio; 36–46 flags MOVE/LOOK |
| R2 | `isHoldingRangedWeapon()Z` | 0–31 aceita `Items.BOW` ou `Items.CROSSBOW` em `mob.isHolding` |
| R3 | `canUse()Z`; `canContinueToUse()Z` | 0–31 target vivo + arma; 0–22 continua por `canUse()` ou `mob.isUsingItem()` |
| R4 | `stop()V` | 0–9 redefine seeTime=0 e cooldown=−1 |
| R5 | `tick()V` | 0–33 target, distância² e LOS; 35–70 integrador seeTime limitado −60…60; 73–126 navegação; 129–141 olhar 30/30 |
| R6 | `tick()V` | 144–229 ramo usando item: aborta com LOS ausente e seeTime≤−60; em carga≥intervalo para item, chama `performRangedAttack(target,BowItem.getPowerForTime(carga))`, grava cooldown=intervalo |
| R7 | `tick()V` | 232–265 fora de uso: decrementa cooldown e começa MAIN_HAND se cooldown≤0, LOS e seeTime≥0 |

## Parâmetros reais e elegibilidade

Construtor recebe `(mob, speedMod, attackInterval, attackRadius)` e armazena os três parâmetros sem clamp local. Cooldown inicial **−1**, `seeTime` inicial **0**, flags **MOVE + LOOK**. O tipo genérico exige `RangedAttackMob`, embora o descriptor JVM apague o tipo para `PathfinderMob`; o cast para `RangedAttackMob` ocorre ao disparar. [R1,R6]

Human Archer e Demon Archer instanciam este goal na prioridade **3** com speed **1.0**, intervalo **selectedProfile.attackInterval** e raio **15.0**. Em ambos `registerArchetypeGoals()V`, PC 115–140 prova a composição. O goal não é registrado pelas outras classes de role no conjunto auditado. Ver [Human Archer](../entities/human-archer.md) e [Demon Archer](../entities/demon-archer.md).

`canUse` exige target não nulo, vivo e `mob.isHolding(Items.BOW)` ou `mob.isHolding(Items.CROSSBOW)`. Isso não é um teste genérico para todo `BowItem`/`CrossbowItem` customizado. A checagem de arma aceita a mão examinada pelo método Minecraft `isHolding`; o início de uso escolhe explicitamente **MAIN_HAND**, sem resolver aqui a mão da arma. `canContinueToUse` também aceita qualquer estado `isUsingItem`, mesmo que os testes de `canUse` deixem de passar. [R2–R3,R7]

## Geometria, visão e navegação

O goal usa a distância² entre entidades e a LOS de `mob.getSensing().hasLineOfSight(target)`. `seeTime` é um **integrador saturado**: soma 1 se há LOS, subtrai 1 sem LOS, limitado a **[−60,60]**; não é zerado nas transições. Recuperar de −60 até 0 exige 60 avaliações com LOS; partir de +60 até −60 exige 120 sem LOS. [R5]

Se distância² > raio², solicita `navigation.moveTo(target,speedMod)` somente quando `mob.tickCount % 5 == 0`; dentro/inclusive no raio chama `navigation.stop()`. Sempre orienta o look control ao target com limites **30°/30°**. A velocidade é um modificador da navegação, não blocos por tick garantidos. [R5]

**O raio limita a decisão de perseguir, não o disparo.** Os ramos de carregar e disparar não reavaliam o raio. Não existe strafe local, raycast de projétil, filtro de equipes/claims, teste de munição ou seleção de projétil nesta classe. [R5–R7]

## Carga, disparo e temporizadores

Enquanto usa item, lê `getTicksUsingItem()`. Se não há LOS e `seeTime≤−60`, apenas chama `stopUsingItem`. Caso contrário, quando carga≥`attackInterval`, chama primeiro `stopUsingItem` e depois `RangedAttackMob.performRangedAttack(target, BowItem.getPowerForTime(carga))`; em seguida grava cooldown=`attackInterval`. Portanto o mesmo intervalo parametriza **limiar de carga e espera entre cargas**, não uma cadência isolada de um tiro a cada N ticks. [R6]

Fora do uso, o cooldown é pré-decrementado; quando ≤0, com LOS presente e seeTime≥0, inicia uso na main hand. O cooldown não é decrementado durante o ramo de uso. Um disparo pode ocorrer sem LOS atual enquanto `seeTime>−60`; não há teste adicional de LOS no ramo de release. A conversão de carga em força é o método vanilla `BowItem.getPowerForTime`, inclusive quando a arma elegível é crossbow; este goal não implementa o pipeline vanilla de carregamento de crossbow. [R6–R7]

Os contadores descritos são avaliações de `tick` do goal. A classe não declara `requiresUpdateEveryTick`; sua cadência física depende do scheduler Minecraft. O contador de carga lido pertence ao mob e pode ter uma cadência diferente. Não converter esses parâmetros diretamente em segundos, DPS ou intervalo efetivo sem QA.

## Dano, custos, persistência e callbacks

O goal não cria projétil nem calcula dano, velocidade balística, dispersão, consumo de munição, durabilidade, encantamentos ou magia. Tudo isso pertence à implementação do mob em `performRangedAttack`. A chamada é uma tentativa de disparo, sem retorno de hit/aceitação. Sem cast/mana/recast próprio; spell barrage e single-use são outros goals, não custos deste. [R6]

`stop` redefine somente `seeTime` e `attackCooldown`; não chama `stopUsingItem`, não cancela navegação e não limpa target. `tick` com target nulo retorna imediatamente, também sem cancelar item. Campos não têm NBT/serializer/packet próprios; cooldown e visão reiniciam com nova instância. Nenhum callback local de hit, dano, cancelamento confirmado ou settlement. [R4–R5]

## Integração por eixo

| Eixo | Contrato observado e limite |
|---|---|
| Identidade / gates | IA da entidade. Sem spell unlock; RPG Skill Tree só recebe progressão/Mastery/gates por fronteiras confirmadas. |
| Targeting / proteção | Target/LOS do mob; raio 15 nos archer callers regula perseguição. Claims/friendly fire pertencem à entidade/projétil/host e não estão validados aqui. |
| Dano / cura / atributos | Delegados a `performRangedAttack` e projétil. Não somar dano nem conceder Mastery por início de carga/release. Cura: N/A local. |
| Custos / mana / munição | N/A mana local; consumo de munição/durabilidade delegado ao mob. Nenhum débito BA adicional. |
| Cooldown / carga / recast | Integra duas fases com o mesmo intervalo e um integrador de LOS. Hook seguro para alteração não verificado; recast mágico N/A local. |
| Movimento / animação | MOVE/LOOK, perseguição a cada quinto tickCount, olhar 30/30 e uso de item. Eventos animados dos archer pertencem ao mob; Epic Fight não testado. |
| Persistência / rede | Sem estado serializado ou pacote próprio. Uso de item é estado Minecraft/mob; reload e multiplayer pendentes. |
| Mundo / callbacks / liquidação | Não altera blocos diretamente; efeitos dos projéteis são delegados. `WorldEffectPolicy` BA não intercepta automaticamente. Nenhum callback de sucesso/exactly-once. |

## QA física pendente

Validar bow/crossbow e armas customizadas em cada mão, munição, troca de equipamento durante carga, target nulo/morto, `stop` durante uso, LOS oscilante, disparo além do raio, cadência real e persistência após unload/restart. Validar dano e dono do projétil no host exato, multiplayer e animações. Esta ficha não cria adapter, código runtime ou certificação.
