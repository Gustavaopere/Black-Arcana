# WarriorMeleeGoal — Acolyte 1.0.3

**Estado:** `EXACT_PUBLISHER_BINARY_STATIC_CONTRACT` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED` · **certificações de perk: 0**.

## Identidade e evidência

`net.raptorzizi.acolyte.entity.goals.WarriorMeleeGoal<T extends AbstractSpellCastingMob & IAnimatedAttacker>` estende Iron's `GenericAnimatedWarlockAttackGoal<T>`. É composição de IA melee e animações do host, sem registry ID ou magia própria; **+0 magias Acolyte**. Magias auxiliares dos warriors são goals separados e continuam Iron's-owned.

Fonte: somente publisher `acolyte-1.0.3.jar`, CurseForge `1534642/8098233`, 621837 bytes; SHA-1 `ad0abc821f3f8a6573ac19a50970fc1bc46b4275`; SHA-256 `73fe745bbb0016fbc00af9ba14c0ecfe0a1d8a7d72a7892557739182b3486256`. Igualdade com instalado não provada. [Contratos binários](../BINARY-CONTRACTS-1.0.3.md) e [manifesto](../ARTIFACT-CATALOG-MANIFEST-1.0.3.json). Evidências W1–W5 apontam classe acima, método/descriptor e PC no `javap -p -c -s -constants`; os fatos não reproduzem implementação ou animações.

| Evidência | Método / descriptor | PC e fato observado |
|---|---|---|
| W1 | `<init>(Lio/redspace/ironsspellbooks/entity/mobs/abstract_spell_casting_mob/AbstractSpellCastingMob;FII)V` | 0–7 delega mob, speed convertido float→double e dois inteiros ao construtor host `(PathfinderMob,double,int,int)` |
| W2 | `tick()V` | 0–35 escolhe moveset por `mainHand.item instanceof AxeItem`; 36–37 chama tick do host; 40–42 grava `wantsToMelee=true` |
| W3 | `doMovement(D)V` | 0–30 target ausente/dead-or-dying para navegação; 31–45 olha target; 48–59 compara argumento com `meleeRange()²`; 62–113 persegue ou para |
| W4 | `doSpellAction()V` | 0 retorna, sem ação local |
| W5 | `<clinit>()V` | 0–79 cria lista SWORD; 82–147 cria lista AXE usando `AttackAnimationData(int,String,int[])` |

## Composição real dos warriors

Human Warrior e Demon Warrior constroem este goal em `registerArchetypeGoals()V`, PC 115–169. Com `A=selectedProfile.attackInterval`, calculam **a=A/2** por divisão inteira Java e **b=a+10**. Passam speed **1.0**, limites **a,b**, configuram `setComboChance(0.3F)`, repetem limites **a,b** em `setMeleeAttackInverval` (grafia publicada), ajustam `setMeleeMovespeedModifier(1.3F)` e registram prioridade **3**. O método de configuração pertence ao host; probabilidade efetiva, seleção temporal e combo final dependem de sua implementação. Ver [Human Warrior](../entities/human-warrior.md) e [Demon Warrior](../entities/demon-warrior.md).

O construtor desta classe não define dano, atributo de ataque, reach, alvo ou timers adicionais; transmite os argumentos à superclass Iron's. `canUse`, continuação, start/stop, cooldowns, janela do hit, seleção de combo, DamageSource e liquidação de dano são herdados. Valores de atributo/arma das entidades constam nas fichas delas; não substituir dano final por um valor do moveset. [W1]

## Movesets e animações

Em cada `tick`, **AxeItem na mão principal** seleciona AXE; qualquer outra classe de item, inclusive mão vazia, seleciona SWORD. Não se exige `SwordItem`. A escolha é refeita antes do `tick` do host, permitindo troca de moveset conforme equipamento. Após o retorno do host, marca `wantsToMelee=true`; a ordem é parte do contrato. [W2]

| Lista | Identificador de animação host | Inteiro temporal fornecido | Marcadores inteiros fornecidos | PC de W5 |
|---|---|---:|---|---|
| SWORD | `simple_sword_lunge_stab` | 8 | `[6]` | 0–16 |
| SWORD | `simple_sword_stab_alternate` | 10 | `[8]` | 19–35 |
| SWORD | `simple_sword_horizontal_cross_swipe` | 10 | `[8]` | 38–54 |
| SWORD | `simple_sword_downstrike` | 20 | `[16]` | 57–73 |
| AXE | `simple_sword_downstrike` | 20 | `[16]` | 82–98 |
| AXE | `simple_sword_horizontal_cross_swipe` | 10 | `[8]` | 101–117 |
| AXE | `sword_slash_stab` | 38 | `[13,33]` | 120–141 |

Esses são argumentos exatos ao API `AttackAnimationData(int,String,int[])`, não provas independentes de FPS visual, número de hits aceitos, multiplicador de dano ou segundos. A interpretação, despacho e consumo dos marcadores pertencem ao goal/animação Iron's no host em uso. Nenhum asset de animação foi copiado. [W5]

## Targeting, reach e movimento

`doMovement(double)` usa o campo `target` herdado. Target nulo ou `isDeadOrDying()` provoca `navigation.stop()` e retorno. Caso válido, olha o target e lê **`meleeRange()` herdado**; compara o argumento recebido com o quadrado desse alcance. **Não há alcance numérico fixo nesta classe.** O significado e a origem do argumento são contrato do caller host; o Acolyte o trata como métrica comparável a alcance². [W3]

Acima do limiar, solicita `navigation.moveTo(target,meleeMoveSpeedModifier)` somente quando `mob.tickCount % 5 == 0`; dentro/inclusive no limiar para a navegação. Nos dois callers, o modificador configurado é **1.3**. O método não possui teste local de LOS, colisão, equipe, dono, claim ou proteção. Esses filtros, a seleção de target e o hit efetivo dependem da entidade e superclass. [W3]

`doSpellAction` vazio suprime a ação de spell desse ponto virtual do goal host; **não desliga todo casting da entidade**. Os warriors também registram SpellBarrageGoal e SingleUseSpellGoal quando seus perfis os fornecem. [W4 e callers `registerArchetypeGoals()V`, PC 8–114]

## Custos, persistência e callbacks

Sem mana, recast, consumo de item/XP, cura ou efeito de bloco declarados localmente. Dano melee, alcance retornado por `meleeRange`, cooldowns e ataques animados são delegados ao host. A classe não redefine `canUse`, `canContinueToUse`, `start`, `stop`, save/load, packet ou callback de dano; apenas declara as listas estáticas e os overrides acima. Não há evento de sucesso próprio para Mastery ou settlement. [W1–W5]

Não inferir persistência do combo/timer a partir das listas estáticas: elas são definições de moveset, não estado de combate salvo. Restart/unload e reset de cooldown dependem dos goals/entidade do host. A origem de atribuição do dono de um ataque também não está neste goal.

## Integração por eixo

| Eixo | Contrato observado e limite |
|---|---|
| Identidade / RPG Skill Tree | Goal não é habilidade aprendível. Perks/Mastery/gates ficam no RPG Skill Tree somente após fronteiras de ataque confirmado; sem nova magia Acolyte. |
| Targeting / proteção | Acolyte decide a navegação ao target herdado. Validação de alcance/hit, friendly fire e claims precisa de prova no host. `WorldEffectPolicy` BA não é um veto comprovado deste melee. |
| Dano / atributos / cura | Fórmula e retorno de dano são do host/entidade/arma. Não tratar marcador de animação como dano confirmado; cura N/A local. |
| Custos / cast / mana | N/A local; `doSpellAction` vazio é somente este ponto virtual. Custos de goals mágicos separados continuam no host. |
| Cooldown / combo / recast | Argumentos a,b e combo 0.3 configurados pelos warriors; sem confirmação de distribuição/duração física. Recast mágico N/A local. Mutação segura não verificada. |
| Movimento / animação | Moveset depende da classe do item main hand; navegação 1.3 nos callers. Host controla consumo dos marcadores. Epic Fight/GeckoLib/multiplayer não testados. |
| Persistência / rede | Sem serializer próprio; goals/entidade host determinam resets. Não escrever campos herdados por reflexão. |
| Eventos / liquidação | Nenhum callback próprio de hit concluído. Black Arcana não cria segundo melee/proc nem premia Mastery por cada tick ou animação. |

## QA física pendente

Verificar host exato, reach efetivo, atributo/arma, hits dos sete registros, mudança entre AxeItem/outras armas durante combo, cadence e cooldown, targets inválidos, LOS/claims, unload/restart e multiplayer. Testar coexistência de casting auxiliar com melee e animações/Epic Fight. Nenhuma alteração runtime, adapter ou certificação é promovida nesta ficha.
