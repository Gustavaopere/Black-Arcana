# Iron's 3.16.3 — Sacrifice: explosão por cast e morte de invocação marcada

**Estado:** ✅ `SOURCE-PINNED / CAUSAL-PARTIAL`; ⚠️ JAR físico, configuração efetiva, dinâmica de morte, team filters, compatibilidade/QA de vários providers e adapter RPG pendentes. O spell `irons_spellbooks:sacrifice` já está entre as 110 identidades do Iron's — **nenhuma magia nova**, e o status `sacrificial_mark` não vira feitiço extra. Fonte upstream clean-room `iron431/irons-spells-n-spellbooks@e4056af90302d37eb1739f5ff05020b020e6e252` para Minecraft 1.21.1, modpack documental Iron's 3.16.3. [Ficha atual](../blood/sacrifice.md).

## Dois ingressos causais distintos

### A. Cast direto do jogador / summon próprio

1. **Defaults:** [`SacrificeSpell`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/blood/SacrificeSpell.java#L47-L86) escola Blood, rarity RARE, níveis 1–5, cast `INSTANT`, mana `25+5×(level−1)`, cooldown default **1 segundo**, `baseSpellPower=2` e `spellPowerPerLevel=1`.
2. **Target preflight:** [`checkPreCastConditions`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/blood/SacrificeSpell.java#L93-L117) usa `RaycastBuilder` de **25 blocos** a partir dos olhos, `bbInflation=0.25`, `checkForBlocks(true)` e filtro por `IMagicSummon` cujo `getSummoner() == caster`. Exige que o alvo final seja `LivingEntity`, grava `TargetEntityCastData`; o resultado é **single-target para iniciar** uma explosão depois, não multi-target cast.
3. **Execução final:** [`onCast`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/blood/SacrificeSpell.java#L119-L132) reobtém target como `IMagicSummon`, revalida `summon.getSummoner().getUUID().equals(caster.getUUID())`, calcula `damage=getDamage(level,caster)+target.health×0.5`, `radius=getRadius(target)`, detona uma explosão provider-native e remove a invocação com `RemovalReason.KILLED`. A expressão `summon.getSummoner().getUUID()` não possui guard explícito para owner nulo nessa fase — testar owner desaparecido/órfão, não declarar crash sem reprodução.
4. **Dano e escala da invocação:** [`getDamage`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/blood/SacrificeSpell.java#L151-L158) = `(10+getSpellPower(level,caster))×SUMMON_DAMAGE_attribute(caster)` para caster não-nulo, mais metade da **vida atual** do summon no cast direto. Sob multiplicadores unitários, apenas o **termo base** é **12/13/14/15/16** nos níveis 1–5; a vida do summon é um componente adicional variável.
5. **Raio nominal dinâmico:** `getRadius(summon)=3×(1+0.5×(health/maxHealth))`. Se `health=maxHealth` e `maxHealth>0`, o valor calculado é **4,5**, contra **3** na borda `health=0`. É valor matemático do parâmetro nominal, **não raio garantido de alvos atingíveis** (ver geometria abaixo).

### B. Morte com Sacrificial Mark (sem cast direto)

6. **Evento independente de cast:** [`SacrificialMarkEffect.onLivingDeath`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/effect/SacrificialMarkEffect.java#L19-L49) escuta **`LivingDeathEvent`**, exige lado servidor e efeito `MobEffectRegistry.SACRIFICIAL_MARK` na entidade que morreu. Obtém owner com `SummonManager.getOwner(entity)`; se não for `LivingEntity`, faz fallback para **a própria entidade morta**. Calcula `damage=getDamage(markAmplifier+1,owner)`, `radius=getRadius(deadEntity)`, dispara `doSacrificeExplosion` e remove a entidade. Não soma `+health×0.5` neste caminho — é **fórmula causalmente distinta** do cast direto.
7. **Origem de marca encontrada:** [`DeadKingBoss.sacrificialMarkHandler`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/mobs/dead_king_boss/DeadKingBoss.java#L100-L113) responde a `SetSummonOwnerEvent`; no modo **ominous**, com chance `Mth.lerp(1−bossHealth/maxHealth,0.2,0.75)` atribui `SACRIFICIAL_MARK` de duração `Integer.MAX_VALUE` e amplifier derivado do nível de Sacrifice. Essa é **uma origem encontrada no código-fonte**, não prova de exclusividade de mark por todos os addons/datapacks.
8. **Risco de raio na morte:** `LivingDeathEvent` consulta `deadEntity.getHealth()` ao calcular raio; o valor naquele instante depende da ordem do ciclo de morte. Portanto não transportar o **4,5 de summon saudável** para o evento de morte. Verificar valores reais de saúde, ratio/caps e estágio de listener; sem QA, o raio efetivo é **não validado**.

## Geometria e damage settlement (compartilhado A/B)

9. **AABB de busca:** [`doSacrificeExplosion`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/blood/SacrificeSpell.java#L134-L149) consulta `level.getEntities(null,AABB.ofSize(center, radius, radius, radius))`. **Atenção:** `AABB.ofSize` recebe **comprimento total das arestas**, então a busca tem **semi-extensão radius/2 por eixo**, embora o filtro subsequente use `distanceSqr < radius²`. A seleção fica restrita ao cubo menor: não interpretar `radius` como esfera inteiramente coberta no runtime. Isso é incompatibilidade geométrica source-observed, **não** bug físico reproduzido.
10. **Queda de dano:** após `canBeHitByProjectile()`, distância e `Utils.hasLineOfSight`, calcula `q=distance²/radius²` e fator `1−q³` sobre dano bruto. Aplica `DamageSources.applyDamage(victim,damage×factor,source)`; em `LivingEntity + SpellDamageSource` o provider publica `SpellDamageEvent` antes da resistência e de `hurt`. **Sem hitbox de projétil** e sem `WorldEffectPolicy` próprio de Black Arcana nesse método: é mecanismo de dano/partículas, não uma `Explosion` vanilla destruidora de blocos.
11. **Alvos adicionais / friendly fire:** loop aceita qualquer entidade `canBeHitByProjectile` dentro da busca e linha de visão; não filtra explicitamente `isFriendlyFireBetween` aqui. Para `LivingEntity + SpellDamageSource`, [`DamageSources.applyDamage`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/damage/DamageSources.java#L44-L65) possui guarda downstream de aliados e PvP. Tipos diferentes de Entity e fontes requerem testes específicos, evitando dizer que a área sempre respeita todos os claims/mods.
12. **Linhagem de proc:** o ramo por morte pode causar dano a outras invocações marcadas e a outros alvos. Se tais hits gerarem novas mortes, novos `LivingDeathEvent` poderão disparar outros efeitos de marca: **cadeia em potencial** sem teto global próprio visível nesse método. Não alegar ocorrência real/infinita sem teste; um adapter de Mastery deve orçar e deduplicar ações e efeitos para não recompensar explosões recursivas como casts.
13. **Separação dos dois ingressos:** o cast direto remove summon após detonação; a morte marcada detona ao receber evento de morte. A inspeção **não prova** se `remove(KILLED)` gera outro `LivingDeathEvent` nesse caso nem a ordem de callbacks de terceiros; evitar double-counting e investigar em dedicated-server.

## Matriz para perks

| Eixo | Código provado | Situação de interoperabilidade |
|---|---|---|
| Dano de cast | `(10+power)×SUMMON_DAMAGE + currentHealth/2` | ⚠️ nível/atributos mudam indiretamente, sem hook individual que reescreva fórmula/provider cast |
| Dano de mark | `getDamage(markAmplifier+1,owner)`, **sem bônus currentHealth/2** | ⚠️ caminho independente de lançamento; `SpellDamageEvent` em LivingEntity permite alterar valor por hit, não origem |
| Raio | `3×(1+0.5×health/maxHealth)` | ⛔ sem setter público per-perk de raio; AABB do provider impede tratar raio nominal como esfera integral |
| Forma AOE | `AABB.ofSize(radius,radius,radius)`, distância, LOS | ⛔ não expandir consulta nem criar segunda explosão pelo adapter |
| Target inicial | caster-owned IMagicSummon dentro de 25 blocos | ⛔ sem hook seguro de retarget, auto-multi-sacrifice ou alvo inimigo |
| Trigger por morte | `SACRIFICIAL_MARK`, server `LivingDeathEvent` | ⚠️ depende de fonte de mark, owner e ciclo de morte; ⛔ sem permissão para transformar qualquer death em Sacrifice |
| Tipo de dano | `SpellDamageSource` de Sacrifice | `SpellDamageEvent.setAmount` em LivingEntity: ✅ seam por hit; ⛔ não muda DamageType, causa causal nem área |
| Mana / cooldown | 25–45 mana / 1 s default para cast A | ⚠️ B é evento automático de mark, não novo cast pago; não cobrar outra vez nem conceder XP de cast |
| Persistência / orçamento | effect `SACRIFICIAL_MARK` de longa duração no Dead King | ⚠️ validar refresh, save/reload, morte de boss, summons e limites de proc por tick |

## Testes de aceitação pendentes

- [ ] JAR exato/modlist, tag/config/dano e Source/bytecode das classes.
- [ ] Cast direto: owner mesmo/diferente/null, summon morto/descarregado, staff/scroll, descontos pré-gate, vida cheia/vazia.
- [ ] Mark: proc de Dead King ominous, sorteio, amplificador, SummonManager.getOwner, morte natural/por spell/kill cancelado.
- [ ] Volume de AABB vs raio anunciado: alvos dentro da esfera nominal mas fora do cubo, nos cantos e no limite; fator de queda e LOS.
- [ ] Friendly-fire, PvP/teams, claims, entities não-`LivingEntity` e proteção de jogadores.
- [ ] Morte em cascata com vários marks e efeitos derivados; determinar dedup, budgets e se `remove(KILLED)` dispara evento de morte.
- [ ] Persistência de marcas e summons após restart/creature unload; callbacks, clean-up.
- [ ] Reconciliar contrato RPG de Mastery/procs com provider sem alterar o owner de Sacrifice/WorldEffectPolicy.

**Clean-room:** documentação de fluxo e fonte pública versionada, não reutilização de código, algoritmo ou assets do provider.
